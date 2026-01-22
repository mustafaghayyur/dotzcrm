import $A from "../helper.js";

/**
 * Allows for adding new comments.
 * @param {str} action: enum ['add']
 * @param {str} formId: html dom id attribute value for entire form.
 */
export async function createCommentForTask(formId) {
    let dictionary = $A.tasks.forms.generateDictionaryFromForm(formId);

    const callback = await $A.tasks.load('genericRecordDetails');
    let request = $A.fetch.route('api.tasks.comments_crud', '0', {
        method: 'POST',
        body: JSON.stringify(dictionary),
    });

    $A.fetch.body(request, 'commentsResponse', callback);
}
