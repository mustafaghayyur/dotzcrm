from django.utils import timezone
from . import Background
from core.helpers import crud, misc

from .create import Create
from .delete import Delete


class CRUD(Background.Operations):
    """
        Many-to-Many CRUD Operations that can be used through out the system.
    """

    def startUpCode(self):
        self.state.set('firstCol', None)
        self.state.set('secondCol', None)
        self.state.set('tbl', None)
        self.state.set('pk', None)
        

    def create(self, dictionary):
        """
            Creation of a single record per M2M CT.
        """
        self.saveSubmission('create', dictionary)  # save to state

        t = crud.generateModelInfo(self.mapper, self.state.get('tbl'))

        if not crud.isValidId(self.submission, self.firstCol):
            return None
        if not crud.isValidId(self.submission, self.secondCol):
            return None
        
        # first, we attempt o update any existing records matching first & second M2M cols...
        Delete.allChildTableM2ms(self.state, self.mapper, t['model'], self.state.get('tbl'), t['table'], t['cols'])

        # next, we will create a new record for first and second columns.
        return Create.childTable(self.state, self.mapper, t['model'], self.state.get('tbl'), t['table'], t['cols'])
        
    def read(self, definitions):
        """
            See documentation on definitions formulation.
        """
        if not isinstance(definitions, dict) or len(definitions) < 1:
            raise Exception(f'Error 2032: Fetch request for {self.firstCol} and {self.secondCol} failed. Improper definitions for query, in {self.state.get('app')}.CRUD.read()')

        if 'latest' not in definitions:
            definitions['latest'] = self.mapper.values.latest('latest')

        t = crud.generateModelInfo(self.mapper, self.state.get('tbl'))
        rawObjs = None

        if self.state.get('pk') in definitions:
            if crud.isValidId(definitions, self.state.get('pk')):
                # specific record being sought:
                rawObjs = t['model'].objects.fetchById(definitions[self.state.get('pk')])
            
        if self.firstCol in definitions and self.secondCol not in definitions:        
            if crud.isValidId(definitions, self.firstCol):
                if definitions['latest']:
                    rawObjs = t['model'].objects.fetchAllCurrentByFirstId(definitions[self.firstCol])
        
        if self.secondCol in definitions and self.firstCol not in definitions:
            if crud.isValidId(definitions, self.secondCol):
                if definitions['latest']:
                    rawObjs = t['model'].objects.fetchAllCurrentBySecondId(definitions[self.secondCol])
        
        if self.firstCol in definitions and self.secondCol in definitions:        
            if crud.isValidId(definitions, self.firstCol) and crud.isValidId(definitions, self.secondCol):
                rawObjs = t['model'].objects.fetchLatest(definitions[self.firstCol], definitions[self.secondCol], definitions['latest'])

        if rawObjs:
            return rawObjs

        return None

    def update(self, dictionary):
        """
            Direct update calls are not supported in M2M records.
        """
        pass

    def delete(self, dictionary):
        """
            Attempts to delete all records matching firstCol and SecondCol. 
        """
        self.saveSubmission('create', dictionary)  # save to state

        if not crud.isValidId(self.submission, self.firstCol) or not crud.isValidId(self.submission, self.secondCol):
            raise Exception(f'Error 2031: M2M Record could not be deleted. Invalid IDs supplied in {self.state.get('app')}.CRUD.deleteM2M()')

        t = crud.generateModelInfo(self.mapper, self.state.get('tbl'))

        return Delete.allChildTableM2ms(self.state, self.mapper, t['model'], self.state.get('tbl'), t['table'], t['cols'])

    def deleteByFirstCol(self, firstColId):
        """
            Deletes all M2M-type children records for provided firstCol ID.
        """
        if not isinstance(firstColId, int) or firstColId < 1:
            raise Exception(f'Error 2030: M2M Records could not be deleted. Invalid single column ID supplied in {self.state.get('app')}.CRUD.deleteM2M()')

        t = crud.generateModelInfo(self.mapper, self.state.get('tbl'))

        return Delete.allChildTableFirstCol(self.state, self.mapper, t['model'], self.state.get('tbl'), t['table'], t['cols'], firstColId)
