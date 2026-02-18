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

document.addEventListener('DOMContentLoaded', function() {
        // 1. On cherche l'élément par son ID
        var tagsElement = document.getElementById('tags-select');
        
        // 2. On vérifie s'il existe
        if (tagsElement) {
            console.log("✅ Champ Tags trouvé ! Activation de Choices.js");
            
            var choices = new Choices(tagsElement, {
                removeItemButton: true,
                searchEnabled: true,
                placeholder: true,
                placeholderValue: 'Rechercher et ajouter des genres...',
                itemSelectText: '',
                noResultsText: 'Aucun genre trouvé',
            });
        } else {
            console.error("❌ ERREUR : Le champ avec id='tags-select' est introuvable dans le HTML.");
        }
    });