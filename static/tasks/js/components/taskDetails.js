import { removeWatcher, createWatcher } from "../crud/watchers.js";
import { createCommentForTask } from "../crud/comments.js";
import { DeleteTask } from '../crud/tasks.js';
import $A from "../helper.js";

/**
 * This mapper function only finds dom elements matching items in the 'TasksO2OKeys' list, if resultSet has the key
 * as well, then subs the resultSet[key] into the HTML of the matching dom elememnt.
 * 
 * containerId is irrelevent in this mapper. This is a callback function passed to Fetcher()
 * 
 * @param {object} resultSet - retrieved from Fetcher() internal function fetchResource()
 * @param {string} containerId - html id for DOM element in which this mapper's rendered HTML will be plugged into
 */
export default function (resultSet, containerId) {
    const TasksO2OKeys = $A.tasks.data['TasksO2OKeys'];
    
    TasksO2OKeys.forEach(key => {
        let fieldContainer = document.getElementById(key);

        if (fieldContainer instanceof HTMLElement) {
            let data = $A.generic.getter(resultSet, key, undefined);
            let item = $A.generic.formatValueToString(data);

            if (item && (item.startsWith('{') || item.startsWith('['))) {
                let pre = $A.app.makeDomElement('pre', 'm-1');
                pre.textContent = $A.forms.escapeHtml(item);
                fieldContainer.appendChild(pre);
                return;
            }
            fieldContainer.textContent = $A.forms.escapeHtml(item);
        }
    });
    addOptionsFunctionalityOnTaskDetailsPane(resultSet);


    /**
     * Adds all the fancy buttons and widgets on the task-details modal.
     */
    async function addOptionsFunctionalityOnTaskDetailsPane(resultSet) {
        // add edit button
        let editBtn = document.getElementById('editTaskBtn');
        editBtn.addEventListener('click', () => {
            $A.tasks.forms.prefillEditForm(resultSet, TasksO2OKeys);
        });

        // add delete button functionality
        const deleteBtn = document.getElementById('deleteTaskBtn');
        deleteBtn.addEventListener('click', (e) => {
            e.preventDefault();
            DeleteTask(resultSet['tata_id']);
        });

        // add (un)watcher button(s)
        let watchbtn = document.getElementById('addWatcher');
        let unwatchbtn = document.getElementById('removeWatcher');
        
        $A.fetch.body(
            $A.fetch.route('api.tasks.watchers_crud', String(resultSet['tata_id'])), 
            'taskDetailsModalResponse', {}, 
            (data, id) => {
                if ($A.generic.isVariableEmpty(data)) {
                    watchbtn.classList.remove('d-none');
                    unwatchbtn.classList.add('d-none');
                } else {
                    unwatchbtn.classList.remove('d-none');
                    watchbtn.classList.add('d-none');
                }
            }
        );

        watchbtn.addEventListener('click', (e) => {
            e.preventDefault();
            createWatcher(resultSet['tata_id'], 'addWatcher', 'removeWatcher');
        });
        unwatchbtn.addEventListener('click', (e) => {
            e.preventDefault();
            removeWatcher(resultSet['tata_id'], 'addWatcher', 'removeWatcher');
        });

        // next, implement rich-text editor and comments form.
        $A.editor.make('commentEditor');
        let saveCommentBtn = document.getElementById('saveComment');
        saveCommentBtn.addEventListener('click', (e) => {
            e.preventDefault();
            let editor = document.querySelector('#newCommentForm #commentEditor');
            let hiddenCommentInput = document.querySelector('#newCommentForm #' + editor.dataset.fieldId);
            hiddenCommentInput.value = editor.innerHTML;
            let taskIdField = document.querySelector('#newCommentForm #task_id');
            taskIdField.value = resultSet['tata_id'];
            createCommentForTask('newCommentForm');
        });

        // finally, retrieve task-level-comments..
        const callback = await $A.tasks.load('commentsList');
        $A.fetch.body(
            $A.fetch.route('api.tasks.comments_list', String(resultSet['tata_id'])), 
            "commentsResponse", {}, 
            callback
        );
    }
}
