class State:
    """
        This class's instance will serve as a state holder.
        It can be passed it between operations to maintain data-integrity.
    """

    # state container [dict]
    state = None

    def __init__(self):
        self.state = {}

    def set(self, keyPath, value):
        """
            Set a key's value in state to provided value.

            :param keyPath: [str] should be '.' seperated path to target, nested key
            :param value: [*] can be any legitimate value stored in dictionary keys.
        """
        path = self.validateKey(keyPath)
        length = len(path)

        if length > 5:
            raise Exception('state().set() cannot handle key paths deeper than 5 levels.')
        
        if length == 1:
            self.state[keyPath] = value
            return
        
        if path[0] not in self.state:
            self.state[path[0]] = {}
        
        if length == 2:
            self.state[path[0]][path[1]] = value
            return
        
        if path[1] not in self.state[path[0]]:
            self.state[path[0]][path[1]] = {}

        if length == 3:
            self.state[path[0]][path[1]][path[2]] = value
            return
        
        if path[2] not in self.state[path[0]][path[1]]:
            self.state[path[0]][path[1]][path[2]] = {}

        if length == 4:
            self.state[path[0]][path[1]][path[2]][path[3]] = value
            return
        
        if path[3] not in self.state[path[0]][path[1]][path[2]]:
            self.state[path[0]][path[1]][path[2]][path[3]] = {}
        
        if length == 5:
            self.state[path[0]][path[1]][path[2]][path[3]][path[4]] = value
            return


    def get(self, keyPath, default = None):
        """
            Get a key from state dictionary.

            :param keyPath: [str] should be in the form of: 'key1.childNodeKey2', mapping out a path to the specific key you wish to retrieve.
            :param default: [*] allows for custom default return value setting upon key match failiure.
        """
        path = self.validateKey(keyPath)

        value = self.state
        for key in path:
            if isinstance(value, dict):
                if key in value:
                    value = value[key]
                    continue
            return default  # @todo: is this the right logic?
            
        return value
    

    def all(self):
        """
            returns entire state
        """
        return self.state

    def validateKey(self, keyPath):
        """
            verify minimum standards of keyPth
            :param keyPath: [str]
        """
        if not isinstance(keyPath, str):
            raise TypeError('state().get() expects a string based key.')
        
        path = keyPath.split('.')

        if not isinstance(path, list):
            raise Exception('Could not retrieve key path in state().get().')
        
        return path