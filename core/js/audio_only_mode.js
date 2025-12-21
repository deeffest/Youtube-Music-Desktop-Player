// ==UserScript==
// @match        https://music.youtube.com/*
// ==/UserScript==

(function () {
    let previousThumbnailUrl = null;
    const useHD = window.ONLY_AUDIO_SETTINGS?.useHDThumbnails ?? 0;

    async function getThumbnailUrl(src) {
        const id = src.match(/\/vi\/([^/]+)\//)?.[1];
        if (!id) return "";

        const hq720 = `https://i1.ytimg.com/vi/${id}/hq720.jpg`;
        const hqdefault = `https://i1.ytimg.com/vi/${id}/hqdefault.jpg`;

        if (!useHD) return hqdefault;

        return await new Promise((resolve) => {
            const img = new Image();
            img.onload = () => {
                resolve(img.naturalWidth >= 720 ? hq720 : hqdefault);
            };
            img.onerror = () => resolve(hqdefault);
            img.src = hq720;
        });
    }

    async function cutVideo(src) {
        const player = document.querySelector(".html5-video-player");
        if (player && src && src !== previousThumbnailUrl) {
            player.style.backgroundImage = "";
            previousThumbnailUrl = null;
        }

        const url = await getThumbnailUrl(src);
        if (!url) return;

        previousThumbnailUrl = src;

        Object.assign(player.style, {
            backgroundImage: `url(${url})`,
            backgroundSize: "cover",
            backgroundPosition: "center",
            backgroundRepeat: "no-repeat",
            width: "100%",
            height: "100%",
            position: "absolute",
            top: "0",
            left: "0",
        });
    }

    const thumbEl = document.querySelector(
        ".thumbnail-image-wrapper .image.style-scope.ytmusic-player-bar",
    );

    if (thumbEl) {
        new MutationObserver((mutations) => {
            for (const m of mutations) {
                if (m.attributeName === "src") {
                    cutVideo(thumbEl.src);
                }
            }
        }).observe(thumbEl, { attributes: true });
    }
})();
