import { Fetcher, defineRequest } from "../../core/js/async.js";
import { isVariableEmpty } from "../../core/js/helper_generic.js";
import { updateUrlParam } from "../../core/js/modal_linking.js";
import { createWatcher, removeWatcher, DeleteTask, createCommentForTask } from "./crud.js";
import { prefillEditForm } from './form_handling.js';
import { Editor } from '../../core/js/editor.js';
import { taskDetailsMapper, commentsMapper } from './mappers.js';

/**
 * A place to define various listeners that don't belong anywhere else...
 */

/**
 * Adds all the fancy buttons and widgets on the task-details modal.
 */
export function addOptionsFunctionalityOnTaskDetailsPane(resultSet) {
    // add edit button
    let editBtn = document.getElementById('editTaskBtn');
    editBtn.addEventListener('click', () => {
        prefillEditForm(resultSet);
    });

    // add delete button functionality
    const deleteBtn = document.getElementById('deleteTaskBtn');
    deleteBtn.addEventListener('click', (e) => {
        e.preventDefault();
        DeleteTask(resultSet['tid']);
    });

    // add (un)watcher button(s)
    let watchbtn = document.getElementById('addWatcher');
    let unwatchbtn = document.getElementById('removeWatcher');
    
    const wtchrRequest = defineRequest('/rest/tasks/watch/' + resultSet['tid'] + '/');
    Fetcher(wtchrRequest, 
        'taskDetailsModalResponse', {}, (data, id) => {
            if (isVariableEmpty(data)) {
                watchbtn.classList.remove('d-none');
            } else {
                unwatchbtn.classList.remove('d-none');
            }
        }
    );

    watchbtn.addEventListener('click', (e) => {
        e.preventDefault();
        createWatcher(resultSet['tid'], 'addWatcher', 'removeWatcher');
    });
    unwatchbtn.addEventListener('click', (e) => {
        e.preventDefault();
        removeWatcher(resultSet['tid'], 'addWatcher', 'removeWatcher');
    });

    // next, implement rich-text editor and comments form.
    Editor('commentEditor');
    let saveCommentBtn = document.getElementById('saveComment');
    saveCommentBtn.addEventListener('click', (e) => {
        e.preventDefault();
        let editor = document.querySelector('#newCommentForm #commentEditor');
        let hiddenCommentInput = document.querySelector('#newCommentForm #' + editor.dataset.fieldId);
        hiddenCommentInput.value = editor.innerHTML;
        let taskIdField = document.querySelector('#newCommentForm #task_id');
        taskIdField.value = resultSet['tid'];
        createCommentForTask('newCommentForm');
    });

    // finally, retrieve task-level-comments..
    let request = defineRequest('/rest/tasks/comments/?task_id=' + resultSet['tid']);
    Fetcher(request, "commentsResponse", {}, commentsMapper);
}

/**
 * Callback function. Adds read functionality to each fetched task.
 * This is a callback that adds event listeners to the fetched tasks, allowing
 * for Task Details Modal to become operational on them.
 * @param {domelement} container - passed by TabbedDashBoard()
 */
export function addListenersToTasks(container){
    if(container instanceof HTMLElement){
        // implment listener and fetcher for item details modal...
        let tasks = container.querySelectorAll('.task-details-link');
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
