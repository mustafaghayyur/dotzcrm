from rest_framework.serializers import Serializer, IntegerField, ChoiceField, CharField

from tasks.drm.mapper_values import WSType
from core.helpers import validators
from restapi.validators.generic import *

class WorkSpaceO2ORecordSerializerGeneric(Serializer):
    """
        Generic Serializer for O2O WorkSpace records.
        All fields must be non-mandatory.
    """
    id = IntegerField(**intNullableOpts)  # id = wowo_id; but different places require different terms.
    wowo_id = IntegerField(**intNullableOpts)

    name = CharField(allow_null=True, allow_blank=True, required=False, max_length=1000)
    type = ChoiceField(allow_null=True, allow_blank=True, required=False, choices=[(c.value, c.value) for c in WSType])

    description = CharField(allow_null=True, allow_blank=True, required=False, min_length=20, max_length=6000)
    creator_id = IntegerField(**intNullableOpts)
    wowo_create_time = DateTimeFieldForJS(**datetimeNullableOpts)
    wowo_delete_time = DateTimeFieldForJS(**datetimeNullableOpts)
    wowo_update_time = DateTimeFieldForJS(**datetimeNullableOpts)


    

class WorkSpaceO2ORecordSerializerLax(WorkSpaceO2ORecordSerializerGeneric):
    pass


class WorkSpaceO2ORecordSerializerStrict(WorkSpaceO2ORecordSerializerLax):
    pass
