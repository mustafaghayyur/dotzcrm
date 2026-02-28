from rest_framework.serializers import Serializer, IntegerField, ChoiceField

from tasks.drm.mapper_values import *
from restapi.validators.generic import *

class UserReportingSerializerGeneric(Serializer):
    """
        Generic serializer, all fields must be nullable
    """
    id = IntegerField(**intNullableOpts)
    usre_id = IntegerField(**intNullableOpts)
    reperter_id = IntegerField(**intNullableOpts)
    reportsTo_id = IntegerField(**intNullableOpts)
    latest = ChoiceField(**latestChoiceOpts)
    create_time = DateTimeFieldForJS(**datetimeNullableOpts)
    delete_time = DateTimeFieldForJS(**datetimeNullableOpts)

class UserReportingSerializerLax(UserReportingSerializerGeneric):
    pass
class UserReportingSerializerStrict(UserReportingSerializerLax):
    pass



