from rest_framework.serializers import Serializer, IntegerField, ChoiceField, CharField, DateTimeField

from tasks.drm.mapper_values import *
from core.helpers import validators

"""
    Repeating options saved to dictionaries for convinient reuse...
"""
intNullableOpts = {
    'allow_null': True, 
    'required': False, 
    'validators': [validators.isPositiveIdOrNone]
}

intMandatoryOpts = {
    'allow_null': False, 
    'required': True, 
    'validators': [validators.isPositiveIdAlways]
}

datetimeNullableOpts = {
    'allow_null': True, 
    'required': False, 
    'validators': [validators.isPastDatetimeOrNone]
}

latestChoiceOpts = {
    'choices': [(c.value, c.value) for c in Latest], 
    'allow_null': True,
    'required': False,
    'validators': [validators.isLatestChoicetOrNone]
}

class DateTimeFieldForJS(DateTimeField):
    def to_representation(self, value):
        # Example format: '2025-01-03T01:55:00Z' (simplified format, often preferred)
        return value.strftime('%Y-%m-%dT%H:%M:%SZ')

class TaskO2ORecord(Serializer):
    """
        Serializer for O2O Task records.
    """
    id = IntegerField(**intNullableOpts)  # id = tid; but different places require different terms.
    tid = IntegerField(**intNullableOpts)
    did = IntegerField(**intNullableOpts)
    lid = IntegerField(**intNullableOpts)
    sid = IntegerField(**intNullableOpts)
    aid = IntegerField(**intNullableOpts)
    vid = IntegerField(**intNullableOpts)

    description = CharField(allow_null=False, required=True, min_length=20, max_length=255)
    details = CharField(allow_null=True, required=False, min_length=50)
    
    status = ChoiceField(choices=[(c.value, c.value) for c in Status], default=Status.created.value)
    visibility = ChoiceField(choices=[(c.value, c.value) for c in Visibility], default=Visibility.private.value)

    deadline = DateTimeFieldForJS(allow_null=True, required=False, validators=[validators.isFutureDeadlineOrNone])

    creator_id = IntegerField(**intMandatoryOpts)
    parent_id = IntegerField(**intNullableOpts)
    assignor_id = IntegerField(**intMandatoryOpts)
    assignee_id = IntegerField(**intNullableOpts)

    dlatest = ChoiceField(**latestChoiceOpts)
    llatest = ChoiceField(**latestChoiceOpts)
    slatest = ChoiceField(**latestChoiceOpts)
    alatest = ChoiceField(**latestChoiceOpts)
    vlatest = ChoiceField(**latestChoiceOpts)

    tcreate_time = DateTimeFieldForJS(**datetimeNullableOpts)
    dcreate_time = DateTimeFieldForJS(**datetimeNullableOpts)
    lcreate_time = DateTimeFieldForJS(**datetimeNullableOpts)
    screate_time = DateTimeFieldForJS(**datetimeNullableOpts)
    acreate_time = DateTimeFieldForJS(**datetimeNullableOpts)
    vcreate_time = DateTimeFieldForJS(**datetimeNullableOpts)

    tdelete_time = DateTimeFieldForJS(**datetimeNullableOpts)
    ddelete_time = DateTimeFieldForJS(**datetimeNullableOpts)
    ldelete_time = DateTimeFieldForJS(**datetimeNullableOpts)
    sdelete_time = DateTimeFieldForJS(**datetimeNullableOpts)
    adelete_time = DateTimeFieldForJS(**datetimeNullableOpts)
    vdelete_time = DateTimeFieldForJS(**datetimeNullableOpts)

    tupdate_time = DateTimeFieldForJS(**datetimeNullableOpts)

    """
    def validate(self, data):
    """
    """
                    #If `tid` is not provided, use the provided `id` value.

        if data.get('tid', None) is None and data.get('id', None) is not None:
            data['tid'] = data['id']

        if data.get('id', None) is None and data.get('tid', None) is not None:
            data['id'] = data['tid']

        misc.log(data, 'I am in validate(), after the validation ')
        return data

    def validate_tid(self, value):
        misc.log(value, 'validate_tid() being called.')
        if value is None:
            return self.initial_data.get('id')
        return value

    def to_internal_value(self, data):
        misc.log(data, 'I am in to_internal_value()')
        if data.get('id', None) is None and data.get('tid', None) is not None:
            data = dict(data) # make a copy
            data['id'] = data['tid']
            return super().to_internal_value(data)
    """

class Comment(Serializer):
    id = IntegerField(**intNullableOpts)
    task_id = IntegerField(**intMandatoryOpts)
    comment = CharField(allow_null=False, required=True, min_length=50, max_length=6000)
    parent_id = IntegerField(**intNullableOpts)
    create_time = DateTimeFieldForJS(**datetimeNullableOpts)
    update_time = DateTimeFieldForJS(**datetimeNullableOpts)
    delete_time = DateTimeFieldForJS(**datetimeNullableOpts)

class Watcher(Serializer):
    id = IntegerField(**intNullableOpts)
    task_id = IntegerField(**intMandatoryOpts)
    watcher_id = IntegerField(**intMandatoryOpts)
    latest = ChoiceField(**latestChoiceOpts)
    create_time = DateTimeFieldForJS(**datetimeNullableOpts)
    delete_time = DateTimeFieldForJS(**datetimeNullableOpts)
