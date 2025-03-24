var script = document.createElement("script");

if (window.trustedTypes && window.trustedTypes.createPolicy) {
    const policy = window.trustedTypes.createPolicy("default", {
        createScriptURL: (url) => url,
    });
    script.src = policy.createScriptURL("qrc:///qtwebchannel/qwebchannel.js");
} else {
    script.src = "qrc:///qtwebchannel/qwebchannel.js";
}

script.onload = function () {
    new QWebChannel(qt.webChannelTransport, function (channel) {
        window.backend = channel.objects.backend;

        var lastState = "";
        var lastTrackInfo = {
            title: "",
            author: "",
            thumbnailUrl: "",
        };
        var lastLikeStatus = "";
        var lastTrackProgress = {
            currentTime: "",
            totalTime: "",
        };

        function updateVideoState() {
            var player = document.getElementById("player");
            var newState = "NoVideo";
            if (player) {
                var video = document.getElementsByTagName("video")[0];
                if (video) {
                    newState =
                        video.readyState === 4
                            ? video.paused
                                ? "VideoPaused"
                                : "VideoPlaying"
                            : "NoVideo";
                }
            }
            if (newState !== lastState) {
                backend.video_state_changed(newState);
                lastState = newState;
            }
            updateTrackInfo();
        }

        function getThumbnailOrCoverUrl() {
            var thumbnailElement = document.querySelector("#song-image #img");
            if (thumbnailElement) {
                if (
                    thumbnailElement.src &&
                    !thumbnailElement.src.startsWith("data:image/gif")
                ) {
                    return thumbnailElement.src;
                }
            }

            var fallbackElement = document.querySelector(
                ".thumbnail-image-wrapper .image.style-scope.ytmusic-player-bar",
            );
            if (fallbackElement) {
                return fallbackElement.src;
            }

            return "";
        }

        function updateTrackInfo() {
            var titleElement = document.querySelector(
                ".title.style-scope.ytmusic-player-bar",
            );
            var authorElement = document.querySelector(
                ".byline.style-scope.ytmusic-player-bar",
            );
            var thumbnailUrl = getThumbnailOrCoverUrl();

            var trackInfo = {
                title: titleElement ? titleElement.textContent.trim() : "",
                author: authorElement ? authorElement.textContent.trim() : "",
                thumbnailUrl: thumbnailUrl || "",
            };

            if (
                trackInfo.title !== lastTrackInfo.title ||
                trackInfo.author !== lastTrackInfo.author ||
                trackInfo.thumbnailUrl !== lastTrackInfo.thumbnailUrl
            ) {
                backend.track_info_changed(
                    trackInfo.title,
                    trackInfo.author,
                    trackInfo.thumbnailUrl,
                );
                lastTrackInfo = trackInfo;
            }
        }

        function updateLikeStatus() {
            var likeButton = document.querySelector(
                "ytmusic-like-button-renderer#like-button-renderer",
            );
            if (likeButton) {
                var likeStatus = likeButton.getAttribute("like-status");
                if (likeStatus && likeStatus !== lastLikeStatus) {
                    likeStatus =
                        likeStatus.toLowerCase().charAt(0).toUpperCase() +
                        likeStatus.slice(1).toLowerCase();
                    backend.like_status_changed(likeStatus);
                    lastLikeStatus = likeStatus;
                }
            }
        }

        function updateTrackProgress() {
            var timeInfoElement = document.querySelector(
                ".time-info.style-scope.ytmusic-player-bar",
            );
            if (timeInfoElement) {
                var timeText = timeInfoElement.textContent.trim();
                var timeParts = timeText.split("/");
                if (timeParts.length === 2) {
                    var currentTime = timeParts[0].trim();
                    var totalTime = timeParts[1].trim();

                    if (
                        currentTime !== lastTrackProgress.currentTime ||
                        totalTime !== lastTrackProgress.totalTime
                    ) {
                        backend.track_progress_changed(currentTime, totalTime);
                        lastTrackProgress = { currentTime, totalTime };
                    }
                }
            }
        }

        var likeObserver = new MutationObserver(updateLikeStatus);
        var likeButton = document.querySelector(
            "ytmusic-like-button-renderer#like-button-renderer",
        );
        if (likeButton) {
            likeObserver.observe(likeButton, {
                attributes: true,
                attributeFilter: ["like-status"],
            });
        }

        var progressObserver = new MutationObserver(updateTrackProgress);
        var timeInfoElement = document.querySelector(
            ".time-info.style-scope.ytmusic-player-bar",
        );
        if (timeInfoElement) {
            progressObserver.observe(timeInfoElement, {
                characterData: true,
                subtree: true,
            });
        }

        const observer = new MutationObserver((mutations) => {
            let shouldUpdate = false;

            mutations.forEach((mutation) => {
                if (mutation.target.closest("ytmusic-player-page")) {
                    shouldUpdate = true;
                }
            });

            if (shouldUpdate) {
                updateVideoState();
            }
        });
        observer.observe(document.body, {
            childList: true,
            subtree: true,
        });
        updateVideoState();
    });
};
document.head.appendChild(script);
