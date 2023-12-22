const toggleBtn = document.querySelector('#menu-icon')
const DropDownMenu = document.querySelector('.dropdown_menu')

toggleBtn.onclick = () => {
    toggleBtn.classList.toggle('bx-x')
    DropDownMenu.classList.toggle('open')
}

function submitLanguage(languageCode) {
    // Aizpildīt pseudo-formas lauku ar valodas kodu
    document.getElementById('languageInput').value = languageCode;

    // Iesniegt pseudo-formu
    document.getElementById('languageForm').submit();
}