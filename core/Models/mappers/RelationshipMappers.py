
class RelationshipMappers():
    """
        This class and its inheritors will help map tables to data in 
        meaningful ways.

        All App-specific extensions of this class should only define the 
        '_' prefixed version of methods defined here, returning simple lists,
        dictionaries, etc as needed.
    """
    
    def __init__(self):
        pass

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
        info = self._ignoreOnUpdates(key)
        return self.returnValue(info, key)

    def m2mFields(self, tbl = 'all'):
        relationships = self._m2mFields(tbl)
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
        mt = self.master('abbreviation')
        o2oTables.append(mt)  # add master-table to list

        commonFields = self.commonFields()

        recordKeys = {}  # open returned dictionary

        for tbl in o2oTables:
            fields = self.tableFields(tbl)

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
        """
        abbrvs = self.tablesForRelationType(relationType)
        ids = []

        for abbrv in abbrvs:
            ids.append(abbrv + 'id')

        return abbrv

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

    def returnValue(self, info, key):
        """
            Helper function. Used internally.
        """
        if key is not None and key in info:
            return info[key]

        if key == 'all':
            return info

        return None

