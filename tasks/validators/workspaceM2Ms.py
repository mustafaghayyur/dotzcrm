from rest_framework.serializers import Serializer, IntegerField, ChoiceField

from tasks.drm.mapper_values import *
from restapi.validators.generic import *

class WSTaskSerializerGeneric(Serializer):
    """
        Generic serializer, all fields must be nullable
    """
    id = IntegerField(**intNullableOpts)
    wota_id = IntegerField(**intNullableOpts)
    workspace_id = IntegerField(**intNullableOpts)
    task_id = IntegerField(**intNullableOpts)
    latest = ChoiceField(**latestChoiceOpts)
    create_time = DateTimeFieldForJS(**datetimeNullableOpts)
    delete_time = DateTimeFieldForJS(**datetimeNullableOpts)

class WSTaskSerializerLax(WSTaskSerializerGeneric):
    pass
class WSTaskSerializerStrict(WSTaskSerializerLax):
    pass





class WSDepartmentSerializerGeneric(Serializer):
    """
        Generic serializer, all fields must be nullable
    """
    id = IntegerField(**intNullableOpts)
    wode_id = IntegerField(**intNullableOpts)
    workspace_id = IntegerField(**intNullableOpts)
    department_id = IntegerField(**intNullableOpts)
    latest = ChoiceField(**latestChoiceOpts)
    create_time = DateTimeFieldForJS(**datetimeNullableOpts)
    delete_time = DateTimeFieldForJS(**datetimeNullableOpts)

class WSDepartmentSerializerLax(WSDepartmentSerializerGeneric):
    pass
class WSDepartmentSerializerStrict(WSDepartmentSerializerLax):
    pass





class WSUserSerializerGeneric(Serializer):
    """
        Generic serializer, all fields must be nullable
    """
    id = IntegerField(**intNullableOpts)
    wous_id = IntegerField(**intNullableOpts)
    workspace_id = IntegerField(**intNullableOpts)
    user_id = IntegerField(**intNullableOpts)
    latest = ChoiceField(**latestChoiceOpts)
    create_time = DateTimeFieldForJS(**datetimeNullableOpts)
    delete_time = DateTimeFieldForJS(**datetimeNullableOpts)

class WSUserSerializerLax(WSUserSerializerGeneric):
    pass
class WSUserSerializerStrict(WSUserSerializerLax):
    pass