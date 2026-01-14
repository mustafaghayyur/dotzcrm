from rest_framework.serializers import Serializer, IntegerField, CharField

from tasks.drm.mapper_values import *
from restapi.validators.generic import *

class CommentSerializerGeneric(Serializer):
    id = IntegerField(**intNullableOpts)
    task_id = IntegerField(**intMandatoryOpts)
    comment = CharField(allow_null=False, required=True, min_length=50, max_length=6000)
    creator_id = IntegerField(**intNullableOpts)
    parent_id = IntegerField(**intNullableOpts)
    create_time = DateTimeFieldForJS(**datetimeNullableOpts)
    update_time = DateTimeFieldForJS(**datetimeNullableOpts)
    delete_time = DateTimeFieldForJS(**datetimeNullableOpts)
