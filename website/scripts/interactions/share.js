export function loadShareButton() {
    const shareButton = document.getElementById("shareButton");
    const shareButtonLabel = document.getElementById("shareButtonLabel");
    const buttonDuration = 1800;

    let resetTimeout;

    shareButton.addEventListener("click", async () => {
        clearTimeout(resetTimeout);

        try {
            await navigator.clipboard.writeText("https://nichothenacho64.github.io/jobless-graduate/");
            shareButtonLabel.textContent = "Link copied!";
        } catch {
            shareButtonLabel.textContent = "Could not copy link";
        }

        resetTimeout = setTimeout(() => {
            shareButtonLabel.textContent = "Share this story";
        }, buttonDuration);
    });
}
