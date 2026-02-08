class Singleton:
    """
        A base class that uses a class attribute to manage a single instance.
        All classes inheriting from Singleton will themselves be singletons.
        
        @todo: confirm this class works as a singleton
    """
    _instances = {}

    def __new__(cls, *args, **kwargs):
        """
            Overrides the default object creation to ensure only one instance
            per derived class is created and stored in _instances.
        """
        if cls not in cls._instances:
            # Create a new instance using the superclass __new__
            instance = super(Singleton, cls).__new__(cls)
            
            # Store the instance
            cls._instances[cls] = instance
       
        # Return the existing instance
        return cls._instances[cls]