import $A from "../helper.js";

const callback = await $A.tasks.load('genericRecordDetails');
const TasksO2OKeys = $A.tasks.data['TasksO2OKeys'];

/**
 * Allows submitted form to update existing record.
 * @param {str} formId: dom element id attr value for form 
 */
export function UpdateTask(formId) {
    let dictionary = $A.tasks.forms.generateDictionaryFromForm(formId, TasksO2OKeys);
    
    $A.fetch.body(
        $A.fetch.route('api.tasks.crud', '0', {
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
    let dictionary = $A.tasks.forms.generateDictionaryFromForm(formId, TasksO2OKeys);
    
    $A.fetch.body(
        $A.fetch.route('api.tasks.crud', '0', {
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
    if (!$A.forms.confirmDeletion(identifyer)) {
        return null;
    }

    const request = $A.fetch.route('api.tasks.crud', String(taskId), {
        method: 'DELETE',
    });

    $A.fetch.body(request, 'taskDetailsModalResponse', callback);
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
        tata_id: record.tata_id,
        tast_id: record.tast_id,
        status: newStatus
    };

    let request = $A.fetch.route('api.tasks.crud', '0', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dictionary),
    });

    $A.fetch.body(request, 'personalTabResponse', callback);

}

/**
 * Deletes a Todo based on id provided.
 * @param {int} todoId: database ID for task to delete
 * @param {string} identifyer: any term to identify the ToDo to user during confirmation. 
 */
export function deleteTodo(todoId, identifyer) {
    if (!$A.forms.confirmDeletion(identifyer)) {
        return null;
    }

    let request = $A.fetch.route('api.tasks.crud', String(todoId), {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    $A.fetch.body(request, 'personalTabResponse', callback);
}
