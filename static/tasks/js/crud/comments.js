import { Fetcher, defineRequest } from "../../../core/js/lib/async.js";
import helper from "../helper.js";

/**
 * Allows for adding new comments.
 * @param {str} action: enum ['add']
 * @param {str} formId: html dom id attribute value for entire form.
 */
export function createCommentForTask(formId) {
    let dictionary = helper.tasks.forms.generateDictionaryFromForm(formId);

    let request = defineRequest('/rest/tasks/comment/0/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dictionary),
    });

    Fetcher(request, 'commentsResponse', helper.tasks.load('genericRecordDetails'));
}
