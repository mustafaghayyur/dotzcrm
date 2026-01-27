departments = {
    'dede': {
        'table': 'users_department',
        'model': 'Department',
        'path': 'users.models',
        'cols': ['id', 'name', 'description', 'create_time', 'update_time', 'delete_time', 'parent_id'],
    },
    'dehe': {
        'table': 'users_departmenthead',
        'model': 'DepartmentHead',
        'path': 'users.models',
        'cols': ['id', 'create_time', 'delete_time', 'department_id', 'user_id'],
    },
    'deus': {
        'table': 'users_usertodepartment',
        'model': 'UserToDepartment',
        'path': 'users.models',
        'cols': ['id', 'create_time', 'delete_time', 'department_id', 'user_id'],
    },
}