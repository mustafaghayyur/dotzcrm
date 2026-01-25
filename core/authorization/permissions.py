from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model
from typing import Dict, List

# User = get_user_model()

class PermissionMatrix:
    """
    Defines permission rules based on user groups and conditions.
    Stores rules for different HTTP methods (GET, POST, PUT, DELETE, etc.)
    """
    
    def __init__(self):
        """Initialize default permission rules"""
        self.matrix = {
            'GET': {
                'user_levels': [5, 10, 15, 20, 99],  # Everyone can read by default
                'dept_ids': None,  # None = no department restriction
                'workspace_ids': None,
            },
            'POST': {
                'user_levels': [10, 15, 20, 99],  # Members and above can create
                'dept_ids': None,
                'workspace_ids': None,
            },
            'PUT': {
                'user_levels': [15, 20, 99],  # Leaders and above can update
                'dept_ids': None,
                'workspace_ids': None,
            },
            'PATCH': {
                'user_levels': [15, 20, 99],
                'dept_ids': None,
                'workspace_ids': None,
            },
            'DELETE': {
                'user_levels': [20, 99],  # Managers and admins only
                'dept_ids': None,
                'workspace_ids': None,
            },
        }
    
    def set_permission(self, method: str, user_levels: List[int] = None, 
                      dept_ids: List[int] = None, workspace_ids: List[int] = None):
        """
        Set permission rule for a specific HTTP method.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            user_levels: List of user_level values allowed for this method
            dept_ids: List of department IDs allowed (None = no restriction)
            workspace_ids: List of workspace IDs allowed (None = no restriction)
        """
        self.matrix[method] = {
            'user_levels': user_levels or [],
            'dept_ids': dept_ids,
            'workspace_ids': workspace_ids,
        }
    
    def get_permission(self, method: str) -> Dict:
        """Get permission rule for a specific HTTP method"""
        return self.matrix.get(method, {})






