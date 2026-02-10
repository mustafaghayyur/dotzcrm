"""
    These settings can be imported to anywhere in the project with:
     > from core.dotzSettings import * (asterisk representing name of dictionary)
"""

project = {
    'mapper': {
        'tblKeySize': 5, # 4 + _ = 5 characters for table-key-size
    },

    # Number of days a task stays in the database system post completion or fail
    'tasksLifeSpan': '1095',
    # Number of days a ticket stays in the database system post completion or fail
    'ticketsLifeSpan': '1095',

    # Number of days the following records stay 'deleted' post being marked deleted:
    'tasksGarbageBin': '90',
    'ticketsGarbageBin': '90',
    'documentsGarbageBin': '30',
    'customersGarbageBin': '90',
}

tasks = {
    'recentInterval': '30',  # what is recent in generic query terms? Number of days.
    'crud_logger_file': '/Users/mustafa/Sites/python/server1/CRUD.log'  # CRUD operations are logged properly when Django's DEBUG setting is True:
}

users = {
    'recentInterval': '30',  # what is recent in generic query terms? Number of days.
    'crud_logger_file': '/Users/mustafa/Sites/python/server1/CRUD.log'  # CRUD operations are logged properly when Django's DEBUG setting is True:
}

tickets = {
    'recentInterval': '30',  # what is recent in generic query terms? Number of days.
    'crud_logger_file': '/Users/mustafa/Sites/python/server1/CRUD.log'  # CRUD operations are logged properly when Django's DEBUG setting is True:
}

documents = {
    'recentInterval': '30',  # what is recent in generic query terms? Number of days.
    'crud_logger_file': '/Users/mustafa/Sites/python/server1/CRUD.log'  # CRUD operations are logged properly when Django's DEBUG setting is True:
}

customers = {
    'recentInterval': '30',  # what is recent in generic query terms? Number of days.
    'crud_logger_file': '/Users/mustafa/Sites/python/server1/CRUD.log'  # CRUD operations are logged properly when Django's DEBUG setting is True:
}
