/**
 * This file holds custom JS to implement Bootstrap into Dotz CRM + PM
 */
import { TabbedDashBoard } from "./dashboard.js";
import { Fetcher, defineRequest } from "../../core/js/async.js";
import { taskDetailsMapper } from "./mappers.js";
import { UpdateTask, CreateTask, DeleteTask, cleanTaskForm } from './crud.js';
import { showModal, updateUrlParam } from "../../core/js/modal_linking.js";
//import { Editor } from "../../core/js/editor.js";

document.addEventListener('DOMContentLoaded', () => {
    
    TabbedDashBoard(addListenersToTasks); // implment dashboard on index.html
    //Editor('#newTaskTextBox');

    // Allow opening of task-modals from url:
    showModal('task_id', 'taskDetailsModalResponse', 'taskDetailsModal', taskDetailsMapper);

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
                Fetcher(request, 'taskDetailsModalResponse', {}, taskDetailsMapper);
                updateUrlParam('task_id', id);
            });
        });
    }
}

