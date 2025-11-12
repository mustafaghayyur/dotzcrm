"""
    These settings can be imported to anywhere in the project with:
    from core.settings import * (asterisk representing name of dictionary)
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
    'recentInterval': '30',
    'keys': {
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

tickets = {
    'recentInterval': '30',
    'keys': {
        'latest': {
            'archive': 'archive',
            'latest': 'latest',
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

documents = {
    'recentInterval': '30',
    'keys': {
        'latest': {
            'archive': 'archive',
            'latest': 'latest',
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

customers = {
    'recentInterval': '30',
    'keys': {
        'latest': {
            'archive': 'archive',
            'latest': 'latest',
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

rdms = {
    'regex': {
        'stringsA': '',
        'ints_big': '^[0-9]{1,9999}$',
        'dates': '^[0-9]{4}\-[0-9]{2}\-[0-9]{2}\s[0-9]{2}\:[0-9]{2}\:[0-9]{2}$',
    }
    'tasks_keys': {
        'all': {
            # Key's carry tbl_abbr[first letter] + column name
            'tid': 't',
            
            'tcreate_time': 't',
            'tupdate_time': 't',
            'tdelete_time': 't',
            
            'did': 'd',
            'lid': 'l',
            'sid': 's',
            'vid': 'v',
            'aid': 'a',

            'description': 't',
            'details': 'd',
            'deadline': 'l',
            'status': 's',
            'visibility': 'v',
            'assignor_id': 'a',
            'assignee_id': 'a',
            'creator_id': 't',
            'parent_id': 't',


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

            'latest': ''

        }
    }
}
