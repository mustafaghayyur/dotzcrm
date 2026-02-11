import $A from "../helper.js";

/**
 * Generic mapper - might be used to catch error messages, etc...
 * Maps error/success messages to elements in dom. 
 * May be used by Fetcher() in forms for rest/tasks/crud/.
 */
export default {
    description: $A.app.makeDomElement('span', 'rec-itm'), 
    status: $A.app.makeDomElement('span', 'rec-itm'), 
    visibility: $A.app.makeDomElement('span', 'rec-itm'),
    taas_id: $A.app.makeDomElement('span', 'rec-itm'),
    assignee_id: $A.app.makeDomElement('span', 'rec-itm'),
    assignor_id: $A.app.makeDomElement('span', 'rec-itm'),
    csrfmiddlewaretoken: $A.app.makeDomElement('span', 'rec-itm'),
    deadline: $A.app.makeDomElement('span', 'rec-itm'),
    description: $A.app.makeDomElement('span', 'rec-itm'),
    details: $A.app.makeDomElement('span', 'rec-itm'),
    tade_id: $A.app.makeDomElement('span', 'rec-itm'),
    tadl_id: $A.app.makeDomElement('span', 'rec-itm'),
    parent_id: $A.app.makeDomElement('span', 'rec-itm'),
    tast_id: $A.app.makeDomElement('span', 'rec-itm'),
    status: $A.app.makeDomElement('span', 'rec-itm'),
    tata_id: $A.app.makeDomElement('span', 'rec-itm'),
    tavi_id: $A.app.makeDomElement('span', 'rec-itm'),
    visibility: $A.app.makeDomElement('span', 'rec-itm'),
    error: $A.app.makeDomElement('span', 'rec-itm'),
    errors: $A.app.makeDomElement('span', 'rec-itm'),
    message: $A.app.makeDomElement('span', 'rec-itm'),
    messages: $A.app.makeDomElement('span', 'rec-itm'),
};
