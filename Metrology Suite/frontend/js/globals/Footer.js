class Footer {

    constructor(footer) {
        this.footer = footer;
        this.initialize();
    }

    initialize() {

        // if no element was instantiated, return null
        if (!this.footer) return null;

        // re-size the navbar every time window is re-sized
        let resizeTimer;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(() => this.adjustBodyPaddingBottom(), 50);
        });

        this.adjustBodyPaddingBottom();

    }

    adjustBodyPaddingBottom() {
        let body = document.getElementsByTagName('body')[0];
        if (body) {
            body.style.paddingBottom = this.footer.offsetHeight;
        }
    };

}