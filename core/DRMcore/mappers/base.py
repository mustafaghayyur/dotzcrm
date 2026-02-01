from core.dotzSettings import project
from .background import Background

class BaseOperations(Background):
    """
        This class and its inheritors will help map tables to data in 
        meaningful ways.
    """
    def tables(self, key = 'all'):
        """
            Grabs the table's (or all tables in mapper)'s full name from schema.
        """
        tablesUsed = self.state.get('tablesUsed')
        if key is not None and key in tablesUsed:
            return tablesUsed[key]

        info = {}
        allTables = self.state.get('tables')
        for tbl in tablesUsed:
            info[tbl] = allTables[tbl]
        return self.returnValue(info, key)

    def models(self, key = 'all'):
        """
            Grabs the model value(s) from schema for mapper table(s).
        """
        tablesUsed = self.state.get('tablesUsed')
        if key is not None and key in tablesUsed:
            allModels = self.state.get('models')
            return allModels[key]
        
        info = {}
        tablesUsed = self.state.get('tablesUsed')
        allModels = self.state.get('models')
        for tbl in tablesUsed:
            info[tbl] = allModels[tbl]
        return self.returnValue(info, key)
    
    def modelPaths(self, key = 'all'):
        """
            Grabs the model-path value(s) from schema for mapper table(s).
        """
        tablesUsed = self.state.get('tablesUsed')
        if key is not None and key in tablesUsed:
            allPaths = self.state.get('models')
            return allPaths[key]
        
        info = {}
        tablesUsed = self.state.get('tablesUsed')
        allPaths = self.state.get('paths')
        for tbl in tablesUsed:
            info[tbl] = allPaths[tbl]
        return self.returnValue(info, key)

    def tableFields(self, name = 'all'):
        """
            Grabs the table-cols list(s) from schema for each table in mappers.
        """
        tablesUsed = self.state.get('tablesUsed')
        if name is not None and name in tablesUsed:
            allColLists = self.state.get('models')
            return allColLists[name]
        
        info = {}
        tablesUsed = self.state.get('tablesUsed')
        allColLists = self.state.get('cols')
        for tbl in tablesUsed:
            info[tbl] = allColLists[tbl]
        return self.returnValue(info, name)
    
    def tableTypes(self, name: str):
        """
            Grabs the list of all tables with type 'name' from schema: 
            
            :param name: [str] must be enum from: 'o2o' | 'm2m' | 'rlc'
            
            :returns [list]
        """
        info = []
        tablesUsed = self.state.get('tablesUsed')
        allTablesType = self.state.get('types')
        for tbl in tablesUsed:
            if tbl in allTablesType and allTablesType[tbl] == name:
                info.append(tbl)
        return info

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


    def generateO2OFields(self):
        """
            Only One-to-One records-types are handled.
        """
        o2oTables = self.tableTypes('o2o')  # fetch all o2o tables used
        return self.generateFieldsDict(o2oTables)
    
    def generateAllFields(self):
        """
            M2M, O2O and RLC tables are included.
        """
        tables = self.tables()  # fetch all tablesUsed
        return self.generateFieldsDict(tables)

    def generateFieldsDict(self, tablesList):
        """
        Generates a dictionary holding all 'FieldNames' => 'table-key' pairs.

        :param tablesList: [list] provided tables list to process.
        """
        commonFields = self.commonFields()

        dictionary = {}  # open returned dictionary

        for tbl in tablesList:
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


    def collectM2MTables(self):
        """
            Many-to-Many tables, by their definition, bring many tables/enities into the mix.
            This method collects all tables associated with the m2m tables of current mapper,
            and returns a list of all tables mentioned in Mapper._m2mFields() definition.
        """
        m2mEntities = self.m2mFields()
        tables = [] # bucket

        for entity in m2mEntities:
            array = []
            array.append(entity) # first add the entity key itself, should be a table key
            if isinstance(m2mEntities[entity]['tables'], list):
                array.extend(m2mEntities[entity]['tables']) # next, add the 'tables' value, which should be a list
            
            tables.extend(array) # finally, merge the array with tables

        return list(set(tables)) # only send back unique tables list


    def column(self, key):
        """
            In the future: if certain columns change name, this intermediary function
            can be used to translate them in legacy code.

            All columns should be referenced through this function.
        """
        return key
