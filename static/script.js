document.addEventListener("DOMContentLoaded", function () {

    /*
    =====================================
    PHONE NUMBER PAGE
    =====================================
    */

    const phoneForm = document.getElementById("phoneForm");

    if (phoneForm) {

        const country = document.getElementById("country");
        const dialCode = document.getElementById("dialCode");
        const phoneNumber = document.getElementById("phoneNumber");
        const nextButton = document.getElementById("nextButton");
        const phoneError = document.getElementById("phoneError");


        // Update country calling code

        country.addEventListener("change", function () {

            const selected =
                country.options[country.selectedIndex];

            dialCode.value = selected.dataset.code;

        });


        // Allow numeric input only

        phoneNumber.addEventListener("input", function () {

            phoneNumber.value =
                phoneNumber.value.replace(/\D/g, "");

            nextButton.disabled =
                phoneNumber.value.length < 7;

            phoneError.textContent = "";

        });


        // Handle phone form submission

        phoneForm.addEventListener("submit", function (event) {

            event.preventDefault();

            if (!phoneForm.checkValidity()) {

                phoneError.textContent =
                    "Please enter a valid phone number.";

                return;

            }

            const number =
                dialCode.value + " " + phoneNumber.value;

            // Local demonstration only

            sessionStorage.setItem(
                "demoPhoneNumber",
                number
            );

            window.location.href = "otp.html";

        });

    }


    /*
    =====================================
    OTP DEMONSTRATION PAGE
    =====================================
    */

    const otpForm = document.getElementById("otpForm");

    if (otpForm) {

        const otpInput =
            document.getElementById("verificationCode");

        const verifyButton =
            document.getElementById("verifyButton");

        const otpError =
            document.getElementById("otpError");

        const displayPhone =
            document.getElementById("displayPhone");


        // Display demonstration phone number

        displayPhone.textContent =
            sessionStorage.getItem("demoPhoneNumber") || "your number";


        // Numeric input validation

        otpInput.addEventListener("input", function () {

            otpInput.value = otpInput.value
                .replace(/\D/g, "")
                .slice(0, 6);

            verifyButton.disabled =
                otpInput.value.length !== 6;

            otpError.textContent = "";

        });


        // Handle OTP form submission

        otpForm.addEventListener("submit", function (event) {

            event.preventDefault();

            if (!otpForm.checkValidity()) {

                otpError.textContent =
                    "Enter a six-digit demonstration code.";

                return;

            }

            otpError.style.color = "#287f63";

            otpError.textContent =
                "Demonstration completed successfully.";

        });

    }

});