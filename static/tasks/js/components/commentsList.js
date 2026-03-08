import $A from "../helper.js";

export default function (data, containerId) {
    console.log('Inside commentsList module, checking data and containerid: ', data, containerId)
    let parentId = containerId.replace(/Response$/,'');
    let container = document.getElementById(parentId);
    let commentCreator = container.querySelector('#createComment');
    let comment = container.querySelector('#commmentContainer');
    container.innerHTML = '';
    container.appendChild(commentCreator);

    if ($A.generic.checkVariableType(data) === 'list') {
        let newComment = null;
        data.forEach(item => {
            console.log('I should be showing up as a list item now.', comment, container)
            newComment = comment.cloneNode(true);    
            newComment.classList.remove('d-none');

            newComment.querySelector('.creator_id').textContent = '' + item.commenter_id + 'wrote...';
            newComment.querySelector('.create_time').textContent = $A.dates.convertToDisplayLocal(item.create_time);
            newComment.querySelector('.update_time').textContent = $A.dates.convertToDisplayLocal(item.update_time);
            newComment.querySelector('.comment_text').innerHTML = $A.forms.escapeHtml(item.comment);

            container.appendChild(newComment);
        });
    }
}
