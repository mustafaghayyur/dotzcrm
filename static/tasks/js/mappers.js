import { makeElement, formatValue } from "../../core/js/helper_mapper.js";
import { escapeHtml } from "../../core/js/helper_forms.js";
import { convertToDisplayLocal } from '../../core/js/helper_dates.js';
import { toggleTodoStatus, deleteTodo } from './crud.js';
import { addListenersToTasks, addOptionsFunctionalityOnTaskDetailsPane } from './listeners.js';

/**
 * This file will hold various mappers our JS libraries may need to operate with data 
 */

// Keys we expect in the resultSet (keeps defined order)
export const keys = [
    'id','tid','did','lid','sid','aid','vid','description','details','status','visibility','deadline',
    'creator_id','parent_id','assignor_id','assignee_id','dlatest','llatest','slatest','alatest','vlatest',
    'tcreate_time','dcreate_time','lcreate_time','screate_time','acreate_time','vcreate_time',
    'tdelete_time','ddelete_time','ldelete_time','sdelete_time','adelete_time','vdelete_time','tupdate_time'
];

/**
 * This mapper function only finds dom elements matching items in the 'keys' list, if resultSet has the key
 * as well, then subs the resultSet[key] into the HTML of the matching dom elememnt.
 * 
 * containerId is irrelevent in this mapper. This is a callback function passed to Fetcher()
 * 
 * @param {object} resultSet - retrieved from Fetcher() internal function fetchResource()
 * @param {string} containerId - html id for DOM element in which this mapper's rendered HTML will be plugged into
 */
export function taskDetailsMapper(resultSet, containerId) {
    keys.forEach(key => {
        let fieldDomElement = document.getElementById(key);

        if (fieldDomElement instanceof HTMLElement) {
            let recordItm = resultSet && Object.prototype.hasOwnProperty.call(resultSet, key) ? resultSet[key] : undefined;
            let rec = formatValue(recordItm);

            if (rec && (rec.startsWith('{') || rec.startsWith('['))) {
                let pre = document.createElement('pre');
                pre.style.margin = 0;
                pre.textContent = escapeHtml(rec);
                fieldDomElement.appendChild(pre);
            } else {
                fieldDomElement.textContent = escapeHtml(rec);
            }
        }
    });
    addOptionsFunctionalityOnTaskDetailsPane(resultSet);
}

/**
 * Callback function for Fetcher() that maps retieved user's tasks to page elements.
 * @param {obj} data: results object from Fetcher call
 * @param {str} containerId: Id of the container to show any error messages.
 */
export function fetchedTaskListMapper(data, containerId) {
    const ulId = containerId.replace(/Response$/,'List');
    let ul = document.getElementById(ulId); // should be the ul parent node.
    let originalLiItem = ul.querySelector('li.list-group-item');
    ul.innerHTML = '';
    let li = null;
    
    if (Array.isArray(data)) {
        data.forEach(item => {
            li = originalLiItem.cloneNode(true);
            li.querySelector('.description').dataset.taskId = escapeHtml(item.tid);
            li.querySelector('.description').textContent = item.description || JSON.stringify(item);
            li.querySelector('.status').textContent = escapeHtml(item.status);
            li.querySelector('.tupdate_time').textContent = convertToDisplayLocal(item.tupdate_time);
            li.querySelector('.deadline').textContent = convertToDisplayLocal(item.deadline);
            ul.appendChild(li);
        });

        addListenersToTasks(ul);
    } else {
        originalLiItem.innerHTML = '<pre>' + escapeHtml(JSON.stringify(data, null, 2)) + '</pre>';
        container.appendChild(originalLiItem);
    }
}

/**
 * Callback function for Fetcher() that maps fetched ToDos to page elemments.
 * @param {obj} data: results object from Fetcher call
 * @param {str} containerId: Id of the container to show any error messages.
 */
export function fetchedTodoListMapper(data, containerId) {
    // I want to take the value held in containerId, and replace 'Responses' with List to get the ul id.
    const ulId = containerId.replace(/Response$/,'List');
    let ul = document.getElementById(ulId); // should be the ul parent node.
    let originalLiItem = ul.querySelector('li.list-group-item');
    ul.innerHTML = '';
    let li = null;

    if (Array.isArray(data)) {
        data.forEach(item => {
            li = originalLiItem.cloneNode(true);
            let status = li.querySelector('.status').querySelector('.' + item.status);
            let desc = li.querySelector('.description');
            desc.dataset.taskId = escapeHtml(item.tid);
            desc.textContent = item.description || JSON.stringify(item);
            
            if (item.status === 'completed') {
                desc.classList.add('text-decoration-line-through');
            }
            if (status instanceof HTMLElement) {
                status.classList.remove('d-none');
            }
            
            li.querySelector('.status').addEventListener('click', () => { toggleTodoStatus(item); });
            li.querySelector('.delete').addEventListener('click', () => { deleteTodo(item.tid, item.description); });

            ul.appendChild(li);
        });
    } else {
        originalLiItem.innerHTML = '<pre>' + escapeHtml(JSON.stringify(data, null, 2)) + '</pre>';
        container.appendChild(originalLiItem);
    }
}

export function commentsMapper(data, containerId) {
    let parentId = containerId.replace(/Response$/,'');
    let container = document.getElementById(parentId);
    let commentCreator = container.querySelector('#createComment');
    let comment = container.querySelector('#commmentContainer');
    container.innerHTML = '';
    container.appendChild(commentCreator);

    if (Array.isArray(data)) {
        let newComment = null;
        data.forEach(item => {
            newComment = comment.cloneNode(true);    
            newComment.classList.remove('d-none');

            newComment.querySelector('.creator_id').textContent = '' + item.creator_user_id + 'wrote...';
            newComment.querySelector('.create_time').textContent = convertToDisplayLocal(item.create_time);
            newComment.querySelector('.update_time').textContent = convertToDisplayLocal(item.update_time);
            newComment.querySelector('.comment_text').innerHTML = item.comment;

            container.appendChild(newComment);
        });
    }
        
}

/**
 * Generic mapper - might be used to catch error messages, etc...
 * Maps error/success messages to elements in dom. 
 * May be used by Fetcher() in forms for rest/tasks/crud/.
 */
export const genericTaskResponseMapper = {
    description: makeElement('span', 'rec-itm'), 
    status: makeElement('span', 'rec-itm'), 
    visibility: makeElement('span', 'rec-itm'),
    aid: makeElement('span', 'rec-itm'),
    assignee_id: makeElement('span', 'rec-itm'),
    assignor_id: makeElement('span', 'rec-itm'),
    csrfmiddlewaretoken: makeElement('span', 'rec-itm'),
    deadline: makeElement('span', 'rec-itm'),
    description: makeElement('span', 'rec-itm'),
    details: makeElement('span', 'rec-itm'),
    did: makeElement('span', 'rec-itm'),
    lid: makeElement('span', 'rec-itm'),
    parent_id: makeElement('span', 'rec-itm'),
    sid: makeElement('span', 'rec-itm'),
    status: makeElement('span', 'rec-itm'),
    tid: makeElement('span', 'rec-itm'),
    vid: makeElement('span', 'rec-itm'),
    visibility: makeElement('span', 'rec-itm'),
    error: makeElement('span', 'rec-itm'),
    errors: makeElement('span', 'rec-itm'),
    message: makeElement('span', 'rec-itm'),
    messages: makeElement('span', 'rec-itm'),
};