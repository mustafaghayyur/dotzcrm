import { convertToDisplayLocal } from "../../../core/js/helpers/dates";

export function commentsMapper(data, containerId) {
    let parentId = containerId.replace(/Response$/,'');
    let container = document.getElementById(parentId);
    let commentCreator = container.querySelector('#createComment');
    let comment = container.querySelector('#commmentContainer');
    container.innerHTML = '';
    container.appendChild(commentCreator);

    if (Array.isArray(data)) {
        let newComment = null;
        data.forEach(item => {
            newComment = comment.cloneNode(true);    
            newComment.classList.remove('d-none');

            newComment.querySelector('.creator_id').textContent = '' + item.creator_user_id + 'wrote...';
            newComment.querySelector('.create_time').textContent = convertToDisplayLocal(item.create_time);
            newComment.querySelector('.update_time').textContent = convertToDisplayLocal(item.update_time);
            newComment.querySelector('.comment_text').innerHTML = item.comment;

            container.appendChild(newComment);
        });
    }
        
}
