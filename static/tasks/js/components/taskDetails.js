import { makeDomElement, formatValueToString, getter } from "../../../core/js/helpers/generic.js";
import { escapeHtml } from "../helpers/forms.js";
import { TasksO2OKeys } from "./constants.js";

/**
 * This mapper function only finds dom elements matching items in the 'TasksO2OKeys' list, if resultSet has the key
 * as well, then subs the resultSet[key] into the HTML of the matching dom elememnt.
 * 
 * containerId is irrelevent in this mapper. This is a callback function passed to Fetcher()
 * 
 * @param {object} resultSet - retrieved from Fetcher() internal function fetchResource()
 * @param {string} containerId - html id for DOM element in which this mapper's rendered HTML will be plugged into
 */
export function taskDetailsMapper(resultSet, containerId) {
    TasksO2OKeys.forEach(key => {
        let fieldContainer = document.getElementById(key);

        if (fieldContainer instanceof HTMLElement) {
            let data = getter(resultSet, key, undefined);
            let item = formatValueToString(data);

            if (item && (item.startsWith('{') || item.startsWith('['))) {
                let pre = makeDomElement('pre', 'm-1');
                pre.textContent = escapeHtml(item);
                fieldContainer.appendChild(pre);
                return;
            }
            fieldContainer.textContent = escapeHtml(item);
        }
    });
    addOptionsFunctionalityOnTaskDetailsPane(resultSet);


    /**
     * Adds all the fancy buttons and widgets on the task-details modal.
     */
    function addOptionsFunctionalityOnTaskDetailsPane(resultSet) {
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

}
