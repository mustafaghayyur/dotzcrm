import { defineRequest } from "../../core/js/async";
import { displayFetchedTodoList } from "./mappers.js";
import { Fetcher, defineRequest } from "../../core/js/async.js";
import { updateUrlParam } from "../../core/js/modal_linking.js";

/**
 * Defines callback functions to be used by the TabbedDashBoard().
 * Note Tasks' TabbedDashBoard() call has singlecall enabled, meaning the data will not be refreshed, while
 * switching between tabs, as long as the page has not been refreshed.
 */
export const tasksCallbacks = {
    // this call evokes all panels defined under the 'Personal' tab of the tasks dashboard
    personal: () => {
        let request = null;
        request = defineRequest('/rest/tasks/private', { credentials: 'same-origin' });
        Fetcher(request, 'privateTabResponses', {}, displayFetchedTodoList);

        //request = defineRequest('/rest/tasks/workspaces', { credentials: 'same-origin' });
        //Fetcher(request, 'workspacesTabResponses', {}, displayFetchedTaskList);
    },

    // this call evokes all minimum panels defined under the 'Workspaces' tab of tasks dashboard
    workspaces: () => {

    },
};

/**
 * Callback function. Adds read functionality to each fetched task.
 * This is a callback that adds event listeners to the fetched tasks, allowing
 * for Task Details Modal to become operational on them.
 * @param {domelement} container - passed by TabbedDashBoard()
 */
export function addListenersToTasks(container){
    if(container instanceof HTMLElement){
        // implment listener and fetcher for item details modal...
        let tasks = container.querySelectorAll('.task-details-link');
        tasks.forEach(task => {
            let id = task.dataset.taskId;
            let request = defineRequest('/rest/tasks/crud/' + id);
            task.addEventListener('click', ()=>{
                Fetcher(request, 'taskDetailsModalResponse', {}, taskDetailsMapper);
                updateUrlParam('task_id', id);
            });
        });
    }
}