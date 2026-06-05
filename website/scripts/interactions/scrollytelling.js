let transitionObserver;

function revealSections(observedSections) {
    for (let observedSection of observedSections) {
        if (!observedSection.isIntersecting) {
            continue;
        }

        observedSection.target.classList.add("visible");
    }
}

function loadTransitions() {
    const observerOptions = { threshold: 0.15 };

    transitionObserver = new IntersectionObserver(revealSections, observerOptions);
    const sections = document.querySelectorAll(".scrollable-section");

    for (let section of sections) {
        transitionObserver.observe(section);
    }
}

function resetTransitions() {
    const sections = document.querySelectorAll(".scrollable-section");

    transitionObserver.disconnect();

    for (let section of sections) {
        section.classList.remove("visible");
    }

    const transitionDelay = 600;

    setTimeout(() => {
        for (let section of sections) {
            transitionObserver.observe(section);
        }
    }, transitionDelay);
}

document.addEventListener("DOMContentLoaded", () => {
    loadTransitions();
});