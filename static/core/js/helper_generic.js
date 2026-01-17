
/**
 * confirms any deletion before the event.
 * @param {string} identifyer
 * @returns true if deletion is to continue | false otherwise
 * 
 * @todo: implement
 */
export function confirmDeletion(identifyer) {
    return true;
}

/**
 * supports only dictionary, list and string data-types.
 * @param {*} item
 * @returns bool
 */
export function isVariableEmpty(item) {
    const type = checkVariableType(item);
    if (type === 'dictionary' && Object.keys(item).length === 0) {
        return true;
    }
    if (type === 'list' && item.length === 0) {
        return true;
    }
    if (type === 'string' && item.length === 0) {
        return true;
    }
    return false;
}

/**
 * Returns a string based definition of data-type.
 * @param {*} variable: any value type
 * @returns ['string' | 'list' | 'null' | 'dictionary' | 'undefined' | 'number' | etc..]
 */
export function checkVariableType(variable) {
    if (typeof variable === 'string') {
        return 'string';
    }
    if (Array.isArray(variable)) {
        return 'list';
    }
    if (variable === null) {
        return 'null';
    }
    if (typeof variable === 'object' && variable !== null) {
        if (Object.prototype.toString.call(variable) === '[object Object]'){
            return 'dictionary';
        }
    }
    return typeof variable; // Handles null, undefined, number, boolean, etc.
}