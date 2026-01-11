
/**
 * takes tag type, class name, id name and forms a simple dom element.
 * @param {str} tagName 
 * @param {str} className 
 * @param {str} idName 
 */
export function makeElement(tagName, className = null, idName = null) {
    let dom = document.createElement(tagName);
    dom.className = className;
    dom.idName = idName;
    return dom;
}

/**
 * Display values retrieved from database to front-end.
 * @param {*} value
 * @returns front-end friendly display
 */
export function formatValue(value) {
    if (value === null || value === undefined) return '';
    if (typeof value === 'object') {
        try {
            return JSON.stringify(value, null, 2);
        } catch (e) {
            return String(value); // just send the value
        }
    }
    return String(value);
}