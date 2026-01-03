/**
 * This module will carry common functions needed throughout the app...
 */

// You can also access specific local time components like this:
// console.log(`Local Hour: ${dateObject.getHours()}`);
// console.log(`Local Minutes: ${dateObject.getMinutes()}`);

export function convertDateTimeToLocal(mysqlString, displayOptions = null) {
    // Create a new Date object. 
    // The browser automatically interprets the 'Z' as UTC
    // mysqlString needs to be in format: "YYYY-MM-DDTHH:MM:SS.000Z"
    const dateObj = new Date(mysqlString);

    if(typeof displayOptions === 'object'){
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
        return dateObj.toLocaleString();
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
