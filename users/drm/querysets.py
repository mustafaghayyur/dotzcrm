from core.DRMcore.querysets import master, child
from .users_mapper import UsersMapper
from .dept_mapper import DepartmentsMapper


class UserQuerySet(master.MTQuerySet):
    """
        UserQuerySet allows for highly versatile Select queries to DB.
        For O2O, M2M and RLC data models (i.e. records).
    """
    def startUpCode(self):
        self.state.set('app', 'users')
        self.mapper = UsersMapper()


class UserCTQuerySet(child.CTQuerySet):
    """
        Generic for all O2O CT models
    """
    def startUpCode(self):
        self.state.set('app', 'users')
        self.mapper = UsersMapper()

class UserM2MQuerySet(child.M2MQuerySet):
    """
        Generic for all M2M CT models
    """
    def startUpCode(self):
        self.state.set('app', 'users')
        self.mapper = UsersMapper()

class UserRLCQuerySet(child.RLCQuerySet):
    """
        Generic for all RLC CT models
    """
    def startUpCode(self):
        self.state.set('app', 'users')
        self.mapper = UsersMapper()




#### Departments QuerySets #####

class DepartmentQuerySet(master.MTQuerySet):
    """
        DepartmentQuerySet allows for highly versatile Select queries to DB.
        For O2O, M2M and RLC data models (i.e. records).
    """
    def startUpCode(self):
        self.state.set('app', 'users')
        self.mapper = DepartmentsMapper()


class DepartmentCTQuerySet(child.CTQuerySet):
    """
        Generic for all O2O CT models
    """
    def startUpCode(self):
        self.state.set('app', 'users')
        self.mapper = DepartmentsMapper()

class DepartmentM2MQuerySet(child.M2MQuerySet):
    """
        Generic for all M2M CT models
    """
    def startUpCode(self):
        self.state.set('app', 'users')
        self.mapper = DepartmentsMapper()

class DepartmentRLCQuerySet(child.RLCQuerySet):
    """
        Generic for all RLC CT models
    """
    def startUpCode(self):
        self.state.set('app', 'users')
        self.mapper = DepartmentsMapper()

        