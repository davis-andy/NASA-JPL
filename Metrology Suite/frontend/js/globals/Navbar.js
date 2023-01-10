class Navbar {

    constructor(ul) {
        this.navbar = ul;
        this.initialize();
    }

    initialize() {

        // if no element was instantiated, return null
        if (!this.navbar) return null;

        // initialize event listener for click on `a` tag that has sub-`ul`
        for (const link of this.navbar.getElementsByTagName('a')) {
            let ul = link.nextElementSibling;
            if (ul) {
                link.addEventListener('click', () => this.toggleSubMenu(ul));
            }
        }

        // add carets to any `li` that has a sub-`ul`
        for (const ul of this.navbar.getElementsByTagName('ul')) {
            ul.parentNode.classList.add('parent');
        }

        // mark the current page as `active`
        for (const link of this.navbar.querySelectorAll(`a[href="${this.navbar.dataset.url}"]`)) {
            link.parentNode.classList.add('active');
        }

        // find all `active` pages, if any are inside a sub-`ul`, mark the parent as `active` and `open`
        for (const li of this.navbar.getElementsByClassName('active')) {
            let parentLi = li.closest('li.parent');
            if (parentLi) {
                parentLi.classList.add('active', 'open');
            }
        }

        // open any sub-`ul` that is inside an `li` with the class `open`
        for (const li of this.navbar.getElementsByClassName('open')) {
            let ul = li.querySelector('ul');
            if (ul) {
                this.openSubMenu(ul);
            }
        }

        // re-size the navbar every time window is re-sized
        let resizeTimer;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(() => this.adjustNavbarHeight(), 50);
        });

        this.adjustNavbarHeight();

    }

    toggleSubMenu(ul) {
        let hidden = ul.offsetHeight === 0;
        this.closeAllSubMenus();
        if (hidden) {
            this.openSubMenu(ul);
        }
        this.adjustNavbarHeight();
    };

    openSubMenu(ul) {
        ul.style.display = 'block';
        ul.parentElement.classList.add('open');
    };

    closeAllSubMenus() {
        for (const ul of this.navbar.getElementsByTagName('ul')) {
            ul.style.display = 'none';
            ul.parentElement.classList.remove('open');
        }
    };

    // re-size the navbar based off the height of the `li` elements and any open sub-`ul` element
    adjustNavbarHeight() {
        let height = this.navbar.querySelector('li').offsetHeight; // TODO: don't use querySelector, if possible
        for (const ul of this.navbar.getElementsByTagName('ul')) {
            height += ul.offsetHeight;
        }
        this.navbar.style.height = height;
    };

}