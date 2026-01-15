from rest_framework.serializers import Serializer, IntegerField, ChoiceField

from tasks.drm.mapper_values import *
from restapi.validators.generic import *

class WatcherSerializerGeneric(Serializer):
    id = IntegerField(**intNullableOpts)
    task_id = IntegerField(**intMandatoryOpts)
    watcher_id = IntegerField(**intMandatoryOpts)
    latest = ChoiceField(**latestChoiceOpts)
    create_time = DateTimeFieldForJS(**datetimeNullableOpts)
    delete_time = DateTimeFieldForJS(**datetimeNullableOpts)
