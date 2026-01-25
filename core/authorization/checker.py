from typing import Dict, List
from core.helpers import misc

class ObjectPermissionChecker:
    """
    Checks if a user has permission to perform an action based on their attributes.
    Works with User.user_level, departments, and workspace affiliations.
    """
    
    def __init__(self, request, permission_matrix: Dict = None):
        """
        Initialize permission checker.
        
        Args:
            request: DRF request object with authenticated user
            permission_matrix: Dict with rules for each HTTP method
        """
        self.request = request
        self.user = request.user
        self.http_method = request.method
        self.permission_matrix = permission_matrix or {}
        
        # Cache user attributes
        self.user_level = getattr(self.user, 'user_level', None)
        self.user_id = getattr(self.user, 'id', None)
        self.user_dept_ids = self._get_user_departments()
        self.user_workspace_ids = self._get_user_workspaces()
    
    def _get_user_departments(self) -> List[int]:
        """
        Get list of department IDs the user is affiliated with.
        Minimizes queries by checking request context first.
        """
        # Try to get from request context if cached
        if hasattr(self.request, '_user_dept_ids'):
            return self.request._user_dept_ids
        
        # Query database if not cached
        try:
            from users.models import UserToDepartment
            dept_ids = list(
                UserToDepartment.objects.filter(
                    user_id=self.user_id,
                    delete_time__isnull=True
                ).values_list('department_id', flat=True)
            )
            # Cache in request
            self.request._user_dept_ids = dept_ids
            return dept_ids
        except Exception as e:
            misc.log(str(e), 'Error fetching user departments')
            return []
    
    def _get_user_workspaces(self) -> List[int]:
        """
        Get list of workspace IDs the user is affiliated with.
        Minimizes queries by checking request context first.
        """
        # Try to get from request context if cached
        if hasattr(self.request, '_user_workspace_ids'):
            return self.request._user_workspace_ids
        
        # Query database if not cached
        try:
            from tasks.models import WorkSpaceUser
            workspace_ids = list(
                WorkSpaceUser.objects.filter(
                    user_id=self.user_id,
                    delete_time__isnull=True
                ).values_list('workspace_id', flat=True)
            )
            # Cache in request
            self.request._user_workspace_ids = workspace_ids
            return workspace_ids
        except Exception as e:
            misc.log(str(e), 'Error fetching user workspaces')
            return []
    
    # This is the core of the checker...
    def check_permission(self, method: str = None, 
                        user_levels: List[int] = None,
                        dept_ids: List[int] = None,
                        workspace_ids: List[int] = None) -> bool:
        """
        Check if user has permission based on conditions.
        
        Args:
            method: HTTP method to check (defaults to request.method)
            user_levels: List of allowed user_levels
            dept_ids: List of allowed department IDs (None = no restriction)
            workspace_ids: List of allowed workspace IDs (None = no restriction)
        
        Returns:
            bool: True if user meets all conditions, False otherwise
        """
        method = method or self.http_method
        
        # Get rules from matrix if not provided
        if user_levels is None and self.permission_matrix:
            rules = self.permission_matrix.get(method, {})
            user_levels = rules.get('user_levels', [])
            dept_ids = rules.get('dept_ids', dept_ids)
            workspace_ids = rules.get('workspace_ids', workspace_ids)
        
        misc.log({
            'user_level': self.user_level,
            'allowed_levels': user_levels,
            'user_dept_ids': self.user_dept_ids,
            'allowed_dept_ids': dept_ids,
        }, f'Checking permission for {method}')
        
        # Check user level
        if user_levels and self.user_level not in user_levels:
            misc.log(f'User level {self.user_level} not in allowed {user_levels}', 'Permission denied')
            return False
        
        # Check department affiliation (if restricted)
        if dept_ids is not None:  # None means no restriction
            if not self.user_dept_ids:
                misc.log('User has no department affiliation', 'Permission denied')
                return False
            
            if not any(dept_id in dept_ids for dept_id in self.user_dept_ids):
                misc.log(f'User dept {self.user_dept_ids} not in allowed {dept_ids}', 'Permission denied')
                return False
        
        # Check workspace affiliation (if restricted)
        if workspace_ids is not None:  # None means no restriction
            if not self.user_workspace_ids:
                misc.log('User has no workspace affiliation', 'Permission denied')
                return False
            
            if not any(ws_id in workspace_ids for ws_id in self.user_workspace_ids):
                misc.log(f'User workspace {self.user_workspace_ids} not in allowed {workspace_ids}', 'Permission denied')
                return False
        
        misc.log(f'Permission granted for {method}', 'Permission check passed')
        return True
    
    def can_read(self) -> bool:
        """Check if user can read (GET)"""
        return self.check_permission('GET')
    
    def can_create(self) -> bool:
        """Check if user can create (POST)"""
        return self.check_permission('POST')
    
    def can_update(self) -> bool:
        """Check if user can update (PUT/PATCH)"""
        return self.check_permission(self.http_method) and self.http_method in ['PUT', 'PATCH']
    
    def can_delete(self) -> bool:
        """Check if user can delete (DELETE)"""
        return self.check_permission('DELETE')
