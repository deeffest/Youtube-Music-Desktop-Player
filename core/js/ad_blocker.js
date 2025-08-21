// ==UserScript==
// @match        https://music.youtube.com/*
// ==/UserScript==

(function () {
    "use strict";

    const AD_SELECTORS = [
        ".ad-showing",
        ".ad-interrupting",
        ".ytp-ad-text",
        ".ytp-ad-timed-pie-countdown-container",
        ".ytp-ad-survey-questions",
    ];

    const isAdPlaying = () => {
        const player = document.querySelector("#movie_player");
        if (!player) return false;
        return AD_SELECTORS.some(
            (sel) => player.matches(sel) || player.querySelector(sel),
        );
    };

    const skipAd = () => {
        const player = document.querySelector("#movie_player");
        if (!player) return;

        const adVideo = player.querySelector("video.html5-main-video");
        if (adVideo && !isNaN(adVideo.duration) && isFinite(adVideo.duration)) {
            adVideo.currentTime = adVideo.duration;
        }

        const skipButton = player.querySelector(".ytp-ad-skip-button");
        if (skipButton) skipButton.click();
    };

    const adBlockerObserver = new MutationObserver((mutations) => {
        for (const mutation of mutations) {
            for (const node of mutation.addedNodes) {
                if (
                    node.nodeType === Node.ELEMENT_NODE &&
                    AD_SELECTORS.some(
                        (selector) =>
                            node.matches(selector) ||
                            node.querySelector(selector),
                    )
                ) {
                    skipAd();
                    return;
                }
            }
        }
    });

    adBlockerObserver.observe(document.documentElement, {
        childList: true,
        subtree: true,
    });

    const muteIfAd = (video) => {
        if (!video) return;

        if (isAdPlaying()) {
            video.muted = true;
        }
    };

    document.addEventListener(
        "loadedmetadata",
        (e) => {
            if (e.target.tagName === "VIDEO") {
                muteIfAd(e.target);
            }
        },
        true,
    );
})();
