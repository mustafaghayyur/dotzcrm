tasks = {
    'tata': {
        'table': 'tasks_task',
        'model': 'Task',
        'path': 'tasks.models',
        'cols': ['id', 'description', 'create_time', 'update_time', 'delete_time', 'creator_id', 'parent_id'],
    },
    'tade': {
        'table': 'tasks_details',
        'model': 'Details',
        'path': 'tasks.models',
        'cols': ['id', 'details', 'latest', 'create_time', 'delete_time', 'task_id'],
    },
    'tadl': {
        'table': 'tasks_deadline',
        'model': 'Deadline',
        'path': 'tasks.models',
        'cols': ['id', 'deadline', 'latest', 'create_time', 'delete_time', 'task_id'],
    },
    'tast': {
        'table': 'tasks_status',
        'model': 'Status',
        'path': 'tasks.models',
        'cols': ['id', 'status', 'latest', 'create_time', 'delete_time', 'task_id'],
    },
    'tavi': {
        'table': 'tasks_visibility',
        'model': 'Visibility',
        'path': 'tasks.models',
        'cols': ['id', 'visibility', 'latest', 'create_time', 'delete_time', 'task_id'],
    },
    'taas': {
        'table': 'tasks_assignment',
        'model': 'Assignment',
        'path': 'tasks.models',
        'cols': ['id', 'latest', 'create_time', 'delete_time', 'assignee_id', 'assignor_id', 'task_id'],
    },
    'tawa': {
        'table': 'tasks_watcher',
        'model': 'Watcher',
        'path': 'tasks.models',
        'cols': ['id', 'latest', 'create_time', 'delete_time', 'task_id', 'watcher_id'],
    },
    'taco': {
        'table': 'tasks_comment',
        'model': 'Comment',
        'path': 'tasks.models',
        'cols': ['id', 'comment', 'parent_id', 'create_time', 'update_time', 'delete_time', 'task_id'],
    },
}