from tasks.models import *
from core.helpers import crud
from core import settings
from .CrudOperations import Background

"""
    Generic CRUD Operations that can be used through out the system.
"""
class Generic(Background):
    idCols = None
    space = None

    def __init__(self):
        # some code..
        super().__init__()

    def create(self, dictionary):
        self.dictValidation(self.space, 'create', dictionary)

        masterRecord = self.createMasterTable(self.mtabbrv, self.mtModel, dictionary)

        if not masterRecord.id or not isinstance(masterRecord.id, int):
            raise Exception(f'Something went wrong. {self.space} could not be created in: {self.space}.CRUD.create().')

        dictionary[settings.rdbms[self.space]['master_id']] = masterRecord.id  # add master table ID to dictionary

        # Time to create child records, loop through each child table:
        for pk in self.idCols:
            if pk == self.mtabbrv + 'id':
                continue

            tbl = pk[0]  # table abbreviation
            t = crud.generateModelInfo(settings.rdbms, self.space, tbl)
            model = globals()[t['model']]  # retrieve Model class with global scope

            self.createChildTable(model, tbl, t['table'], t['cols'], dictionary)

    def read(self):
        pass

    def update(self, dictionary):
        self.dictValidation(self.space, 'update', dictionary)

        if self.mtabbrv + 'id' not in dictionary:
            raise Exception(f'Update operation needs {self.space} id, in: {self.space}.CRUD.update().')

        if not isinstance(dictionary['tid'], int) or dictionary['tid'] < 1:
            raise Exception(f'{self.space} ID provided must be of int() format and greater than zero, in: {self.space}.CRUD.update().')

        completeRecord = self.fetchFullRecordForUpdate(dictionary['tid'])

        if not completeRecord:
            raise Exception(f'No valid record found for provided Task ID, in: {self.space}.CRUD.update().')

        # Loop through each defined Primary Key to see if its table needs an update
        for pk in self.idCols:
            tbl = pk[0]  # table abbreviation
            t = crud.generateModelInfo(settings.rdbms, self.space, tbl)
            model = globals()[t['model']]  # retrieve Model class with global scope

            if pk == self.mtabbrv + 'id':
                self.updateMasterTable(self.space, completeRecord, dictionary, model, t['table'], t['cols'])
                continue

            if pk not in dictionary:
                self.createChildTable(model, tbl, t['table'], t['cols'], dictionary)
                continue
                
            if not isinstance(dictionary[pk], int) or dictionary[pk] < 1:  # create a new record for child table
                self.createChildTable(model, tbl, t['table'], t['cols'], dictionary)
                continue

            # determine if an update is necessary and carry out update operations...
            self.updateChildTable(model, completeRecord, tbl, t['table'], t['cols'], dictionary)

    def delete(self, masterId):
        # Delete the tasks
        if not isinstance(masterId, int) or masterId < 1:
            raise Exception(f'{self.space} Record could not be deleted. Invalid id supplied in {self.space}.CRUD.delete()')

        for pk in self.idCols:
            tbl = pk[0]  # table abbreviation

            if pk == self.mtabbrv + 'id':
                continue  # skip, we delete master table at the end.

            t = crud.generateModelInfo(settings.rdbms, self.space, tbl)
            model = globals()[t['model']]  # retrieve Model class with global scope

            # run a 'delete' operation for latest child table record. 
            self.deleteChildTable(model, latest, tbl, t['table'], t['cols'], masterId)

        # once all children records have been updated with delete markers
        self.deleteMasterTable(masterId)


    