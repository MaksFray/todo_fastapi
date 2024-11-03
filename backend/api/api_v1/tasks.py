from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import NoResultFound
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


@router.get("", response_model=list[TaskRead])
async def get_all_task(
session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ],
):
    tasks = await tasks_crud.get_all_tasks(session=session)
    return tasks

@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ],
        task_id: int) -> Task:
    try:
        todo = await tasks_crud.get_task(session=session, task_id=task_id)
        return todo
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail=f"Todo with id {task_id} not found"
        )



