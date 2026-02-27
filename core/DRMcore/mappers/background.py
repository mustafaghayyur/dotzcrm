from ...lib.state import State
from ...helpers import misc
from .modifiers import Manipulate
from .schema.main import schema
from .ValuesMapper import ValuesMapperGeneric

class Background():
    """
        Defines background utility operations.
    """
    state = None
    values = None  # holds the ValuesMapper instance

    def __init__(self):
        self.state = State()

        # extract all values from schema needed by mapper.
        dictionary = Manipulate.makeStateLists(schema)
        self.state.set('tables', dictionary['tables'])
        self.state.set('models', dictionary['models'])
        self.state.set('paths', dictionary['paths'])
        self.state.set('cols', dictionary['cols'])
        self.state.set('types', dictionary['types'])

        self.values = ValuesMapperGeneric()  # incase app-level mapper has no VM of their own.

        self.startUpCode()

        # update tablesUsed with mapperTables
        tables = self.state.get('mapperTables')
        self.state.set('tablesUsed', tables)

    
    def startUpCode(self):
        """
            write startup operations you need done in init()
        """
        pass

    def rebuildMapper(self, additions: list):
        """
            Essentially, updates 'tablesUsed' key in state so mapper functions correctly.
        """        
        array = []
        tables = self.state.get('tables')

        if isinstance(additions, list):
            array = [tbl for tbl in additions if tbl in tables]
            
        tablesUsed = list(set(array))  # make list full of unique tbl-keys
        self.state.set('tablesUsed', tablesUsed)
        

    def setNewStateObject(self, stateObj):
        if stateObj is not None and isinstance(stateObj, State):
            self.state = stateObj

    def setValuesMapper(self, VMClassInstance):
        """
            Set's the self.values property
        """
        self.values = None  # reset values attribute
        self.values = VMClassInstance()

    def returnValue(self, info, key):
        """
            Helper function. Used internally.
        """
        if key is not None and key in info:
            return info[key]

        if key == 'all':
            return info

        return None
    