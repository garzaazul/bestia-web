document.addEventListener('DOMContentLoaded', async () => {
    // Wait for the tsparticles global to be available
    // We assume tsparticles-slim is loaded via CDN in the template

    // Check if container exists
    const container = document.getElementById('hero-particles');
    if (!container) return;

    await tsParticles.load("hero-particles", {
        fullScreen: { enable: false }, // Confine to container
        fpsLimit: 120,
        background: {
            color: "transparent", // Use the section's blue background
        },
        particles: {
            number: {
                value: 60, // Balanced density
                density: {
                    enable: true,
                    area: 800
                }
            },
            color: {
                value: ["#22d3ee", "#0ea5e9"] // Tailwind Cyan-400, Sky-500 (Subtle Blue/Cyan)
            },
            shape: {
                type: "circle"
            },
            opacity: {
                value: 0.3,
                random: true,
                animation: {
                    enable: true,
                    speed: 0.5,
                    minimumValue: 0.1,
                    sync: false
                }
            },
            size: {
                value: { min: 1, max: 3 },
                random: true
            },
            links: {
                enable: true,
                distance: 150,
                color: "#2dd4bf", // Teal-400
                opacity: 0.15, // Very subtle lines
                width: 1
            },
            move: {
                enable: true,
                speed: 0.6, // Slow movement
                direction: "none",
                random: true,
                straight: false,
                outModes: "bounce",
                attract: {
                    enable: false,
                    rotateX: 600,
                    rotateY: 1200
                }
            }
        },
        interactivity: {
            events: {
                onHover: {
                    enable: true,
                    mode: "grab" // Subtle connection on hover
                },
                onClick: {
                    enable: false,
                    mode: "push"
                },
                resize: true
            },
            modes: {
                grab: {
                    distance: 140,
                    links: {
                        opacity: 0.4
                    }
                }
            }
        },
        detectRetina: true
    });
});
