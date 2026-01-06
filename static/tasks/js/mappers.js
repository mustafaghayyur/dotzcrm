/**
 * This file will hold various mappers our JS libraries may need to operate with data 
 */
import { convertDateTimeToLocal } from "../../core/js/helper_dates.js";
import { makeElement } from "../../core/js/helper_mapper.js";

/**
 * This mapper function only finds dom elements matching items in the 'keys' list, if resultSet has the key
 * as well, then subs the resultSet[key] into the HTML of the matching dom elememnt.
 * 
 * containerId is irrelevent in this mapper. This is a callback function passed to Fetcher()
 * 
 * @param {object} resultSet - retrieved from Fetcher() internal function fetchResource()
 * @param {string} containerId - html id for DOM element in which this mapper's rendered HTML will be plugged into
 */

// Keys we expect in the resultSet (keeps defined order)
export const keys = [
    'id','tid','did','lid','sid','aid','vid','description','details','status','visibility','deadline',
    'creator_id','parent_id','assignor_id','assignee_id','dlatest','llatest','slatest','alatest','vlatest',
    'tcreate_time','dcreate_time','lcreate_time','screate_time','acreate_time','vcreate_time',
    'tdelete_time','ddelete_time','ldelete_time','sdelete_time','adelete_time','vdelete_time','tupdate_time'
];

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

    function escapeHtml(str) {
        return String(str).replace(/[&<>"]+/g, s => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[s]));
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

    let editBtn = document.getElementById('taskEditBtn');
    editBtn.addEventListener('click', () => {
        prefillEditForm(resultSet);
    });
}

/**
 * Not a mapper. A helper function.
 * This function simply pre-populates the Edit Task Form with record details, for which it was invoked.
 * @param {object} data: the data-object which will fill the form fields.
 */
function prefillEditForm(data){
    const form = document.querySelector('#taskEditForm'); // Get the form element

    if (!(form instanceof HTMLElement)) {
        console.log('Error: form could not be found. Cannot pre-populate.');
        return;
    }

    keys.forEach(key => {
        let value = data && Object.prototype.hasOwnProperty.call(data, key) ? data[key] : undefined;
        let field = form.elements.namedItem(key);

        if (!value || !field) {
            return; // @todo, should I have better handling here? What about missing values for fields?
        }

        // If the key ends with '_time' or contains 'deadline', convert to appropriate format first
        if (/(_time$)|deadline/.test(key)) {
            field.value = convertDateTimeToLocal(value);
            return; // continue to next key after handling datetime/deadline
        }

        field.value = value;
    });
}

/**
 * Maps error/success messages to elements in dom. 
 * Used by Fetcher() when posting form to rest/tasks/crud.
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