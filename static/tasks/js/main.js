import $A from './helper.js';
import { Main } from '../../core/js/lib/app.js';

/**
 * Begin Tasks Application
 */
Main(async () => {
    $A.dashboard({
        // 'Personal' tab of the tasks dashboard:
        personal: async () => {
            let request = null;
            const dashboardTodoList = await $A.tasks.load('dashboardTodoList');
            const dashboardTaskList = await $A.tasks.load('dashboardTaskList');

            request = $A.fetch.route('api.tasks.list', 'private');
            $A.fetch.body(request, 'personalTabResponse', {}, dashboardTodoList);

            let dictionary = {
                tbl: 'tata',
                selectors: ['tata_id', 'tast_id', 'description', 'tata_update_time', 'status', 'deadline'],
                conditions: {
                    tata_delete_time: 'is Null',
                    assignee_id: $A.app.memFetch('user_id'),
                    workspace: null,
                    visibility: 'workspaces',
                    status: ['assigned', 'queued', 'started']
                }
            }
            request = $A.fetch.route('api.terminal.list', null, { method: 'POST', body: JSON.stringify(dictionary) });
            $A.fetch.body(request, 'workspacesTabResponse', {}, dashboardTaskList);
        },
        // 'Workspaces' tab of tasks dashboard:
        workspaces: () => {},
    }, true);

    const cleanForm = await $A.tasks.load('cleanFormFunctionality'); 
    const taskDetailsWindow = await $A.tasks.load('taskDetails');
    const enableEditFunctionality = await $A.tasks.load('editTaskForm');
    
    cleanForm();    // load form clean functionality..
    enableEditFunctionality();  // we must now add edit functionality.
        
    // Allow opening of task-modals from url:
    $A.router.create(
        'task_id', 
        'taskDetailsModalResponse', 
        'taskDetailsModal', 
        taskDetailsWindow
    );
});
