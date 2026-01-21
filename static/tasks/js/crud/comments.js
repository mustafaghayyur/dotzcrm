import helper from "../helper.js";

/**
 * Allows for adding new comments.
 * @param {str} action: enum ['add']
 * @param {str} formId: html dom id attribute value for entire form.
 */
export async function createCommentForTask(formId) {
    let dictionary = helper.tasks.forms.generateDictionaryFromForm(formId);

    const callback = await helper.tasks.load('genericRecordDetails');
    let request = helper.fetch.route('api.tasks.comments_crud', '0', {
        method: 'POST',
        body: JSON.stringify(dictionary),
    });

    helper.fetch.body(request, 'commentsResponse', callback);
}
