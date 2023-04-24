const isModule = {
    Android: function () {
        return navigator.userAgent.match(/Android/i);
    },
    BlackBerry: function () {
        return navigator.userAgent.match(/BlackBerry/i);

    },
    iOS: function () {
        return navigator.userAgent.match(/iPhone|iPad|iPad/i);
    },
    Opera: function () {
        return navigator.userAgent.match(/Opera Mini/i);
    },
    Windows: function () {
        return navigator.userAgent.match(/IEModule/i);
    },
    any: function () {
        return (
            isModule.Android() ||
            isModule.BlackBerry() ||
            isModule.iOS() ||
            isModule.Opera() ||
            isModule.Windows()
        )
    }
}

if (isModule.any()) {
    document.body.classList.add('_touch');
    let menuArrows = document.querySelectorAll('.nav__menu-link');
    if (menuArrows.length > 0) {
        for (let i = 0; i < menuArrows.length; i++) {
            const menuArrow = menuArrows[i];
            menuArrow.addEventListener('click', function (e) {
                menuArrow.parentElement.classList.toggle('_active');
            })
        }
    }
} else {
    document.body.classList.add('_ps');
}

// Меню бургер
const iconMenu = document.querySelector('.nav__menu-icon');
const menuBody = document.querySelector('.nav__menu-body');
if (iconMenu) {
    iconMenu.addEventListener('click', function (e) {
        document.body.classList.toggle('_lock');
        iconMenu.classList.toggle('_active');
        menuBody.classList.toggle('_active');
    })
}

// Прокрутка при клике
const menuLinks = document.querySelectorAll('.nav__menu-link[data-goto]');
if (menuLinks.length > 0) {
    menuLinks.forEach(menuLink => {
        menuLink.addEventListener('click', onMenuLinkClick);
    });

    function onMenuLinkClick(e) {
        const menuLink = e.target
        console.log(menuLink);
        if (menuLink.dataset.goto && document.querySelector(menuLink.dataset.goto)) {
            const gotoBlock = document.querySelector(menuLink.dataset.goto);
            const gotoBlockValue = gotoBlock.getBoundingClientRect().top + pageYOffset - document.querySelector('nav').offsetHeight;

            if (iconMenu.classList.contains("_active")) {
                document.body.classList.remove('_lock');
                iconMenu.classList.remove('_active');
                menuBody.classList.remove('_active');
            }

            window.scrollTo({
                top: gotoBlockValue,
                behavior: "smooth"
            });
            e.preventDefault();
        }
    }
}