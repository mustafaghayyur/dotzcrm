from rest_framework.serializers import Serializer, IntegerField, ChoiceField, CharField

from tasks.drm.mapper_values import *
from core.helpers import validators
from restapi.validators.generic import *

class TaskO2ORecordSerializerGeneric(Serializer):
    """
        Generic Serializer for O2O Task records.
        All fields must be non-mandatory.
    """
    id = IntegerField(**intNullableOpts)  # id = tid; but different places require different terms.
    tid = IntegerField(**intNullableOpts)
    did = IntegerField(**intNullableOpts)
    lid = IntegerField(**intNullableOpts)
    sid = IntegerField(**intNullableOpts)
    aid = IntegerField(**intNullableOpts)
    vid = IntegerField(**intNullableOpts)

    description = CharField(allow_null=True, required=False, min_length=20, max_length=255)
    details = CharField(allow_null=True, required=False, min_length=50)
    
    status = ChoiceField(allow_null=True, required=False, choices=[(c.value, c.value) for c in Status])
    visibility = ChoiceField(allow_null=True, required=False, choices=[(c.value, c.value) for c in Visibility])

    deadline = DateTimeFieldForJS(allow_null=True, required=False, validators=[validators.isFutureDeadlineOrNone])

    creator_id = IntegerField(**intNullableOpts)
    parent_id = IntegerField(**intNullableOpts)
    assignor_id = IntegerField(**intNullableOpts)
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

        return data

    def validate_tid(self, value):
\        if value is None:
            return self.initial_data.get('id')
        return value

    def to_internal_value(self, data):
\        if data.get('id', None) is None and data.get('tid', None) is not None:
            data = dict(data) # make a copy
            data['id'] = data['tid']
            return super().to_internal_value(data)
    """
