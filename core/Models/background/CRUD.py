from tasks.models import *
from core.helpers import crud
from .CrudOperations import Background

"""
    Generic CRUD Operations that can be used through out the system.
"""
class Generic(Background):

    def __init__(self):
        super().__init__()

    def create(self, dictionary):
        self.saveSubmission('create', dictionary)  # hence forth dictionary => self.submission
        
        #self.log(self.submission, 'FORM-------------------------------------')
        #self.log(completeRecord, 'DB-------------------------------------', 2)
        
        masterRecord = self.createMasterTable(self.dbConfigs['mtAbbrv'], self.mtModel)
        rdbms = {self.space: self.dbConfigs, 'tables': self.tables}

        if not hasattr(masterRecord, 'id') or not isinstance(masterRecord.id, int):
            raise Exception(f'Something went wrong. {self.space} record could not be created in: {self.space}.CRUD.create().')

        self.submission[self.dbConfigs['mtId']] = masterRecord.id  # add master table ID to dictionary

        # Time to create child records, loop through each child table:
        for pk in self.idCols:
            if pk == self.dbConfigs['mtAbbrv'] + 'id':
                continue

            tbl = pk[0]  # table abbreviation
            t = crud.generateModelInfo(rdbms, self.space, tbl)
            model = globals()[t['model']]  # retrieve Model class with global scope

            self.createChildTable(model, tbl, t['table'], t['cols'])

    def read(self):
        pass  # defined in individual Module's class extensions.

    def update(self, dictionary):
        self.saveSubmission('update', dictionary)  # hence forth dictionary => self.submission

        mtId = self.dbConfigs['mtAbbrv'] + 'id'
        rdbms = {self.space: self.dbConfigs, 'tables': self.tables}

        if mtId not in self.submission:
            raise Exception(f'Update operation needs {self.space} id, in: {self.space}.CRUD.update().')

        if not crud.isValidId(self.submission, mtId):
            raise Exception(f'{self.space} ID provided must be a valid integer and greater than zero, in: {self.space}.CRUD.update().')

        self.submission[mtId] = int(self.submission[mtId])
        completeRecord = self.fetchFullRecordForUpdate(self.submission[mtId])

        if not completeRecord:
            raise Exception(f'No valid record found for provided {self.space} ID, in: {self.space}.CRUD.update().')

        # Loop through each defined Primary Key to see if its table needs an update
        for pk in self.idCols:
            tbl = pk[0]  # child table abbreviation
            t = crud.generateModelInfo(rdbms, self.space, tbl)
            model = globals()[t['model']]  # retrieve Model class with global scope

            if pk == mtId:
                self.updateMasterTable(model, t['table'], t['cols'], completeRecord)
                continue

            if pk not in self.submission:
                self.createChildTable(model, tbl, t['table'], t['cols'])
                continue
                
            if not crud.isValidId(self.submission, pk):
                # create a new record for child table if pk is invalid
                self.createChildTable(model, tbl, t['table'], t['cols'])
                continue

            # determine if an update is necessary and carry out update operations...
            self.updateChildTable(model, tbl, t['table'], t['cols'], completeRecord)

    def delete(self, masterId):
        if not isinstance(masterId, int) or masterId < 1:
            raise Exception(f'{self.space} Record could not be deleted. Invalid id supplied in {self.space}.CRUD.delete()')

        rdbms = {self.space: self.dbConfigs, 'tables': self.tables}

        for pk in self.idCols:
            tbl = pk[0]  # table abbreviation

            if pk == self.dbConfigs['mtAbbrv'] + 'id':
                continue  # skip, we delete master table at the end.

            t = crud.generateModelInfo(rdbms, self.space, tbl)
            model = globals()[t['model']]  # retrieve Model class with global scope

            # run a 'delete' operation for latest child table record. 
            self.deleteChildTable(model, tbl, t['table'], t['cols'], masterId)

        # once all children records have been updated with delete markers
        self.deleteMasterTable(masterId)


    