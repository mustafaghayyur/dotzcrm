from core.DRMcore.querysets import master, child
from .tasks_mapper import TasksMapper
from .workspaces_mapper import WorkSpacesMapper


class TaskQuerySet(master.MTQuerySet):
    """
        TaskQuerySet allows for highly versatile Select queries to DB.
        For O2O, M2M and RLC data models (i.e. records).
    """
    def startUpCode(self):
        self.state.set('app', 'tasks')
        self.mapper = TasksMapper()


class DetailQuerySet(child.CTQuerySet):
    def startUpCode(self):
        self.state.set('app', 'tasks')
        self.mapper = TasksMapper()


class DeadlineQuerySet(child.CTQuerySet):
    def startUpCode(self):
        self.state.set('app', 'tasks')
        self.mapper = TasksMapper()


class StatusQuerySet(child.CTQuerySet):
    def startUpCode(self):
        self.state.set('app', 'tasks')
        self.mapper = TasksMapper()


class VisibilityQuerySet(child.CTQuerySet):
    def startUpCode(self):
        self.state.set('app', 'tasks')
        self.mapper = TasksMapper()


class AssignmentQuerySet(child.CTQuerySet):
    def startUpCode(self):
        self.state.set('app', 'tasks')
        self.mapper = TasksMapper()


class WatcherQuerySet(child.M2MQuerySet):
    def startUpCode(self):
        self.state.set('app', 'tasks')
        self.mapper = TasksMapper()

class CommentQuerySet(child.RLCQuerySet):
    def startUpCode(self):
        self.state.set('app', 'tasks')
        self.mapper = TasksMapper()


#### WorkSpaces QuerySets #####

class WorkSpaceQuerySet(master.MTQuerySet):
    """
        WorkSpaceQuerySet allows for highly versatile Select queries to DB.
        For O2O, M2M and RLC data models (i.e. records).
    """
    def startUpCode(self):
        self.state.set('app', 'tasks')
        self.mapper = WorkSpacesMapper()


class WorkSpaceCTQuerySet(child.CTQuerySet):
    """
        Generic for all O2O CT models
    """
    def startUpCode(self):
        self.state.set('app', 'tasks')
        self.mapper = WorkSpacesMapper()

class WorkSpaceM2MQuerySet(child.M2MQuerySet):
    """
        Generic for all M2M CT models
    """
    def startUpCode(self):
        self.state.set('app', 'tasks')
        self.mapper = WorkSpacesMapper()

class WorkSpaceRLCQuerySet(child.RLCQuerySet):
    """
        Generic for all RLC CT models
    """
    def startUpCode(self):
        self.state.set('app', 'tasks')
        self.mapper = WorkSpacesMapper()

