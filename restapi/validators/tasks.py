from rest_framework import serializers
from datetime import datetime
from django.utils import timezone
from typing import Annotated

from tasks.drm.mapper_values import *
from core.helpers import crud

class TaskO2ORecord(serializers.Serializer):
    tid = serializers.IntegerField(allow_null=True, required=False, validators=[crud.isPositiveIdOrNone])
    did = serializers.IntegerField(allow_null=True, required=False, validators=[crud.isPositiveIdOrNone])
    lid = serializers.IntegerField(allow_null=True, required=False, validators=[crud.isPositiveIdOrNone])
    sid = serializers.IntegerField(allow_null=True, required=False, validators=[crud.isPositiveIdOrNone])
    aid = serializers.IntegerField(allow_null=True, required=False, validators=[crud.isPositiveIdOrNone])
    vid = serializers.IntegerField(allow_null=True, required=False, validators=[crud.isPositiveIdOrNone])

    description = serializers.CharField(allow_null=False, required=True, min_length=20, max_length=255)
    details = serializers.CharField(allow_null=True, required=False, min_length=50)
    
    status = serializers.ChoiceField(choices=[(c.value, c.value) for c in Status], default=Status.created.value)
    visibility = serializers.ChoiceField(choices=[(c.value, c.value) for c in Visibility], default=Visibility.private.value)

    deadline = serializers.DateTimeField(allow_null=True, required=False, validators=[crud.isFutureDeadlineOrNone])

    creator = serializers.IntegerField(allow_null=False, required=True, validators=[crud.isPositiveIdAlways])
    parent = serializers.IntegerField(allow_null=True, required=False, validators=[crud.isPositiveIdOrNone])
    assignor = serializers.IntegerField(allow_null=False, required=True, validators=[crud.isPositiveIdAlways])
    assignee = serializers.IntegerField(allow_null=True, required=False, validators=[crud.isPositiveIdOrNone])

    dlatest = serializers.ChoiceField(choices=[(c.value, c.value) for c in Latest], default=Latest.latest.value)
    llatest = serializers.ChoiceField(choices=[(c.value, c.value) for c in Latest], default=Latest.latest.value)
    slatest = serializers.ChoiceField(choices=[(c.value, c.value) for c in Latest], default=Latest.latest.value)
    alatest = serializers.ChoiceField(choices=[(c.value, c.value) for c in Latest], default=Latest.latest.value)
    vlatest = serializers.ChoiceField(choices=[(c.value, c.value) for c in Latest], default=Latest.latest.value)

    tcreate_time = serializers.DateTimeField(allow_null=True, required=False, validators=[crud.isPastDatetimeOrNone])
    dcreate_time = serializers.DateTimeField(allow_null=True, required=False, validators=[crud.isPastDatetimeOrNone])
    lcreate_time = serializers.DateTimeField(allow_null=True, required=False, validators=[crud.isPastDatetimeOrNone])
    screate_time = serializers.DateTimeField(allow_null=True, required=False, validators=[crud.isPastDatetimeOrNone])
    acreate_time = serializers.DateTimeField(allow_null=True, required=False, validators=[crud.isPastDatetimeOrNone])
    vcreate_time = serializers.DateTimeField(allow_null=True, required=False, validators=[crud.isPastDatetimeOrNone])

    tdelete_time = serializers.DateTimeField(allow_null=True, required=False, validators=[crud.isPastDatetimeOrNone])
    ddelete_time = serializers.DateTimeField(allow_null=True, required=False, validators=[crud.isPastDatetimeOrNone])
    ldelete_time = serializers.DateTimeField(allow_null=True, required=False, validators=[crud.isPastDatetimeOrNone])
    sdelete_time = serializers.DateTimeField(allow_null=True, required=False, validators=[crud.isPastDatetimeOrNone])
    adelete_time = serializers.DateTimeField(allow_null=True, required=False, validators=[crud.isPastDatetimeOrNone])
    vdelete_time = serializers.DateTimeField(allow_null=True, required=False, validators=[crud.isPastDatetimeOrNone])

    tupdate_time = serializers.DateTimeField(allow_null=True, required=False, validators=[crud.isPastDatetimeOrNone])


    

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