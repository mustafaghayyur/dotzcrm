from datetime import datetime
from django.utils import timezone
from pydantic import BaseModel, Field, PositiveInt, StringConstraints

from tasks.models import *
from tasks.drm.mapper_values import *

"""
    Find out more: https://docs.pydantic.dev/latest/concepts/models/#model-methods-and-properties
"""
class TaskO2ORecord(BaseModel):
    tid: int
    did: int
    lid: int
    sid: int
    aid: int
    vid: int

    description: str = 'Task Description', StringConstraints(max_length=255)
    details: str
    deadline: datetime = None
    status: Status
    visibility: Visibility
    creator: int
    parent: int
    assignor: int
    assignee: int

    dlatest: Latest
    llatest: Latest
    slatest: Latest
    alatest: Latest
    vlatest: Latest

    tcreate_time: datetime = Field(default_factory=timezone.now)
    dcreate_time: datetime = Field(default_factory=timezone.now)
    lcreate_time: datetime = Field(default_factory=timezone.now)
    screate_time: datetime = Field(default_factory=timezone.now)
    acreate_time: datetime = Field(default_factory=timezone.now)
    vcreate_time: datetime = Field(default_factory=timezone.now)

    tdelete_time: datetime
    ddelete_time: datetime
    ldelete_time: datetime
    sdelete_time: datetime
    adelete_time: datetime
    vdelete_time: datetime

    tupdate_time: datetime = Field(default_factory=timezone.now)


    

"""
    external_data = {
        'id': 123,
        'signup_ts': '2019-06-01 12:22',  
        'tastes': {
            'wine': 9,
            b'cheese': 7,  
            'cabbage': '1',  
        },
    }

    task = TaskO2ORecord(**external_data)  

    print(task.id)  
    #> 123
    # task.model_dump() (dict) or task.model_dump_json() (JSON string) t
    print(task.model_dump())
"""