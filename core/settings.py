"""
    These settings can be imported to anywhere in the project with:
     > from core.settings import * (asterisk representing name of dictionary)
"""

project = {
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
    'values': {  # defines enums for crud operations
        'latest': {
            'archive': 2,
            'latest': 1,
        },
        'visibility': {
            'private': 'private',
            'assigned': 'assigned',
            'organization': 'organization',
            'stakeholders': 'stakeholders',
        },
        'status': {
            'assigned': 'assigned',
            'viewed': 'viewed',
            'queued': 'queued',
            'started': 'started',
            'onhold': 'onhold',
            'abandoned': 'abandoned',
            'reassigned': 'reassigned',
            'awaitingfeedback': 'awaitingfeedback',
            'completed': 'completed',
            'failed': 'failed',
        },
    },

}

####################################################################
# BELOW THIS ONLY QUALIFIED DEVELOPERS SHOULD TOUCH
# ----------------------------------------------------
# Below configurations impact the integrity of DotzCRM. Modifications
# will result in dire consequences to the system.
####################################################################
rdbms = {
    'tasks': {
        'keys': {
            # all primary_keys for Tasks (and children tables) should be
            # listed here:
            'only_pk': ['tid', 'did', 'lid', 'sid', 'vid', 'aid', 'wid'],

            # these keys tend to be found in every table and cause problems if not handled separately
            'problematic': ['id', 'create_time', 'update_time', 'delete_time'],

            ############################################################################
            # Full Record: those keys that can be queried by core.Models.querysets.tasks
            # as a whole record with one-to-one relations. This means they can only have
            # one active record for a single active task record.
            # Many-to-one records like watchers are not included in the 'full_record'
            ############################################################################
            'full_record': {
                # Key's carry tbl_abbrv[first letter] + column name
                'tid': 't',
                'did': 'd',
                'lid': 'l',
                'sid': 's',
                'vid': 'v',
                'aid': 'a',

                'tcreate_time': 't',
                'tupdate_time': 't',
                'tdelete_time': 't',

                'dcreate_time': 'd',
                'lcreate_time': 'l',
                'screate_time': 's',
                'vcreate_time': 'v',
                'acreate_time': 'a',

                'ddelete_time': 'd',
                'ldelete_time': 'l',
                'sdelete_time': 's',
                'vdelete_time': 'v',
                'adelete_time': 'a',

                # These keys don't carry table identifiers in key name
                'description': 't',
                'details': 'd',
                'deadline': 'l',
                'status': 's',
                'visibility': 'v',
                'assignor_id': 'a',
                'assignee_id': 'a',
                'creator_id': 't',
                'parent_id': 't',
                'latest': ''
            },  # end of full_record
        },  # end of keys

        'table_names': {  # index of all names by their abbreviations used in CRUD operations
            't': 'tasks_task',
            'd': 'tasks_details',
            'l': 'tasks_deadline',
            's': 'tasks_status',
            'v': 'tasks_visibility',
            'a': 'tasks_assignment',
            'w': 'tasks_watcher',
        },
        'model_names': {  # index of all names by their abbreviations used in CRUD operations
            't': 'Task',
            'd': 'Details',
            'l': 'Deadline',
            's': 'Status',
            'v': 'Visibility',
            'a': 'Assignment',
            'w': 'Watcher',
        },
    },  # end of tasks
    'tables': {
        'tasks_task': ['id', 'create_time', '...']
    }
}
