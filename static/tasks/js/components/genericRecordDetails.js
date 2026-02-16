import $A from "../helper.js";

/**
 * Generic mapper - might be used to catch error messages, etc...
 * Maps error/success messages to elements in dom. 
 * May be used by Fetcher() in forms for rest/tasks/crud/.
 */
export default function(data, containerId) {
    let container = document.getElementById(containerId);
    
    container.appendChild($A.generic.loopObject(data, (key, value) => {
        let elem = $A.app.makeDomElement('span', 'rec-itm '+ key);
        elem.innerHTML = value;
        return elem;
    }));
};
