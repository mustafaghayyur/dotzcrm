import { displayFetchedTodoList, displayFetchedTaskList } from "./mappers.js";
import { Fetcher, defineRequest } from "../../core/js/async.js";
import { updateUrlParam } from "../../core/js/modal_linking.js";
import { taskDetailsMapper } from "./mappers.js";
import { confirmDeletion } from "../../core/js/helper_generic.js";
import { genericTaskResponseMapper } from "./mappers.js";

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
        Fetcher(request, 'personalTabResponses', {}, displayFetchedTodoList);

        request = defineRequest('/rest/tasks/workspaces', { credentials: 'same-origin' });
        Fetcher(request, 'workspacesTabResponses', {}, displayFetchedTaskList);
    },

    // this call evokes all minimum panels defined under the 'Workspaces' tab of tasks dashboard
    workspaces: () => {

    },
};

export function toggleTodoStatus(todoId, oldStatus) {
    const allStatuses = 'queuedcompleted';
    const newStatus = allStatuses.replace(oldStatus, '');

    const dictionary = {
        tid: todoId,
        status: newStatus
    };

    let request = defineRequest('/rest/tasks/crud/0/', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dictionary),
    });

    Fetcher(request, 'taskEditModalResponse', genericTaskResponseMapper);

}

export function deleteTodo(todoId, identifyer) {
    if (!confirmDeletion(identifyer)) {
        return null;
    }

    let request = defineRequest('/rest/tasks/crud/' + todoId + '/', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    Fetcher(request, 'personalTabResponses', genericTaskResponseMapper);
}

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