"""
    These settings can be imported to anywhere in the project with:
     > from core.settings import * (asterisk representing name of dictionary)
"""

project = {
    'mapper': {
        'tbl_code_size': 4,
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
    # CRUD operations are logged properly when Django's DEBUG setting is True:
    'crud_logger_file': '/Users/mustafa/Sites/python/server1/CRUD.log'
}
