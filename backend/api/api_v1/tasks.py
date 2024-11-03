from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.models import db_helper, Task
from core.schemas.tasks import TaskRead, TaskCreate, TaskUpdate

from crud import tasks as tasks_crud

router = APIRouter(
    tags=["Tasks"],
)


@router.post("", response_model=TaskRead)
async def create_task(
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
async def get_all_tasks(
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
@router.put("/{task_id}", response_model=TaskRead)
async def patch_task_by_id(
        task_update: TaskUpdate,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ],
        task: Task = Depends(tasks_crud.task_by_id),
):
    updated_task = await tasks_crud.update_task(
        session=session,
        task=task,
        task_update=task_update
    )
    return updated_task

@router.delete("/{task_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ],
        task: Task = Depends(tasks_crud.task_by_id),
) -> None:
    await tasks_crud.delete_task(session=session, task=task)
