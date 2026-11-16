document.addEventListener('DOMContentLoaded', () => {
    
    // ================= PAGE 1 LOGIC =================
    const countrySelect = document.getElementById('countrySelect');
    const countryCodeInput = document.getElementById('countryCodeInput');
    const phoneNumberInput = document.getElementById('phoneNumberInput');
    const step1NextBtn = document.getElementById('nextBtn');

    if (countrySelect && phoneNumberInput) {
        countrySelect.addEventListener('change', (e) => {
            if(e.target.value === 'Nigeria') countryCodeInput.value = '+ 234';
            if(e.target.value === 'United States') countryCodeInput.value = '+ 1';
            if(e.target.value === 'United Kingdom') countryCodeInput.value = '+ 44';
            if(e.target.value === 'India') countryCodeInput.value = '+ 91';
        });

        phoneNumberInput.addEventListener('input', (e) => {
            const val = e.target.value.trim();
            step1NextBtn.disabled = val.length < 7;
        });
    }

        // ================= PAGE 2 LOGIC (Single OTP Input) =================
    const otpInput = document.getElementById('otpInput');
    const step2VerifyBtn = document.getElementById('nextBtn');
    const displayPhoneNumber = document.getElementById('displayPhoneNumber');
    const hiddenPhoneField = document.getElementById('hiddenPhoneField');

    if (otpInput) {
        const urlParams = new URLSearchParams(window.location.search);
        const cc = urlParams.get('cc') || '+ 234';
        const phone = urlParams.get('phone') || '706 620 0591';
        const fullNumberString = `${cc} ${phone}`;

        if (displayPhoneNumber) displayPhoneNumber.textContent = fullNumberString;
        if (hiddenPhoneField) hiddenPhoneField.value = fullNumberString;

        otpInput.addEventListener('input', (e) => {
            // Strip out non-numeric entries and restrict to 6 digits
            const sanitizedValue = e.target.value.replace(/\D/g, '').slice(0, 6);
            e.target.value = sanitizedValue;

            // Enable button only when exactly 6 digits are provided
            step2VerifyBtn.disabled = sanitizedValue.length !== 6;
        });
    }
