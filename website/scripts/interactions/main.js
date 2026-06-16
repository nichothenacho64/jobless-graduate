import { loadNavbarTheme } from "./navbar.js";
import { loadTransitions, resetTransitions } from "./scrollytelling.js";
import { loadShareButton } from "./share.js";

window.resetTransitions = resetTransitions;

document.addEventListener("DOMContentLoaded", () => {
    loadTransitions();
    loadNavbarTheme();
    loadShareButton();
});
