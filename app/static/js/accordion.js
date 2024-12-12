document.addEventListener('DOMContentLoaded', () => {
    const hash = window.location.hash;
    if (hash) {
        const target = document.querySelector(hash);
        if (target && target.classList.contains('accordion-collapse')) {
            const accordionButton = target.previousElementSibling.querySelector('.accordion-button');
            if (accordionButton) {
                accordionButton.click(); // Opens the accordion
            }
        }
    }
});