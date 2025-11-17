Types of Validation
=============================

The validations being referred to in this directory's classes deal with:

 1. User Access Roles: can the current user making CRUD (or other) requests to
    the DB actually perform those CRUD operations.

 2. T.B.A.: There might be other layers of validation performed in this section.
    Those updates should be documented here (as well as the User Docs).


The Validation of actual form content should be performed by:
 1. The front-end (i.e. Bootstrap) layer of this application.
 2. The django.forms.Form Instances found in core.modules section of this CRM.
    This is the back-end (i.e. Python) level validation.
 3. The Django XSS, CSRF and SQL Inject validations (in views and other places)
 4. The MySQL DB should also prune out some errors.

 I realize this might not be enough validation of content. We might explore a thicker
 layer of Python level validations in the future.

