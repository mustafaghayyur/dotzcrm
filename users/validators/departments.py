from rest_framework.serializers import Serializer, IntegerField, ChoiceField, CharField

from users.drm.mapper_values import *
from core.helpers import validators
from restapi.validators.generic import *

class DepartmentO2ORecordSerializerGeneric(Serializer):
    """
        Generic Serializer for O2O Department records.
        All fields must be non-mandatory.
    """
    id = IntegerField(**intNullableOpts)  # id = dede_id; but different places require different terms.
    dede_id = IntegerField(**intNullableOpts)

    name = CharField(allow_null=True, allow_blank=True, required=False, max_length=70)
    description = CharField(allow_null=True, allow_blank=True, required=False, min_length=20, max_length=1000)
    
    creator_id = IntegerField(**intNullableOpts)
    parent_id = IntegerField(**intNullableOpts)

    dede_create_time = DateTimeFieldForJS(**datetimeNullableOpts)
    dede_delete_time = DateTimeFieldForJS(**datetimeNullableOpts)
    dede_update_time = DateTimeFieldForJS(**datetimeNullableOpts)

    

class DepartmentO2ORecordSerializerLax(DepartmentO2ORecordSerializerGeneric):
    pass


class DepartmentO2ORecordSerializerStrict(DepartmentO2ORecordSerializerLax):
    pass
