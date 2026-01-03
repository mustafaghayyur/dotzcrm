/**
 * This file will hold various mappers our JS libraries may need to operate with data 
 */

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
    // Keys we expect in the resultSet (keeps defined order)
    const keys = [
        'id','tid','did','lid','sid','aid','vid','description','details','status','visibility','deadline',
        'creator_id','parent_id','assignor_id','assignee_id','dlatest','llatest','slatest','alatest','vlatest',
        'tcreate_time','dcreate_time','lcreate_time','screate_time','acreate_time','vcreate_time',
        'tdelete_time','ddelete_time','ldelete_time','sdelete_time','adelete_time','vdelete_time','tupdate_time'
    ];

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
}