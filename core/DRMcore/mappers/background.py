from ...lib.state import State
from .modifiers import Manipulate
from .schema.main import schema

class Background():
    """
        Defines background utility operations.
    """
    state = None
    universal = False
    values = None  # holds the ValuesMapper instance

    def __init__(self):
        """
        """
        if self.state is None:
            self.state = State()
            self.universal = True

        self.state.set('tables', Manipulate.makeTablesList(schema))
        self.state.set('models', Manipulate.makeModelsList(schema))
        self.state.set('paths', Manipulate.makeModelPathsList(schema))
        self.state.set('cols', Manipulate.makeTableColsList(schema))

        self.startUpCode()

    
    def startUpCode(self):
        """
            write startup operations you need done in init()
        """
        pass

    def addTables(self, mapperTables: list):
        """
        Merges tables defined in app-level mappers, and tables collected during 
        query generting operations.
        
        :param mapperTables: list of tables defined in app-level child-class.
        """
        addedTables = self.state.get('addedTables')
        if isinstance(addedTables, list):
            mapperTables.extend(addedTables)

        return mapperTables

    def setNewStateObject(self, stateObj):
        if stateObj is not None and isinstance(stateObj, State):
            self.state = stateObj

    def setValuesMapper(self, VMClassInstance):
        """
            Set's the self.values property
        """
        self.values = VMClassInstance()


    