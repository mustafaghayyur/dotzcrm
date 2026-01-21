import helper from "../helper.js";

const callback = await helper.tasks.load('genericRecordDetails');
const TasksO2OKeys = helper.tasks.data['TasksO2OKeys'];

/**
 * Allows submitted form to update existing record.
 * @param {str} formId: dom element id attr value for form 
 */
export function UpdateTask(formId) {
    let dictionary = helper.tasks.forms.generateDictionaryFromForm(formId, TasksO2OKeys);
    
    helper.fetch.body(
        helper.fetch.route('api.tasks.crud', '0', {
            method: 'PUT',
            body: JSON.stringify(dictionary),
        }), 
        'taskEditModalResponse', callback
    );
}

/**
 * Allows submitted form to create existing record.
 * @param {str} formId: dom element id attr value for form 
 */
export function CreateTask(formId) {
    let dictionary = helper.tasks.forms.generateDictionaryFromForm(formId, TasksO2OKeys);
    
    helper.fetch.body(
        helper.fetch.route('api.tasks.crud', '0', {
            method: 'POST',
            body: JSON.stringify(dictionary),
        }), 
        'taskEditModalResponse', 
        callback
    );
}

/**
 * Allows submitted form to update existing record.
 * @param {str} formId: dom element id attr value for form 
 */
export function DeleteTask(taskId, identifyer) {
    if (!helper.forms.confirmDeletion(identifyer)) {
        return null;
    }

    const request = helper.fetch.route('api.tasks.crud', String(taskId), {
        method: 'DELETE',
    });

    helper.fetch.body(request, 'taskDetailsModalResponse', callback);
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

    let request = helper.fetch.route('api.tasks.crud', '0', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dictionary),
    });

    helper.fetch.body(request, 'personalTabResponse', callback);

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

    let request = helper.fetch.route('api.tasks.crud', String(todoId), {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    helper.fetch.body(request, 'personalTabResponse', callback);
}
