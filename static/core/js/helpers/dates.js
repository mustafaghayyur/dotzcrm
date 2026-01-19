
export default {
    /**
     * Convert's a datetime value supplied by the back-end into a human-readable date and time value,
     * in the timezone of the current browser.
     * @param {string} mysqlString: needs to be in format: "YYYY-MM-DDTHH:MM:SS.000Z"
     * @param {object} displayOptions: object spefifying paramerters for display (see default for ideas)
     */
    convertToDisplayLocal: (mysqlString, displayOptions = null) => {
        // Create a new Date object. The browser automatically interprets the 'Z' as UTC
        const dateObj = new Date(mysqlString);

        if(displayOptions !== null && displayOptions !== 'default'){
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
    },

    /**
     * Convert's a datetime value supplied by the back-end into a format readble by the datetime-local
     * input field found in our input forms.
     * @param {string} mysqlString: needs to be in format: "YYYY-MM-DDTHH:MM:SS.000Z"
     * @returns {string} datetime-local formatted string "YYYY-MM-DDTHH:MM" (local timezone)
     */
    convertDateTimeToLocal: (mysqlString) => {
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
    },

    /**
     * Performs reverse operation of convertDateTimeToLocal(), taking a datetime-local
     * formatted string or Date object and converting it to back-end UTC timezone string format.
     * @param {Date object | string} localString: string can be "YYYY-MM-DDTHH:MM" (local timezone)
     * @returns string format "YYYY-MM-DDTHH:MM:SS.000Z"
     */
    convertLocalToBackendUTC: (localDate) => {
        try {
            if (!localDate) return '';

            let d;
            if (localDate instanceof Date) {
                d = localDate;
                if (isNaN(d.getTime())) return '';
            } else if (typeof localDate === 'string') {
                // Accept strings like: YYYY-MM-DDTHH:MM or YYYY-MM-DDTHH:MM:SS
                const m = localDate.match(/^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})(?::(\d{2}))?$/);
                if (!m) return '';
                const [, y, mo, day, hh, mm, ss] = m;
                const yyyy = parseInt(y, 10);
                const month = parseInt(mo, 10) - 1;
                const dd = parseInt(day, 10);
                const hour = parseInt(hh, 10);
                const minute = parseInt(mm, 10);
                const second = ss ? parseInt(ss, 10) : 0;

                // Construct a local Date using components (treated as local time)
                d = new Date(yyyy, month, dd, hour, minute, second);
                if (isNaN(d.getTime())) return '';
            } else {
                return '';
            }

            const pad = (n) => String(n).padStart(2, '0');
            const utcYYYY = d.getUTCFullYear();
            const utcMM = pad(d.getUTCMonth() + 1);
            const utcDD = pad(d.getUTCDate());
            const utcHH = pad(d.getUTCHours());
            const utcMin = pad(d.getUTCMinutes());
            const utcSec = pad(d.getUTCSeconds());

            return `${utcYYYY}-${utcMM}-${utcDD}T${utcHH}:${utcMin}:${utcSec}.000Z`;
        } catch (err) {
            return '';
        }
    },

    /**
     * Can correct sloppy dates formed by users.
     * Useful to ensure user supplied values are formatted correctly.
     * @param {string} dtValuePrivided - user supplied string representation of the datetime value
     */
    sloppyDateTimeCorrection: (dtValuePrivided) => {
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
};