from .querysets.tasks import *
from tasks.models import *
from .background import O2ORecords, RevisionlessChildren, M2OChildren

"""
    Handles all O1O crud operations for Tasks Module of DotzCRM.
    Please read the README.md in this folder before using.
"""
class CRUD(O2ORecords.CRUD):

    def __init__(self):
        self.space = 'tasks'  # holds the name of current module/space
        self.mtModel = Task  # holds the class reference for Master Table's model

        super().__init__()

    def read(self, selectors, conditions = None, orderBy = 't.update_time DESC', limit = '20'):
        """
            See documentation on how to form selectors, conditions, etc.
            @return: None | RawQuerySet
        """
        if not isinstance(selectors, list) or len(selectors) < 1:
            raise Exception(f'Record fetch request for {self.space} failed. Improper selectors, in {self.space}.CRUD.read()')

        if 'all' in selectors:
            selectors = list(self.dbConfigs['keys']['full_record'].keys())

        rawObjs = self.mtModel.objects.fetchTasks(selectors, conditions, orderBy, limit)
        
        if rawObjs:
            return rawObjs

        return None

    def fetchFullRecordForUpdate(self, task_id):
        conditions = {
            #"assignee_id": None,
            "update_time": None,
            "latest": self.module['values']['latest']['latest'],
            "visibility": None,
            "status": None,
            "tid": task_id,
        }

        rawObj = self.read(['all'], conditions)

        if rawObj:
            return rawObj[0]  # we only want one
        return None

class Comments(RevisionlessChildren.CRUD):
    """
        Comments are a RLC table type.
        All CRUD operations for Comments within Task module, are handled by
        this class.
    """
    def __init__(self):
        super.__init__(CRUD)  # satisfy parent class' requirement for MasterCRUDClass

    def read(self, definitions):
        """
            Takes requirements for retrieval of comments. If valid, executes
            relevant Query. See documentation on definitions formulation.
        """
        if not isinstance(definitions, dict) or len(definitions) < 1:
            raise Exception(f'Record fetch request for Comments failed. Improper definitions for query, in {self.space}.CRUD.read()')

        for pk in self.rlcidCols:
            model = globals()[self.dbConfigs['models'][pk]]
            if pk in definitions:
                # specific record being sought:
                rawObjs = model.objects.fetchById(definitions[self.dbConfigs['mtId']], definitions[pk])

            else:
                rawObjs = model.objects.fetchAllByMasterIdRLC(definitions[self.dbConfigs['mtId']])
        
        if rawObjs:
            return rawObjs

        return None

class Assignments(M2OChildren.CRUD):
    """
       Assignments pertain to Many-to-One relations where certain items are
       being assigned to the Tasks' MT. Such as watchers, following an open
       task.
    """

    def __init__(self):
        super.__init__(CRUD)  # satisfy parent class' requirement for MasterCRUDClass

    def read(self, definitions):
        """
            Takes requirements for retrieval of M2O Assignments. If valid,
            executes relevant Query. See documentation on definitions
            formulation.
        """
        if not isinstance(definitions, dict) or len(definitions) < 1:
            raise Exception(f'Record fetch request for Comments failed. Improper definitions for query, in {self.space}.CRUD.read()')

        for pk in self.m2oidCols:
            model = globals()[self.dbConfigs['models'][pk]]
            if pk in definitions:
                # specific record being sought:
                rawObjs = model.objects.fetchById(definitions[self.dbConfigs['mtId']], definitions[pk])

            else:
                rawObjs = model.objects.fetchAllByMasterIdRLC(definitions[self.dbConfigs['mtId']])
        
        if rawObjs:
            return rawObjs

        return None
