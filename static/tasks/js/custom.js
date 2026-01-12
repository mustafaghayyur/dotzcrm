import { Fetcher, defineRequest } from "../../core/js/async.js";
import { TabbedDashBoard } from "../../core/js/dashboard.js";
import { taskDetailsMapper, fetchedTodoListMapper, fetchedTaskListMapper } from "./mappers.js";
import { UpdateTask, CreateTask } from './crud.js';
import { cleanTaskForm } from './form_handling.js';
import { showModal } from "../../core/js/modal_linking.js";

/**
 * This file holds custom JS to implement UI on Tasks Module
 */

document.addEventListener('DOMContentLoaded', () => {
    
    // Tasks' TabbedDashBoard() call has singlecall enabled, 
    // data will not be refreshed, while switching between tabs
    TabbedDashBoard({
        // 'Personal' tab of the tasks dashboard:
        personal: () => {
            let request = null;
            request = defineRequest('/rest/tasks/private', { credentials: 'same-origin' });
            Fetcher(request, 'personalTabResponses', {}, fetchedTodoListMapper);

            request = defineRequest('/rest/tasks/workspaces', { credentials: 'same-origin' });
            Fetcher(request, 'workspacesTabResponses', {}, fetchedTaskListMapper);
        },
        // 'Workspaces' tab of tasks dashboard:
        workspaces: () => {},
    }, true);
    
    

    // Allow opening of task-modals from url:
    showModal(
        'task_id', 
        'taskDetailsModalResponse', 
        'taskDetailsModal', 
        taskDetailsMapper
    );

    // Edit Task Modal: Save Operations Setup...
    const editTaskSaveBtn = document.getElementById('taskEditFormSaveBtn');
    editTaskSaveBtn.addEventListener('click', (e) => {
        e.preventDefault();
        const tid = document.querySelector('#taskEditForm input[name="tid"]');
        if (!(tid instanceof HTMLElement)) {
            throw Error('Cannot find `tid` field, unable to perform edit/create operation.');
        }
        if(tid.value){
            UpdateTask('taskEditForm');
        }else{
            CreateTask('taskEditForm');
        }
    });

    // add 'clean form' functionality to all .open-form btns...
    const openFormBtn = document.querySelectorAll('.open-form');
    openFormBtn.forEach(button => {
        button.addEventListener('click', () => {
            cleanTaskForm('#taskEditForm');
        });
    });
});
