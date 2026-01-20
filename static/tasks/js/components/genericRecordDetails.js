import helper from "../helper.js";

/**
 * Generic mapper - might be used to catch error messages, etc...
 * Maps error/success messages to elements in dom. 
 * May be used by Fetcher() in forms for rest/tasks/crud/.
 */
const genericTaskResponseMapper = {
    description: helper.app.makeDomElement('span', 'rec-itm'), 
    status: helper.app.makeDomElement('span', 'rec-itm'), 
    visibility: helper.app.makeDomElement('span', 'rec-itm'),
    aid: helper.app.makeDomElement('span', 'rec-itm'),
    assignee_id: helper.app.makeDomElement('span', 'rec-itm'),
    assignor_id: helper.app.makeDomElement('span', 'rec-itm'),
    csrfmiddlewaretoken: helper.app.makeDomElement('span', 'rec-itm'),
    deadline: helper.app.makeDomElement('span', 'rec-itm'),
    description: helper.app.makeDomElement('span', 'rec-itm'),
    details: helper.app.makeDomElement('span', 'rec-itm'),
    did: helper.app.makeDomElement('span', 'rec-itm'),
    lid: helper.app.makeDomElement('span', 'rec-itm'),
    parent_id: helper.app.makeDomElement('span', 'rec-itm'),
    sid: helper.app.makeDomElement('span', 'rec-itm'),
    status: helper.app.makeDomElement('span', 'rec-itm'),
    tid: helper.app.makeDomElement('span', 'rec-itm'),
    vid: helper.app.makeDomElement('span', 'rec-itm'),
    visibility: helper.app.makeDomElement('span', 'rec-itm'),
    error: helper.app.makeDomElement('span', 'rec-itm'),
    errors: helper.app.makeDomElement('span', 'rec-itm'),
    message: helper.app.makeDomElement('span', 'rec-itm'),
    messages: helper.app.makeDomElement('span', 'rec-itm'),
};

export default genericTaskResponseMapper