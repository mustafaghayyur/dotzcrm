import { convertDateTimeToLocal } from "../../core/js/helper_dates.js";
import { keys } from "./mappers.js";

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