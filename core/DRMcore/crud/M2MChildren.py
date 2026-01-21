from django.utils import timezone
from . import Background
from core.helpers import crud, misc

"""
    Many-to-Many CRUD Operations that can be used through out the system.
"""
class CRUD(Background.CrudOperations):

    firstCol = None  # defined in inheritor
    secondCol = None  # defined in inheritor
    
    def __init__(self):
        super().__init__()

    def create(self, dictionary):
        """
            Creation of a single record per M2M CT.
        """
        self.saveSubmission('create', dictionary)  # hence forth dictionary => self.submission

        t = crud.generateModelInfo(self.mapper, self.tbl)

        if not crud.isValidId(self.submission, self.firstCol):
            return None
        if not crud.isValidId(self.submission, self.secondCol):
            return None
        
        # first, we attempt o update any existing records matching first & second M2M cols...
        self.updateChildTable(t['model'], self.tbl, t['table'], t['cols'])

        # next, we will create a new record for first andsecond columns.
        return self.createChildTable(t['model'], self.tbl, t['table'], t['cols'])
        
    def read(self, definitions):
        """
            See documentation on definitions formulation.
        """
        if not isinstance(definitions, dict) or len(definitions) < 1:
            raise Exception(f'Record fetch request for Comments failed. Improper definitions for query, in {self.space}.CRUD.read()')

        if 'latest' not in definitions:
            definitions['latest'] = self.mapper.values.latest('latest')

        t = crud.generateModelInfo(self.mapper, self.tbl)
        rawObjs = None

        if self.pk in definitions:
            if crud.isValidId(definitions, self.pk):
                # specific record being sought:
                rawObjs = t['model'].objects.fetchById(definitions[self.pk])
            
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
        self.saveSubmission('create', dictionary)  # hence forth dictionary => self.submission

        if not crud.isValidId(self.submission, self.firstCol) or not crud.isValidId(self.submission, self.secondCol):
            raise Exception(f'M2M Record could not be deleted. Invalid IDs supplied in {self.space}.CRUD.deleteM2M()')

        t = crud.generateModelInfo(self.mapper, self.tbl)

        return self.updateChildTable(t['model'], self.tbl, t['table'], t['cols'])

    def deleteAllForFirstCol(self, firstColId):
        """
            Attempts to delete all M2M-type children records for a firstCol ID
            provided.
        """
        if not isinstance(firstColId, int) or firstColId < 1:
            raise Exception(f'M2M Records could not be deleted. Invalid single column ID supplied in {self.space}.CRUD.deleteM2M()')

        t = crud.generateModelInfo(self.mapper, self.tbl)

        return self.deleteAllM2M(t['model'], self.tbl, t['table'], t['cols'], firstColId)

    def updateChildTable(self, modelClass, tbl, tableName, columnsList):
        """
            updateChildTable() will be overwritten in M2MChildren for special handling.
            We will simply archive any existing records matching firstCal & secondCol
        """
        self.log(None, f'ENTERING update for childtable [{tbl}]')

        fieldsF = {}
        fieldsF[self.firstCol] = self.submission[self.firstCol]
        fieldsF[self.secondCol] = self.submission[self.secondCol]

        fieldsU = {}
        fieldsU['delete_time'] = timezone.now()
        fieldsU['latest'] = self.mapper.values.latest('archive')        

        modelClass.objects.filter(**fieldsF).update(**fieldsU)
        self.log({'fields': fieldsU}, f'Attempted update For: [{tbl}]')

    def deleteAllM2M(self, modelClass, tbl, tableName, columnsList, firstColId):
        """
            Helper function for deleteAllForFirstCol(). M2M nodes only.
        """
        self.log(None, f'ENTERING deleteAllForFirstCol for CT [{self.tbl}]')
        
        fieldsF = {}  # fields to find records with
        fieldsF[self.firstCol] = firstColId
        
        fieldsU = {}  # fields to update in found records
        fieldsU['delete_time'] = timezone.now()
        fieldsU['latest'] = self.mapper.values.latest('archive')

        self.log({'find': fieldsF, 'update': fieldsU}, f'Fields for deletion find | Fields for deletion update [{self.tbl}]')
        return modelClass.objects.filter(**fieldsF).update(**fieldsU)
