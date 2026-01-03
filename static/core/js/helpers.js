/**
 * This module will carry common functions needed throughout the app...
 */

const mysqlDatetime = '2024-01-27 15:50:00'; // Example MySQL DATETIME string

function convertMysqlToDatetimeToLocal(mysqlString) {
  // Create a Date object from the MySQL string. 
  // If the MySQL time is not explicitly UTC, JS may treat it as local or UTC depending on browser implementation.
  const dateObj = new Date(mysqlString);

  // Adjust for the local timezone offset to display the actual local time 
  // represented by the MySQL string (assuming MySQL stores local time).
  dateObj.setMinutes(dateObj.getMinutes() - dateObj.getTimezoneOffset());
  
  // Format the date object to ISO string format (which uses 'T' delimiter and UTC)
  // then slice to get the required "YYYY-MM-DDTHH:mm" format.
  return dateObj.toISOString().slice(0, 16);
}

// Get the input element
const datetimeInput = document.getElementById('myDatetimeLocalInput');

// Assign the converted value
datetimeInput.value = convertMysqlToDatetimeLocal(mysqlDatetime);
