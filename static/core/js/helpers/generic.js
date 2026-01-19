export default {
    /**
     * supports only dictionary, list and string data-types.
     * @param {*} item
     * @returns bool
     */
    isVariableEmpty: (item) => {
        const type = checkVariableType(item);
        if (type === 'dictionary' && Object.keys(item).length === 0) {
            return true;
        }
        if (type === 'list' && item.length === 0) {
            return true;
        }
        if (type === 'string' && item.length === 0) {
            return true;
        }
        return false;
    },

    /**
     * Returns a string based definition of data-type.
     * @param {*} variable: any value type
     * @returns ['string' | 'list' | 'null' | 'dictionary' | 'undefined' | 'integer' | etc..]
     */
    checkVariableType: (variable) => {
        if (typeof variable === 'string') {
            return 'string';
        }
        if (Array.isArray(variable)) {
            return 'list';
        }
        if (variable === null) {
            return 'null';
        }
        if (variable !== null && typeof variable !== 'boolean' && Number.isInteger(+value)) {
            return 'number';
        }
        if (variable instanceof HTMLElement) {
            return 'domelement'
        }
        if (typeof variable === 'object' && variable !== null) {
            if (Object.prototype.toString.call(variable) === '[object Object]') {
                return 'dictionary';
            }
        }
        return typeof variable; // Handles null, undefined, number, boolean, etc.
    },

    /**
     * Takes an object and key, and returns the value or a default you provide.
     * @param {obj} object 
     * @param {str} key 
     * @param {*} defaultsTo 
     * @returns 
     */
    getter: (object, key, defaultsTo = null) => {
        if (checkVariableType(object) === 'dictionary') {
            return (object && Object.prototype.hasOwnProperty.call(object, key)) ? object[key] : defaultsTo;
        }
        return defaultsTo;
    },

    /**
     * takes tag type, class name, id name and forms a simple dom element.
     * @param {str} tagName 
     * @param {str} className 
     * @param {str} idName 
     */
    makeDomElement: (tagName, className = null, idName = null) => {
        let dom = document.createElement(tagName);
        dom.className = className;
        dom.idName = idName;
        return dom;
    },

    /**
     * Display values retrieved from database to front-end.
     * @param {*} value
     * @returns front-end friendly display
     */
    formatValueToString: (value) => {
        if (checkVariableType(value) === 'dictionary') {
            try {
                return JSON.stringify(value, null, 2);
            } catch (e) {
                return String(value); // just send the value
            }
        }
        return String(value);
    },

    /**
     * Loads a component specified with arguments.
     * @param {str} component: name of specific component. Components in sub-folders should be denoted with a 'subfolder.compoenentName' notation.
     * @param {str} app: name of django app/module we are operating in 
     * @returns 
     */
    load: async (component, app) => {
        const componentPath = component.replace(/\./, '/');
        console.log('Inside load(), checking if component path is generating correctly', component, componentPath);
        const modulePath = `../../../${app}/js/components/${componentPath}.js`;
        try {
            // The import() function accepts the string variable
            const module = await import(modulePath);
            return module.default;
        } catch (error) {
            console.error('Error loading component:', error);
        }
    }
};
