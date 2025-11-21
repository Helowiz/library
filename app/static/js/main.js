document.addEventListener('DOMContentLoaded', () => {

    const flashContainer = document.getElementById('flash-container');
    
    if (!flashContainer) {
        return;
    }

    const flashMessages = flashContainer.querySelectorAll('.flash-message');

    flashMessages.forEach(flash => {
        
        const autoCloseTimer = setTimeout(() => {
            closeFlash(flash);
        }, 5000);

        const closeButton = flash.querySelector('.flash-close');
        if (closeButton) {
            closeButton.addEventListener('click', () => {
                clearTimeout(autoCloseTimer);
                closeFlash(flash);
            });
        }
    });

    /**
     * Fonction pour fermer un message flash avec une animation
     * @param {HTMLElement} flashElement 
     */
    function closeFlash(flashElement) {
        flashElement.classList.add('fade-out');

        flashElement.addEventListener('animationend', () => {
            flashElement.remove();

            if (flashContainer.children.length === 0) {
                flashContainer.remove();
            }
        }, { once: true });
    }
});