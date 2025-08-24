// ==UserScript==
// @match        https://music.youtube.com/*
// ==/UserScript==

(function () {
    let previousThumbnailUrl = null;

    function getThumbnailUrl() {
        const thumbnailElement = document.querySelector(
            ".thumbnail-image-wrapper .image.style-scope.ytmusic-player-bar",
        );
        if (
            thumbnailElement?.src &&
            thumbnailElement.src.includes("i.ytimg.com")
        ) {
            return thumbnailElement.src;
        }
        return "";
    }

    function cutVideo() {
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

        const thumbnailUrl = getThumbnailUrl();
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
