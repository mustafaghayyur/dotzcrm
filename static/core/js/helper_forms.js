/**
 * Cleans all fields that have a name matching a key provided by the supplied keys const.
 *
 * @param {string} formId: should be the while id value along with the '#' selector
 * @param {list} keys: keys is a list of all keys possible in the given form.
 */
export function cleanForm(formId, keys) {
    
    keys.forEach(key => {
        const field = document.querySelector(formId+' [name="'+key+'"]');
        if (!(field instanceof HTMLElement)){
            return;  // return only the foreach loop...
        }
        field.value = '';
    });
}

/**
 * Helps prevent xss attacks. 
 * Django should be performing this check.
 * @param {string} str: string to escape 
 * @returns 
 */
export function escapeHtml(str) {
    return String(str).replace(/[&<>"]+/g, s => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[s]));
}
