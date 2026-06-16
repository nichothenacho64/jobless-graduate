let navbarThemeFrame;

function updateNavbarTheme() {
    const navbar = document.querySelector("header > nav");
    const openingSection = document.querySelector("#openingSection");

    const newBackgroundTop = openingSection.getBoundingClientRect().bottom;
    const navbarHeight = navbar.offsetHeight;

    navbar.classList.toggle("dark-navbar", newBackgroundTop > navbarHeight);
}

function requestNavbarThemeUpdate() {
    if (navbarThemeFrame) return;

    navbarThemeFrame = requestAnimationFrame(() => {
        navbarThemeFrame = null;
        updateNavbarTheme();
    });
}

export function loadNavbarTheme() {
    const eventOptions = { passive: true };

    updateNavbarTheme();
    window.addEventListener("scroll", requestNavbarThemeUpdate, eventOptions);
    window.addEventListener("resize", requestNavbarThemeUpdate);
}
