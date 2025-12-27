from . import Background

"""
    Generic CRUD Operations that can be used through out the system.
    One-to-One relationship CRUD types
"""
class CRUD(Background.CrudOperations):

    mtModel = None  # set inheritor class

    def __init__(self):
        super().__init__()

    def create(self, dictionary):
        """
            Validates a given dictionary of key: value pairs. If valid, 
            attempts to save to DB. Else, throws an exception.
        """
        self.saveSubmission('create', dictionary)  # hence forth dictionary => self.submission
        
        # self.log(self.submission, 'FORM-------------------------------------')
        # self.log(completeRecord, 'DB-------------------------------------', 2)
        
        masterRecord = self.createMasterTable(self.mapper.master('abbreviation'), self.mtModel)

        if not hasattr(masterRecord, 'id') or not isinstance(masterRecord.id, int):
            raise Exception(f'Something went wrong. {self.space} record could not be created in: {self.space}.CRUD.create().')

        self.submission[self.mapper.master('foreignKeyName')] = masterRecord.id  # add master table ID to dictionary

        # Time to create child records, loop through each child table:
        for pk in self.idCols:
            if pk == self.mapper.master('abbreviation') + 'id':
                continue

            tbl = pk[0]  # table abbreviation
            t = crud.generateModelInfo(self.mapper, tbl)
            model = globals()[t['model']]  # retrieve Model class with global scope

            self.createChildTable(model, tbl, t['table'], t['cols'])

    def read(self):
        pass  # defined in individual Module's class extensions.

    def update(self, dictionary):
        """
            Validates a given dictionary of key: walue pairs. If valid, 
            attempts to save to DB. Else, throws an exception.
        """
        self.saveSubmission('update', dictionary)  # hence forth dictionary => self.submission

        mId = self.mapper.master('abbreviation') + 'id'

        records = self.fetchFullRecordForUpdate(self.submission[mId])

        if not records:
            raise Exception(f'No valid record found for provided {self.space} ID, in: {self.space}.CRUD.update().')

        if len(records) > 1:
            completeRecord = self.pruneLatestRecords(records, mId)
        else:
            completeRecord = records[0]

        # Loop through each defined Primary Key to see if its table needs an update
        for pk in self.idCols:
            tbl = pk[0]  # child table abbreviation
            t = crud.generateModelInfo(self.mapper, tbl)
            model = globals()[t['model']]  # retrieve Model class with global scope

            if pk == mId:
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
        """
            Validates a given record ID. If valid, attempts to  mark record
            as deleted in DB. Else, throws an exception.
        """
        if not isinstance(masterId, int) or masterId < 1:
            raise Exception(f'{self.space} Record could not be deleted. Invalid id supplied in {self.space}.CRUD.delete()')

        for pk in self.idCols:
            tbl = pk[0]  # table abbreviation

            if pk == self.mapper.master('abbreviation') + 'id':
                continue  # skip, we delete master table at the end.

            t = crud.generateModelInfo(self.mapper, tbl)
            model = globals()[t['model']]  # retrieve Model class with global scope

            # run a 'delete' operation for latest child table record. 
            self.deleteChildTable(model, tbl, t['table'], t['cols'], masterId)

        # once all children records have been updated with delete markers
        t = crud.generateModelInfo(self.mapper, self.mapper.master('abbreviation'))
        model = globals()[t['model']]
        self.deleteMasterTable(model, self.mapper.master('foreignKeyName'), t['table'], t['cols'], masterId)


    def pruneLatestRecords(self, fetchedRecords, mId):
        """
            Handles scenario where multiple CT records are found to be marked 
            'latest' in DB. These multiples need to be pruned to a single record 
            for each CT.
        """
        pass

        for pk in self.idCols:
            tbl = pk[0]  # table abbreviation

            if pk == self.mapper.master('abbreviation') + 'id':
                continue  # can't prune MT duplicates...

            t = crud.generateModelInfo(self.mapper, tbl)
            model = globals()[t['model']]  # retrieve Model class with global scope

            self.checkChildForMultipleLatests(model, tbl, t['table'], t['cols'], fetchedRecords)

        records = self.fetchFullRecordForUpdate(mId)

        if not records:
            raise Exception(f'No valid record found for provided {self.space} ID, in: {self.space}.CRUD.update().')

        if len(records) > 1:
            return self.pruneLatestRecords(records, mId)  # bit if recursion

        return records[0]


