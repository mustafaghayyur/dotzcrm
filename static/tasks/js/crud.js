import { Fetcher, defineRequest } from "../../core/js/async.js";
import { keys, editFormResponseMapper } from "./mappers.js";
import { validate } from './validate.js';
import { cleanForm } from "../../core/js/helper_forms.js";

export function UpdateTask(form) {
    let dictionary = {};

    const formData = new FormData(form);
    const formObject = Object.fromEntries(formData.entries());

    keys.forEach(key => {
        let val = formObject[key];

        if (!val) {
            dictionary[key] = validate(key, val);
        }
    });

    let request = defineRequest('/rest/tasks/crud/0/', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dictionary),
    });

    Fetcher(request, 'taskEditModalResponse', editFormResponseMapper);
}

export function CreateTask(form) {
    let dictionary = {};

    const formData = new FormData(form);
    const formObject = Object.fromEntries(formData.entries());

    keys.forEach(key => {
        let val = formObject[key];

        if (!val) {
            dictionary[key] = validate(key, val);
        }
    });

    let request = defineRequest('/rest/tasks/crud/0/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dictionary),
    });

    Fetcher(request, 'taskEditModalResponse', editFormResponseMapper);
}

export function DeleteTask() {
    const id = document.querySelector('#taskDetailsModal #tid');
    console.log('pickup id val: ', id);
    if (!(id instanceof HTMLElement)) {
        throw Error('Record ID for detletion not found.');
    }

    let request = defineRequest('/rest/tasks/crud/' + id.textContent + '/', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    Fetcher(request, 'taskDetailsModalResponse', editFormResponseMapper);
}

/**
 * Wrapper for clean function.
 * @param {string} formId: should be the while Id with the # selection 
 */
export function cleanTaskForm(formId) {
    cleanForm(formId, keys);
}

/**
 * Calls the appropriate api for watcher.
 * @param {string} action: enum ('add' | 'remove') 
 */
export function watcherPost(action, watchbtn, unwatchbtn){
    const tid = document.getElementById('tid').innerText;
    
    const dictionary = {
        add: {task_id: tid, watcher_id: 'me'},
        remove: { wid: tid }
    };
    const params = {
        add: {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dictionary.add),
        },
        remove: {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dictionary.remove),
        }
    };
    const callbacks = {
        add: () => {
            watchbtn.classList.add('d-none');
            unwatchbtn.classList.remove('d-none');
        },
        remove: () => {
            unwatchbtn.classList.add('d-none');
            watchbtn.classList.remove('d-none');
        }
    }
    const request = defineRequest('/rest/tasks/watch/' + tid, params[action]);
    Fetcher(request, 'watchTaskResponse', {}, callbacks[action]());
}