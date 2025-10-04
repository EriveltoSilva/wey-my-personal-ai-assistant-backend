from datetime import datetime

from src.core.config import settings
from src.core.database import AsyncSessionLocal


async def create_root_user():
    from sqlalchemy import select
    from src.core.security import hash_password
    from src.users.enums import UserRoleEnum
    from src.users.models import User

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).filter_by(username=settings.ADMIN_USERNAME))
        admin = result.scalars().first()
        if not admin:
            admin = User(
                full_name=settings.ADMIN_FULL_NAME,
                username=settings.ADMIN_USERNAME,
                phone=settings.ADMIN_PHONE,
                email=settings.ADMIN_EMAIL,
                role=UserRoleEnum.SUPER_ADMIN.value,
                password=hash_password(settings.ADMIN_PASSWORD),  # ensure ADMIN_PASSWORD is defined in settings
            )
            session.add(admin)
            await session.commit()


async def seed_interests_and_professional_areas():
    from src.users.models import Interest, ProfessionalArea

    async with AsyncSessionLocal() as session:
        async with session.begin():
            # Example professional areas
            professional_areas = [
                ProfessionalArea(
                    name="Engineering",
                    description="Field of designing, building, and maintaining structures, machines, and technology.",
                    code="ENG",
                    is_active=True,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                ),
                ProfessionalArea(
                    name="Law",
                    description="Legal profession and related services.",
                    code="LAW",
                    is_active=True,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                ),
                ProfessionalArea(
                    name="Medicine",
                    description="Healthcare and medical professions.",
                    code="MED",
                    is_active=True,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                ),
            ]

            # Example interests
            interests = [
                Interest(
                    name="Artificial Intelligence",
                    description="Exploring AI applications and research.",
                    category="Technology",
                    is_active=True,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                ),
                Interest(
                    name="Blockchain",
                    description="Decentralized ledger and crypto-related technology.",
                    category="Finance",
                    is_active=True,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                ),
                Interest(
                    name="Renewable Energy",
                    description="Clean and sustainable energy solutions.",
                    category="Environment",
                    is_active=True,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                ),
            ]

            # Add all to the session
            session.add_all(professional_areas + interests)

        await session.commit()
