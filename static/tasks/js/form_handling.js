import { convertDateTimeToLocal } from "../../core/js/helper_dates.js";
import { keys } from "./mappers.js";
import { cleanForm } from "../../core/js/helper_forms.js";
import { validate } from './validate.js';

/**
 * A helper function.
 * This function simply pre-populates the Edit Task Form with record details, for which it was invoked.
 * @param {object} data: the data-object which will fill the form fields.
 */
export function prefillEditForm(data){
    const form = document.querySelector('#taskEditForm'); // Get the form element

    if (!(form instanceof HTMLElement)) {
        console.log('Error: form could not be found. Cannot pre-populate.');
        return;
    }

    keys.forEach(key => {
        let value = data && Object.prototype.hasOwnProperty.call(data, key) ? data[key] : undefined;
        let field = form.elements.namedItem(key);

        if (!value || !field) {
            return; // @todo, should I have better handling here? What about missing values for fields?
        }

        // If the key ends with '_time' or contains 'deadline', convert to appropriate format first
        if (/(_time$)|deadline/.test(key)) {
            field.value = convertDateTimeToLocal(value);
            return; // continue to next key after handling datetime/deadline
        }

        field.value = value;
    });
}

/**
 * Wrapper for clean function.
 * @param {string} formId: should be the while Id with the # selection 
 */
export function cleanTaskForm(formId) {
    cleanForm(formId, keys);
}

/**
 * Forms a dictionary/object of key/value pairs from the form.
 * 
 * @param {string} formId: should be string html id attribute value
 * @param {*} keysList: optional list of keys to check/validate
 */
export function generateDictionaryFromForm(formId, keysList = null) {
    const form = document.getElementById(formId);

    if (!(form instanceof HTMLElement)) {
        console.log('Error: form could not be found. Cannot form request object.', form);
    }

    // 1. Create a FormData object from the form element
    const formData = new FormData(form);

    // 2. Convert the FormData entries into a plain JavaScript object (dictionary format)
    const formObject = Object.fromEntries(formData.entries());

    if (keysList !== null && Array.isArray(keysList)) {
        let dictionary = {};
        keysList.forEach(key => {    
            if (formObject[key]) {
                dictionary[key] = validate(formObject[key]);
            }
        });

        return dictionary; // return validated data
    }

    return formObject; // return unvalidated data

    // If you need a JSON string, you can use JSON.stringify():
    // JSON.stringify(dictionary, null, 2);
}