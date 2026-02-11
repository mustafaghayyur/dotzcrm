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
    def fixTimeZones(value):
        """
            attempts to convert datetime value (if naive) into correct timezone.
            
            :param value: [datetime] dataabase datetime field value
        """
        if value is not None and isinstance(value, datetime.datetime) and value.tzinfo is None:
            value = timezone.make_aware(value, timezone.get_current_timezone())

        return value