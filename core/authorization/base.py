from rest_framework.permissions import BasePermission
from .checker import  ObjectPermissionChecker

class BaseObjectPermission(BasePermission):
    """
    Base permission class for DRF views.
    Define permission_matrix in your view to customize.
    
    Usage:
        class MyView(APIView):
            permission_classes = [BaseObjectPermission]
            
            def get(self, request):
                # Define custom permission rules
                permission_matrix = {
                    'GET': {'user_levels': [10, 15, 20, 99]},
                    'POST': {'user_levels': [15, 20, 99]},
                }
                checker = ObjectPermissionChecker(request, permission_matrix)
                if not checker.check_permission():
                    raise PermissionDenied("Insufficient permissions")
                # Continue with view logic
    """
    
    def has_permission(self, request, view):
        """
        Check if user has permission based on view's permission_matrix.
        """
        # Get permission matrix from view
        permission_matrix = getattr(view, 'permission_matrix', None)
        
        if not permission_matrix:
            # No matrix defined, allow access
            return True
        
        # Check permission
        checker = ObjectPermissionChecker(request, permission_matrix)
        return checker.check_permission()
    
class IsTeamMember(BasePermission):
    """Allow access to team members (level 10 and above)"""
    def has_permission(self, request, view):
        if not request.user or not hasattr(request.user, 'user_level'):
            return False
        return request.user.user_level >= 10


class IsTeamLeader(BasePermission):
    """Allow access to team leaders (level 15 and above)"""
    def has_permission(self, request, view):
        if not request.user or not hasattr(request.user, 'user_level'):
            return False
        return request.user.user_level >= 15


class IsManager(BasePermission):
    """Allow access to managers (level 20 and above)"""
    def has_permission(self, request, view):
        if not request.user or not hasattr(request.user, 'user_level'):
            return False
        return request.user.user_level >= 20


class IsAdmin(BasePermission):
    """Allow access to admins only (level 99)"""
    def has_permission(self, request, view):
        if not request.user or not hasattr(request.user, 'user_level'):
            return False
        return request.user.user_level == 99
