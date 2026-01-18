import helper from "../helpers/main";

/**
 * Live text editor for all rich text editing needs.
 * 
 * @todo: make mobile and tablet compatable.
 * Use Instructions: add following element to dom, replacing 'elementId' and 'hidden_field_id' correctly:
 *  > <div id="elementId" class="rich-editor" data-field-id="hidden_field_id" contenteditable="true" placeholder="start typing..."></div>
 *  > <input type="hidden" id="hidden_field_id" name="hidden_field_name">
 * 
 * @param {string} elementId: the CSS selector of the editable element (e.g. 'myEditor') 
*/
export function Editor(elementId){
    const editor = document.getElementById(elementId); // class '.rich-editor' should be there as well...

    editor.addEventListener('keyup', () => {
        // Get the current HTML content of the editor
        let html = editor.innerHTML;

        // Save the current cursor position/selection range
        const selection = window.getSelection();
        const range = selection.getRangeAt(0);

        // Define tag-based styles: [b]...[-b], [i]...[-i], [u]...[-u], [h1]...[-h1], etc.
        // Patterns use non-greedy multiline captures so tags can wrap multiple lines.
        const styles = {
            bold: {
                regex: /\*\*(.*?)\*\*\s/g, // regex: /\[b\]([\s\S]*?)\[-b\]/g,
                replacement: '<b>$1</b> ',
            },
            italic: {
                regex: /\*\s(.*?)\s\*\s/g,
                replacement: '<i>$1</i> ',
            },
            underline: {
                regex: /__(.*?)__\s/g,
                replacement: '<u>$1</u> ',
            },
            h2: {
                // Matches '# heading' at start or immediately after a newline, captures text until newline or end
                regex: /(^|\r?\n|\<div\>)#\s([^\r\n]+)(?=\r?\n|$)/g,
                replacement: '$1<h2>$2</h2>',
            },
            h3: {
                regex: /(^|\r?\n|\<div\>)##\s([^\r\n]+)(?=\r?\n|$)/g,
                replacement: '$1<h3>$2</h3>',
            },
            h4: {
                regex: /(^|\r?\n|\<div\>)###\s([^\r\n]+)(?=\r?\n|$)/g,
                replacement: '$1<h4>$2</h4>',
            },
            red: {
                regex: /\[red\]([\s\S]*?)\[-red\]/g,
                replacement: '<span class="text-red">$1</span> ',
            },
            green: {
                regex: /\[yellow\]([\s\S]*?)\[-yellow\]/g,
                replacement: '<span class="text-yellow">$1</span> ',
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
}
