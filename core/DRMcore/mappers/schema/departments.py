departments = {
    'dede': {
        'table': 'users_department',
        'model': 'Department',
        'path': 'users.models',
        'type': 'o2o',
        'cols': [
            'id',
            'name',
            'description',
            'create_time',
            'update_time',
            'delete_time',
            'parent_id'
        ],
    },
    'dehe': {
        'table': 'users_departmenthead',
        'model': 'DepartmentHead',
        'path': 'users.models',
        'type': 'm2m',
        'cols': [
            'id',
            'create_time',
            'delete_time',
            'department_id',
            'user_id',
            'latest'
        ],
    },
    'deus': {
        'table': 'users_usertodepartment',
        'model': 'DepartmentUser',
        'path': 'users.models',
        'type': 'm2m',
        'cols': [
            'id',
            'latest',
            'create_time',
            'delete_time',
            'department_id',
            'user_id'
        ],
    },
}