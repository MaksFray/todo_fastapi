from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Task
from core.schemas.tasks import TaskCreate

async def create_task(
    session: AsyncSession,
    task_create: TaskCreate,
) -> Task:
    task = Task(**task_create.model_dump())
    session.add(task)
    await session.commit()
    # await session.refresh(user)
    return task