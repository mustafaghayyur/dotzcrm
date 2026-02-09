from django.utils import timezone
import datetime

class Values:
    """
        Static Class
        Translates CRUD values between form and database
    """
    
    @staticmethod 
    def convertModelToId(value):
        """
            attempts to convert provided Model object into it's 'id' attribute.
            
            :param value: [Model instance] any Django model insatnce
        """
        if hasattr(value, 'id'):
                value = value.id
        return value

    @staticmethod
    def fixTimeZones(dbValue):
        """
            attempts to convert datetime value into correct timezone.
            
            :param dbValue: [datetime] dataabase datetime field value
        """
        if dbValue is not None and isinstance(dbValue, datetime.datetime):
            dbValue = timezone.make_aware(dbValue, timezone.get_current_timezone())

        return dbValue