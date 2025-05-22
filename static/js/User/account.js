function showSection(sectionId) {
    hideAllSections();
    document.getElementById(sectionId).style.display = 'block';

    // Maina URL atkarībā no izvēlētās sadaļas
    var button = Array.from(document.querySelectorAll('.navbar button')).find(btn => btn.getAttribute('onclick').includes(sectionId));
    if (button) {
        var url = button.getAttribute('data-url');
        if (url) {
            window.history.pushState({}, '', url);
        }
    }
}

function hideAllSections() {
    var sections = document.getElementsByClassName('section');
    for (var i = 0; i < sections.length; i++) {
        sections[i].style.display = 'none';
    }
}


document.addEventListener('DOMContentLoaded', checkErrors);


function enableEditing(event) {
    if (event) {
        event.preventDefault(); // Prevent the default form submission
    }

    // Get all input elements in the form
    var inputs = document.querySelectorAll('#personalInfoForm input');

    inputs.forEach(function(input) {
        if (input.name !== 'first_name' && input.name !== 'last_name') {
            input.removeAttribute('readonly');
            input.style.backgroundColor = '#fff'; // White background for editable fields
        }
    });

    // Make "Edit Data" button hidden and "Save Data" button visible
    document.getElementById('editButton').style.display = 'none';
    document.getElementById('saveButton').style.display = 'inline-block';
}

function checkErrors() {
    var form = document.getElementById('personalInfoForm');
    if (!form) return;

    var hasErrors = form.querySelectorAll('.invalid-feedback').length > 0;

    if (hasErrors) {
        enableEditing();
    }
}

document.addEventListener('DOMContentLoaded', checkErrors);

// Automātiski aizvērt ziņojumus pēc 10 sekundēm
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        var messages = document.querySelectorAll('.alert');
        messages.forEach(function(message) {
            message.style.display = 'none';
        });
    }, 10000); // 10 seconds
});