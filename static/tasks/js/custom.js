/**
 * This file holds custom JS to implement Bootstrap into Dotz CRM + PM
 */
import { TabbedDashBoard } from "./dashboard.js";
import { Fetcher, defineRequest } from "../../core/js/async.js";
import { taskDetailsMapper } from "./mappers.js";
import { UpdateTask, CreateTask, DeleteTask, cleanTaskForm } from './crud.js';

// implment dashboard on index.html
document.addEventListener(
    'DOMContentLoaded', 
    TabbedDashBoard(addListenersToTasks)
);

watchbtn = document.getElementById('addWatcher');
unwatchbtn = document.getElementById('removeWatcher');

watchbtn.addEventListener('click', (e) => {
    e.preventDefault();
    const tid = document.getElementById('tid').innerText;
    let dictionary = {task_id: tid, watcher_id: 'me'};
    const request = defineRequest('/rest/tasks/watch/' + tid, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dictionary),
    });
    Fetcher(request, 'watchTaskResponse', {}, () => {
        watchbtn.classList.add('d-none');
        unwatchbtn.classList.remove('d-none');
    });
});

unwatchbtn.addEventListener('click', (e) => {
    e.preventDefault();
    const tid = document.getElementById('tid').innerText;
    let dictionary = { wid: tid };
    const request = defineRequest('/rest/tasks/watch/' + tid, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dictionary),
    });
    Fetcher(request, 'watchTaskResponse', {}, () => {
        unwatchbtn.classList.add('d-none');
        watchbtn.classList.remove('d-none');
    });
});

/**
 * CRUD Operations Setup...
 */
const form = document.querySelector('#taskEditForm'); // Get the form element
if (!(form instanceof HTMLElement)) {
    console.log('Error: form could not be found. Cannot pre-populate.', form);
}

form.addEventListener('submit', (e) => {
    e.preventDefault();
    const tid = document.querySelector('#taskEditForm input[name="tid"]');
    if (!(tid instanceof HTMLElement)) {
        throw Error('Cannot find `tid` field, unable to perform edit/create operation.');
    }
    if(tid.value){
        UpdateTask(form);
    }else{
        CreateTask(form);
    }
});

const deleteBtn = document.getElementById('deleteTaskBtn');
deleteBtn.addEventListener('click', (e) => {
    e.preventDefault();
    DeleteTask();
});

const openFormBtn = document.querySelectorAll('.open-form');
openFormBtn.forEach(button => {
    button.addEventListener('click', () => {
        cleanTaskForm('#taskEditForm');
    });
});

/**
 * Callback function. Adds read functionality to each fetched task.
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
