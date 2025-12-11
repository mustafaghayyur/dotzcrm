from core.helpers import misc

class RelationshipMappers():
    """
        This class and its inheritors will help map tables to data in 
        meaningful ways.

        All App-specific extensions of this class should only define the 
        '_' prefixed version of methods defined here, returning simple lists,
        dictionaries, etc as needed.
    """
    
    def __init__(self, mainTable):
        self.mainTable = mainTable

    def defaults(self, requestedFunc):
        if not isinstance(requestedFunc, str):
            raise Exception('Mapper.defaults() cannot execute provided function. Exiting.')

        requestedFunc = 'defaults_' + requestedFunc

        if hasattr(self, requestedFunc):
            functionCall = getattr(self, requestedFunc)

            if callable(functionCall):
                return functionCall()

        return None

    def defaults_orderBy(self):
        return self._defaults_orderBy()

    def commonFields(self):
        return self._commonFields()

    def tablesForRelationType(self, relationType = 'o2o'):
        return self._tablesForRelationType(relationType)

    def ignoreOnRetrieval(self):
        return self._ignoreOnRetrieval()

    def tableFields(self, name = 'all'):
        tables = self._tableFields()
        return self.returnValue(tables, name)

    def master(self, key = 'all'):
        info = self._master()
        return self.returnValue(info, key)

    def tables(self, key = 'all'):
        info = self._tables()
        return self.returnValue(info, key)

    def models(self, key = 'all'):
        info = self._models()
        return self.returnValue(info, key)

    def ignoreOnUpdates(self, key = 'all'):
        info = self._ignoreOnUpdates()
        return self.returnValue(info, key)

    def m2mFields(self, tbl = 'all'):
        relationships = self._m2mFields()
        return self.returnValue(relationships, tbl)

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

    def columnName(self, key, sphere = 'all'):
        """
            For future implementation.
            Validate requested key is valid in mapper.
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

