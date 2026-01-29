from core.dotzSettings import project
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
        tablesUsed = self.state.get('tablesUsed')
        allTables = self.state.get('tables')
        for tbl in tablesUsed:
            info.append(allTables[tbl])
        return self.returnValue(info, key)

    def models(self, key = 'all'):
        """
            Grabs the model value(s) from schema.
        """
        info = []
        tablesUsed = self.state.get('tablesUsed')
        allModels = self.state.get('models')
        for tbl in tablesUsed:
            info.append(allModels[tbl])
        return self.returnValue(info, key)
    
    def modelPaths(self, key = 'all'):
        """
            Grabs the model-path value(s) from schema.
        """
        info = []
        tablesUsed = self.state.get('tablesUsed')
        allPaths = self.state.get('paths')
        for tbl in tablesUsed:
            info.append(allPaths[tbl])
        return self.returnValue(info, key)

    def tableFields(self, name = 'all'):
        """
            Grabs the table-cols list(s) from schema.
        """
        info = []
        tablesUsed = self.state.get('tablesUsed')
        allColLists = self.state.get('cols')
        for tbl in tablesUsed:
            info.append(allColLists[tbl])
        return self.returnValue(info, name)
    
    def tableTypes(self, name = 'all'):
        """
            Grabs the list of all table's type from schema: ['o2o' | 'm2m' | 'rlc'].
        """
        info = []
        tablesUsed = self.state.get('tablesUsed')
        allTablesType = self.state.get('types')
        for tbl in tablesUsed:
            info.append(allTablesType[tbl])
        return self.returnValue(info, name)

    def tableAbbreviation(self, fullTableName = None):
        """
            Determine single full-table-name's correct abbreviation.
            Or return none.
        """
        allTables = self.state.get('tables')
        for tbl in allTables:
            if allTables[tbl] == fullTableName:
                return tbl
            
        return None


    def isCommonField(self, key, prefix = False):
        """
            Determine whether field is common among children tables.
        """
        sz = project['mapper']['tblKeySize']
        field = key[sz:] if prefix else key  # grab correct fieldName to compare

        if field in self.commonFields():
            return True
        return False
    


    def tablesForRelationType(self, relationType = 'o2o'):
        """
            Returns list of all tables in use by mapper, with specific relationship type.
            
            :param relationType: [str] 'o2o' | 'm2m' | 'rlc' 
        """
        if not isinstance(relationType, str):
            raise TypeError('Mapper().tablesForRelationType() requires string argument.')
        
        tablesUsed = self.state.get('tablesUsed')
        tableTypes = self.state.get('types')
        if not isinstance(tablesUsed, list):
            return []
        
        array = []
        for tbl in tablesUsed:
            if tbl in tableTypes and tableTypes[tbl] == relationType:
                array.append(tbl)

        return array


    def generateO2OFields(self):
        """
            Generates a completed dict of databaseColumn => tbl-abbreviation pairs.
            This dictionary can be used to manage Mapper's full records' validation.
            
            Only One-to-One records-types are handled.
        """
        o2oTables = self.tablesForRelationType('o2o')  # fetch all o2o tables
        commonFields = self.commonFields()

        dictionary = {}  # open returned dictionary

        for tbl in o2oTables:
            tblName = self.tables(tbl)
            fields = self.tableFields(tblName)

            if not isinstance(fields, list):
                continue

            for field in fields:
                if field in commonFields:
                    fullName = f'{tbl}_{field}'
                else:
                    fullName = field

                dictionary[fullName] = tbl

        return dictionary


    def column(self, key):
        """
            In the future: if certain columns change name, this intermediary function
            can be used to translate them in legacy code.

            All columns should be referenced through this function.
        """
        return key
