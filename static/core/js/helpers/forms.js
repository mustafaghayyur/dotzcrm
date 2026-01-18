import { checkVariableType, getter } from "./generic.js";

const forms = {
    /**
     * confirms any deletion before the event.
     * @param {string} identifyer
     * @returns true if deletion is to continue | false otherwise
     * 
     * @todo: implement
     */
    confirmDeletion: (identifyer) => {
        return true;
    },
    /**
     * Cleans all fields that have a name matching a key provided by the supplied keys const.
     *
     * @param {string} formId: should be the while id value along with the '#' selector
     * @param {list} keys: keys is a list of all keys possible in the given form.
     */
    cleanForm: (formId, keys) => {
        
        keys.forEach(key => {
            const field = document.querySelector(formId+' [name="'+key+'"]');
            if (!(field instanceof HTMLElement)){
                return;  // return only the foreach loop...
            }
            field.value = '';
        });
    },

    /**
     * Helps prevent xss attacks. 
     * Django should be performing this check.
     * @todo: improve...
     * @param {string} str: string to escape 
     * @returns 
     */
    escapeHtml: (str) => {
        return String(str).replace(/[&<>"]+/g, s => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[s]));
    },

    /**
     * Forms a dictionary/object of key/value pairs from the form.
     * 
     * @param {string} formId: should be string html id attribute value
     * @param {*} keysList: optional list of keys to check/validate
     */
    formToDictionary: (formId, keysList = null) => {
        const form = document.getElementById(formId);

        if (!(form instanceof HTMLElement)) {
            console.log('Error: form could not be found. Cannot form request object.', form);
        }

        // 1. Create a FormData object from the form element
        const formData = new FormData(form);

        // 2. Convert the FormData entries into a plain JavaScript object (dictionary format)
        const formObject = Object.fromEntries(formData.entries());

        if (checkVariableType(keysList) === 'list') {
            let dictionary = {};
            keysList.forEach(key => {    
                if (formObject[key]) {
                    dictionary[key] = formObject[key];
                }
            });

            return dictionary; // return validated data
        }
        return formObject; // return unvalidated data
    },

    /**
     * Pre-populate a form with record details using keys list.
     * @param {object} data: the data-object which will fill the form fields.
     * @param {str} formId: html dom id attr value 
     * @param {list} keys: holds list of all possible fields to expect for form.
     */
    prefillForms: (data, formId, keys) => {
        const form = document.getElementById(formId); // Get the form element

        if (!(form instanceof HTMLElement)) {
            console.log('Error: form with id "' + formId + '"could not be found. Cannot pre-populate.');
            return;
        }

        keys.forEach(key => {
            let value = getter(data, key, undefined);
            let field = form.elements.namedItem(key);

            if (!value || !field) {
                return; // @todo: should I have better handling here? What about missing values for fields?
            }

            if (hasDateTimeData(key)) {
                field.value = convertDateTimeToLocal(value);  // convert to appropriate format first
                return;
            }

            field.value = value;
        });
    },

    /**
     * Determines if field is a DateTime type.
     * If the key ends with '_time' or contains 'deadline'
     * @param {str} key: inidvidual key name which should correlate with a Model column name in Django.
     * @returns 
     */
    hasDateTimeData: (key) => {
        return /(_time$)|deadline/.test(key);
    }
}

export default forms;

