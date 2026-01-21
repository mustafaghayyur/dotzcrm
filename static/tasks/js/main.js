import helper from './helper.js';
import { Main } from '../../core/js/lib/app.js';

/**
 * Begin Tasks Application
 */
Main(async () => {
    helper.dashboard({
        // 'Personal' tab of the tasks dashboard:
        personal: async () => {
            let request = null;
            const dashboardTodoList = await helper.tasks.load('dashboardTodoList');
            const dashboardTaskList = await helper.tasks.load('dashboardTaskList');

            request = helper.fetch.route('api.tasks.list', 'private');
            helper.fetch.body(request, 'personalTabResponse', {}, dashboardTodoList);

            request = helper.fetch.route('api.tasks.list', 'workspaces');
            helper.fetch.body(request, 'workspacesTabResponse', {}, dashboardTaskList);
        },
        // 'Workspaces' tab of tasks dashboard:
        workspaces: () => {},
    }, true);

    const cleanForm = await helper.tasks.load('cleanFormFunctionality'); 
    const taskDetailsWindow = await helper.tasks.load('taskDetails');

    cleanForm();    // load form clean functionality..
    
    // Allow opening of task-modals from url:
    helper.router.create(
        'task_id', 
        'taskDetailsModalResponse', 
        'taskDetailsModal', 
        taskDetailsWindow
    );
});
