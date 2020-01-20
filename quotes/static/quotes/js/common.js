document.addEventListener('DOMContentLoaded', function() {
  // START ADD/REMOVE CLASS AT THE FOOTER
  var footer = document.querySelector('.footer--toggleBg');

  if (footer) {
    if (document.documentElement.clientWidth <= 768) {
      footer.classList.remove('footer--white');
    }

    window.addEventListener('resize', function() {
      var width = document.documentElement.clientWidth;

      width <= 768
        ? footer.classList.remove('footer--white')
        : footer.classList.add('footer--white');
    });
  }
  // END ADD/REMOVE CLASS AT THE FOOTER

  // START OPEN/CLOSE MENU
  var headerMenu = document.querySelector('.header__menu');

  if (headerMenu) {
    headerMenu.addEventListener('click', function(e) {
      var tg = e.target;
      var toggleMenuButton = headerMenu.querySelector('.header__menu-button');
      var pageWrapper = document.querySelector('.page-wrapper');
      var overlayMenu = document.querySelectorAll('.overlayMenu');
      var navMenu = headerMenu.querySelector('.header__menu-nav');

      if (tg.closest('.header__menu-button')) {
        toggleMenuButton.classList.toggle('active');
        pageWrapper.classList.toggle('menuActive');
        toggleOverlay(overlayMenu);
        animateMenu(navMenu, 100);
      }
    });
  }

  function toggleOverlay(elems) {
    for (var i = 0; i < elems.length; i++) {
      elems[i].classList.toggle('menuActive');
    }
  }

  function animateMenu(elem, timeout) {
    if (elem.classList.contains('active')) {
      elem.classList.remove('active');

      setTimeout(function() {
        elem.classList.remove('preActive');
      }, 100);

      return;
    }

    elem.classList.add('preActive');
    elem.style.bottom = -elem.clientHeight + 'px';

    setTimeout(function() {
      elem.classList.add('active');
    }, timeout);
  }
  // END OPEN/CLOSE MENU

  // START QUOTE BACKGROUND WIDTH
  (function() {
    var quoteBg = document.querySelector('.quote__bg img');

    if (quoteBg && quoteBg.clientWidth < 815) {
      quoteBg.style.width = '100%';
    }
  })();
  // END QUOTE BACKGROUND WIDTH

  // START POLYFILLS FOR IE AND OTHER BROWSERS
  // START POLYFILL FOR MATCHES METHOD
  (function() {
    // проверяем поддержку
    if (!Element.prototype.matches) {
      // определяем свойство
      Element.prototype.matches =
        Element.prototype.matchesSelector ||
        Element.prototype.webkitMatchesSelector ||
        Element.prototype.mozMatchesSelector ||
        Element.prototype.msMatchesSelector;
    }
  })();
  // END POLYFILL FOR MATCHES METHOD

  // START POLYFILL FOR CLOSEST METHOD
  (function() {
    // проверяем поддержку
    if (!Element.prototype.closest) {
      // реализуем
      Element.prototype.closest = function(css) {
        var node = this;

        while (node) {
          if (node.matches(css)) return node;
          else node = node.parentElement;
        }
        return null;
      };
    }
  })();
  // END POLYFILL FOR CLOSEST METHOD
});
