The Models being referred to here are not actual models defined within Django. This 
is more of a convenience term used to refer to collections of models for entire 
normalized objects in our RDMS (i.e. MYSQL).

Therefore:

 -> the Tasks Model is a wrapper class meant to assist in convenient CRUD operations
    of ALL Tasks(and O2O Children) tables. including tasks_assignments, tasks_status, etc...

 -> the Tickets Model is a wrapper class meant to assist in convenient CRUD operations
    of ALL Tickets(and O2O Children) tables. Including tickets_status, etc...

 -> the Documents Model is a wrapper class meant to assist in convenient CRUD operations
    of ALL Documents(and O2O Children) tables. Including document_summary, etc...

 -> the Customer Model is a wrapper class meant to assist in convenient CRUD operations
    of ALL Customers(and O2O Children) tables. Including customer_address, etc...


LAWS OF CRUD Operations:
=======================================================
Create Read Update Delete Operations
------------------------------------

 1) All crud operations will be done with these core.Models files/folders. Operation 
    modification can be done in the actual core.Models files. While raw query modification 
    in the core.Models.querysets directory. THIS IS ABSOLUTE.

 2) If a certain crud operation is missing. It must be added/modified in this same directory.
    And the related core.Models.querysets folder (which carries the actual raw SQL queries.)

 3) The django models are not to be touched unless for adding/modifying tables structures
    in the DotzCRM MySQL database structure.

These laws are designed to maintain consistent, reliable data structures within the CRM.

Since DotzCRM relies heavily on Raw MySQL queries, we need a way to maintain our own order.

