from core.authorization.permissions import BasePermission

class UserPermissions(BasePermission):
    """
        This class handles CRUD and Search permissions setting/handling
        for the Users Mapper.
    """
    def laws(self):
        return {
            'read': {
                'banned': {
                    'usus': ['password', 'last_login', 'is_superuser', 'is_staff', 'date_joined'],
                    'usse': ['settings'],
                    'used': ['change_log']
                }
            },
            'update': {
                'banned': {
                    'usus': 'all',
                    'uspr': 'all',
                    'usre': 'all',
                    'usse': 'all',
                    'used': 'all',
                }
            },
            'create': {
                'banned': {
                    'usus': 'all',
                    'uspr': 'all',
                    'usre': 'all',
                    'usse': 'all',
                    'used': 'all',
                }
            },
            'delete': {
                'banned': {
                    'usus': 'all',
                    'uspr': 'all',
                    'usre': 'all',
                    'usse': 'all',
                    'used': 'all',
                }
            }
        }