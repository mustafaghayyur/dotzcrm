import { Fetcher, defineRequest } from "../../../core/js/lib/async.js";
import { genericTaskResponseMapper } from "../components/genericRecordDetails.js";
import { generateDictionaryFromForm } from '.../helpers/forms.js';
import helper from "../../../core/js/helpers/main";


/**
 * Allows for adding new comments.
 * @param {str} action: enum ['add']
 * @param {str} formId: html dom id attribute value for entire form.
 */
export function createCommentForTask(formId) {
    let dictionary = generateDictionaryFromForm(formId);

    let request = defineRequest('/rest/tasks/comment/0/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dictionary),
    });

    Fetcher(request, 'commentsResponse', genericTaskResponseMapper);
}
