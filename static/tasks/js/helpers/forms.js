import { TasksO2OKeys } from "../constants.js";
import { validate } from './validate.js';
import helper from "../../../core/js/helpers/main";

/**
 * A helper function.
 * This function simply pre-populates the Edit Task Form with record details, for which it was invoked.
 * @param {object} data: the data-object which will fill the form fields.
 */
export function prefillEditForm(data){
    return prefillForms(data, 'taskEditForm', TasksO2OKeys);
}

/**
 * Wrapper for clean function.
 * @param {string} formId: should be the while Id with the # selection 
 */
export function cleanTaskForm(formId) {
    helper.generic.cleanForm(formId, TasksO2OKeys);
}

/**
 * Forms a dictionary/object of key/value pairs from the form.
 * Then performs validation checks on them and returns a dictionary.
 * 
 * @param {string} formId: should be string html id attribute value
 * @param {list} keys: optional list of keys to check/validate
 */
export function generateDictionaryFromForm(formId, keys = null) {
    let dictionary = helper.forms.formToDictionary(formId, keys = null);

    if (helper.generic.checkVariableType(keysList) === 'list') {
        keysList.forEach(key => {    
            if (dictionary[key]) {
                dictionary[key] = validate(dictionary[key]);
            }
        });
        return dictionary;
    }
}