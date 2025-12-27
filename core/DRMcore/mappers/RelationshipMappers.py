from .RMWrappers import Wrappers
from core.helpers import misc

class RelationshipMappers(Wrappers):
    """
        This class and its inheritors will help map tables to data in 
        meaningful ways.

        The Mapper is Singleton. Thus, only data that relates to Schema should
        be stored in properties, so it can be shared across Query operations.
    """
    values = None  # holds the ValuesMapper instance

    def __init__(self, VMClassInstance, mainTable = None):
        self.values = self.setValuesMapper(VMClassInstance)
        self.mainTable = mainTable  # @todo remove?

    def isCommonField(self, key, prefix = False):
        """
            Determine whether field is common among children tables.
        """
        k = key[1:] if prefix else key  # grab correct key to compare

        if k in self.commonFields():
            return True
        return False

    def generateO2OFields(self):
        """
            Generates a completed dict of fields with tbl-abbrv (where necessary).
            This dictionary is used to fetch full records of current module.
            
            Many-to-Many & Many-to-One records like tasks.watchers and 
            tasks.comments are not included in the 'full record'
        """
        o2oTables = self.tablesForRelationType('o2o')  # fetch all o2o tables
        commonFields = self.commonFields()

        recordKeys = {}  # open returned dictionary

        for tbl in o2oTables:
            tblName = self.tables(tbl)
            fields = self.tableFields(tblName)

            if not isinstance(fields, list):
                continue

            for field in fields:
                if field in self.ignoreOnRetrieval():
                    continue

                if field in commonFields:
                    key = tbl + field
                else:
                    key = field

                recordKeys[key] = tbl

        return recordKeys

    def generateRelationTypeIds(self, relationType):
        """
            Returns [list] of id column names with tbl prefix prepended.
            You can fetch 'o2o', 'm2m', 'rlc' columns with this.
            Defaults to 'o2o'
        """
        abbrvs = self.tablesForRelationType(relationType)
        ids = []

        for abbrv in abbrvs:
            ids.append(abbrv + 'id')

        return ids

    def abbreviations(self):
        """
            returns list of table abbreviations for App/Space/Module
        """
        tables = self.tables()
        return tables.keys()

    def getAbbreviationForTable(self, tableName):
        """
            returns specific table's abbreviation.
        """
        if not tableName:
            return None

        tables = self.tables()

        for abbrv, name in tables.items():
            if tableName == name:
                return abbrv
        return None

    def columnName(self, key):
        """
            For future implementation.
            Validate requested key exists in mapper.
        """
        return key

    def returnValue(self, info, key):
        """
            Helper function. Used internally.
        """
        if key is not None and key in info:
            return info[key]

        if key == 'all':
            return info

        return None

