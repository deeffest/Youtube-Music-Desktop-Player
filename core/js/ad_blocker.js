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

const observer = new MutationObserver((mutations) => {
    let shouldUpdate = false;

    mutations.forEach((mutation) => {
        if (mutation.target.closest(".ytmusic-player")) {
            shouldUpdate = true;
        }
    });

    if (shouldUpdate) {
        skipAd();
    }
});
observer.observe(document.body, {
    childList: true,
    subtree: true,
    attributes: true,
});
