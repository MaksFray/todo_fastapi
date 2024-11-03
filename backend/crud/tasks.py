from typing import Sequence, Annotated

from fastapi import Path, Depends, HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Task, db_helper
from core.schemas.tasks import TaskCreate, TaskUpdate


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


async def task_by_id(
        task_id: Annotated[int, Path],
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ],
) -> Task:
    task = await get_task(session=session, task_id=task_id)
    if task is not None:
        return task


async def update_task(
        session: AsyncSession,
        task: Task,
        task_update: TaskUpdate
) -> Task:
    for name, value in task_update.model_dump().items():
        setattr(task, name, value)
    await session.commit()
    return task
