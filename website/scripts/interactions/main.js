import { loadNavbarTheme } from "./navbar.js";
import { loadTransitions, resetTransitions } from "./scrollytelling.js";

window.resetTransitions = resetTransitions;

document.addEventListener("DOMContentLoaded", () => {
    loadTransitions();
    loadNavbarTheme();
});
