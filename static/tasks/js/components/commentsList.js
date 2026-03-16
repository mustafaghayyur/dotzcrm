import $A from "../helper.js";

export default function (comments, containerId) {
    let container = $A.app.containerElement(containerId);
    let commentCreator = $A.app.searchElementCorrectly('#createComment', container);
    let comment = $A.app.searchElementCorrectly('#commmentContainer', container);
    
    container.innerHTML = '';
    container.appendChild(commentCreator);

    if ($A.generic.checkVariableType(comments) === 'list') {
        comments.forEach(item => {
            let newComment = $A.app.embedData(item, comment.cloneNode(true), true);
            const user = $A.app.user(item.commenter_id, containerId);

            newComment.classList.remove('d-none');
            newComment.querySelector('.creator_id').textContent = '' + user.username + 'wrote...';
            container.appendChild(newComment);
            
            /*newComment.querySelector('.create_time').textContent = $A.dates.convertToDisplayLocal(item.create_time);
            newComment.querySelector('.update_time').textContent = $A.dates.convertToDisplayLocal(item.update_time);
            newComment.querySelector('.comment_text').innerHTML = $A.forms.escapeHtml(item.comment);*/
        });
    }
}
