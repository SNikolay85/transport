from sqlalchemy import select

from tripes.database import new_session, TaskOrm
from tripes.schema import STasksAdd


class TaskRepository:
    @classmethod
    async def add_task(cls, data: STasksAdd) -> int:
        async with new_session as session:
            task_dict = data.model_dump()

            task = TaskOrm(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task.id

    @classmethod
    async def find_all(cls):
        async with new_session as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            return task_models
