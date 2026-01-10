import { makeElement } from "../../core/js/helper_mapper.js";
import { escapeHtml } from "../../core/js/helper_forms.js";
import { watcherPost } from "./crud.js";
import { prefillEditForm } from './form_handling.js';
import { addListenersToTasks } from "./dashboardSettings.js";

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
    function formatValue(v) {
        if (v === null || v === undefined) return '';
        if (typeof v === 'object') {
            try {
                return JSON.stringify(v, null, 2);
            } catch (e) {
                return String(v);
            }
        }
        return String(v);
    }

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

    // add edit button
    let editBtn = document.getElementById('taskEditBtn');
    editBtn.addEventListener('click', () => {
        prefillEditForm(resultSet);
    });

    // add (un)watcher button(s)
    let watchbtn = document.getElementById('addWatcher');
    let unwatchbtn = document.getElementById('removeWatcher');
    watchbtn.addEventListener('click', (e) => {
        e.preventDefault();
        watcherPost('add', watchbtn, unwatchbtn);
    });
    unwatchbtn.addEventListener('click', (e) => {
        e.preventDefault();
        watcherPost('remove', watchbtn, unwatchbtn);
    });
}

/**
 * @todo: make appropriate mapper for task-list fetched.
 */
export function displayFetchedTaskList(resultSet, containerId) {
    const container = containers[tabName];
    if (Array.isArray(data)) {
        const ul = document.createElement('ul');
        ul.className = 'list-group';
        data.forEach(item => {
            const li = document.createElement('li');
            li.className = 'list-group-item';
            let desc = item.description || JSON.stringify(item);
            let meta = item.status ? '<div class="text-muted small">' + escapeHtml(item.status) + '</div>' : '';
            let more = ''
            let details = ''
            if (tabName == 'private') {
                    more = '<a class="btn position-absolute top-0 end-0 m-3" data-bs-toggle="collapse" href="#collapseExample-' + escapeHtml(item.id) + '" role="button" aria-expanded="false" aria-controls="collapseExample-' + escapeHtml(item.id) + '"><i class="bi bi-info-circle"></i></a>'
                    details = '<div class="collapse" id="collapseExample-' + escapeHtml(item.id) + '"><div class="card card-body">' + escapeHtml(item.details) + '</div></div>'
            }
            li.innerHTML = '<div class="position-relative"><a class="link task-details-link" data-task-id="'+ escapeHtml(item.id) +'" role="button" data-bs-toggle="modal" data-bs-target="#taskDetailsModal">' + escapeHtml(String(desc)) + '</a>' + meta + more + details + '</div>';
            ul.appendChild(li);
        });
        container.innerHTML = '';
        container.appendChild(ul);
        if(typeof callbackFunction === 'function'){
            callbackFunction(container);
        }

        addListenersToTasks(container);
    } else {
        container.innerHTML = '<pre>' + escapeHtml(JSON.stringify(data, null, 2)) + '</pre>';
    }
}

/**
 * @todo: make appropriate mapper for todo-list fetched.
 */
export function displayFetchedTodoList(resultSet, containerId) {
    let container = document.getElementById(containerId); // should be the ul parent node.
    let originalLiItem = document.querySelector('#' + containerId + ' li.list-group-item');
    container.innerHTML = '';
    let li = null;
    if (Array.isArray(data)) {
        data.forEach(item => {
            li = originalLiItem.cloneNode(true);
            let status = li.querySelector('.status').querySelector('.' + item.status);

            if (status instanceof HTMLElement) {
                status.classList.remove('d-none');
            }
            li.querySelector('.description').textContent = item.description || JSON.stringify(item);
            container.appendChild(li);
        });
    } else {
        originalLiItem.innerHTML = '<pre>' + escapeHtml(JSON.stringify(data, null, 2)) + '</pre>';
        container.appendChild(originalLiItem);
    }
}

/**
 * Generic mapper - might be used to catch error messages, etc...
 * Maps error/success messages to elements in dom. 
 * May be used by Fetcher() in forms for rest/tasks/crud/.
 */
export const editFormResponseMapper = {
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