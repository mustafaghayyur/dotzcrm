import { Fetcher, defineRequest } from "../../core/js/async.js";
import { keys, genericTaskResponseMapper } from "./mappers.js";
import { confirmDeletion } from "../../core/js/helper_generic.js";
import { generateDictionaryFromForm } from './form_handling.js';

/**
 * Allows submitted form to update existing record.
 * @param {str} formId: dom element id attr value for form 
 */
export function UpdateTask(formId) {
    let dictionary = generateDictionaryFromForm(formId, keys);

    let request = defineRequest('/rest/tasks/crud/0/', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dictionary),
    });

    Fetcher(request, 'taskEditModalResponse', genericTaskResponseMapper);
}

/**
 * Allows submitted form to create existing record.
 * @param {str} formId: dom element id attr value for form 
 */
export function CreateTask(formId) {
    let dictionary = generateDictionaryFromForm(formId, keys);

    let request = defineRequest('/rest/tasks/crud/0/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dictionary),
    });

    Fetcher(request, 'taskEditModalResponse', genericTaskResponseMapper);
}

/**
 * Allows submitted form to update existing record.
 * @param {str} formId: dom element id attr value for form 
 */
export function DeleteTask(taskId, identifyer) {
    if (!confirmDeletion(identifyer)) {
        return null;
    }
    //const id = document.querySelector('#taskDetailsModal #tid');

    let request = defineRequest('/rest/tasks/crud/' + taskId + '/', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    Fetcher(request, 'taskDetailsModalResponse', genericTaskResponseMapper);
}

/**
 * Creates a new record in the back-end for current user as watcher of supplied task id.
 * @param {int} taskId: database ID for task in question
 * @param {str} watchBtnId: html dom element id attr value
 * @param {str} unwatchBtnId: html dom element id attr value
 */
export function createWatcher(taskId, watchBtnId, unwatchBtnId){    
    let watchbtn = document.getElementById(watchBtnId);
    let unwatchbtn = document.getElementById(unwatchBtnId);

    const dictionary = {
        task_id: taskId
    };
    const params = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    };

    const request = defineRequest('/rest/tasks/watch/' + taskId + '/', params);
    Fetcher(request, 
        'taskDetailsModalResponse', {}, 
        () => {
            watchbtn.classList.add('d-none');
            unwatchbtn.classList.remove('d-none');
        }
    );
}

/**
 * Removes existing record in the back-end for current user as watcher of supplied task id.
 * @param {int} taskId: database ID for task in question
 * @param {str} watchBtnId: html dom element id attr value
 * @param {str} unwatchBtnId: html dom element id attr value
 */
export function removeWatcher(taskId, watchBtnId, unwatchBtnId){
    let watchbtn = document.getElementById(watchBtnId);
    let unwatchbtn = document.getElementById(unwatchBtnId);

    const params = {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        }
    };

    const request = defineRequest('/rest/tasks/watch/' + taskId + '/', params);
    Fetcher(
        request, 
        'taskDetailsModalResponse', {}, 
        () => {
            watchbtn.classList.remove('d-none');
            unwatchbtn.classList.add('d-none');
        }
    );
}

/**
 * Changes ToDo item's status between 'queued' and 'completed'
 * @param {str} todoId: database ID for task record.
 * @param {str} oldStatus: the status to remove
 */
export function toggleTodoStatus(record) {
    const allStatuses = 'queuedcompleted'; // @todo: find a better determining operation ... no pun intended.
    const newStatus = allStatuses.replace(record.status, '');

    const dictionary = {
        tid: record.tid,
        sid: record.sid,
        status: newStatus
    };

    let request = defineRequest('/rest/tasks/crud/0/', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dictionary),
    });

    Fetcher(request, 'personalTabResponse', genericTaskResponseMapper);

}

/**
 * Deletes a Todo based on id provided.
 * @param {int} todoId: database ID for task to delete
 * @param {string} identifyer: any term to identify the ToDo to user during confirmation. 
 */
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

    Fetcher(request, 'personalTabResponse', genericTaskResponseMapper);
}

/**
 * Allows for adding new comments.
 * @param {str} action: enum ['add']
 * @param {str} formId: html dom id attribute value for entire form.
 */
export function createCommentForTask(formId) {
    let dictionary = generateDictionaryFromForm(formId);

    let request = defineRequest('/rest/tasks/comment/0/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dictionary),
    });

    Fetcher(request, 'commentsResponse', genericTaskResponseMapper);
}
