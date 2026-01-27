schema = {
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




    'usus': {
        'table': 'auth_user',
        'model': 'User',
        'path': 'users.models',
        'cols': ['id', 'password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined', 'create_time', 'delete_time', 'update_time', 'user_level'],
    },
    'uspr': {
        'table': 'users_userprofile',
        'model': 'UserProfile',
        'path': 'users.models',
        'cols': ['id', 'legal_first_name', 'legal_last_name', 'office_phone', 'office_ext', 'cell_phone', 'home_phone', 'office_location', 'create_time', 'update_time', 'delete_time', 'user_id'],
    },
    'usre': {
        'table': 'users_userreportsto',
        'model': 'UserReportsTo',
        'path': 'users.models',
        'cols': ['id', 'create_time', 'delete_time', 'reports_to_id', 'user_id'],
    },
    'usse': {
        'table': 'users_usersettings',
        'model': 'UserSettings',
        'path': 'users.models',
        'cols': ['id', 'settings', 'create_time', 'update_time', 'delete_time', 'user_id'],
    },
    'used': {
        'table': 'users_editlog',
        'model': 'UserSettings',
        'path': 'users.models',
        'cols': ['id', 'change_log', 'create_time', 'delete_time', 'user_id'],
    },





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