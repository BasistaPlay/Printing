function showSection(sectionId) {
    hideAllSections();
    document.getElementById(sectionId).style.display = 'block';
  }
  
  function hideAllSections() {
    var sections = document.getElementsByClassName('section');
    for (var i = 0; i < sections.length; i++) {
      sections[i].style.display = 'none';
    }
  }

  function enableEditing() {
    document.getElementById("email").readOnly = false;
    document.getElementById("phone").readOnly = false;
    document.getElementById("username").readOnly = false;
    document.getElementById("editButton").style.display = "none";
    document.getElementById("saveButton").style.display = "block";
}

function saveData() {
  var emailValue = document.getElementById("email").value;
  var phoneValue = document.getElementById("phone").value;
  var usernameValue = document.getElementById("username").value; 

  var emailValid = validateEmail(emailValue);
  var phoneValid = validatePhoneNumber(phoneValue);


  if (!emailValid && !phoneValid) {
      document.getElementById("messageContainer").innerText = gettext("Nederīgs e-pasts un tālruņa numurs.");
      return;
  }

  if (!emailValid) {
      document.getElementById("messageContainer").innerText = "Nederīgs e-pasts.";
      return;
  }

  if (!phoneValid) {
      document.getElementById("messageContainer").innerText = "Nederīgs tālruņa numurs.";
      return;
  }

  if (!validateUsername(usernameValue)) {
      document.getElementById("messageContainer").innerText = "Nederīgs lietotājvārds.";
      return;
  }

  fetch('/save_user_data/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': getCookie('csrftoken')
      },

      body: 'email=' + encodeURIComponent(emailValue) + '&phone=' + encodeURIComponent(phoneValue) + '&username=' + encodeURIComponent(usernameValue)
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
          alert("Dati veiksmīgi saglabāti");
          showEditButton();
      } else {
          document.getElementById("messageContainer").innerText = data.error;
      }
  })
  .catch(error => console.error('Kļūda:', error));
}

function validateUsername(username) {
  return /^[a-zA-Z0-9._-]+$/.test(username);
}

function validateEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function validatePhoneNumber(phone) {
  return /^[\d+]+$/.test(phone);
}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

document.getElementById("phone").addEventListener("input", function(event) {
  var input = event.target;
  var inputValue = input.value;

  var validCharacters = /^[0-9+]*$/;
  
  if (!validCharacters.test(inputValue)) {
      input.value = inputValue.replace(/[^0-9+]/g, '');
  }
});

function showEditButton() {
  document.getElementById("editButton").style.display = "block";
  document.getElementById("saveButton").style.display = "none";
}




// Pasword change

document.addEventListener("DOMContentLoaded", function() {
  const newPassword1Input = document.getElementById("newPassword1");
  const newPassword2Input = document.getElementById("newPassword2");
  const oldPasswordInput = document.getElementById("oldPassword");
  const oldPasswordIndicator = document.getElementById("oldPasswordIndicator");
  const lengthIndicator = document.getElementById("lengthIndicator");
  const numberIndicator = document.getElementById("numberIndicator");
  const uppercaseIndicator = document.getElementById("uppercaseIndicator");
  const newDifferentIndicator = document.getElementById("newDifferentIndicator");
  const messageContainerPassword = document.getElementById("messageContainerPassword");
  const border = document.getElementById("conditionIndicator");
  const changePasswordButton = document.querySelector(".button-password");

  const showOldPasswordIcon = document.getElementById("showOldPassword");
  const showNewPassword1Icon = document.getElementById("showNewPassword1");
  const showNewPassword2Icon = document.getElementById("showNewPassword2");

  showOldPasswordIcon.addEventListener("click", function() {
      togglePasswordVisibility(oldPasswordInput, showOldPasswordIcon);
  });

  showNewPassword1Icon.addEventListener("click", function() {
      togglePasswordVisibility(newPassword1Input, showNewPassword1Icon);
  });

  showNewPassword2Icon.addEventListener("click", function() {
      togglePasswordVisibility(newPassword2Input, showNewPassword2Icon);
  });

  function togglePasswordVisibility(inputField, icon) {
      const type = inputField.getAttribute("type");
      inputField.setAttribute("type", type === "password" ? "text" : "password");
      icon.classList.toggle("fa-eye");
      icon.classList.toggle("fa-eye-slash");
  }

  newPassword1Input.addEventListener("input", checkPasswordStrength);
  newPassword1Input.addEventListener("input", checkOldPassword);
  newPassword1Input.addEventListener("input", comparePasswords);
  newPassword2Input.addEventListener("input", comparePasswords);
  oldPasswordInput.addEventListener("input", checkOldPassword);

  newPassword1Input.addEventListener("input", checkIndicators);
  newPassword2Input.addEventListener("input", checkIndicators);
  oldPasswordInput.addEventListener("input", checkIndicators);

  changePasswordButton.addEventListener("mouseover", checkIndicators);

  function checkIndicators() {
      const allIndicatorsGreen = oldPasswordIndicator.textContent.includes("✅") &&
                                 newDifferentIndicator.textContent.includes("✅")&&
                                 lengthIndicator.textContent.includes("✅") &&
                                 numberIndicator.textContent.includes("✅") &&
                                 uppercaseIndicator.textContent.includes("✅");
      const allIndicatorsVisible = messageContainerPassword.textContent.includes("✅");
                                   
      if (allIndicatorsGreen && allIndicatorsVisible) {
        border.style.borderColor = "green";
        changePasswordButton.style.cursor = "pointer"; // Nomainiet kursoru uz "pointer"
        changePasswordButton.addEventListener("click", changePassword); // Pievienojiet click event listener
    } else {
        border.style.borderColor = "red";
        changePasswordButton.style.cursor = "not-allowed"; // Nomainiet kursoru uz "not-allowed"
        changePasswordButton.removeEventListener("click", changePassword); // Noņemiet click event listener
    }
}

  function checkOldPassword() {
      const oldPassword = oldPasswordInput.value;
      const password = newPassword1Input.value;

      const oldPasswordCondition = oldPassword.length > 0;

      oldPasswordIndicator.textContent = oldPasswordCondition ? "✅ Vecā parole ir ievadīta!" : "❌ Ievadiet veco paroli!";
      oldPasswordIndicator.style.color = oldPasswordCondition ? "green" : "red";

      const newPasswordDiffers = password !== oldPassword;
      newDifferentIndicator.textContent = newPasswordDiffers ? "✅ Jaunā parole atšķiras no vecās paroles" : "❌ Jaunā parole nevar būt vienāda ar veco paroli!";
      newDifferentIndicator.style.color = newPasswordDiffers ? "green" : "red";

      checkPasswordStrength();
      comparePasswords();
  }

  function checkPasswordStrength() {
      const password = newPassword1Input.value;

      const lengthCondition = password.length >= 8;
      const numberCondition = /\d/.test(password);
      const uppercaseCondition = /[A-Z]/.test(password);

      lengthIndicator.textContent = lengthCondition ? "✅ Parole ir pietiekami gara" : "❌ Parolei jābūt vismaz 8 rakstzīmēm garai";
      numberIndicator.textContent = numberCondition ? "✅ Parolē ir vismaz viens cipars" : "❌ Parolē jāsatur vismaz viens cipars";
      uppercaseIndicator.textContent = uppercaseCondition ? "✅ Parolē ir vismaz viens lielais burts" : "❌ Parolē jāsatur vismaz viens lielais burts";

      lengthIndicator.style.color = lengthCondition ? "green" : "red";
      numberIndicator.style.color = numberCondition ? "green" : "red";
      uppercaseIndicator.style.color = uppercaseCondition ? "green" : "red";

  }

  function comparePasswords() {
      const password1 = newPassword1Input.value;
      const password2 = newPassword2Input.value;

      if (password1 !== password2) {
          messageContainerPassword.innerText = "❌ Paroles nesakrī!";
          messageContainerPassword.style.color = "red";
      } else {
          messageContainerPassword.innerText = "✅ Parole sakrī!";
          messageContainerPassword.style.color = "green";
      }
  }
  
});

function changePassword() {
  const oldPassword = document.getElementById("oldPassword").value;
  const newPassword = document.getElementById("newPassword1").value;

  const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');


  const formData = new FormData();
  formData.append('oldPassword', oldPassword);
  formData.append('newPassword', newPassword);


  fetch('change_password/', {
      method: 'POST',
      body: formData,
      headers: {
          'X-CSRFToken': csrfToken
      }
  })
  .then(response => response.json())
  .then(data => {

      if (data.success) {
          document.getElementById("message").innerHTML = '<div class="alert alert-success" role="alert">Parole veiksmīgi nomainīta!</div>';
      } else {
          document.getElementById("message").innerHTML = '<div class="alert alert-danger" role="alert">' + data.error + '</div>';
      }
  })
  .catch(error => {
      document.getElementById("message").innerHTML = '<div class="alert alert-danger" role="alert">Kļūda sazinoties ar serveri: ' + error.message + '</div>';
  });
}