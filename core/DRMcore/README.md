Data Relationship Manager (DRM)
===============================================================

The DRM works on top of Django's ORM to provide powerful CRUD operability over
the entire Module/App/Space at once..

Therefore:

 -> the Tasks DRM is a wrapper class meant to assist in convenient CRUD operations
    of ALL Tasks(and O2O Children) tables. including tasks_assignments, tasks_status, etc...

 -> the Tickets DRM is a wrapper class meant to assist in convenient CRUD operations
    of ALL Tickets(and O2O Children) tables. Including tickets_status, etc...

 -> the Documents DRM is a wrapper class meant to assist in convenient CRUD operations
    of ALL Documents(and O2O Children) tables. Including document_summary, etc...

 -> the Customer DRM is a wrapper class meant to assist in convenient CRUD operations
    of ALL Customers(and O2O Children) tables. Including customer_address, etc...

In addition to O2O; M2M and M2O (referred to as RLC) are also handled with our DRMs.

LAWS OF CRUD Operations:
=======================================================
Create Read Update Delete Operations
------------------------------------

 1) All crud operations will be done with these the DRM files. Operation 
    modification can be done in the crud classes. While raw query modification 
    in the DRM.querysets files. THIS IS ABSOLUTE.

 2) If a certain crud operation is missing. It must be added/modified in the DRM files.
    And the related DRM.querysets folder (which carries the raw SQL queries.)

 3) The django models are not to be touched unless for modifying DB/table structures
    in the DotzCRM MySQL database.

These laws are designed to maintain consistent, reliable data structures within the CRM.

Since DotzCRM relies heavily on Raw MySQL queries, we need a way to maintain our own order.

