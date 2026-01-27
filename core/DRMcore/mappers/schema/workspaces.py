workspaces = {
    'wowo': {
        'table': 'users_department',
        'model': 'Department',
        'path': 'users.models',
        'cols': ['id', 'name', 'description', 'create_time', 'update_time', 'delete_time', 'parent_id'],
    },
    'wode': {
        'table': 'users_departmenthead',
        'model': 'DepartmentHead',
        'path': 'users.models',
        'cols': ['id', 'create_time', 'delete_time', 'department_id', 'user_id'],
    },
    'wous': {
        'table': 'users_usertodepartment',
        'model': 'UserToDepartment',
        'path': 'users.models',
        'cols': ['id', 'create_time', 'delete_time', 'department_id', 'user_id'],
    },
    'wota': {
        'table': 'users_usertodepartment',
        'model': 'UserToDepartment',
        'path': 'users.models',
        'cols': ['id', 'create_time', 'delete_time', 'department_id', 'user_id'],
    },

}