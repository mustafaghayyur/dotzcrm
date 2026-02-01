from core.helpers import strings

class Joins():
    """
        This is a static class.
        Helps parse and manage joins arguments.
    """

    @staticmethod 
    def parse(state, mapper):
        """
        Takes dictionary of Join definitions, along with native Mapper join functionaility,
        and ensures only valid, required tables are joined.
        
        :param state: QSM() state instance
        :param mapper: Mapper() instance
        """
        mt = mapper.master('abbreviation')
        mtId = mapper.master('foreignKeyName')
        joins = []
        tblsJoined = []  # bucket to keep track of added tables
        latestKey = mapper.column('latest')
        mapperTables = state.get('mapperTables')
        allTablesUsed = state.get('tablesUsed')
        revisionedTables = state.get('revisionedTables')
        joinsDict = state.get('joins')

        # first we add Mapper tables.
        for tbl in allTablesUsed:
            if tbl == mt or tbl == '':
                continue

            tableName = mapper.tables(tbl)
            
            joins.append(f' LEFT JOIN {tableName} AS {tbl} ON {mt}.id = {tbl}.{mtId}')
            tblsJoined.append(tbl)

            if state.get('latestFlag') and tbl in revisionedTables:
                joins.append(f' AND {tbl}.{latestKey} = %({latestKey})s')

        # next we add any additional tables specified in the joins argument to Manager.fetch()
        for leftStmt, rightStmt in joinsDict.items():
            left = strings.seperateTableKeyFromJoinArgument(leftStmt, state)
            right = strings.seperateTableKeyFromJoinArgument(rightStmt, state)

            if not isinstance(left, list) or not isinstance(right, list) or len(left) < 2 or len(right) < 2:
                raise KeyError('Error 1011: Join statements formed incorrectly.')
            
            if left[1] in allTablesUsed and right[1] in allTablesUsed:
                if right[1] in tblsJoined:
                    tableName = mapper.tables(tbl)  # fetch full table name
                    
                    joinType =  'LEFT JOIN' if left[0] is None else f'{left[0][:-1]} JOIN'
                    
                    joins.append(f' {joinType} {tableName} AS {left[1]} ON {left[1]}.{left[2]} = {right[1]}.{right[2]}')
                    tblsJoined.append(left[1])

                    if state.get('latestFlag') and tbl in revisionedTables:
                        joins.append(f' AND {left[1]}.{latestKey} = %({latestKey})s')

        return strings.concatenate(joins)
    
    
    