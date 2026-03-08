import $A from "../helper.js";

export default (taskInfo) => {
    $A.query().search('tata').fields('tata_id', 'description').join({
            'left|wowo_id': 'tata_workspace_id'
        }).where({
            workspace_id: taskInfo['workspace_id'],
        }).order([{tbl:'tata', col: 'id', sort: 'desc'}])
        .execute('taskEditModalResponse', embedTasksDataIntoForm);


    $A.query().search('usus').fields('usus_id', 'username', 'first_name', 'last_name').join({
            'left|usus_id': 'wous_user_id',
        }).where({
            wous_workspace_id: taskInfo['workspace_id'],
        }).order([{tbl:'usus', col: 'last_name', sort: 'asc'}])
        .execute('taskEditModalResponse', embedUsersDataIntoForm);


    
    function embedTasksDataIntoForm(data, containerId) {
        console.log('We are inside embedTasksDataIntoForm().', data, containerId);
    }

    function embedUsersDataIntoForm(data, containerId) {
        console.log('We are inside embedUsersDataIntoForm().', data, containerId);
    }
}