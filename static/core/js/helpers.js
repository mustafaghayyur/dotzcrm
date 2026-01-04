/**
 * This module will carry common functions needed throughout the app...
 */

// You can also access specific local time components like this:
// console.log(`Local Hour: ${dateObject.getHours()}`);
// console.log(`Local Minutes: ${dateObject.getMinutes()}`);

/**
 * Convert's a datetime value supplied by the back-end into a human-readable date and time value,
 * in the timezone of the current browser.
 * @param {string} mysqlString: needs to be in format: "YYYY-MM-DDTHH:MM:SS.000Z"
 * @param {object} displayOptions: object spefifying paramerters for display (see default for ideas)
 */
export function convertToDisplayLocal(mysqlString, displayOptions = null) {
    // Create a new Date object. The browser automatically interprets the 'Z' as UTC
    const dateObj = new Date(mysqlString);

    if(displayOptions !== null && typeof displayOptions === 'object'){
        return new Intl.DateTimeFormat(navigator.language, displayOptions).format(dateObj);
    } 
    
    if(displayOptions === 'default') {
        const options = {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: 'numeric',
            minute: 'numeric',
            timeZoneName: 'short',
        };

        return new Intl.DateTimeFormat(navigator.language, options).format(dateObj);        
    } else {
        return dateObj.toLocaleString(); // what we get: 1/15/2026, 7:00:00 AM
    }
}

/**
 * Convert's a datetime value supplied by the back-end into a format readble by the datetime-local
 * input field found in our input forms.
 * @param {string} mysqlString: needs to be in format: "YYYY-MM-DDTHH:MM:SS.000Z"
 * @returns {string} datetime-local formatted string "YYYY-MM-DDTHH:MM" (local timezone)
 */
export function convertDateTimeToLocal(mysqlString) {
    try {
        if (!mysqlString) return '';

        // Create Date object (browser treats trailing Z as UTC)
        const d = new Date(mysqlString);
        if (isNaN(d.getTime())) return '';

        const pad = (n) => String(n).padStart(2, '0');
        const yyyy = d.getFullYear();
        const mm = pad(d.getMonth() + 1);
        const dd = pad(d.getDate());
        const hh = pad(d.getHours());
        const min = pad(d.getMinutes());

        return `${yyyy}-${mm}-${dd}T${hh}:${min}`;
    } catch (err) {
        return '';
    }
}

/**
 * Useful to ensure user supplied values are formatted correctly.
 * @param {string} dtValuePrivided - user supplied string representation of the datetime value
 */
export function sloppyDateTimeCorrection(dtValuePrivided) {
    try {
        const dt = new Date(dtValuePrivided);
        const pad = str => String(str).padStart(2, '0');

        if (!isNaN(dt.getTime())) {
            const yyyy = dt.getFullYear();
            const mm = pad(dt.getMonth() + 1);
            const dd = pad(dt.getDate());
            const hh = pad(dt.getHours());
            const min = pad(dt.getMinutes());
            return `${yyyy}-${mm}-${dd}T${hh}:${min}`;
        } else {
            throw Error('Error: Privided string not a recognized date.');
        }
    } catch (err) {
        field.value = String(value);
    }
}
