/**
 * Live text editor for all rich text editing needs.
 * Use: add following element to dom:
 *  > <div class="rich-editor" contenteditable="true" placeholder="start typing..."></div>
 * @todo: implement this function.
*/
document.addEventListener('DOMContentLoaded', () => {
    const editor = document.querySelector('.rich-editor');
    editor.addEventListener('keyup', () => {
        // Get the current HTML content of the editor
        let html = editor.innerHTML;

        // Save the current cursor position/selection range
        const selection = window.getSelection();
        const range = selection.getRangeAt(0);

        // Define the regex for **bold** text. The (.*?) captures the text inside the asterisks.
        // The g flag is for global search, i for case-insensitive (optional).
        const styles = {
            bold: {
                regex: /\*\*(.*?)\*\*/g,
                replacement: '<b>$1</b>',
            },
            italic: {
                regex: /\*(.*?)\*/g,
                replacement: '<i>$1</i>',
            },
            underline: {
                regex: /__(.*?)__/g,
                replacement: '<u>$1</u>',
            },
            h1: {
                regex: /# (.*?)\n/g,
                replacement: '<h1>$1</h1>',
            },
            h2: {
                regex: /## (.*?)\n/g,
                replacement: '<h2>$1</h2>',
            },
            h3: {
                regex: /### (.*?)\n/g,
                replacement: '<h3>$1</h3>',
            },
            red: {
                regex: /~~(.*?)~~/g,
                replacement: '<span style="color:red;">$1</span>',
            },
            green: {
                regex: /==(.+?)==/g,
                replacement: '<span style="color:green;">$1</span>',
            },
        };

        Object.values(styles).forEach(element => {
            html = html.replace(element.regex, element.replacement);
        });

        // Update the editor's content. This causes the cursor to jump.
        editor.innerHTML = html;
        
        // Restore the cursor position (basic restoration, advanced editors need more complex logic)
        // This simple method places the cursor at the end of the content.
        // For a full rich text editor experience, explore libraries or the execCommand method,
        // although execCommand is deprecated.
        range.setStart(editor, editor.childNodes.length);
        range.collapse(true);
        selection.removeAllRanges();
        selection.addRange(range);
    });
});
