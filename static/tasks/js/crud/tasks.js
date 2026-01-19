import { Fetcher, defineRequest } from "../../../core/js/lib/async.js";
import { TasksO2OKeys } from "../constants.js";
import helper from "../helper.js";

/**
 * Allows submitted form to update existing record.
 * @param {str} formId: dom element id attr value for form 
 */
export function UpdateTask(formId) {
    let dictionary = helper.tasks.forms.generateDictionaryFromForm(formId, TasksO2OKeys);

    let request = defineRequest('/rest/tasks/crud/0/', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dictionary),
    });

    Fetcher(request, 'taskEditModalResponse', helper.tasks.load('genericRecordDetails'));
}

/**
 * Allows submitted form to create existing record.
 * @param {str} formId: dom element id attr value for form 
 */
export function CreateTask(formId) {
    let dictionary = helper.tasks.forms.generateDictionaryFromForm(formId, TasksO2OKeys);

    let request = defineRequest('/rest/tasks/crud/0/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dictionary),
    });

    Fetcher(request, 'taskEditModalResponse', helper.tasks.load('genericRecordDetails'));
}

/**
 * Allows submitted form to update existing record.
 * @param {str} formId: dom element id attr value for form 
 */
export function DeleteTask(taskId, identifyer) {
    if (!helper.forms.confirmDeletion(identifyer)) {
        return null;
    }
    //const id = document.querySelector('#taskDetailsModal #tid');

    let request = defineRequest('/rest/tasks/crud/' + taskId + '/', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    Fetcher(request, 'taskDetailsModalResponse', helper.tasks.load('genericRecordDetails'));
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

    Fetcher(request, 'personalTabResponse', helper.tasks.load('genericRecordDetails'));

}

/**
 * Deletes a Todo based on id provided.
 * @param {int} todoId: database ID for task to delete
 * @param {string} identifyer: any term to identify the ToDo to user during confirmation. 
 */
export function deleteTodo(todoId, identifyer) {
    if (!helper.forms.confirmDeletion(identifyer)) {
        return null;
    }

    let request = defineRequest('/rest/tasks/crud/' + todoId + '/', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    Fetcher(request, 'personalTabResponse', helper.tasks.load('genericRecordDetails'));
}
