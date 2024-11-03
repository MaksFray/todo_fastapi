from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Task
from core.schemas.tasks import TaskRead, TaskCreate

from crud import tasks as tasks_crud

router = APIRouter(
    tags=["Tasks"],
)

@router.post("", response_model=TaskRead)
async def create_user(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ],
    task_create: TaskCreate,
) -> Task:
    task = await tasks_crud.create_task(
        session=session,
        task_create=task_create)
    return task


