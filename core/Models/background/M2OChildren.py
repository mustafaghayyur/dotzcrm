from tasks.models import *
from core.helpers import crud  # , misc
from . import CrudOperations

"""
    Many-to-One CRUD Operations that can be used through out the system.
    
    In a M2O relationship, there are two key columns to watch out for, the
    one ID (often MT ID) that cannot have multiples; and the many ID (CT) which 
    can show up numerous times in the result sets.
    
    By making sure many-correct FKs are handled correctly in reference to
    a single MT ID, we can keep the M2O relationship meaningful.
"""
class CRUD(CrudOperations.Background):

    def __init__(self):
        super().__init__()

    def create(self, dictionary):
        """
            Creation of a single record per M2O CT.
        """
        self.saveSubmission('create', dictionary)  # hence forth dictionary => self.submission
        rdbms = {self.space: self.dbConfigs, 'tables': self.tables}

        tbl = self.pk[0]  # table abbreviation
        t = crud.generateModelInfo(rdbms, self.space, tbl)
        model = globals()[t['model']]  # retrieve Model class with global scope
        
        m2oKeys = self.dbConfigs['keys']['m2o'][t['table']]  # fetch m2o keys for table
        skip = False

        if not crud.isValidId(self.submission, m2oKeys['oneCol']):
            skip = True

        if not crud.isValidId(self.submission, m2oKeys['manyCol']):
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
        t = crud.generateModelInfo(rdbms, self.space, tbl)
        model = globals()[t['model']]  # retrieve Model class with global scope
        m2oKeys = self.dbConfigs['keys']['m2o'][t['table']]  # fetch m2o keys for table

        if self.pk in definitions:
            if crud.isValidId(definitions, self.pk):
                # specific record being sought:
                rawObjs = model.objects.fetchById(definitions[self.pk])
            
        if m2oKeys['oneCol'] in definitions and m2oKeys['manyCol'] not in definitions:        
            if crud.isValidId(definitions, m2oKeys['oneCol']):
                if definitions['latest']:
                    rawObjs = model.objects.fetchAllCurrentByOneId(definitions[m2oKeys['oneCol']])
        
        if m2oKeys['manyCol'] in definitions and m2oKeys['oneCol'] not in definitions:
            if crud.isValidId(definitions, m2oKeys['manyCol']):
                if definitions['latest']:
                    rawObjs = model.objects.fetchAllCurrentByManyId(definitions[m2oKeys['manyCol']])
        
        if m2oKeys['oneCol'] in definitions and m2oKeys['manyCol'] in definitions:        
            if crud.isValidId(definitions, m2oKeys['oneCol']) and crud.isValidId(definitions, m2oKeys['manyCol']):
                rawObjs = model.objects.fetchAllRevisions(definitions[m2oKeys['oneCol']], definitions[m2oKeys['manyCol']])

        if rawObjs:
            return rawObjs

        return None

    def update(self, dictionary):
        """
            Update of a single record per M2O CT.
        """
        self.saveSubmission('update', dictionary)  # hence forth dictionary => self.submission

        if not crud.isValidId(self.submission, self.pk):
            raise Exception(f'No valid M2O ID provided, in: {self.space}.CRUD.update().')

        rdbms = {self.space: self.dbConfigs, 'tables': self.tables}
        
        tbl = self.pk[0]  # child table abbreviation
        t = crud.generateModelInfo(rdbms, self.space, tbl)
        model = globals()[t['model']]  # retrieve Model class with global scope
        m2oKeys = self.dbConfigs['keys']['m2o'][t['table']]  # fetch m2o keys for table

        originalM2O = self.read({self.pk: self.submission[self.pk]})
        self.log(originalM2O, 'JUST CONFIRMING if originalM2O record is being fetched correctly in updateM2O()')

        if not originalM2O:
            raise Exception(f'No valid M2O record found for provided ID, in: {self.space}.CRUD.update().')
            
        # determine if an update is necessary and carry out update operations...
        self.updateChildTable(model, tbl, t['table'], t['cols'], originalM2O)

    def deleteById(self, m2oId):
        """
            Attempts to delete a single child record that of M2O relationship
            type, by its Unique ID.
        """
        if not isinstance(m2oId, int) or m2oId < 1:
            raise Exception(f'M2O Record could not be deleted. Invalid id supplied in {self.space}.CRUD.deleteM2O()')

        rdbms = {self.space: self.dbConfigs, 'tables': self.tables}


        tbl = self.pk[0]  # table abbreviation
        t = crud.generateModelInfo(rdbms, self.space, tbl)
        model = globals()[t['model']]  # retrieve Model class with global scope

        self.__deleteChildTableById(model, tbl, t['table'], t['cols'], m2oId)

    def deleteAllForOneCol(self, oneColId):
        """
            Attempts to delete all M2O-type children records for a MT ID
            provided.
        """
        if not isinstance(oneColId, int) or oneColId < 1:
            raise Exception(f'M2O Records could not be deleted. Invalid single column ID supplied in {self.space}.CRUD.deleteM2O()')

        rdbms = {self.space: self.dbConfigs, 'tables': self.tables}

        tbl = self.pk[0]  # table abbreviation
        t = crud.generateModelInfo(rdbms, self.space, tbl)
        model = globals()[t['model']]  # retrieve Model class with global scope

        self.__deleteAllM2O(model, tbl, t['table'], t['cols'], oneColId)

    def __deleteAllM2O(self, modelClass, tbl, tableName, columnsList, oneColId):
        """
            Helper function for deleteAllForOneCol()
            For M2O type nodes only
        """
        self.log(None, f'ENTERING deleteAllForOneCol for CT [{tbl}]')
        m2oKeys = self.dbConfigs['keys']['m2o'][t['table']]  # fetch m2o keys for table
        
        fieldsF = {}  # fields to find records with
        fieldsF[m2oKeys['oneCol']] = oneColId
        
        fieldsU = {}  # fields to update in found records
        fieldsU['delete_time'] = timezone.now()
        fieldsU['latest'] = self.module['values']['latest']['archive']

        self.log({'find': fieldsF, 'update': fieldsU}, f'Fields for deletion find | Fields for deletion update [{tbl}]')
        return modelClass.objects.filter(**fieldsF).update(**fieldsU)


    def __deleteChildTableById(self, modelClass, tbl, tableName, columnsList, childId):
        """
            Helper function for deleteById()
            For M2O type nodes only
        """
        self.log(None, f'ENTERING deleteById for CT [{tbl}]')
        
        fieldsF = {}  # fields to find records with
        fieldsF['id'] = childId
        
        fieldsU = {}  # fields to update in found records
        fieldsU['delete_time'] = timezone.now()
        fieldsU['latest'] = self.module['values']['latest']['archive']

        self.log({'find': fieldsF, 'update': fieldsU}, f'Fields for deletion find | Fields for deletion update [{tbl}]')
        return modelClass.objects.filter(**fieldsF).update(**fieldsU)
