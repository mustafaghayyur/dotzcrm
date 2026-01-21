import helper from "../helper.js";

export default {
    /**
     * A helper function.
     * This function simply pre-populates the Edit Task Form with record details, for which it was invoked.
     * @param {object} data: the data-object which will fill the form fields.
     */
    prefillEditForm: (data, keys) => {
        return prefillForms(data, 'taskEditForm', keys);
    },

    /**
     * Wrapper for clean function.
     * @param {string} formId: should be the html Id attr value 
     */
    cleanTaskForm: (formId, keys) => {
        helper.generic.cleanForm(formId, keys);
    },

    /**
     * Forms a dictionary/object of key/value pairs from the form.
     * Then performs validation checks on them and returns a dictionary.
     * 
     * @param {string} formId: should be string html id attribute value
     * @param {list} keys: optional list of keys to check/validate
     */
    generateDictionaryFromForm: (formId, keys = null) => {
        let dictionary = helper.forms.formToDictionary(formId, keys = null);

        if (helper.generic.checkVariableType(keys) === 'list') {
            keys.forEach(key => {    
                if (dictionary[key]) {
                    dictionary[key] = helper.tasks.validators.validate(dictionary[key]);
                }
            });
        }
        return dictionary;
    }
};