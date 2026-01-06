import { Fetcher, defineRequest } from "../../core/js/async.js";
import { keys, editFormResponseMapper } from "./mappers.js";
import { validate } from './validate.js';

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

export function cleanCreateTaskForm(form) {
    
    keys.forEach(key => {
        const field = document.querySelector('#taskEditForm input[name="'+key+'"]');
        if (!(field instanceof HTMLElement)){
            return;  // return only the foreach loop...
        }
        console.log('Cleaning field name = ', field);
        field.value = '';
    });

}
