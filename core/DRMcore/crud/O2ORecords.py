from . import Background
from core.helpers import crud
from ...dotzSettings import project

"""
    Generic CRUD Operations that can be used through out the system.
    One-to-One relationship CRUD types
"""
class CRUD(Background.CrudOperations):

    mtModel = None  # set in inheritor class

    def __init__(self):
        super().__init__()
        self.abrvSize = project['mapper']['tblKeySize'] - 1

    def create(self, dictionary):
        """
            Validates a given dictionary of key: value pairs. If valid, 
            attempts to save to DB. Else, throws an exception.
        """
        self.saveSubmission('create', dictionary)  # hence forth dictionary => self.submission
        
        masterRecord = self.createMasterTable(self.mapper.master('abbreviation'), self.mtModel)

        if not hasattr(masterRecord, 'id') or not isinstance(masterRecord.id, int):
            raise Exception(f'Something went wrong. {self.space} record could not be created in: {self.space}.CRUD.create().')

        self.submission[self.mapper.master('foreignKeyName')] = masterRecord.id  # add master table ID to dictionary

        # Time to create child records, loop through each child table:
        for pk in self.idCols:
            if pk == self.mapper.master('abbreviation') + 'id':
                continue

            tbl = pk[:self.abrvSize]  # table abbreviation
            t = crud.generateModelInfo(self.mapper, tbl)

            self.createChildTable(t['model'], tbl, t['table'], t['cols'])

        # return masterRecord.id
        return masterRecord

    def read(self, selectors, conditions = None, orderBy = None, limit = None, joins = None, translations = None):
        """
            See documentation on how to form selectors, conditions, etc.
            Chaining enabled when no arguments are provided.
            @return: RawQuerySet | None

            @todo: make read static
        """
        if selectors is None and conditions is None and orderBy is None and limit is None and joins is None and translations is None:
            return self.mtModel.objects  # chaining method initiated
        
        return self.mtModel.objects.fetch(selectors, conditions, orderBy, limit, joins, translations)

    def update(self, dictionary):
        """
            Validates a given dictionary of key: walue pairs. If valid, 
            attempts to save to DB. Else, throws an exception.
        """
        self.saveSubmission('update', dictionary)  # hence forth dictionary => self.submission

        mId = self.mapper.master('abbreviation') + 'id'

        records = self.fullRecord(self.submission[mId])

        if not records:
            raise Exception(f'No valid record found for provided {self.space} ID, in: {self.space}.CRUD.update().')

        if len(records) > 1:
            completeRecord = records[0] # self.pruneLatestRecords(records, mId) @todo: implement pruneLatestRecords()
        else:
            completeRecord = records[0]

        # Loop through each defined Primary Key to see if its table needs an update
        for pk in self.idCols:
            tbl = pk[:self.abrvSize]  # child table abbreviation
            t = crud.generateModelInfo(self.mapper, tbl)

            if pk == mId:
                if crud.isValidId(self.submission, pk):
                    self.updateMasterTable(t['model'], t['table'], t['cols'], completeRecord)
                    continue
            
            # @todo: we could remove the need for child-ids from updates, making front-end dev easier. Not very important.
            if pk not in self.submission:
                self.createChildTable(t['model'], tbl, t['table'], t['cols'])
                continue
                
            if not crud.isValidId(self.submission, pk):
                # create a new record for child table if pk is invalid
                self.createChildTable(t['model'], tbl, t['table'], t['cols'])
                continue

            # determine if an update is necessary and carry out update operations...
            self.updateChildTable(t['model'], tbl, t['table'], t['cols'], completeRecord)

        return { mId: self.submission[mId] } # since .update() operation only returns # of rows affected, not the updated record.

    def delete(self, masterId):
        """
            Validates a given record ID. If valid, attempts to  mark record
            as deleted in DB. Else, throws an exception.
        """
        mtId = self.mapper.master('abbreviation') + 'id'
        if not crud.isValidId({mtId: masterId}, masterId):
            raise Exception(f'{self.space} Record could not be deleted. Invalid id supplied in {self.space}.CRUD.delete()')

        for pk in self.idCols:
            tbl = pk[:self.abrvSize]  # table abbreviation

            if pk == mtId:
                continue  # skip, we delete master table at the end.

            t = crud.generateModelInfo(self.mapper, tbl)

            # run a 'delete' operation for latest child table record. 
            self.deleteChildTable(t['model'], tbl, t['table'], t['cols'], masterId)

        # once all children records have been updated with delete markers
        t = crud.generateModelInfo(self.mapper, self.mapper.master('abbreviation'))
        return self.deleteMasterTable(t['model'], self.mapper.master('foreignKeyName'), t['table'], t['cols'], masterId)


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


