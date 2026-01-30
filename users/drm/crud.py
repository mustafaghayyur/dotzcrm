from core.DRMcore.crud import O2ORecords, RevisionlessChildren, M2MChildren

from users.models import *
from .mappers import UsersMapper
from .mapper_values import ValuesMapper

class Users(O2ORecords.CRUD):
    """
        Handles all O2O crud operations for Tasks Module of DotzCRM.
        Please read the README.md in this folder before using.
    """
    
    def __init__(self):
        self.space = 'tasks'  # holds the name of current module/space
        self.mtModel = User  # holds the class reference for Master Table's model

        self.mapper = UsersMapper()
        self.mapper.setValuesMapper(ValuesMapper)
        
        super().__init__()

    def fullRecord(self, task_id):
        """
            fetch full records with all CT records marked 'latest'
        """
        conditions = {
            # "assignee_id": None,
            "update_time": None,
            "latest": self.mapper.values.latest('latest'),
            "visibility": None,
            "status": None,
            "tid": task_id,
        }

        rawObj = self.read(['all'], conditions)

        if rawObj:
            return rawObj  # returns all records found.
        return None

class Departments(M2MChildren.CRUD):
    """
    """

    def __init__(self):
        self.pk = 'wid'  # set table_abbrv for use in queries.
        self.space = 'tasks'  # holds the name of current module/space
        self.tbl = 'w'

        self.mapper = UsersMapper()

        cols = self.mapper.m2mFields(self.pk[0])
        self.firstCol = cols['firstCol']
        self.secondCol = cols['secondCol']
        super().__init__()


class Hierarchy(M2MChildren.CRUD):
    """
    """

    def __init__(self):
        self.pk = 'wid'  # set table_abbrv for use in queries.
        self.space = 'tasks'  # holds the name of current module/space
        self.tbl = 'w'
        
        self.mapper = UsersMapper()

        cols = self.mapper.m2mFields(self.pk[0])
        self.firstCol = cols['firstCol']
        self.secondCol = cols['secondCol']
        super().__init__()
        
