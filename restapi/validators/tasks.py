from datetime import datetime
from django.utils import timezone
from pydantic import BaseModel, Field, AfterValidator
from typing import Annotated

from tasks.models import *
from tasks.drm.mapper_values import *
from core.helpers import crud

"""
    Find out more: https://docs.pydantic.dev/latest/concepts/models/#model-methods-and-properties
"""
class TaskO2ORecord(BaseModel):
    tid: Annotated[int, Field(gt=0)]
    did: Annotated[int, Field(None, gt=0)]
    lid: Annotated[int, Field(None, gt=0)]
    sid: Annotated[int, Field(None, gt=0)]
    aid: Annotated[int, Field(None, gt=0)]
    vid: Annotated[int, Field(None, gt=0)]

    description: Annotated[str, Field(None, max_length=255)]
    details: Annotated[str, Field(None, min_length=50)]
    status: Annotated[Status, Field(None, max_length=20)]
    visibility: Annotated[Visibility, Field(None, max_length=20)]

    deadline: Annotated[datetime | None, Field(default_factory=timezone.now), AfterValidator(crud.isFutureDatetime)]

    creator: Annotated[int, Field(None, gt=0)]
    parent: Annotated[int, Field(None, gt=0)]
    assignor: Annotated[int, Field(None, gt=0)]
    assignee: Annotated[int, Field(None, gt=0)]

    dlatest: Annotated[Latest, Field(None, max_length=1)]
    llatest: Annotated[Latest, Field(None, max_length=1)]
    slatest: Annotated[Latest, Field(None, max_length=1)]
    alatest: Annotated[Latest, Field(None, max_length=1)]
    vlatest: Annotated[Latest, Field(None, max_length=1)]

    tcreate_time: Annotated[datetime, Field(default_factory=timezone.now), AfterValidator(crud.isPastDatetime)]
    dcreate_time: Annotated[datetime | None, Field(default_factory=timezone.now), AfterValidator(crud.isPastDatetime)]
    lcreate_time: Annotated[datetime | None, Field(default_factory=timezone.now), AfterValidator(crud.isPastDatetime)]
    screate_time: Annotated[datetime | None, Field(default_factory=timezone.now), AfterValidator(crud.isPastDatetime)]
    acreate_time: Annotated[datetime | None, Field(default_factory=timezone.now), AfterValidator(crud.isPastDatetime)]
    vcreate_time: Annotated[datetime | None, Field(default_factory=timezone.now), AfterValidator(crud.isPastDatetime)]

    tdelete_time: Annotated[datetime | None, AfterValidator(crud.isPastDatetime)]
    ddelete_time: Annotated[datetime | None, AfterValidator(crud.isPastDatetime)]
    ldelete_time: Annotated[datetime | None, AfterValidator(crud.isPastDatetime)]
    sdelete_time: Annotated[datetime | None, AfterValidator(crud.isPastDatetime)]
    adelete_time: Annotated[datetime | None, AfterValidator(crud.isPastDatetime)]
    vdelete_time: Annotated[datetime | None, AfterValidator(crud.isPastDatetime)]

    tupdate_time: Annotated[datetime, Field(default_factory=timezone.now), AfterValidator(crud.isPastDatetime)]


    

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

    =======================================
    error handling possibility (in Model class):
    from pydantic import field_validator
    @field_validator('details')
    @classmethod
    def _validate_details(cls, v):
        if v is None:
            return v
        if isinstance(v, str) and len(v) > 20:
            raise ValueError('details must be at most 20 characters')
        return v
"""