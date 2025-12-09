from django.conf import settings as ds  # stands for django-settings
from core.helpers import misc, crud


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
        
        if self.mapper.master('abbreviation') + 'id' not in dictionary:
            raise Exception(f'Could not complete operation; Master-Table ID is missing. In {self.space}.CRUD.{operation}()')

        if masterId not in dictionary:
            dictionary[masterId] = dictionary[self.mapper.master('abbreviation') + 'id']

        if not crud.isValidId(dictionary, masterId):
            raise Exception(f'Could not complete operation; \'master_id\' missing. In {self.space}.CRUD.{operation}()')

        if 'id' not in dictionary:
            dictionary['id'] = dictionary[masterId]

        return dictionary


    def log(self, subject, log_message, level = 1):
        if ds.DEBUG:
            misc.log(subject, {'space': self.space, 'msg': log_message}, level, self.module['crud_logger_file'], crud=True)
