
class RelationshipMappers():
    """
        This class and its inheritors will help map tables to data in 
        meaningful ways.
    """
    def __init__(self):
        pass

    def ignoreOnRetrieval(self):
        return []

    def tableFields(self):
        return []

    def commonFields(self):
        return []

    def tablesForRelationType(self):
        return []

    def master(self):
        return {
            'table': '',
            'abbreviation': '',
            'foreignKeyName': '',
        }

    def tables(self):
        return {}

    def models(self):
        return {}

    def ignoreOnUpdates(self):
        return {}

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
        abbrvs = self.tablesForRelationType(relationType)
        ids = []

        for abbrv in abbrvs:
            ids.append(abbrv + 'id')

        return abbrv

    def abbreviations(self):
        tables = self.tables()
        return tables.keys()
