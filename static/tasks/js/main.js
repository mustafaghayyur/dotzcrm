import { Fetcher, defineRequest } from "../../core/js/lib/async.js";
import { TabbedDashBoard } from "../../core/js/lib/dashboard.js";
//import { showModal } from "../../core/js/lib/router.js";
import { Main } from '../../core/js/lib/app.js';
import helper from './helper.js';
import { TasksO2OKeys } from "./constants.js";

/**
 * Begin Tasks Application:
 */
Main(() => {

    // Tasks' TabbedDashBoard() call has singlecall enabled, 
    // data will not be refreshed, while switching between tabs
    TabbedDashBoard({
        // 'Personal' tab of the tasks dashboard:
        personal: () => {
            let request = null;
            request = defineRequest('api.tasks.list', 'private', { credentials: 'same-origin' });
            //const mod1 = );
            //console.log('checking loader: ', mod1);
            Fetcher(request, 'personalTabResponse', {}, helper.tasks.load('dashboardTodoList'));

            request = defineRequest('api.tasks.list', 'workspaces', { credentials: 'same-origin' });
            Fetcher(request, 'workspacesTabResponse', {}, helper.tasks.load('dashboardTaskList'));
        },
        // 'Workspaces' tab of tasks dashboard:
        workspaces: () => {},
    }, true);

    // Allow opening of task-modals from url:
    /**Routes.add('task_id').modal('taskDetailsModal').component(helper.tasks.load('taskDetails'));
    showModal(
        'task_id', 
        'taskDetailsModalResponse', 
        'taskDetailsModal', 
        taskDetailsMapper
    );*/

    // add 'clean form' functionality to all .open-form btns...
    const openFormBtn = document.querySelectorAll('.open-form');
    openFormBtn.forEach(button => {
        button.addEventListener('click', () => {
            helper.tasks.forms.cleanTaskForm('taskEditForm', TasksO2OKeys);
        });
    });
});
