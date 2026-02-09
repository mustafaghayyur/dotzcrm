from django.conf import settings as ds  # stands for django-settings

from core.lib.state import State
from core import dotzSettings
from .validation import Validate
from .logger import Logger
from core.helpers import crud

class Operations():
    """
        This class holds the background operations.
    """
    state = None
    mapper = None

    def __init__(self):
        self.state = State()
        # loads configs related to the module (defined in self.state.get('app'))
        self.state.set('module', getattr(dotzSettings, self.state.get('app')))

        # holds all O2O primary keys for given space/module
        self.state.set('idCols', Validate.generateIdColumnsForRelationType(self.mapper, 'o2o'))
        
        self.state.set('abrvSize', dotzSettings.project['mapper']['tblKeySize'] - 1)
        self.state.set('mtModel', None) 

        # submission will hold dictionary of submitted data to use for crud operation in question
        self.state.set('submission', None)
        
        # setup logger
        self.state.set('log', Logger())
        self.state.get('log').settings(self.state.get('app'), self.state.get('module')['crud_logger_file'])

        self.startUpCode()


    def startUpCode(self):
        """
            Used by app-level inheritor classes to run init processes.
        """
        pass


    def setMasterCrudClass(self, classReference):
        self.state.set('masterCrudObj', classReference())


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
            tbl = pk[:self.state.get('abrvSize')]  # table abbreviation

            if pk == self.mapper.master('abbreviation') + '_id':
                continue  # can't prune MT duplicates...

            t = crud.generateModelInfo(self.mapper, tbl)

            self.checkChildForMultipleLatests(t['model'], tbl, t['table'], t['cols'], fetchedRecords)

        records = self.fullRecord(mId)

        if not records:
            raise Exception(f'Error 2090: No valid record found for provided {self.state.get('app')} ID, in: {self.state.get('app')}.CRUD.update().')

        if len(records) > 1:
            return self.pruneLatestRecords(records, mId)  # bit if recursion

        return records[0]
    
