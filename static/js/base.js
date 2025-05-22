document.addEventListener('DOMContentLoaded', function () {
    const navlist = document.querySelector('.navlist');
    const menuIconSvg = document.getElementById('menu-icon-svg');
    const closeIconSvg = document.getElementById('close-icon-svg');
    const menuIconDiv = document.getElementById('menu-icon');

    if (menuIconDiv && navlist && menuIconSvg && closeIconSvg) {
        menuIconDiv.addEventListener('click', () => {
            const isMenuOpen = menuIconSvg.style.display !== 'none';
            menuIconSvg.style.display = isMenuOpen ? 'none' : 'block';
            closeIconSvg.style.display = isMenuOpen ? 'block' : 'none';
            navlist.classList.toggle('open');
        });
    }

    setTimeout(() => {
        document.querySelectorAll('.messages').forEach(message => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.style.display = 'none';
            }, 1000);
        });
    }, 5000);

    const dropdownBtn = document.getElementById('dropdownButton');
    const dropdownMenu = document.getElementById('dropdownMenu');

    if (dropdownBtn && dropdownMenu) {
        dropdownBtn.addEventListener('click', () => {
            dropdownMenu.classList.toggle('hidden');
        });

        window.addEventListener('click', (event) => {
            if (!dropdownBtn.contains(event.target) && !dropdownMenu.contains(event.target)) {
                dropdownMenu.classList.add('hidden');
            }
        });
    }

    const dropdown = document.querySelector('.dropdown');
    const dropdownToggle = dropdown?.querySelector('button');
    const dropdownContent = dropdown?.querySelector('.dropdown-content');

    if (dropdown && dropdownToggle && dropdownContent) {
        dropdownToggle.addEventListener('click', () => {
            dropdownContent.classList.toggle('hidden');
        });

        document.addEventListener('click', (event) => {
            if (!dropdown.contains(event.target)) {
                dropdownContent.classList.add('hidden');
            }
        });
    }

    document.addEventListener('contextmenu', (event) => {
        if (event.target.classList.contains('no-search')) {
            event.preventDefault();
        }
    });

    document.querySelectorAll('.no-search').forEach(img => {
        img.addEventListener('dragstart', e => e.preventDefault());
        img.addEventListener('mousedown', e => e.preventDefault());
    });

    document.querySelectorAll('.draggable').forEach(img => {
        img.setAttribute('draggable', 'true');
    });

    localStorage.setItem('currentSide', 'front');
});
