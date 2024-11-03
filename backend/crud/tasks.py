from typing import Sequence

from sqlalchemy import select
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

async def get_all_tasks(session: AsyncSession) -> Sequence[Task]:
    stmt = select(Task).order_by(Task.id)
    result = await session.scalars(stmt)
    return result.all()

async def get_task(session: AsyncSession, task_id: int) -> Task | None:
    return await session.get(Task, task_id)
