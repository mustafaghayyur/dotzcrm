
export function makeElement(tagName, className = null, idName = null) {
    let dom = document.createElement(tagName);
    dom.className = className;
    dom.idName = idName;
    return dom;
}