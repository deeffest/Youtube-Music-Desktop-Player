(function () {
    let previousThumbnailUrl = null;

    function getThumbnailUrl() {
        var fallbackElement = document.querySelector(
            ".thumbnail-image-wrapper .image.style-scope.ytmusic-player-bar",
        );

        if (fallbackElement) {
            const thumbnailUrl = fallbackElement.src;
            if (thumbnailUrl !== previousThumbnailUrl) {
                previousThumbnailUrl = thumbnailUrl;
            }
            return thumbnailUrl;
        }
        return "";
    }

    function cutVideo() {
        const videoElement = document.querySelector("video");
        if (!videoElement) return;

        const unnecessarySelectors = [
            ".ytp-suggested-action",
            ".ytp-suggested-action-badge",
            ".ytp-playlist-menu-button",
            ".ytp-chrome-top",
            ".ytp-title-channel",
            ".ytp-title-channel-logo",
            ".ytp-paid-content-overlay",
            ".ytp-cards-teaser",
            ".ytp-player-content",
            ".ytp-caption-window-container",
            ".ytp-spinner",
        ];

        unnecessarySelectors.forEach((selector) => {
            const elements = document.querySelectorAll(selector);
            elements.forEach((element) => {
                element.remove();
            });
        });

        videoElement.style.opacity = "0";
        videoElement.style.pointerEvents = "none";

        const thumbnailUrl = getThumbnailUrl();
        if (thumbnailUrl) {
            const player = document.querySelector(".html5-video-player");
            if (player) {
                player.style.backgroundImage = `url(${thumbnailUrl})`;
                player.style.backgroundSize = "contain";
                player.style.backgroundRepeat = "no-repeat";
                player.style.backgroundPosition = "center";
                player.style.backgroundColor = "black";
            }
        }
    }

    const observer = new MutationObserver((mutations) => {
        let shouldUpdate = false;

        mutations.forEach((mutation) => {
            if (mutation.target.closest(".ytmusic-player")) {
                shouldUpdate = true;
            }
        });

        if (shouldUpdate) {
            cutVideo();
        }
    });
    observer.observe(document.body, {
        childList: true,
        subtree: true,
    });
})();
