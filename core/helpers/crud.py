from django import forms

def generateModelInfo(mapper, tbl):  # rdbms, space, tbl):
    tableName = mapper.tables(tbl)
    return {
        'model': mapper.models(tbl),  # identify model
        'table': tableName,  # identify table
        'cols': mapper.tableFields(tableName),  # grab column names
    }
    
def isValidId(dictionary, idKey):
    if idKey in dictionary and dictionary[idKey] is not None:
        if not isinstance(dictionary[idKey], int) and dictionary[idKey].isdigit():
            item = int(dictionary[idKey])
            if item > 0:
                return True
    return False

class DateTimeLocalInput(forms.DateTimeInput):
    input_type = 'datetime-local'

