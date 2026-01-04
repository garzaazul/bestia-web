// bestIA Engineering - Custom JS
// Scripts adicionales

document.addEventListener('DOMContentLoaded', () => {

    // Funnel de Conversión: Academy CTA -> Contact Form
    const academyBtn = document.getElementById('btn-academy-cta');
    const contactForm = document.getElementById('contact-form');
    // Note: The select element ID is id_interest based on previous view_file
    const interestSelect = document.getElementById('id_interest');
    const nameInput = document.getElementById('id_name');

    if (academyBtn && contactForm) {
        academyBtn.addEventListener('click', (e) => {
            e.preventDefault();

            // 1. Scroll suave
            contactForm.scrollIntoView({ behavior: 'smooth' });

            // 2. Pre-seleccionar opción
            if (interestSelect) {
                // 'academy' is the value option we saw in the previous file view
                interestSelect.value = 'academy';

                // Visual feedback (opcional): flash effect
                interestSelect.classList.add('ring-2', 'ring-primary', 'ring-offset-2', 'ring-offset-background-dark');
                setTimeout(() => {
                    interestSelect.classList.remove('ring-2', 'ring-primary', 'ring-offset-2', 'ring-offset-background-dark');
                }, 1000);
            }

            // 3. Foco en el input
            if (nameInput) {
                // Small delay to allow scroll to start/finish slightly
                setTimeout(() => {
                    nameInput.focus();
                }, 800);
            }
        });
    }
});
