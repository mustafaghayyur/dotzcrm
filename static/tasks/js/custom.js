import { TabbedDashBoard } from "../../core/js/dashboard.js";
import { taskDetailsMapper } from "./mappers.js";
import { tasksCallbacks } from "./dashboardSettings.js";
import { UpdateTask, CreateTask, DeleteTask, cleanTaskForm } from './crud.js';
import { showModal } from "../../core/js/modal_linking.js";
//import { Editor } from "../../core/js/editor.js";

/**
 * This file holds custom JS to implement UI on Tasks Module
 */

document.addEventListener('DOMContentLoaded', () => {
    TabbedDashBoard(tasksCallbacks, true); // implment dashboard on index.html
    
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

