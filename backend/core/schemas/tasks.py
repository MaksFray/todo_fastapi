from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    title: str
    description: str


class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    model_config = ConfigDict(
        from_attributes=True,
    )
    id: int