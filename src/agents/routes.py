"""Agent routes for API endpoints."""

from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Path, Query, status
from src.agents.models import Agent
from src.agents.schemas import (
    AgentAdminResponse,
    AgentCommonResponse,
    AgentCreate,
    AgentListParams,
    AgentListResponsePaginated,
    AgentRating,
    AgentUpdate,
)
from src.agents.services import AgentService
from src.core.logger import logger
from src.core.security import admin_user_dependency, auth_user_dependency, db_dependency
from src.exceptions import NotFoundException

router = APIRouter(prefix="/agents", tags=["Agents"])


def _build_agent_list_response(agent: Agent) -> AgentCommonResponse:
    """Helper function to build AgentListResponse from Agent model."""

    return AgentCommonResponse(
        **{
            "id": str(agent.id),
            "name": agent.name,
            "description": agent.description,
            "expertise_area": agent.expertise_area,
            "avatar_url": agent.avatar_url,
            "avatar_emoji": agent.avatar_emoji,
            "primary_color": agent.primary_color,
            "is_featured": agent.is_featured,
            "is_premium": agent.is_premium,
            "created_at": agent.created_at,
            "updated_at": agent.updated_at,
        },
        professional_areas=agent.get_agent_professional_areas(),  # type: ignore
    )


def _build_agent_response(agent) -> AgentAdminResponse:
    """Helper function to build AgentAdminResponse from Agent model."""
    return AgentAdminResponse(
        **{
            "id": str(agent.id),
            "name": agent.name,
            "description": agent.description,
            "expertise_area": agent.expertise_area,
            "system_prompt": agent.system_prompt,
            "personality_traits": agent.personality_traits,
            "conversation_style": agent.conversation_style,
            "avatar_url": agent.avatar_url,
            "avatar_emoji": agent.avatar_emoji,
            "primary_color": agent.primary_color,
            "tools_enabled": agent.get_configuration()["tools_enabled"],
            "max_context_length": agent.max_context_length,
            "temperature": agent.temperature,
            "is_featured": agent.is_featured,
            "is_premium": agent.is_premium,
            "status": agent.status,
            "usage_count": agent.usage_count,
            "rating_average": agent.rating_average,
            "rating_count": agent.rating_count,
            "created_at": agent.created_at,
            "updated_at": agent.updated_at,
        },
        professional_areas=agent.get_agent_professional_areas(),
    )


@router.get("", response_model=AgentListResponsePaginated, status_code=status.HTTP_200_OK)
async def get_agents(
    params: Annotated[AgentListParams, Query()], db: db_dependency, current_user: auth_user_dependency
):
    """Get paginated list of agents with filtering and sorting."""
    try:
        logger.info("Fetching agents list")

        service = AgentService(db)
        agents, total = await service.get_agents(params)

        # Convert to response model
        agent_responses = [_build_agent_list_response(agent) for agent in agents]

        return AgentListResponsePaginated(
            agents=agent_responses,
            total=total,
            skip=params.skip,
            limit=params.limit,
            has_next=params.skip + params.limit < total,
            has_prev=params.skip > 0,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error retrieving agents: {str(e)}"
        )


@router.post("", response_model=AgentAdminResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_data: Annotated[AgentCreate, Body(description="Agent data for creation")],
    db: db_dependency,
    current_user: admin_user_dependency,
):
    """Create a new agent (admin only)."""

    try:
        service = AgentService(db)
        agent = await service.create_agent(agent_data)

        return _build_agent_response(agent)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar o agent de nome {agent_data.name}: {str(e)}",
        )


@router.get("/{agent_id}", response_model=AgentAdminResponse)
async def get_agent(
    agent_id: Annotated[str, Path(description="Agent ID")], db: db_dependency, current_user: auth_user_dependency
):
    """Get a specific agent by ID."""
    try:
        service = AgentService(db)
        agent = await service.get_agent_by_id(agent_id)

        if not agent:
            raise NotFoundException(f"Agente com id {agent_id} não encontrado!")

        return _build_agent_response(agent)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar agente: {str(e)}",
        )


@router.put("/{agent_id}", response_model=AgentAdminResponse)
async def update_agent(
    agent_id: Annotated[str, Path(description="Agent ID")],
    agent_data: Annotated[AgentUpdate, Body(description="Agent data for update")],
    db: db_dependency,
    current_user: admin_user_dependency,
):
    """Update an agent (admin only)."""

    try:
        service = AgentService(db)
        agent = await service.update_agent(agent_id, agent_data)
        return _build_agent_response(agent)

    except NotFoundException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao atualizar agente: {str(e)}"
        )


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: Annotated[str, Path(description="Agent ID")], db: db_dependency, current_user: admin_user_dependency
):
    try:
        service = AgentService(db)
        await service.delete_agent(agent_id)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error deleting agent: {str(e)}")


@router.post("/{agent_id}/rate", response_model=AgentCommonResponse)
async def rate_agent(
    agent_id: Annotated[str, Path(description="Agent ID")],
    rating_data: Annotated[AgentRating, Body(description="Rating data for the agent")],
    db: db_dependency,
    current_user: auth_user_dependency,
):
    """Rate an agent."""
    try:
        service = AgentService(db)
        agent = await service.rate_agent(agent_id, rating_data)
        return _build_agent_response(agent)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error rating agent: {str(e)}")
