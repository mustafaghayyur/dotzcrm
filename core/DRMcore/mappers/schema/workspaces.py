workspaces = {
    'wowo': {
        'table': 'tasks_workspace',
        'model': 'WorkSpace',
        'path': 'tasks.models',
        'type': 'o2o',
        'cols': [
            'id',
			'name',
			'description',
			'type',
			'create_time',
			'update_time',
			'delete_time'
        ],
    },
    'wode': {
        'table': 'tasks_workspacedepartment',
        'model': 'WorkSpaceDepartment',
        'path': 'tasks.models',
        'type': 'm2m',
        'cols': [
            'id',
			'create_time',
			'delete_time',
			'department_id',
			'workspace_id'
        ],
    },
    'wous': {
        'table': 'tasks_workspaceuser',
        'model': 'WorkSpaceUser',
        'path': 'tasks.models',
        'type': 'm2m',
        'cols': [
            'id',
			'create_time',
			'delete_time',
			'user_id',
			'workspace_id'
        ],
    },
    'wota': {
        'table': 'tasks_workspacetasks',
        'model': 'WorkSpaceTasks',
        'path': 'tasks.models',
        'type': 'm2m',
        'cols': [
            'id',
			'create_time',
			'delete_time',
			'task_id',
			'workspace_id'
        ],
    },

}