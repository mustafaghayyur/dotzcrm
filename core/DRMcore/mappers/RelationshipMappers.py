from .RMWrappers import Wrappers
from .state import State

class RelationshipMappers(Wrappers):
    """
        This class and its inheritors will help map tables to data in 
        meaningful ways.

        The Mapper is Singleton. Thus, only data that relates to Schema should
        be stored in properties, so it can be shared across Query operations.
    """
    values = None  # holds the ValuesMapper instance
    universal = False



    def __init__(self, VMClassInstance = None, state = None):
        """
            setup value-mapper instance in constructor
        """
        if state is not None and isinstance(state, State):
            self.state = state
            self.universal = True

        super().__init__()

        if VMClassInstance is not None:
            self.setValuesMapper(VMClassInstance)

    
    def setValuesMapper(self, VMClassInstance):
        """
            Set's the self.values property
        """
        self.values = VMClassInstance()


    def isCommonField(self, key, prefix = False):
        """
            Determine whether field is common among children tables.
        """
        k = key[4:] if prefix else key  # grab correct key to compare

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
            In the future: if certain columns change name, this intermediary function
            can be used to translate them in legacy code.

            All columns should be referenced through this function.
        """
        return key
