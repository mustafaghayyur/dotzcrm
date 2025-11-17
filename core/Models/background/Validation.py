

"""
    This class is crudely designed to hold all error handling code for 
    CRUD Operations. Code should be designed to accommodate all modules of CRM
"""
class ErrorHandling:
    currentUser = None

    def __init__(self):
        pass
        
    def dictValidation(self, space, operation, dictionary):
        if not isinstance(dictionary, dict):
            raise Exception(f'Invalid input provided to {space}.CRUD.{operation}(). Expecting Dictionary.')
    
        if len(dictionary) < 1:
            raise Exception(f'Provided dictionary length zero in: {space}.CRUD.{operation}().')

