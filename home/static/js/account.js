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
    var usernameValid = validateUsername(usernameValue);

    var errorMessages = [];

    if (!emailValid || !phoneValid || !usernameValid) {
        if (!emailValid) {
            errorMessages.push("Nederīgs e-pasts.");
        }
        
        if (!phoneValid) {
            errorMessages.push("Nederīgs tālruņa numurs.");
        }

        if (!usernameValid) {
            errorMessages.push("Nederīgs lietotājvārds.");
        }

        displayErrorMessage(errorMessages.join("\n"));
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
            displaySuccessMessage("Dati veiksmīgi saglabāti");
            document.getElementById("editButton").style.display = "block";
            document.getElementById("saveButton").style.display = "none";
            
            document.getElementById("email").readOnly = true;
            document.getElementById("phone").readOnly = true;
            document.getElementById("username").readOnly = true;
        } else {
            if (data.errors) {
                if (data.errors.email) {
                    displayErrorMessage(data.errors.email);
                }
                if (data.errors.phone) {
                    displayErrorMessage(data.errors.phone);
                }
                if (data.errors.username) {
                    displayErrorMessage(data.errors.username);
                }
            } else {
                displayErrorMessage(data.error);
            }
        }
    })
    .catch(error => {
        console.error('Kļūda:', error);
        displayErrorMessage("Kļūda: Neizdevās saglabāt datus.");
    });
}

function displayErrorMessage(message) {
    var messageContainer = document.getElementById("messageContainer-savedata");
    messageContainer.innerText = message;
    messageContainer.classList.remove("success-message");
    messageContainer.classList.add("error-message");
    messageContainer.style.opacity = "1";
    messageContainer.style.transform = "translateX(0%)";
    messageContainer.style.display = "block";
}

function displaySuccessMessage(message) {
    var messageContainer = document.getElementById("messageContainer-savedata");
    messageContainer.innerText = message;
    messageContainer.classList.remove("error-message");
    messageContainer.classList.add("success-message");
    messageContainer.style.opacity = "1";
    messageContainer.style.transform = "translateX(0%)";
    messageContainer.style.display = "block";
    setTimeout(function() {
        messageContainer.style.opacity = "0";
        messageContainer.style.transform = "translateX(100%)";
        setTimeout(function() {
            messageContainer.style.display = "none";
        }, 500);
    }, 5000);
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
        changePasswordButton.style.cursor = "pointer";
        changePasswordButton.addEventListener("click", changePassword);
    } else {
        border.style.borderColor = "red";
        changePasswordButton.style.cursor = "not-allowed";
        changePasswordButton.removeEventListener("click", changePassword);
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
        const messageContainer = document.getElementById("message-password");
        if (data.success) {
            messageContainer.innerHTML = '<div class="alert success-message" role="alert">Parole veiksmīgi nomainīta!</div>';

        } else {
            messageContainer.innerHTML = '<div class="alert error-message" role="alert">' + data.error + '</div>';
        }
    
        messageContainer.style.opacity = "1";
        messageContainer.style.transform = "translateX(0)";
    
        setTimeout(function() {
            messageContainer.style.opacity = "0";
            messageContainer.style.transform = "translateX(100%)";
        }, 5000);
    })
}

// Delite Profile

document.getElementById("deleteProfileBtn").addEventListener("click", function() {
    var password = document.getElementById("password").value;
    var csrfToken = "{{ csrf_token }}";
    var deleteProfileUrl = "/account/delete_account/";
    var home = '/';
    var seconds = 5; // Sekundes, pēc kurām pārmest uz sākumlapu
    var count = seconds;
    
    var formData = new FormData();
    formData.append('password', password);
    
    fetch(deleteProfileUrl, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        var messagesElement = document.getElementById("deleteuser-messages");
        if (data.success) {
            messagesElement.innerHTML = '<div class="success-message">Jūsu profils ir veiksmīgi izdzēsts. Jūs tiksiet pārmests uz sākumlapu pēc ' + seconds + ' sekundēm.</div>';
            messagesElement.classList.remove("error-message");
            messagesElement.classList.add("success");
            messagesElement.style.opacity = "1";
            messagesElement.style.transform = "translateX(0)";
            
            var interval = setInterval(function() {
                count--;
                if (count === 0) {
                    clearInterval(interval);
                    window.location.href = home;
                } else {
                    messagesElement.innerHTML = '<div class="success-message">Jūsu profils ir veiksmīgi izdzēsts. Jūs tiksiet pārmests uz sākumlapu pēc ' + count + ' sekundēm.</div>';
                }
            }, 1000);
        } else {
            messagesElement.innerHTML = '<div class="error-message">' + data.error + '</div>';
            messagesElement.style.opacity = "1";
            messagesElement.style.transform = "translateX(0)";
        }
    })
    .catch(error => {
        var messagesElement = document.getElementById("deleteuser-messages");
        messagesElement.innerHTML = '<div class="error">Kļūda: Neizdevās sazināties ar serveri.</div>';
        messagesElement.classList.remove("success-message");
        messagesElement.classList.add("error-message");
        messagesElement.style.opacity = "1";
        setTimeout(function() {
            messagesElement.style.opacity = "0";
        }, 5000);
        console.error('There has been a problem with your fetch operation:', error);
    });
    
});

document.getElementById("password").addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("deleteProfileBtn").click();
    }
});

function showLogoutConfirmation() {
    var confirmation = confirm("Vai tiešām vēlaties iziet no sava profila?");
    if (confirmation) {
        window.location.href = "/logout/"
    }
}