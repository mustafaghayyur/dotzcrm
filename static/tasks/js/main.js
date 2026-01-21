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

            request = $A.fetch.route('api.tasks.list', 'workspaces');
            $A.fetch.body(request, 'workspacesTabResponse', {}, dashboardTaskList);
        },
        // 'Workspaces' tab of tasks dashboard:
        workspaces: () => {},
    }, true);

    const cleanForm = await $A.tasks.load('cleanFormFunctionality'); 
    const taskDetailsWindow = await $A.tasks.load('taskDetails');

    cleanForm();    // load form clean functionality..
    
    // Allow opening of task-modals from url:
    $A.router.create(
        'task_id', 
        'taskDetailsModalResponse', 
        'taskDetailsModal', 
        taskDetailsWindow
    );
});
