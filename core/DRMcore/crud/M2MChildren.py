from django.utils import timezone
from . import Background
from core.helpers import crud

"""
    Many-to-Many CRUD Operations that can be used through out the system.
    
    In a M2M relationship, there are two key columns to watch out for: 
     - FirstId: refers to the first FK of another table we are tracking
     - SecondId: refers to the second FK of yet, another table we wish
       the firstId to be associated with.

    Note: first and second can carry significance for each specific 'Model'
    that inherits this class. Should be appropriately assigned in mapper.
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

        tbl = self.pk[0]  # table abbreviation
        t = crud.generateModelInfo(self.mapper, tbl)
        model = globals()[t['model']]  # retrieve Model class with global scope
        
        skip = False

        if not crud.isValidId(self.submission, self.firstCol):
            skip = True

        if not crud.isValidId(self.submission, self.secondCol):
            skip = True

        if skip:
            return None

        self.createChildTable(model, tbl, t['table'], t['cols'])

    def read(self, definitions):
        """
            See documentation on definitions formulation.
        """
        if not isinstance(definitions, dict) or len(definitions) < 1:
            raise Exception(f'Record fetch request for Comments failed. Improper definitions for query, in {self.space}.CRUD.read()')

        if 'latest' not in definitions:
            definitions['latest'] = True

        tbl = self.pk[0]  # table abbreviation
        t = crud.generateModelInfo(self.mapper, tbl)
        model = globals()[t['model']]  # retrieve Model class with global scope

        if self.pk in definitions:
            if crud.isValidId(definitions, self.pk):
                # specific record being sought:
                rawObjs = model.objects.fetchById(definitions[self.pk])
            
        if self.firstCol in definitions and self.secondCol not in definitions:        
            if crud.isValidId(definitions, self.firstCol):
                if definitions['latest']:
                    rawObjs = model.objects.fetchAllCurrentByFirstId(definitions[self.firstCol])
        
        if self.secondCol in definitions and self.firstCol not in definitions:
            if crud.isValidId(definitions, self.secondCol):
                if definitions['latest']:
                    rawObjs = model.objects.fetchAllCurrentBySecondId(definitions[self.secondCol])
        
        if self.firstCol in definitions and self.secondCol in definitions:        
            if crud.isValidId(definitions, self.firstCol) and crud.isValidId(definitions, self.secondCol):
                rawObjs = model.objects.fetchAllRevisions(definitions[self.firstCol], definitions[self.secondCol])

        if rawObjs:
            return rawObjs

        return None

    def update(self, dictionary):
        """
            Update of a single record per M2M CT.
        """
        self.saveSubmission('update', dictionary)  # hence forth dictionary => self.submission

        if not crud.isValidId(self.submission, self.pk):
            raise Exception(f'No valid M2M ID provided, in: {self.space}.CRUD.update().')
        
        tbl = self.pk[0]  # child table abbreviation
        t = crud.generateModelInfo(self.mapper, tbl)
        model = globals()[t['model']]  # retrieve Model class with global scope

        originalM2M = self.read({self.pk: self.submission[self.pk]})
        self.log(originalM2M, 'JUST CONFIRMING if originalM2M record is being fetched correctly in updateM2M()')

        if not originalM2M:
            raise Exception(f'No valid M2M record found for provided ID, in: {self.space}.CRUD.update().')
            
        # determine if an update is necessary and carry out update operations...
        self.updateChildTable(model, tbl, t['table'], t['cols'], originalM2M)

    def deleteById(self, m2mId):
        """
            Attempts to delete a single child record that of M2M relationship
            type, by its Unique ID.
        """
        if not isinstance(m2mId, int) or m2mId < 1:
            raise Exception(f'M2M Record could not be deleted. Invalid id supplied in {self.space}.CRUD.deleteM2M()')

        tbl = self.pk[0]  # table abbreviation
        t = crud.generateModelInfo(self.mapper, tbl)
        model = globals()[t['model']]  # retrieve Model class with global scope

        self.__deleteChildTableById(model, tbl, t['table'], t['cols'], m2mId)

    def deleteAllForFirstCol(self, firstColId):
        """
            Attempts to delete all M2M-type children records for a MT ID
            provided.
        """
        if not isinstance(firstColId, int) or firstColId < 1:
            raise Exception(f'M2M Records could not be deleted. Invalid single column ID supplied in {self.space}.CRUD.deleteM2M()')

        tbl = self.pk[0]  # table abbreviation
        t = crud.generateModelInfo(self.mapper, tbl)
        model = globals()[t['model']]  # retrieve Model class with global scope

        self.__deleteAllM2M(model, tbl, t['table'], t['cols'], firstColId)

    def __deleteAllM2M(self, modelClass, tbl, tableName, columnsList, firstColId):
        """
            Helper function for deleteAllForFirstCol()
            For M2M type nodes only
        """
        self.log(None, f'ENTERING deleteAllForFirstCol for CT [{tbl}]')
        
        fieldsF = {}  # fields to find records with
        fieldsF[self.firstCol] = firstColId
        
        fieldsU = {}  # fields to update in found records
        fieldsU['delete_time'] = timezone.now()
        fieldsU['latest'] = self.mapper.values.latest('archive')

        self.log({'find': fieldsF, 'update': fieldsU}, f'Fields for deletion find | Fields for deletion update [{tbl}]')
        return modelClass.objects.filter(**fieldsF).update(**fieldsU)


    def __deleteChildTableById(self, modelClass, tbl, tableName, columnsList, childId):
        """
            Helper function for deleteById()
            For M2M type nodes only
        """
        self.log(None, f'ENTERING deleteById for CT [{tbl}]')
        
        fieldsF = {}  # fields to find records with
        fieldsF['id'] = childId
        
        fieldsU = {}  # fields to update in found records
        fieldsU['delete_time'] = timezone.now()
        fieldsU['latest'] = self.mapper.values.latest('archive')

        self.log({'find': fieldsF, 'update': fieldsU}, f'Fields for deletion find | Fields for deletion update [{tbl}]')
        return modelClass.objects.filter(**fieldsF).update(**fieldsU)
