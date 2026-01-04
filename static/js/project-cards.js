/**
 * bestIA Engineering - Project Cards & Image Carousel
 * Refactorizado para incluir carrusel de imágenes dinámico.
 */

const projectsData = [
    {
        id: 1,
        title: "Plataforma de Gestión de Condominios",
        category: "Gestión Inmobiliaria",
        icon: "apartment",
        status: { type: "active", label: "En Operación", color: "emerald" },
        client: { name: "Edificio Costanera", location: "Puerto Montt" },
        aiFeature: { title: "Asistente para residentes", type: "Evolución IA" },
        challenge: "Administración compleja de gastos comunes, reservas de espacios y comunicación con residentes.",
        solution: "Sistema web integral para administradores y app para residentes. Control total financiero y operativo.",
        gallery: [
            "https://images.unsplash.com/photo-1560518883-ce09059eeffa?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1460925895917-afdab827c52f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1554469384-e58fac16e23a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
        ]
    },
    {
        id: 2,
        title: "Control de Asistencia Digital",
        category: "Seguridad Privada",
        icon: "security",
        status: { type: "active", label: "En Operación", color: "emerald" },
        client: { name: "Seguridad Austral", location: "Puerto Varas" },
        aiFeature: { title: "Detección de anomalías", type: "Evolución IA" },
        challenge: "Dificultad para controlar turnos y asistencia en múltiples ubicaciones remotas en tiempo real.",
        solution: "App móvil con georeferencia para marcaje de turnos y panel de control central para supervisores.",
        gallery: [
            "https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1563986768609-322da13575f3?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
        ]
    },
    {
        id: 3,
        title: "Sistema de Control de Inventario",
        category: "Logística",
        icon: "inventory_2",
        status: { type: "active", label: "En Operación", color: "emerald" },
        client: { name: "Distribuidora Los Lagos", location: "Puerto Montt" },
        aiFeature: { title: "Predicción de demanda", type: "Evolución IA" },
        challenge: "Pérdidas por descontrol de stock y errores en la entrada/salida manual de datos.",
        solution: "Plataforma digital con lectura de códigos QR/Barras y trazabilidad completa de movimientos.",
        gallery: [
            "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1566576912321-d58ddd7a6047?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1580674684081-7617fbf3d745?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
        ]
    },
    {
        id: 4,
        title: "Despacho y Asistencia en Ruta",
        category: "Field Service",
        icon: "local_shipping",
        status: { type: "integrating", label: "Integrando IA", color: "purple" },
        client: { name: "Logística Sur", location: "Osorno" },
        aiFeature: { title: "Optimización de rutas", type: "Evolución IA" },
        challenge: "Gestión ineficiente de flota y servicios de cambio de baterías a domicilio.",
        solution: "Software moderno de despacho, asignación inteligente de técnicos y seguimiento de servicio.",
        gallery: [
            "https://images.unsplash.com/photo-1616432043562-3671ea2e5242?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1526304640152-d4619684e484?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1494412651409-ae1e0d557e82?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
        ]
    }
];

class ImageCarousel {
    constructor(images, elementId) {
        this.images = images;
        this.currentIndex = 0;
        this.elementId = elementId;
        this.container = null;
    }

    render() {
        // Create unique IDs for accessibility and control
        const carouselId = `carousel-${this.elementId}`;

        // Generate slides HTML
        const slidesHtml = this.images.map((url, index) => `
            <div class="absolute inset-0 transition-opacity duration-500 ease-in-out ${index === 0 ? 'opacity-100 z-10' : 'opacity-0 z-0'}" 
                 data-index="${index}">
                <img src="${url}" 
                     alt="Project screenshot ${index + 1}" 
                     class="w-full h-full object-cover"
                     ${index === 0 ? '' : 'loading="lazy"'}
                >
                <div class="absolute inset-0 bg-gradient-to-t from-surface-dark/90 via-transparent to-transparent"></div>
            </div>
        `).join('');

        // Generate dots HTML
        const dotsHtml = this.images.map((_, index) => `
            <button 
                class="size-2 rounded-full transition-all duration-300 ${index === 0 ? 'bg-white w-4' : 'bg-white/40 hover:bg-white/60'}"
                data-index="${index}"
                aria-label="Go to slide ${index + 1}"
            ></button>
        `).join('');

        return `
            <div class="relative h-48 w-full overflow-hidden group/carousel" id="${carouselId}">
                <!-- Slides -->
                <div class="carousel-track h-full w-full relative">
                    ${slidesHtml}
                </div>

                <!-- Controls (Visible on Hover of Card/Carousel) -->
                
                <!-- Prev Button -->
                <button class="absolute left-2 top-1/2 -translate-y-1/2 z-20 size-8 rounded-full bg-black/30 hover:bg-black/60 backdrop-blur-sm text-white flex items-center justify-center opacity-0 group-hover/carousel:opacity-100 transition-opacity duration-300"
                        onclick="window.carouselControllers['${this.elementId}'].prev()">
                    <span class="material-symbols-outlined text-lg">chevron_left</span>
                </button>

                <!-- Next Button -->
                <button class="absolute right-2 top-1/2 -translate-y-1/2 z-20 size-8 rounded-full bg-black/30 hover:bg-black/60 backdrop-blur-sm text-white flex items-center justify-center opacity-0 group-hover/carousel:opacity-100 transition-opacity duration-300"
                        onclick="window.carouselControllers['${this.elementId}'].next()">
                    <span class="material-symbols-outlined text-lg">chevron_right</span>
                </button>

                <!-- Pagination Dots -->
                <div class="absolute bottom-3 left-1/2 -translate-x-1/2 z-20 flex gap-2">
                    ${dotsHtml}
                </div>

                <!-- Category Badge (Overlay) -->
                <div class="absolute top-3 left-3 z-20 
                            bg-surface-dark/80 backdrop-blur-md border border-white/10 
                            px-3 py-1 rounded-full shadow-lg">
                     <!-- This will be injected by the card, or we can leave it here if we pass category -->
                     <span class="text-xs font-bold text-white uppercase tracking-wider category-label"></span>
                </div>
            </div>
        `;
    }

    updateSlide() {
        const container = document.getElementById(`carousel-${this.elementId}`);
        if (!container) return;

        // Update slides opacity
        const slides = container.querySelectorAll('[data-index]');
        slides.forEach(slide => {
            const index = parseInt(slide.dataset.index);
            // Check if it's a slide div or a button based on class checking
            if (slide.tagName === 'DIV') {
                if (index === this.currentIndex) {
                    slide.classList.remove('opacity-0', 'z-0');
                    slide.classList.add('opacity-100', 'z-10');
                } else {
                    slide.classList.remove('opacity-100', 'z-10');
                    slide.classList.add('opacity-0', 'z-0');
                }
            }
        });

        // Update dots
        const dots = container.querySelectorAll('button[data-index]');
        dots.forEach(dot => {
            const index = parseInt(dot.dataset.index);
            if (index === this.currentIndex) {
                dot.classList.remove('bg-white/40', 'hover:bg-white/60');
                dot.classList.add('bg-white', 'w-4');
            } else {
                dot.classList.remove('bg-white', 'w-4');
                dot.classList.add('bg-white/40', 'hover:bg-white/60');
            }
        });
    }

    next() {
        this.currentIndex = (this.currentIndex + 1) % this.images.length;
        this.updateSlide();
    }

    prev() {
        this.currentIndex = (this.currentIndex - 1 + this.images.length) % this.images.length;
        this.updateSlide();
    }

    // Allow clicking on dots
    goTo(index) {
        this.currentIndex = index;
        this.updateSlide();
    }
}

// Global registry for controllers so inline onClick can find them
window.carouselControllers = {};

function createProjectCard(project) {
    const carousel = new ImageCarousel(project.gallery, project.id);

    // Store controller instance
    window.carouselControllers[project.id] = carousel;

    // Status Colors
    const statusDotColor = project.status.color === 'emerald' ? 'bg-emerald-500' : 'bg-purple-500';
    const statusTextColor = project.status.color === 'emerald' ? 'text-emerald-500' : 'text-purple-400';
    const statusPulse = project.status.color === 'emerald' ? '' : 'animate-pulse';

    // HTML Structure
    const cardHTML = `
        <div class="group bg-surface-dark rounded-xl border border-border-dark overflow-hidden hover:border-primary/50 transition-all duration-300 flex flex-col h-full">
            
            <!-- Carousel Header -->
            <div class="rounded-t-lg overflow-hidden relative">
                 ${carousel.render()}
            </div>

            <!-- Content -->
            <div class="p-6 flex flex-col gap-4 flex-1">
                
                <div class="flex items-start justify-between">
                    <h3 class="text-white text-xl font-bold">${project.title}</h3>
                     <span class="material-symbols-outlined text-slate-600">${project.icon}</span>
                </div>

                <div class="flex flex-col gap-2">
                    <span class="text-xs font-bold text-slate-500 uppercase tracking-wider">El Desafío</span>
                    <p class="text-slate-400 text-sm line-clamp-3">${project.challenge}</p>
                </div>

                <div class="flex flex-col gap-2">
                    <span class="text-xs font-bold text-slate-500 uppercase tracking-wider">Solución</span>
                    <p class="text-slate-300 text-sm line-clamp-3">${project.solution}</p>
                </div>

                <!-- Footer / Status -->
                <div class="mt-auto pt-4 border-t border-border-dark flex items-center justify-between">
                    <div class="flex items-center gap-2">
                        <span class="size-2 rounded-full ${statusDotColor} ${statusPulse}"></span>
                        <span class="${statusTextColor} text-xs font-bold uppercase">${project.status.label}</span>
                    </div>
                    <div class="text-right">
                        <span class="block text-slate-400 text-sm mb-1 line-clamp-1">${project.client.name}</span>
                        <span class="text-primary text-xs font-bold block">${project.aiFeature.type}</span>
                        <span class="text-slate-500 text-xs">${project.aiFeature.title}</span>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Inject category label logic (post-render equivalent for string generation)
    // simpler to just replace the placeholder in the string
    return cardHTML.replace(
        '<span class="text-xs font-bold text-white uppercase tracking-wider category-label"></span>',
        `<span class="text-xs font-bold text-white uppercase tracking-wider category-label">${project.category}</span>`
    );
}

document.addEventListener('DOMContentLoaded', () => {
    const gridContainer = document.getElementById('projects-grid');
    if (gridContainer) {
        gridContainer.innerHTML = projectsData.map(project => createProjectCard(project)).join('');

        // Add event listeners for dots (since inline onClick is messy for dynamic lists of dots)
        // We delegate the click event for dots
        gridContainer.addEventListener('click', (e) => {
            if (e.target.matches('button[data-index]')) {
                // Find closest carousel ID
                const carouselEl = e.target.closest('[id^="carousel-"]');
                if (carouselEl) {
                    const id = carouselEl.id.replace('carousel-', '');
                    const index = parseInt(e.target.dataset.index);
                    if (window.carouselControllers[id]) {
                        window.carouselControllers[id].goTo(index);
                    }
                }
            }
        });
    }
});
