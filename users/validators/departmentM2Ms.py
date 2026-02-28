from rest_framework.serializers import Serializer, IntegerField, ChoiceField

from tasks.drm.mapper_values import *
from restapi.validators.generic import *

class DeptHeadSerializerGeneric(Serializer):
    """
        Generic serializer, all fields must be nullable
    """
    id = IntegerField(**intNullableOpts)
    dehe_id = IntegerField(**intNullableOpts)
    department_id = IntegerField(**intNullableOpts)
    head_id = IntegerField(**intNullableOpts)
    latest = ChoiceField(**latestChoiceOpts)
    create_time = DateTimeFieldForJS(**datetimeNullableOpts)
    delete_time = DateTimeFieldForJS(**datetimeNullableOpts)

class DeptHeadSerializerLax(DeptHeadSerializerGeneric):
    pass
class DeptHeadSerializerStrict(DeptHeadSerializerLax):
    pass





class DeptUserSerializerGeneric(Serializer):
    """
        Generic serializer, all fields must be nullable
    """
    id = IntegerField(**intNullableOpts)
    deus_id = IntegerField(**intNullableOpts)
    department_id = IntegerField(**intNullableOpts)
    user_id = IntegerField(**intNullableOpts)
    latest = ChoiceField(**latestChoiceOpts)
    create_time = DateTimeFieldForJS(**datetimeNullableOpts)
    delete_time = DateTimeFieldForJS(**datetimeNullableOpts)

class DeptUserSerializerLax(DeptUserSerializerGeneric):
    pass
class DeptUserSerializerStrict(DeptUserSerializerLax):
    pass