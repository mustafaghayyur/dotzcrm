# Types of Validation
=============================

The validations being referred to in this directory's classes deal with:

 1. Authentication: handling all customizations of our token authentication system.

 2. User Access Roles: can the current user making CRUD (or other) requests to the DB actually perform those CRUD operations.


## Notes:

 - We have (for now) entirely removed session-based authentication from the non-reastapi views.
 - implemented auto-authencation on all restapi views that is token-based, not session based.
 - implemented removal of user-record DB queries upon every HTTP request authentication. Instead we are using user data stored in token claims to record current user.


### Data Validation (side note)

The Validation of actual form content should be performed by:
 1. The front-end (i.e. Bootstrap) layer of this application.
 2. The django serializers (will be the major validation later). This is the back-end (i.e. Python) level validation.
 3. The Django XSS, CSRF and SQL Inject validations (in views and other places)
 4. The MySQL DB should also prune out some errors.

 I realize this might not be enough validation of content. We might explore a thicker layer of Python level validations in the future.

