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
    document.getElementById("editButton").style.display = "none";
    document.getElementById("saveButton").style.display = "block";
}

function enableEditing() {
  document.getElementById("email").readOnly = false;
  document.getElementById("phone").readOnly = false;
  document.getElementById("editButton").style.display = "none";
  document.getElementById("saveButton").style.display = "block";
}

function saveData() {
  var emailValue = document.getElementById("email").value;
  var phoneValue = document.getElementById("phone").value;
  var emailValid = validateEmail(emailValue);
  var phoneValid = validatePhoneNumber(phoneValue);

  if (!emailValid && !phoneValid) {
      document.getElementById("messageContainer").innerText = "Invalid email and phone number.";
      return;
  }

  if (!emailValid) {
      document.getElementById("messageContainer").innerText = "Invalid email.";
      return;
  }

  if (!phoneValid) {
      document.getElementById("messageContainer").innerText = "Invalid phone number.";
      return;
  }

  fetch('/save_user_data/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': getCookie('csrftoken')
      },
      body: 'email=' + encodeURIComponent(emailValue) + '&phone=' + encodeURIComponent(phoneValue)
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
          alert("Data saved successfully");
          showEditButton();
      } else {
          document.getElementById("messageContainer").innerText = data.error;
      }
  })
  .catch(error => console.error('Error:', error));
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
