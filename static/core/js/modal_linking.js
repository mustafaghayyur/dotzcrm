/**
 * Allows us to request a modal for matched key/value pairs
 * @param {str} key: key you are requesting
 * @param {str} value: value it should hold
 * @param {str} modal: #modalId we should show if true
 */
export function showModal(key, value, modal) {
    // Check if the 'modal' parameter is set to 'open'
    if (getQueryParam(key) === value) {
        // Select the modal element using its ID
        const modalEl = document.getElementById(modal);

        // Create a new Bootstrap Modal instance (for Bootstrap 5+)
        if (modalEl) {
            const modalInstance = new bootstrap.Modal(modalEl);
            modalInstance.show();
        }
    }
}

/**
 * Returns requested param's value if set in url params.
 * @param {str} paramStr: whic key are you requesting?
 */
export function getQueryParam(paramStr) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}
