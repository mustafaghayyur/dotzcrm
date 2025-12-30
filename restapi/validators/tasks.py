from rest_framework.serializers import Serializer, IntegerField, ChoiceField, CharField, DateTimeField

from tasks.drm.mapper_values import *
from core.helpers import crud, misc

"""
    Repeating options saved to dictionaries for convinient reuse...
"""
intNullableOpts = {
    'allow_null': True, 
    'required': False, 
    'validators': [crud.isPositiveIdOrNone]
}

intMandatoryOpts = {
    'allow_null': False, 
    'required': True, 
    'validators': [crud.isPositiveIdAlways]
}

datetimeNullableOpts = {
    'allow_null': True, 
    'required': False, 
    'validators': [crud.isPastDatetimeOrNone]
}

latestChoiceOpts = {
    'choices': [(c.value, c.value) for c in Latest], 
    'allow_null': True,
    'required': False,
    'validators': [crud.isLatestChoicetOrNone]
}

class TaskO2ORecord(Serializer):
    """
        Serializer for O2O Task records.
    """
    id = IntegerField(**intMandatoryOpts)  # id = tid; but different places require different terms.
    tid = IntegerField(allow_null = True, required = False, validators = [crud.isPositiveIdOrNone])
    did = IntegerField(**intNullableOpts)
    lid = IntegerField(**intNullableOpts)
    sid = IntegerField(**intNullableOpts)
    aid = IntegerField(**intNullableOpts)
    vid = IntegerField(**intNullableOpts)

    description = CharField(allow_null=False, required=True, min_length=20, max_length=255)
    details = CharField(allow_null=True, required=False, min_length=50)
    
    status = ChoiceField(choices=[(c.value, c.value) for c in Status], default=Status.created.value)
    visibility = ChoiceField(choices=[(c.value, c.value) for c in Visibility], default=Visibility.private.value)

    deadline = DateTimeField(allow_null=True, required=False, validators=[crud.isFutureDeadlineOrNone])

    creator_id = IntegerField(**intMandatoryOpts)
    parent_id = IntegerField(**intNullableOpts)
    assignor_id = IntegerField(**intMandatoryOpts)
    assignee_id = IntegerField(**intNullableOpts)

    dlatest = ChoiceField(**latestChoiceOpts)
    llatest = ChoiceField(**latestChoiceOpts)
    slatest = ChoiceField(**latestChoiceOpts)
    alatest = ChoiceField(**latestChoiceOpts)
    vlatest = ChoiceField(**latestChoiceOpts)

    tcreate_time = DateTimeField(**datetimeNullableOpts)
    dcreate_time = DateTimeField(**datetimeNullableOpts)
    lcreate_time = DateTimeField(**datetimeNullableOpts)
    screate_time = DateTimeField(**datetimeNullableOpts)
    acreate_time = DateTimeField(**datetimeNullableOpts)
    vcreate_time = DateTimeField(**datetimeNullableOpts)

    tdelete_time = DateTimeField(**datetimeNullableOpts)
    ddelete_time = DateTimeField(**datetimeNullableOpts)
    ldelete_time = DateTimeField(**datetimeNullableOpts)
    sdelete_time = DateTimeField(**datetimeNullableOpts)
    adelete_time = DateTimeField(**datetimeNullableOpts)
    vdelete_time = DateTimeField(**datetimeNullableOpts)

    tupdate_time = DateTimeField(**datetimeNullableOpts)

    def validate(self, data):
        """
            If `tid` is not provided, use the provided `id` value.
        """
        if data.get('tid') is None and data.get('id') is not None:
            data['tid'] = data['id']
        return data
    
    def validate_tid(self, value):
        misc.log(value, 'validate_tid() being called.')
        if value is None:
            return self.initial_data.get('id')
        return value
    
    def to_internal_value(self, data):
        misc.log(data, 'I am in to_internal_value()')
        if data.get('tid') is None and data.get('id') is not None:
            data = dict(data) # make a copy
            data['tid'] = data['id']
            return super().to_internal_value(data)
    
