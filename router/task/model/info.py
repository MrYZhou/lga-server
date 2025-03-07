from laorm import Field, table


@table("task")
class TaskInfo:
    """
    id \n
    task_name  \n
    type 任务类型 \n
    cron
    execute_time
    content
    description
    seconds
    run_count
    last_run_times
    status
    uid
    """

    id: str = Field(primary=True)
    task_name: str = Field("任务名")
    type: str = Field()
    cron: str = Field()
    execute_time: str = Field()
    content: str = Field()
    description: str = Field()
    seconds: int = Field()
    run_count: str = Field()
    last_run_times: int = Field()
    status: str = Field()
    uid: str = Field()
