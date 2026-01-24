"""
    This file will carry classes over-writing permissions system of Django.
    We aim to create a permission system using the Users.user_level column (newly created).
    Where:
     - level 5 user: is an external member of the organization like a steakholder or client/customer.
     - level 10 user: is a team member of the CRM+PM as a company employee (lowest level permission within company employees)
     - level 15 user: is a team leader of the CRM+PM as a Project leader/manager. They can edit things within the tasks/documents/tickets on a highler level than general level ten users.
     - level 20 user: is a TBA but they would be of even higher privilage in the system, like sernior management, etc.
     ...
     - level 99 user: is the highest level user access. Chances are system admins will have this access level.

     Notes:
      - we may climb higher than 99 if the need arises in the future.
      - What happens to access levels newly discovered, later in the process that are in the middle or below the lowest? We will use middle-numbers that have not been allocated yet.

    Principles for permission system:
     - We want the least number of database-operations needed to make secure, reliable permission checks.
     - We want to ideally store meta data about a user in the token claim that will be repeatedly needed to make permission-acess level decisions upon every authentication request.
     - Im thinking of using the folliwng items to make these decisions (Model.column_name reference below):
        - User.user_level
        - user's Depertment.id (id would tell us if the dept has permissions to a certain view)
        - user's WorkSpace affilations [Task app only] (all users have limited access to specific workspaces)

    I want an algorythm that allows me to define:
        - user-groups that have permission to any given view based on:
            1. User.user_level x Department.id (the user is affiliated with):
                to determine which of C.R.U.D. permissions they have in the current rest-api view request
            2. In tasks: User.user_level x WorkSpace (user is affilaited with)
                to determine which of the C.R.U.D. permissions they have in that rest-api view.

    Basically can we leave the permissions open to a matrix which says:
        if a user-group has the the following table.col_name value conditions met, then they have either create, read, update or delete permission. Placed into a generic function that isn't affilaited with a view. So I can call that method in any rest-api view (that has CRUD operations defined), and say:
            conditions = {
                - user_group_name = 'some name',
                - dept_ids in [2, 55, ... some list of depts allowed for that view],
                - work_space_user_id = 'some id value like 33',
            }

    So if the current user matches those conditions defined in the conditions dictionary, the permissions system grants the user access to the view requested (based on the HTTP method they are using).

    Please do your best to fulfill as many of these criterion. If some thing can't be done right away, I can make more specific requests later, when I have refined your code.

    create classes here...
"""

