if (typeof qt !== "undefined" && qt.webChannelTransport) {
    new QWebChannel(qt.webChannelTransport, (channel) => {
        const backend = channel.objects.backend;
        let lastState = "",
            lastTrackInfo = {},
            lastTrackProgress = {};
        let debounceTimer = null,
            DEBOUNCE_DELAY = 500;

        const getThumbnailOrCoverUrl = () => {
            const src = document.querySelector(
                ".thumbnail-image-wrapper .image.style-scope.ytmusic-player-bar",
            )?.src;
            return src?.includes("lh3.googleusercontent.com")
                ? src.replace(/w\d+-h\d+/, "w544-h544")
                : src || "";
        };

        const getVideoId = () => {
            const link = document.querySelector(".ytp-title-link");
            return link?.href
                ? new URL(link.href).searchParams.get("v") || ""
                : "";
        };

        const updateTrackInfo = () => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                const title =
                    document
                        .querySelector(".title.style-scope.ytmusic-player-bar")
                        ?.textContent.trim() || "";
                const author =
                    document
                        .querySelector(".byline.style-scope.ytmusic-player-bar")
                        ?.textContent.trim() || "";
                const thumbnailUrl = getThumbnailOrCoverUrl();
                const videoId = getVideoId();
                const changed =
                    title !== lastTrackInfo.title ||
                    author !== lastTrackInfo.author ||
                    thumbnailUrl !== lastTrackInfo.thumbnailUrl ||
                    videoId !== lastTrackInfo.videoId;

                if (!changed) return;
                backend.track_info_changed(
                    title,
                    author,
                    thumbnailUrl,
                    videoId,
                );
                lastTrackInfo = { title, author, thumbnailUrl, videoId };
            }, DEBOUNCE_DELAY);
        };

        const updateVideoState = () => {
            const video = document.querySelector("video");
            const state =
                video?.readyState === 4
                    ? video.paused
                        ? "VideoPaused"
                        : "VideoPlaying"
                    : "NoVideo";
            if (state !== lastState) {
                backend.video_state_changed(state);
                lastState = state;
            }
        };

        const updateTrackProgress = () => {
            const [currentTime, totalTime] =
                document
                    .querySelector(".time-info.style-scope.ytmusic-player-bar")
                    ?.textContent.trim()
                    .split("/")
                    .map((t) => t.trim()) || [];
            if (
                currentTime !== lastTrackProgress.currentTime ||
                totalTime !== lastTrackProgress.totalTime
            ) {
                backend.track_progress_changed(currentTime, totalTime);
                lastTrackProgress = { currentTime, totalTime };
            }
        };

        const observe = (el, fn, opts) =>
            el && new MutationObserver(fn).observe(el, opts);

        observe(
            document.querySelector(
                ".middle-controls.style-scope.ytmusic-player-bar",
            ),
            updateTrackInfo,
            { childList: true, subtree: true },
        );
        observe(document.querySelector("ytmusic-player"), updateVideoState, {
            childList: true,
            subtree: true,
        });
        observe(
            document.querySelector(".time-info.style-scope.ytmusic-player-bar"),
            updateTrackProgress,
            { characterData: true, subtree: true },
        );

        updateTrackInfo();
        updateVideoState();
    });
}
