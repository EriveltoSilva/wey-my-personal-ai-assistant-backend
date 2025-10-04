"""Agent services for business logic."""

from typing import List, Optional

from sqlalchemy import and_, delete, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.agents.enums import AgentStatusEnum
from src.agents.models import Agent
from src.agents.schemas import AgentCreate, AgentListParams, AgentRating, AgentUpdate
from src.exceptions import NotFoundException


class AgentService:
    """Service for managing agents."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_agents(self, params: AgentListParams) -> tuple[List[Agent], int]:
        """Get paginated list of agents with filters."""
        # Base query with eager loading of professional_areas
        query = select(Agent).options(selectinload(Agent.professional_areas))
        count_query = select(func.count(Agent.id))

        # Apply filters
        filters = []

        if params.professional_area_id:
            # Join with professional areas to filter by professional area
            from src.users.models import ProfessionalArea

            query = query.join(Agent.professional_areas)
            count_query = count_query.join(Agent.professional_areas)
            filters.append(ProfessionalArea.id == params.professional_area_id)

        if params.is_featured is not None:
            filters.append(Agent.is_featured == params.is_featured)

        if params.is_premium is not None:
            filters.append(Agent.is_premium == params.is_premium)

        # Only show active agents by default
        filters.append(Agent.status == AgentStatusEnum.ACTIVE.value)

        if params.search:
            search_term = f"%{params.search}%"
            filters.append(
                or_(
                    Agent.name.ilike(search_term),
                    Agent.description.ilike(search_term),
                    Agent.expertise_area.ilike(search_term),
                )
            )

        if filters:
            query = query.where(and_(*filters))
            query = query.where(and_(Agent.status == AgentStatusEnum.ACTIVE.value))
            count_query = count_query.where(and_(*filters))

        # Apply sorting
        order_by = Agent.name.asc()
        query = query.order_by(order_by)

        # Apply pagination
        query = query.offset(params.skip).limit(params.limit)

        # Execute queries
        result = await self.db.execute(query)
        agents = result.scalars().all()

        count_result = await self.db.execute(count_query)
        total = count_result.scalar()

        return agents, total

    async def create_agent(self, agent_data: AgentCreate) -> Agent:
        """Create a new agent."""
        # Extract data and handle special fields separately
        agent = Agent(
            **agent_data.model_dump(exclude={"professional_area_ids", "status"}),
            status=agent_data.status.value if agent_data.status else AgentStatusEnum.ACTIVE.value,
        )

        self.db.add(agent)
        await self.db.commit()
        await self.db.refresh(agent)

        # Handle many-to-many relationship with professional areas
        if agent_data.professional_area_ids:
            # Import here to avoid circular imports
            from src.agents.models import agent_professional_area_association
            from src.users.models import ProfessionalArea

            # Use direct insertion into association table to avoid lazy loading issues
            for area_id in agent_data.professional_area_ids:
                # Get the professional area directly from the database
                area = await self.db.get(ProfessionalArea, area_id)
                if area:
                    # Insert directly into the association table
                    insert_stmt = agent_professional_area_association.insert().values(
                        agent_id=agent.id, professional_area_id=area.id
                    )
                    await self.db.execute(insert_stmt)

            await self.db.commit()

            # Refresh agent with professional_areas loaded
            agent_query = select(Agent).where(Agent.id == agent.id).options(selectinload(Agent.professional_areas))
            result = await self.db.execute(agent_query)
            agent = result.scalars().first()

        return agent

    async def get_agent_by_id(self, agent_id: str, include_examples: bool = False) -> Optional[Agent]:
        """Get agent by ID."""
        query = select(Agent).where(Agent.id == agent_id)
        query = query.where(Agent.status == AgentStatusEnum.ACTIVE.value)

        # Always include professional areas
        query = query.options(selectinload(Agent.professional_areas))

        if include_examples:
            query = query.options(selectinload(Agent.examples))

        result = await self.db.execute(query)
        return result.scalars().first()

    async def update_agent(self, agent_id: str, agent_data: AgentUpdate) -> Agent:
        """Update an existing agent."""
        agent = await self.get_agent_by_id(agent_id)
        if not agent:
            raise NotFoundException(f"Agent with id {agent_id} not found")

        # Extract update data and handle special fields separately
        update_dict = agent_data.model_dump(exclude_unset=True, exclude={"professional_area_ids", "status"})

        # Handle enum field manually
        if agent_data.status is not None:
            update_dict["status"] = agent_data.status.value

        # Update fields using dictionary unpacking
        for field, value in update_dict.items():
            setattr(agent, field, value)

        # Handle many-to-many relationship with professional areas
        if agent_data.professional_area_ids is not None:
            # Import here to avoid circular imports
            from src.agents.models import agent_professional_area_association
            from src.users.models import ProfessionalArea

            # Clear existing relationships using direct SQL
            delete_stmt = delete(agent_professional_area_association).where(
                agent_professional_area_association.c.agent_id == agent.id
            )
            await self.db.execute(delete_stmt)

            # Add new relationships using direct insertion into association table
            for area_id in agent_data.professional_area_ids:
                # Get the professional area directly from the database
                area = await self.db.get(ProfessionalArea, area_id)
                if area:
                    # Insert directly into the association table
                    insert_stmt = agent_professional_area_association.insert().values(
                        agent_id=agent.id, professional_area_id=area.id
                    )
                    await self.db.execute(insert_stmt)

        await self.db.commit()

        # Reload agent with professional_areas for the response
        agent_query = select(Agent).where(Agent.id == agent.id).options(selectinload(Agent.professional_areas))
        result = await self.db.execute(agent_query)
        agent = result.scalars().first()

        return agent

    async def delete_agent(self, agent_id: str) -> bool:
        """Delete an agent (soft delete by setting status to inactive)."""
        agent = await self.get_agent_by_id(agent_id)
        if not agent:
            raise NotFoundException(f"Agent with id {agent_id} not found")

        agent.status = AgentStatusEnum.INACTIVE.value
        await self.db.commit()
        return True

    # #############################################################################
    async def rate_agent(self, agent_id: str, rating_data: AgentRating) -> Agent:
        """Rate an agent."""
        agent = await self.get_agent_by_id(agent_id)
        if not agent:
            raise NotFoundException(f"Agent with id {agent_id} not found")

        agent.update_rating(rating_data.rating)
        await self.db.commit()
        await self.db.refresh(agent)
        return agent

    async def increment_agent_usage(self, agent_id: str) -> Agent:
        """Increment agent usage count."""
        agent = await self.get_agent_by_id(agent_id)
        if not agent:
            raise NotFoundException(f"Agent with id {agent_id} not found")

        agent.increment_usage()
        await self.db.commit()
        await self.db.refresh(agent)
        return agent
