export default {
    /**
     * supports only dictionary, list and string data-types.
     * @param {*} item
     * @returns bool
     */
    isVariableEmpty: function (item) {
        const type = this.checkVariableType(item);
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
    checkVariableType: function (variable) {
        if (typeof variable === 'string') {
            return 'string';
        }
        if (Array.isArray(variable)) {
            return 'list';
        }
        if (variable === null) {
            return 'null';
        }
        if (variable !== null && typeof variable !== 'boolean' && Number.isInteger(+variable)) {
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

    isPrimitiveValue: function (variable) {
        let type = this.checkVariableType(variable);
        const allowed = ['string', 'number', 'bigint', "boolean", 'undefined', 'null', 'symbol']
    },

    /**
     * Takes an object and key, and returns the value or a default you provide.
     * @param {obj} object 
     * @param {str} key 
     * @param {*} defaultsTo 
     * @returns 
     */
    getter: function (object, key, defaultsTo = null) {
        if (this.checkVariableType(object) === 'dictionary') {
            return (object && Object.prototype.hasOwnProperty.call(object, key)) ? object[key] : defaultsTo;
        }
        return defaultsTo;
    },

    /**
     * Display values retrieved from database to front-end.
     * @param {*} value
     * @returns front-end friendly display
     */
    formatValueToString: function (value) {
        if (this.checkVariableType(value) === 'dictionary') {
            try {
                return JSON.stringify(value, null, 2);
            } catch (e) {
                return String(value); // just send the value
            }
        }
        return String(value);
    },

    loopObject: function (object, callbackFunction) {
        for (const key in object) {
            // .hasOwnProperty ensures only defined properties are looped.
            if (Object.hasOwnProperty.call(object, key)) {
                callbackFunction(key, object[key]);
            }
        }
    },
    
    /**
     * Returns requested param's value if set in url params.
     * @param {str} paramStr: whic key are you requesting?
     */
    getQueryParam: function (paramStr) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(paramStr);
    }
};

