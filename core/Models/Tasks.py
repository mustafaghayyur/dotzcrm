from tasks.models import *
from .mappers.tasks import TasksMapper, ValuesManager
from .querysets.Tasks import *
from .background import O2ORecords, RevisionlessChildren, M2MChildren

class CRUD(O2ORecords.CRUD):
    """
        Handles all O2O crud operations for Tasks Module of DotzCRM.
        Please read the README.md in this folder before using.
    """
    
    def __init__(self):
        self.space = 'tasks'  # holds the name of current module/space
        self.mtModel = Task  # holds the class reference for Master Table's model

        self.mapper = TasksMapper()
        self.valuesMapper = ValuesManager()
        super().__init__()

    def read(self, selectors, conditions = None, orderBy = 't.update_time DESC', limit = '20'):
        """
            See documentation on how to form selectors, conditions, etc.
            @return: None | RawQuerySet
        """
        if not isinstance(selectors, list) or len(selectors) < 1:
            raise Exception(f'Record fetch request for {self.space} failed. Improper selectors, in {self.space}.CRUD.read()')

        if 'all' in selectors:
            recordKeys = self.mapper.generateO2OFields()  # returns a dictionary
            selectors = list(recordKeys.keys())

        rawObjs = self.mtModel.objects.fetch(selectors, conditions, orderBy, limit)
        
        if rawObjs:
            return rawObjs

        return None

    def fetchFullRecordForUpdate(self, task_id):
        """
            fetch full records with all CT records marked 'latest'
        """
        conditions = {
            # "assignee_id": None,
            "update_time": None,
            "latest": self.valuesMapper.latest('latest'),
            "visibility": None,
            "status": None,
            "tid": task_id,
        }

        rawObj = self.read(['all'], conditions)

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

        self.mapper = TasksMapper()
        self.valuesMapper = ValuesManager()
        super.__init__(CRUD)  # satisfy parent class' requirement for MasterCRUDClass

    def read(self, definitions):
        """
            Takes requirements for retrieval of comments. If valid, executes
            relevant Query. See documentation on definitions formulation.
        """
        if not isinstance(definitions, dict) or len(definitions) < 1:
            raise Exception(f'Record fetch request for Comments failed. Improper definitions for query, in {self.space}.CRUD.read()')

        for pk in self.rlcIdCols:
            model = globals()[self.mapper.models(pk)]
            if pk in definitions:
                # specific record being sought:
                rawObjs = model.objects.fetchById(definitions[pk])

            else:
                rawObjs = model.objects.fetchAllByMasterIdRLC(definitions[self.mapper.master('foreignKeyName')])
        
        if rawObjs:
            return rawObjs

        return None

class Watchers(M2MChildren.CRUD):
    """
       This is a Many-to-One relations table, where many 'watchers' are
       being assigned to a single Tasks' MT record.
    """

    def __init__(self):
        self.pk = 'wid'  # set table_abbrv for use in queries.
        self.space = 'tasks'  # holds the name of current module/space

        self.mapper = TasksMapper()
        self.valuesMapper = ValuesManager()

        cols = self.mapper.m2mFields(self.pk[0])
        self.firstCol = cols['firstCol']
        self.secondCol = cols['secondCol']
        super.__init__()
        
