/**
 * This file holds custom JS to implement Bootstrap into Dotz CRM + PM
 */
import { TabbedDashBoard } from "./dashboard.js";
import { Fetcher, defineRequest } from "../../core/js/async.js";
import { taskDetailsMapper, keys, editFormResponseMapper } from "./mappers.js";
import { validate } from './validate.js';

// implment dashboard on index.html
document.addEventListener(
    'DOMContentLoaded', 
    TabbedDashBoard(addListenersToTasks)
);

/**
 * This is a callback that adds event listeners to the fetched tasks, allowing
 * for Task Details Modal to become operational on them.
 * @param {domelement} container - passed by TabbedDashBoard()
 */
function addListenersToTasks(container){
    if(container instanceof HTMLElement){
        // implment listener and fetcher for item details modal...
        let tasks = document.querySelectorAll('.task-details-link');
        tasks.forEach(task => {
            let id = task.dataset.taskId;
            let request = defineRequest('/rest/tasks/crud/' + id);
            task.addEventListener('click', ()=>{
                Fetcher(request, 'taskDetailsModalResponse', {}, taskDetailsMapper)
            });
        });
    }
}

const form = document.querySelector('#taskEditForm'); // Get the form element

if (!(form instanceof HTMLElement)) {
    console.log('Error: form could not be found. Cannot pre-populate.', form);
}

form.addEventListener('submit', (event) => {
    event.preventDefault();
    let dictionary = {};

    const formData = new FormData(form);
    const formObject = Object.fromEntries(formData.entries());
    console.log('Form Data:', formObject);

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
});

