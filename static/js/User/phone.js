document.addEventListener('DOMContentLoaded', function() {
    const phoneNumberInput = document.querySelector('#phone-number-input');
    const phoneNumberHidden = document.querySelector('#phone-number-hidden');
    const countryCodeSelect = document.querySelector('#country-code');
    const errorElement = document.querySelector('#phone-number-error');

    function updatePhoneNumber() {
        const countryCodeSelect = document.getElementById('countryCodeSelect');
        const phoneNumberInput = document.getElementById('phoneNumberInput');
        const phoneNumberHidden = document.getElementById('phoneNumberHidden');

        if (!countryCodeSelect || !phoneNumberInput || !phoneNumberHidden) {
            return;
        }

        const countryCode = countryCodeSelect.value;
        const inputValue = phoneNumberInput.value.replace(/^\+.*?/, '');
        phoneNumberHidden.value = countryCode + inputValue;
    }
    if (phoneNumberInput) {
        phoneNumberInput.addEventListener('input', function () {
            updatePhoneNumber();
        });
    }

    if (countryCodeSelect) {
        countryCodeSelect.addEventListener('change', function () {
            updatePhoneNumber();
        });
    }

    document.querySelector('form').addEventListener('submit', function(event) {
        // Example validation check
        if (!phoneNumberHidden.value.match(/^\+\d{8,}$/)) {
            event.preventDefault();
            errorElement.textContent = '{% trans "Lūdzu, ievadiet derīgu telefona numuru." %}';
            phoneNumberInput.classList.add('error');
        } else {
            errorElement.textContent = '';
            phoneNumberInput.classList.remove('error');
        }
    });

    // Initialize the hidden input with default value
    updatePhoneNumber();
});

// static/js/User/phone.js

export function initPhonePage() {
    const countryCodeSelect = document.getElementById('country-code');
    const phoneNumberInput = document.getElementById('phone-number-input');
    const phoneNumberHidden = document.getElementById('phone-number-hidden');

    if (!countryCodeSelect || !phoneNumberInput || !phoneNumberHidden) {
      console.warn('❗ phone.js: nepieciešamie elementi nav atrasti!');
      return;
    }

    // Inicializē hidden lauku
    phoneNumberHidden.value = countryCodeSelect.value + phoneNumberInput.value;

    countryCodeSelect.addEventListener('change', () => {
      phoneNumberHidden.value = countryCodeSelect.value + phoneNumberInput.value;
    });

    phoneNumberInput.addEventListener('input', () => {
      phoneNumberHidden.value = countryCodeSelect.value + phoneNumberInput.value;
    });
  }
