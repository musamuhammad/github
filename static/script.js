document.addEventListener('DOMContentLoaded', () => {
    const nextBtn = id => document.getElementById(id);

    // ================= PAGE 1: PHONE INPUT LOGIC =================
    const countrySelect = document.getElementById('countrySelect');
    const countryCodeInput = document.getElementById('countryCodeInput');
    const phoneNumberInput = document.getElementById('phoneNumberInput');
    const step1NextBtn = document.getElementById('nextBtn');

    if (countrySelect && phoneNumberInput) {
        countrySelect.addEventListener('change', (e) => {
            countryCodeInput.value = e.target.value;
        });

        phoneNumberInput.addEventListener('input', (e) => {
            const val = e.target.value.trim();
            step1NextBtn.disabled = val.length < 7;
        });

        step1NextBtn.addEventListener('click', () => {
            const fullNumber = `${countryCodeInput.value} ${phoneNumberInput.value.trim()}`;
            // Optional: Store phone number in browser session storage to display on step 2
            sessionStorage.setItem('targetPhone', fullNumber);
            
            // Redirect to step 2 page
            window.location.href = 'verify.html';
        });
    }

    // ================= PAGE 2: OTP VERIFICATION LOGIC =================
    const otpInputs = document.querySelectorAll('.otp-input');
    const step2VerifyBtn = document.getElementById('nextBtn');
    const displayPhoneNumber = document.getElementById('displayPhoneNumber');
    const resendBtn = document.getElementById('resendBtn');
    const timerText = document.getElementById('timerText');

    if (otpInputs.length > 0) {
        // Retrieve and display saved phone number if available
        const savedPhone = sessionStorage.getItem('targetPhone');
        if (savedPhone && displayPhoneNumber) {
            displayPhoneNumber.textContent = savedPhone;
        }

        function updateOtpButtonState() {
            const allFilled = Array.from(otpInputs).every(input => input.value.length === 1);
            step2VerifyBtn.disabled = !allFilled;
        }

        otpInputs.forEach((input, index) => {
            input.addEventListener('input', (e) => {
                const value = e.target.value;
                if (!/^[0-9]$/.test(value)) {
                    e.target.value = '';
                    return;
                }
                if (value && index < otpInputs.length - 1) {
                    otpInputs[index + 1].focus();
                }
                updateOtpButtonState();
            });

            input.addEventListener('keydown', (e) => {
                if (e.key === 'Backspace') {
                    if (input.value === '' && index > 0) {
                        otpInputs[index - 1].focus();
                        otpInputs[index - 1].value = '';
                    } else {
                        input.value = '';
                    }
                    updateOtpButtonState();
                    e.preventDefault();
                }
            });

            input.addEventListener('paste', (e) => {
                e.preventDefault();
                const pasteData = e.clipboardData.getData('text').trim();
                if (/^\d{6}$/.test(pasteData)) {
                    otpInputs.forEach((inp, idx) => {
                        inp.value = pasteData[idx];
                    });
                    otpInputs[otpInputs.length - 1].focus();
                    updateOtpButtonState();
                }
            });
        });

        // Timer countdown simulation
        let timeLeft = 120;
        resendBtn.classList.add('disabled');
        
        const countdownInterval = setInterval(() => {
            if (timeLeft <= 0) {
                clearInterval(countdownInterval);
                timerText.textContent = '';
                resendBtn.classList.remove('disabled');
            } else {
                timeLeft--;
                const minutes = Math.floor(timeLeft / 60);
                const seconds = timeLeft % 60;
                timerText.textContent = `(${minutes}:${seconds < 10 ? '0' : ''}${seconds})`;
            }
        }, 1000);

        step2VerifyBtn.addEventListener('click', () => {
            const otpCode = Array.from(otpInputs).map(inp => inp.value).join('');
            alert(`[Lab Simulation] OTP Code Submitted: ${otpCode}`);
        });
    }
});
