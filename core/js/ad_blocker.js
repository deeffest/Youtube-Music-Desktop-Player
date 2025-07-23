// ==UserScript==
// @match        https://music.youtube.com/*
// ==/UserScript==

function skipAd() {
    const adShowing = document.querySelector(".ad-showing");
    const pieCountdown = document.querySelector(
        ".ytp-ad-timed-pie-countdown-container",
    );
    const surveyQuestions = document.querySelector(".ytp-ad-survey-questions");
    if (adShowing === null && pieCountdown === null && surveyQuestions === null)
        return;

    const playerEl = document.querySelector("#movie_player");
    if (playerEl === null) {
        return;
    }

    const adVideo = document.querySelector(
        "#movie_player video.html5-main-video",
    );
    if (
        adVideo === null ||
        !adVideo.src ||
        adVideo.paused ||
        isNaN(adVideo.duration)
    )
        return;

    adVideo.muted = true;
    adVideo.currentTime = adVideo.duration;

    const skipButton = document.querySelector(".ytp-ad-skip-button");
    if (skipButton) skipButton.click();
}

const adBlockerObserver = new MutationObserver(skipAd);
adBlockerObserver.observe(document.querySelector("ytmusic-player-page"), {
    childList: true,
    subtree: true,
});
