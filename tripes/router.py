from typing import Annotated

from fastapi import APIRouter, Depends

from tripes.schema import STasksAdd
from tripes.reposit import TaskRepository

router = APIRouter(
    prefix='/tasks',
    tags=['Задачи']
)


@router.post('')
async def add_tasks(task: Annotated[STasksAdd, Depends()]):
    task_id = await TaskRepository.add_task(task)
    return {'ok': True, 'task_id': task_id}


@router.get('')
async def get_tasks():
    tasks = await TaskRepository.find_all()
    return {'tasks': tasks}
