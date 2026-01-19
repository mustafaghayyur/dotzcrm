import helper from "../helper.js";

/**
 * Generic mapper - might be used to catch error messages, etc...
 * Maps error/success messages to elements in dom. 
 * May be used by Fetcher() in forms for rest/tasks/crud/.
 */
const genericTaskResponseMapper = {
    description: helper.generic.makeDomElement('span', 'rec-itm'), 
    status: helper.generic.makeDomElement('span', 'rec-itm'), 
    visibility: helper.generic.makeDomElement('span', 'rec-itm'),
    aid: helper.generic.makeDomElement('span', 'rec-itm'),
    assignee_id: helper.generic.makeDomElement('span', 'rec-itm'),
    assignor_id: helper.generic.makeDomElement('span', 'rec-itm'),
    csrfmiddlewaretoken: helper.generic.makeDomElement('span', 'rec-itm'),
    deadline: helper.generic.makeDomElement('span', 'rec-itm'),
    description: helper.generic.makeDomElement('span', 'rec-itm'),
    details: helper.generic.makeDomElement('span', 'rec-itm'),
    did: helper.generic.makeDomElement('span', 'rec-itm'),
    lid: helper.generic.makeDomElement('span', 'rec-itm'),
    parent_id: helper.generic.makeDomElement('span', 'rec-itm'),
    sid: helper.generic.makeDomElement('span', 'rec-itm'),
    status: helper.generic.makeDomElement('span', 'rec-itm'),
    tid: helper.generic.makeDomElement('span', 'rec-itm'),
    vid: helper.generic.makeDomElement('span', 'rec-itm'),
    visibility: helper.generic.makeDomElement('span', 'rec-itm'),
    error: helper.generic.makeDomElement('span', 'rec-itm'),
    errors: helper.generic.makeDomElement('span', 'rec-itm'),
    message: helper.generic.makeDomElement('span', 'rec-itm'),
    messages: helper.generic.makeDomElement('span', 'rec-itm'),
};

export default genericTaskResponseMapper