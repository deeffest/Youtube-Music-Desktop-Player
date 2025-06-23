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

        videoElement.style.opacity = "0";
        videoElement.style.pointerEvents = "none";

        [
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
            ".ytp-large-play-button",
            ".ytp-iv-video-content",
            ".ytp-iv-player-content",
            ".iv-branding",
            ".iv-click-target",
        ].forEach((selector) => document.querySelector(selector)?.remove());

        const thumbnailUrl = getThumbnailUrl();
        const player = document.querySelector(".html5-video-player");

        if (!player) return;

        if (!thumbnailUrl) {
            if (previousThumbnailUrl !== null) {
                previousThumbnailUrl = null;
                player.style.backgroundImage = "";
                player.style.backgroundColor = "black";
            }
            return;
        }

        if (thumbnailUrl === previousThumbnailUrl) return;

        previousThumbnailUrl = thumbnailUrl;

        player.style.backgroundImage = `url(${thumbnailUrl})`;
        player.style.backgroundSize = "contain";
        player.style.backgroundRepeat = "no-repeat";
        player.style.backgroundPosition = "center";
        player.style.backgroundColor = "black";
    }

    const onlyAudioObserver = new MutationObserver(cutVideo);
    onlyAudioObserver.observe(document.querySelector("ytmusic-player-page"), {
        childList: true,
        subtree: true,
    });
})();
