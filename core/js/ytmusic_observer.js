if (typeof qt !== "undefined" && qt.webChannelTransport) {
    new QWebChannel(qt.webChannelTransport, function (channel) {
        window.backend = channel.objects.backend;

        let lastState = "";
        let lastTrackInfo = {
            title: "",
            artist: "",
            thumbnailUrl: "",
        };
        let lastTrackProgress = {
            currentTime: "",
            totalTime: "",
        };

        let debounceTimer = null;
        const DEBOUNCE_DELAY = 200;

        function getThumbnailOrCoverUrl() {
            const cover = document.querySelector("#song-image #img");
            if (cover?.src.includes("lh3.googleusercontent.com")) {
                return cover.src;
            }

            const thumb = document.querySelector(
                ".thumbnail-image-wrapper .image.style-scope.ytmusic-player-bar",
            );
            if (thumb?.src.includes("i.ytimg.com")) {
                return thumb.src;
            }

            return "";
        }

        function updateTrackInfo() {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                const titleEl = document.querySelector(
                    ".title.style-scope.ytmusic-player-bar",
                );
                const authorEl = document.querySelector(
                    ".byline.style-scope.ytmusic-player-bar",
                );

                let title = titleEl?.textContent.trim() || "";
                let author = authorEl?.textContent.trim() || "";
                let thumbnailUrl = getThumbnailOrCoverUrl();

                const allEmpty = !title && !author && !thumbnailUrl;
                const allFilled = title && author && thumbnailUrl;

                if (!(allEmpty || allFilled)) {
                    return;
                }

                const changed =
                    title !== lastTrackInfo.title ||
                    author !== lastTrackInfo.author ||
                    thumbnailUrl !== lastTrackInfo.thumbnailUrl;

                if (changed) {
                    backend.track_info_changed(title, author, thumbnailUrl);
                    lastTrackInfo = { title, author, thumbnailUrl };
                }
            }, DEBOUNCE_DELAY);
        }

        function updateVideoState() {
            const video = document.querySelector("video");
            let newState = "NoVideo";

            if (video && video.readyState === 4) {
                newState = video.paused ? "VideoPaused" : "VideoPlaying";
            }

            if (newState !== lastState) {
                backend.video_state_changed(newState);
                lastState = newState;
            }
        }

        function updateTrackProgress() {
            const timeEl = document.querySelector(
                ".time-info.style-scope.ytmusic-player-bar",
            );
            const timeText = timeEl?.textContent.trim();
            const parts = timeText?.split("/") ?? [];

            if (parts.length === 2) {
                const [currentTime, totalTime] = parts.map((t) => t.trim());
                if (
                    currentTime !== lastTrackProgress.currentTime ||
                    totalTime !== lastTrackProgress.totalTime
                ) {
                    backend.track_progress_changed(currentTime, totalTime);
                    lastTrackProgress = { currentTime, totalTime };
                }
            }
        }

        const playerBar = document.querySelector(
            ".middle-controls.style-scope.ytmusic-player-bar",
        );
        if (playerBar) {
            new MutationObserver(updateTrackInfo).observe(playerBar, {
                childList: true,
                subtree: true,
            });
        }

        const playerPage = document.querySelector("ytmusic-player-page");
        if (playerPage) {
            new MutationObserver(updateVideoState).observe(playerPage, {
                childList: true,
                subtree: true,
            });
        }

        const progressEl = document.querySelector(
            ".time-info.style-scope.ytmusic-player-bar",
        );
        if (progressEl) {
            new MutationObserver(updateTrackProgress).observe(progressEl, {
                characterData: true,
                subtree: true,
            });
        }

        updateTrackInfo();
        updateVideoState();
    });
}
