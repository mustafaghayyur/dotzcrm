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
    'tasks': {
        'all': {
            # Key's carry tbl_abbr[first letter] + column name
            # values carry regex used for that column
            'tid': 'ints_big',
            
            #ISO 8601 string format: 'YYYY-MM-DD HH:MM:SS'
            'tct': 'dates',
            'tut': 'dates',
            'tdt': 'dates',
            
            'did': 'ints_big',
            'lid': 'ints_big',
            'sid': 'ints_big',
            'vid': 'ints_big',
            'aid': 'ints_big',

            'description': 'description',
            'deadline': 'deadline',
            'status': 'status',
            'visibility': 'visibility',
            'assignor': 'assignor',
            'assignee': 'assignee',

            'dct': 'dates',
            'lct': 'dates',
            'sct': 'dates',
            'vct': 'dates',
            'act': 'dates',

            'ddt': 'dates',
            'ldt': 'dates',
            'sdt': 'dates',
            'vdt': 'dates',
            'adt': 'dates',

        }
    }
}
