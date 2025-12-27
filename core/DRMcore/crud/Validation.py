from django.conf import settings as ds  # stands for django-settings
from django.utils import timezone

from core.helpers import misc, crud
from .staticHelpers import ValuesHandler

"""
    This class is crudely designed to hold all error handling code for 
    CRUD Operations. Code should be designed to accommodate all modules of CRM
"""
class ErrorHandling:

    def __init__(self):
        pass
        
    def dictValidation(self, space, operation, dictionary):
        if not isinstance(dictionary, dict):
            raise Exception(f'Invalid input provided to {space}.CRUD.{operation}(). Expecting Dictionary.')
    
        if len(dictionary) < 1:
            raise Exception(f'Provided dictionary length zero in: {space}.CRUD.{operation}().')

    def mtIdValidation(self, operation, dictionary):
        masterId = self.mapper.master('foreignKeyName')
        mId = self.mapper.master('abbreviation') + 'id'
        flag = False

        if  mId not in dictionary:
            dictionary[mId] = ''
            flag = True

        if 'id' not in dictionary and not flag:
            dictionary['id'] = dictionary[mId]

        if masterId not in dictionary and not flag:
            dictionary[masterId] = dictionary[mId]

        if 'id' not in dictionary or masterId not in dictionary:
            raise Exception(f'Could not complete operation; master-id is missing. In {self.space}.CRUD.{operation}()')

        if not crud.isValidId(dictionary, mId):
            raise Exception(f'Could not complete operation; master-id not valid. In {self.space}.CRUD.{operation}()')

        return dictionary


    def log(self, subject, log_message, level = 1):
        if ds.DEBUG:
            misc.log(subject, {'space': self.space, 'msg': log_message}, level, self.module['crud_logger_file'], crud=True)
