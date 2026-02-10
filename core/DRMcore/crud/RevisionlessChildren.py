from django.utils import timezone
from . import Background
from core.helpers import crud, misc

from .create import Create
from .update import Update
from .delete import Delete


class CRUD(Background.Operations):
    """
        Handles all crud operations for Revision-less Children (RLC) tables.
    """
    def startUpCode(self):
        self.state.set('tbl', None)
        self.state.set('pk', None)

    def create(self, dictionary):
        """
            Creates single RLC CT record.
            Validates a given dictionary of key: value pairs. If valid, 
            attempts to save to DB. Else, throws an exception.
        """
        self.saveSubmission('create', dictionary)  # save to state
        mtId = self.mapper.master('abbreviation') + '_id'
        masterId = self.mapper.master('foreignKeyName')

        masterRecord = self.masterCrudObj.read([mtId], {mtId: self.submission[masterId]})

        if not masterRecord:
            raise Exception(f'Error 2064: Master Record could not be found. RLC cannot be created in {self.state.get('app')}.CRUD.create()')

        t = crud.generateModelInfo(self.mapper, self.state.get('tbl'))

        return Create.childTable(self.state, self.mapper, t['model'], self.state.get('tbl'), t['table'], t['cols'], True)
        
    def read(self):
        pass  # defined in individual Module's class extensions.

    def update(self, dictionary):
        """
            Updates single RLC CT record.
            Validates a given dictionary of key: value pairs. If valid, 
            attempts to save to DB. Else, throws an exception.
        """
        self.saveSubmission('update', dictionary)  # save to state

        mtId = self.mapper.master('abbreviation') + '_id'
        mtForeignKey = self.mapper.master('foreignKeyName')

        # masterRecords gets the parent record id, to which this RLC belongs
        masterRecord = self.masterCrudObj.read([mtId], {mtId: self.submission[mtId]})

        if not masterRecord:
            raise Exception(f'Error 2063: No valid record found for provided {self.state.get('app')} ID for RLC update, in: {self.state.get('app')}.CRUD.update().')

        pk = self.state.get('pk')
        originalRLC = self.read({pk: self.submission[pk], mtForeignKey: self.submission[mtForeignKey]})

        if not originalRLC:
            raise Exception(f'Error 2062: No valid RLC record found for provided ID, in: {self.state.get('app')}.CRUD.update().')
        
        t = crud.generateModelInfo(self.mapper, self.state.get('tbl'))
            
        # determine if an update is necessary and carry out update operations...
        return Update.childTable(self.state, self.mapper, t['model'], self.state.get('tbl'), t['table'], t['cols'], originalRLC, True)

    def delete(self, rlcId):
        """
            Delete specific RLC child record by its ID.
        """
        if not crud.isValidId({'id': rlcId}, 'id'):
            raise Exception(f'Error 2061: RLC Record could not be deleted. Invalid id supplied in {self.state.get('app')}.CRUD.delete()')

        t = crud.generateModelInfo(self.mapper, self.state.get('tbl'))

        return Delete.childTableById(self.state, self.mapper, t['model'], self.state.get('tbl'), t['table'], t['cols'], rlcId)

    def deleteAll(self, masterId):
        """
            Delete all child RLC records for master-table record Id.
        """
        if not crud.isValidId({'id': masterId}, 'id'):
            raise Exception(f'Error 2060: RLC Records could not be deleted. Invalid Master-ID supplied in {self.state.get('app')}.CRUD.delete()')

        t = crud.generateModelInfo(self.mapper, self.state.get('tbl'))

        return Delete.childTable(self.state, self.mapper, t['model'], self.state.get('tbl'), t['table'], t['cols'], masterId, True)

