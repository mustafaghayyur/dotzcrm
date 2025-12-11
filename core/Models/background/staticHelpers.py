from django.utils import timezone
import datetime

class ValuesHandler:
    """
        Holds only static methods.
        You call them with:
         > ValuesHandler.{method_name}(args)
    """
    
    @staticmethod 
    def amendFormValue(dbValue, formValue):
        if isinstance(formValue, object):
            if hasattr(formValue, 'id'):
                # need to overwrite dictionary key with int value for comparison
                formValue = formValue.id

        return formValue

    @staticmethod
    def amendDatabaseValue(dbValue, formValue):
        if formValue is not None and isinstance(formValue, datetime.datetime):
            dbValue = timezone.make_aware(dbValue, timezone.get_current_timezone())

        return dbValue