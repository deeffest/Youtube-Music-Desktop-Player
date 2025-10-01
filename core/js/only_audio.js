// ==UserScript==
// @match        https://music.youtube.com/*
// ==/UserScript==

(function () {
    let previousThumbnailUrl = null;
    const useHD = window.ONLY_AUDIO_SETTINGS?.useHDThumbnails ?? 0;

    function getHDThumbnailUrl(url) {
        return new Promise((resolve) => {
            if (!useHD) return resolve(url);

            const hdUrl = url.replace("sddefault.jpg", "maxresdefault.jpg");
            const img = new Image();

            img.onload = () => {
                if (img.naturalWidth >= 1280 && img.naturalHeight >= 720) {
                    resolve(hdUrl);
                } else {
                    resolve(url);
                }
            };

            img.onerror = () => resolve(url);
            img.src = hdUrl;
        });
    }

    async function getThumbnailUrl() {
        const thumbnailElement = document.querySelector(
            ".thumbnail-image-wrapper .image.style-scope.ytmusic-player-bar",
        );

        if (
            !thumbnailElement?.src ||
            !thumbnailElement.src.includes("i.ytimg.com")
        ) {
            return "";
        }

        const url = thumbnailElement.src;
        return await getHDThumbnailUrl(url);
    }

    async function cutVideo() {
        const videoElement = document.querySelector("video");
        if (!videoElement) return;

        [
            ".iv-branding",
            ".ytp-spinner",
            ".ytp-large-play-button",
            ".ytp-cards-button",
            ".ytp-cards-teaser",
            ".ytp-paid-content-overlay-link",
        ].forEach((selector) => document.querySelector(selector)?.remove());

        const player = document.querySelector(".html5-video-player");
        if (!player) return;

        const thumbnailUrl = await getThumbnailUrl();
        if (!thumbnailUrl) {
            if (previousThumbnailUrl !== null) {
                previousThumbnailUrl = null;
                player.style.backgroundImage = "";
            }
            return;
        }

        if (thumbnailUrl === previousThumbnailUrl) return;
        previousThumbnailUrl = thumbnailUrl;
        player.style.background = `center/contain no-repeat url(${thumbnailUrl})`;
    }

    const onlyAudioObserver = new MutationObserver(cutVideo);
    onlyAudioObserver.observe(document.querySelector("ytmusic-player-page"), {
        childList: true,
        subtree: true,
    });
})();
