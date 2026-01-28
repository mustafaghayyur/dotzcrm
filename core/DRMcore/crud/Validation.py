from django.conf import settings as ds  # stands for django-settings
from core.helpers import misc, crud

"""
    This class is crudely designed to hold all error handling code for 
    CRUD Operations. Code should be designed to accommodate all modules of CRM
"""
class ErrorHandling:
        
    def dictValidation(self, space, operation, dictionary):
        """
            Validates a dictionary passed to CRUD class.
        
            :param space: [string] App this crud is belongs to.
            :param operation: [string] CRUD operation
            :param dictionary: [dict] of submitted data to process
        """
        if not isinstance(dictionary, dict):
            raise Exception(f'Invalid input provided to {space}.CRUD.{operation}(). Expecting Dictionary.')
    
        if len(dictionary) < 1:
            raise Exception(f'Provided dictionary length zero in: {space}.CRUD.{operation}().')

    def mtIdValidation(self, operation, dictionary):
        """
            Ensures master-record-id is present in submitted-dictionary.
        """        
        keys = ['id', self.mapper.master('abbreviation') + 'id', self.mapper.master('foreignKeyName')]
        id = None

        for key in keys:
            if key not in dictionary:
                dictionary[key] = None
        
        for key in keys:
            if dictionary[key] is not None:
                id = dictionary[key]
        
        if id is None or not crud.isValidId({'id': id}, 'id'):
            raise Exception(f'Could not complete operation; master-record-id is not valid or missing. In {self.space}.CRUD.{operation}()')
        
        for key in keys:
            dictionary[key] = id
        
        return dictionary
    

    def generateRelationTypeIds(self, relationType):
        """
            Returns [list] of id column names with tbl prefix prepended.
            You can fetch 'o2o', 'm2m', 'rlc' columns with this.
            Defaults to 'o2o'
        """
        abbrvs = self.mapper.tablesForRelationType(relationType)
        ids = []

        for abbrv in abbrvs:
            ids.append(abbrv + '_id')
        return ids


    def log(self, subject, log_message, level = 1):
        """
            Logs all C.U.D. operations in CRUD.log
            
            :param subject: [*] any variable to inspect in logs
            :param log_message: string message for log
            :param level: 1 = minimal details | 2 = deep dive into subject
        """
        if ds.DEBUG:
            misc.log(subject, {'space': self.space, 'msg': log_message}, level, self.module['crud_logger_file'], crud=True)
