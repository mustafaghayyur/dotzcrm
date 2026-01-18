import { makeDomElement } from "../../../core/js/helpers/generic.js";

/**
 * Generic mapper - might be used to catch error messages, etc...
 * Maps error/success messages to elements in dom. 
 * May be used by Fetcher() in forms for rest/tasks/crud/.
 */
export const genericTaskResponseMapper = {
    description: makeDomElement('span', 'rec-itm'), 
    status: makeDomElement('span', 'rec-itm'), 
    visibility: makeDomElement('span', 'rec-itm'),
    aid: makeDomElement('span', 'rec-itm'),
    assignee_id: makeDomElement('span', 'rec-itm'),
    assignor_id: makeDomElement('span', 'rec-itm'),
    csrfmiddlewaretoken: makeDomElement('span', 'rec-itm'),
    deadline: makeDomElement('span', 'rec-itm'),
    description: makeDomElement('span', 'rec-itm'),
    details: makeDomElement('span', 'rec-itm'),
    did: makeDomElement('span', 'rec-itm'),
    lid: makeDomElement('span', 'rec-itm'),
    parent_id: makeDomElement('span', 'rec-itm'),
    sid: makeDomElement('span', 'rec-itm'),
    status: makeDomElement('span', 'rec-itm'),
    tid: makeDomElement('span', 'rec-itm'),
    vid: makeDomElement('span', 'rec-itm'),
    visibility: makeDomElement('span', 'rec-itm'),
    error: makeDomElement('span', 'rec-itm'),
    errors: makeDomElement('span', 'rec-itm'),
    message: makeDomElement('span', 'rec-itm'),
    messages: makeDomElement('span', 'rec-itm'),
};