from django.utils import timezone
from django.db import models
from django.conf import settings as ds  # stands for django-settings

from core.lib.state import State
from . import Validation
from core import dotzSettings
from .validation import Validate
from core.helpers import misc


class Operations():
    """
        This class holds the background operations.
    """
    state = None
    mapper = None


    def __init__(self):
        self.state = State()
        # loads configs related to the module (defined in self.space)
        self.state.set('module', getattr(dotzSettings, self.space))

        # holds all O2O primary keys for given space/module
        self.state.set('idCols', Validate.generateIdColumnsForRelationType(self.mapper, 'o2o'))

        # submission will hold dictionary of submitted data to use for crud operation in question
        self.state.set('submission', None)

        self.startUpCode()


    def startUpCode(self):
        """
            Used by app-level inheritor classes to run init processes.
        """
        pass


    def saveSubmission(self, operation, submission):
        # First, we do some error checking on the dictionary supplied:
        Validate.dictValidation(self.state.get('app'), operation, submission)
        
        if operation != 'create':
            # Second, we make sure the master-table-id is included in record:
            submission = Validate.mtIdValidation(self.mapper, self.state.get('app'), operation, submission)
            
        # Finally, we save the submitted form into state
        self.state.set('submission', submission)



    def checkChildForMultipleLatests(self, modelClass, tbl, tableName, columnsList, fetchedRecords):
        """
            For given CT, see if fetched records have multiple entries 
            marked as 'latest' in the DB.
            @todo
        """
        pass

    def pruneLatestRecords(self, fetchedRecords, mId):
        """
            Handles scenario where multiple CT records are found to be marked 
            'latest' in DB. These multiples need to be pruned to a single record 
            for each CT.
            @todo: implement the whole operation!
        """
        pass

        for pk in self.idCols:
            tbl = pk[:self.abrvSize]  # table abbreviation

            if pk == self.mapper.master('abbreviation') + 'id':
                continue  # can't prune MT duplicates...

            t = crud.generateModelInfo(self.mapper, tbl)

            self.checkChildForMultipleLatests(t['model'], tbl, t['table'], t['cols'], fetchedRecords)

        records = self.fullRecord(mId)

        if not records:
            raise Exception(f'No valid record found for provided {self.space} ID, in: {self.space}.CRUD.update().')

        if len(records) > 1:
            return self.pruneLatestRecords(records, mId)  # bit if recursion

        return records[0]
    
    
    def log(self, subject, log_message, level = 1):
        """
            Logs all C.U.D. operations in CRUD.log
            
            :param subject: [*] any variable to inspect in logs
            :param log_message: string message for log
            :param level: 1 = minimal details | 2 = deep dive into subject
        """
        if ds.DEBUG:
            misc.log(subject, {'space': self.state.get('app'), 'msg': log_message}, level, self.module['crud_logger_file'], crud=True)
