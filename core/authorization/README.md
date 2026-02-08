# What is covered in 'Authorization'
=============================

The validations being referred to in this directory's classes deal with:

 1. Authentication: handling all customizations of our token authentication system.

 2. User Access Roles: can the current user making CRUD (or other) requests to the DB actually perform those CRUD operations.

## Permissions Architecture (W.I.P.):

This file will carry classes overwriting permissions system of Django.
    We aim to create a permission system using the Users.user_level column.
    
    User Access Levels:
     - level 5:  External member (stakeholder/client)
     - level 10: Team member (employee, lowest level)
     - level 15: Team leader (project manager)
     - level 20+: Senior management
     - level 99: System administrator (highest)

    Permission System Architecture:
     - Uses User.user_level as primary permission indicator
     - Considers Department affiliations
     - Considers WorkSpace affiliations (for tasks)
     - Minimizes database queries by caching in JWT token
     - Provides matrix-based permission checking for CRUD operations

    Usage:
        ```
        condition_matrix = {
            'readers': {'user_levels': [5, 10, 15, 20, 99], 'dept_ids': None, 'workspace_ids': None},
            'writers': {'user_levels': [15, 20, 99], 'dept_ids': [1, 2, 3], 'workspace_ids': None},
            'deleters': {'user_levels': [20, 99], 'dept_ids': None, 'workspace_ids': None},
        }
        perm = ObjectPermissionChecker(request, condition_matrix)
        perm.can_read()  # returns True/False
        ```


## Notes:

 - We have (for now) entirely removed session-based authentication from the non-reastapi views.

 - implemented auto-authencation on all restapi views that is token-based, not session based.
 
 - implemented removal of user-record DB queries upon every HTTP request authentication. Instead we are using user data stored in token claims to record current user.


 ------------------------------------
 
### Data Validation (side note)

The Validation of actual form content should be performed by:

 1. The front-end (i.e. Bootstrap) layer of this application.

 2. The django serializers (will be the major validation later). This is the back-end (i.e. Python) level validation.

 3. The Django XSS, CSRF and SQL Inject validations (in views and other places)

 4. The MySQL DB should also prune out some errors.

 I realize this might not be enough validation of content. We might explore a thicker layer of Python level validations in the future.

