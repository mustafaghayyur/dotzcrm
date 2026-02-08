from core.DRMcore.crud import O2ORecords, RevisionlessChildren, M2MChildren

from tasks.models import *
from .mappers import TasksMapper

class Tasks(O2ORecords.CRUD):
    """
        Handles all O2O crud operations for Tasks Module of DotzCRM.
        Please read the README.md in this folder before using.
    """
    
    def __init__(self):
        self.space = 'tasks'  # holds the name of current module/space
        self.mtModel = Task  # holds the class reference for Master Table's model
        self.mapper = TasksMapper()
        
        super().__init__()

    def fullRecord(self, task_id):
        """
            fetch full O2O record with all CT records marked 'latest'
        """
        conditions = {
            "tata_update_time": None,
            "latest": self.mapper.values.latest('latest'),
            "visibility": None,
            "status": None,
            "tata_id": task_id,
        }

        recordKeysDict = self.mapper.generateO2OFields()  # returns a dictionary
        selectors = list(recordKeysDict.keys())

        rawObj = self.read(selectors, conditions)

        if rawObj:
            return rawObj  # returns all records found.
        return None

class Comments(RevisionlessChildren.CRUD):
    """
        Comments are a RLC table type.
        All CRUD operations for Comments within Task module, are handled by
        this class.
    """

    def __init__(self):
        self.space = 'tasks'  # holds the name of current module/space
        self.mtModel = Task  # holds the class reference for Master Table's model
        self.tbl = 'taco'
        self.pk = 'taco_id'
        self.mapper = TasksMapper()
        
        self.setMasterCrudClass(Tasks)

    def read(self, definitions):
        """
            Takes requirements for retrieval of comments. If valid, executes
            relevant Query. See documentation on definitions formulation.
        """
        if not isinstance(definitions, dict) or len(definitions) < 1:
            raise Exception(f'Record fetch request for Comments failed. Improper definitions for query, in {self.space}.CRUD.read()')

        model = globals()[self.mapper.models(self.tbl)]

        if self.pk in definitions:
            rawObjs = model.objects.fetchById(definitions[self.pk])  # specific record being sought

        else:
            rawObjs = model.objects.fetchAllByMasterIdRLC(definitions[self.mapper.master('foreignKeyName')])
        
        if rawObjs:
            return rawObjs

        return None

class Watchers(M2MChildren.CRUD):
    """
       This is a Many-to-Many relations table, where many 'watchers' are
       being assigned to many Tasks' record.
    """

    def __init__(self):
        self.pk = 'tawa_id'  # set table_abbrv for use in queries.
        self.space = 'tasks'  # holds the name of current module/space
        self.tbl = 'tawa'
        
        self.mapper = TasksMapper()

        cols = self.mapper.m2mFields(self.tbl)
        self.firstCol = cols['firstCol']
        self.secondCol = cols['secondCol']
        super().__init__()
        
