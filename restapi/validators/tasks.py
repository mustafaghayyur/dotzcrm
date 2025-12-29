from datetime import datetime
from django.utils import timezone
from pydantic import BaseModel, PositiveInt, StringConstraints

from tasks.models import *

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
    status: str
    visibility: str
    creator: int
    parent: int
    assignor: int
    assignee: int

    dlatest: int = 1
    llatest: int = 1
    slatest: int = 1
    alatest: int = 1
    vlatest: int = 1

    tcreate_time: datetime | timezone.now()
    dcreate_time: datetime | timezone.now()
    lcreate_time: datetime | timezone.now()
    screate_time: datetime | timezone.now()
    acreate_time: datetime | timezone.now()
    vcreate_time: datetime | timezone.now()

    tdelete_time: datetime | timezone.now()
    ddelete_time: datetime | timezone.now()
    ldelete_time: datetime | timezone.now()
    sdelete_time: datetime | timezone.now()
    adelete_time: datetime | timezone.now()
    vdelete_time: datetime | timezone.now()

    tupdate_time: datetime | timezone.now()


    


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