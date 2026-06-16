let transitionObserver;

function revealSections(observedSections) {
    for (let observedSection of observedSections) {
        if (!observedSection.isIntersecting) {
            continue;
        }

        observedSection.target.classList.add("visible"); // trigger the CSS reveal once a section enters the viewport
    }
}

export function loadTransitions() {
    const observerOptions = { threshold: 0.15 }; // low threshold = reveal starts before the section is fully on the screen

    transitionObserver = new IntersectionObserver(revealSections, observerOptions);
    const sections = document.querySelectorAll(".scrollable-section");

    for (let section of sections) {
        transitionObserver.observe(section);
    }
}

export function resetTransitions() {
    const sections = document.querySelectorAll(".scrollable-section");
    const transitionDelay = 600;

    transitionObserver.disconnect(); // pause while the jump scroll settles, then let reveals run again

    for (let section of sections) {
        section.classList.remove("visible");
    }

    setTimeout(() => {
        for (let section of sections) {
            transitionObserver.observe(section);
        }
    }, transitionDelay);
}
