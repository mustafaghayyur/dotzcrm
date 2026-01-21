import helper from "../helper.js";

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

    const request = helper.fetch.route('api.tasks.watchers_crud', String(taskId), params);
    helper.fetch.body(request, 
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

    const request = helper.fetch.route('api.tasks.watchers_crud', String(taskId), params);
    helper.fetch.body(
        request, 
        'taskDetailsModalResponse', {}, 
        () => {
            watchbtn.classList.remove('d-none');
            unwatchbtn.classList.add('d-none');
        }
    );
}

