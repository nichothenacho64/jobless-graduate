import { loadNavbarTheme } from "./navbar.js";
import { loadTransitions, resetTransitions } from "./scrollytelling.js";
import { loadShareButton } from "./share.js";

window.resetTransitions = resetTransitions;
history.scrollRestoration = "manual";

window.addEventListener("load", () => {
    window.scrollTo(0, 0);
});

document.addEventListener("DOMContentLoaded", () => {
    loadTransitions();
    loadNavbarTheme();
    loadShareButton();
});
