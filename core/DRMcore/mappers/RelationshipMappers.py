from .base import BaseOperations
from .schema.main import schema

class RelationshipMappers(BaseOperations):
    """
        Along with BaseOperations(), RelationshipMappers() defines meaningful methods to
        access vital schema related info for all your database crud operations.

        References to _*() methods in the code point to data-definition functions defined
        in child classes on app-level.
    """
    tableList = None

    def master(self, key = 'all'):
        info = self._master()
        return self.returnValue(info, key)

    def commonFields(self):
        return self._commonFields()

    def tablesForRelationType(self, relationType = 'o2o'):
        return self._tablesForRelationType(relationType)

    def ignoreOnRetrieval(self):
        return self._ignoreOnRetrieval()

    def ignoreOnUpdates(self, key = 'all'):
        info = self._ignoreOnUpdates()
        if key not in schema:
            key = self.tableAbbreviation(key)  # ignoreOnUpdates() changed from ful-name-keys to abbreviations name
        return self.returnValue(info, key)

    def m2mFields(self, tbl = 'all'):
        relationships = self._m2mFields()
        return self.returnValue(relationships, tbl)

