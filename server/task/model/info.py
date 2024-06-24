from laorm import FieldDescriptor, table
from pydantic import BaseModel


@table("task")
class TaskInfo(BaseModel):
    """
    id \n
    task_name 任务名 \n
    type 任务类型 \n
    cron
    execute_time
    content
    description
    run_count
    last_run_times
    status
    uid
    """

    id: str = FieldDescriptor(primary=True)
    task_name: str = FieldDescriptor()
    type: str = FieldDescriptor()
    cron: str = FieldDescriptor()
    execute_time: str = FieldDescriptor()
    content: str = FieldDescriptor()
    description: str = FieldDescriptor()
    run_count: str = FieldDescriptor()
    last_run_times: int = FieldDescriptor()
    status: str = FieldDescriptor()
    uid: str = FieldDescriptor()
