try {
    var adSkipperIntervalID = setInterval(findVideo, 100);
    var adSkipperIterations = 0;
} catch (error) {
    adSkipperIntervalID = setInterval(findVideo, 100);
    adSkipperIterations = 0;
}

if (typeof videoPlayerObserver === 'undefined') {
    var videoPlayerObserver = new MutationObserver(findAndSkipAds);
    var options = {
        attributes: true,
        attributeFilter: ['class'],
        attributeOldValue: true
    };
}

function findAndSkipAds(mutations) {
    for (let mutation of mutations) {
        const videoElement = mutation.target.querySelector("video");
        
        if (mutation.target.classList.contains("ad-showing") && mutation.target.classList.contains("playing-mode")) {
            if (videoElement) {
                if (videoElement.paused && videoElement.readyState >= 2) {
                    videoElement.play().catch(() => {});
                }

                if (videoElement.currentTime < videoElement.duration) {
                    videoElement.currentTime = videoElement.duration;
                }
            }
        }

        if (mutation.target.classList.contains("ended-mode")) {
            const skipButton = document.querySelector(".ytp-ad-skip-button");
            if (skipButton != null) {
                skipButton.click();
            }
        }
    }
}

function findVideo() {
    adSkipperIterations++;
    let videoElements = document.getElementsByTagName('video');
    if (videoElements && videoElements.length) {
        let video = null,
            videoRect = 0;
        for (let i = 0; i < videoElements.length; i++) {
            videoRect = videoElements[i].getBoundingClientRect();
            if (videoElements[i].src.indexOf("music.youtube.com") == -1) {
                if (videoRect.width > 0 && videoRect.height > 0) {
                    video = videoElements[i];
                    break;
                }
            } else {
                video = videoElements[i];
                break;
            }
        }
        if (!video) video = videoElements[0];
        videoPlayerObserver.observe(video.parentNode.parentNode, options);
        clearInterval(adSkipperIntervalID);
    }
    if (adSkipperIterations >= 500) clearInterval(adSkipperIntervalID);
}
