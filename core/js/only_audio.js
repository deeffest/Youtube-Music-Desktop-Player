(function () {
    let previousThumbnailUrl = null;

    async function getThumbnailUrl() {
        var fallbackElement = document.querySelector('.thumbnail-image-wrapper .image.style-scope.ytmusic-player-bar');
        if (fallbackElement) {
            const thumbnailUrl = fallbackElement.src;

            if (thumbnailUrl !== previousThumbnailUrl) {
                previousThumbnailUrl = thumbnailUrl;
            }
            
            return thumbnailUrl;
        }

        return '';
    }

    async function configureVideo() {
        const videoElement = document.querySelector("video");
        if (videoElement) {
            const unnecessarySelectors = [
                '.ytp-suggested-action',
                '.ytp-suggested-action-badge',
                '.ytp-playlist-menu-button',
                '.ytp-chrome-top',
                '.ytp-title-channel',
                '.ytp-title-channel-logo',
                '.ytp-paid-content-overlay',
                '.ytp-cards-teaser',
                '.annotation',
                '.iv-branding',
                '.ytp-caption-window-container',
            ];
            unnecessarySelectors.forEach(selector => {
                const elements = document.querySelectorAll(selector);
                
                elements.forEach(element => {
                    element.remove();
                });
            });
            
            videoElement.style.opacity = "0";
            videoElement.style.pointerEvents = "none";

            const thumbnailUrl = await getThumbnailUrl();
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
    }

    const observer = new MutationObserver(() => {
        configureVideo();
    });
    observer.observe(document.body, { childList: true, subtree: true });
})();