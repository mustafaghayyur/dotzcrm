from core.dotzSettings import project
from .schema.main import schema
from .background import Background

class BaseOperations(Background):
    """
        This class and its inheritors will help map tables to data in 
        meaningful ways.
    """
    def tables(self, key = 'all'):
        """
            Grabs the table value(s) from schema.
        """
        info = []
        for tbl in self.state.get('tablesUsed'):
            info.append(schema[tbl]['table'])
        return self.returnValue(info, key)

    def models(self, key = 'all'):
        """
            Grabs the model value(s) from schema.
        """
        info = []
        for tbl in self.state.get('tablesUsed'):
            info.append(schema[tbl]['model'])
        return self.returnValue(info, key)
    
    def modelPaths(self, key = 'all'):
        """
            Grabs the model-path value(s) from schema.
        """
        info = []
        for tbl in self.state.get('tablesUsed'):
            info.append(schema[tbl]['path'])
        return self.returnValue(info, key)

    def tableFields(self, name = 'all'):
        """
            Grabs the table-cols list(s) from schema.
        """
        info = []
        for tbl in self.state.get('tablesUsed'):
            info.append(schema[tbl]['cols'])
        return self.returnValue(info, name)

    def tableAbbreviation(self, fullTableName):
        """
            Determine single full-table-name's correct abbreviation.
            Or return list of table abbreviations being used.
        """
        for tbl in schema:
            if schema[tbl]['table'] == fullTableName:
                return tbl
            
        tables = self.tables()
        return tables.keys()


    def isCommonField(self, key, prefix = False):
        """
            Determine whether field is common among children tables.
        """
        sz = project['mapper']['tbl_code_size']
        field = key[sz:] if prefix else key  # grab correct fieldName to compare

        if field in self.commonFields():
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


    def column(self, key):
        """
            In the future: if certain columns change name, this intermediary function
            can be used to translate them in legacy code.

            All columns should be referenced through this function.
        """
        return key
