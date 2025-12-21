// ==UserScript==
// @match        https://music.youtube.com/*
// ==/UserScript==

(function () {
    const isDialogActive = (d) =>
        d?.closest("tp-yt-paper-dialog") &&
        !d.closest("tp-yt-paper-dialog").hasAttribute("aria-hidden");

    const autoResume = () => {
        const dialog = document.querySelector("ytmusic-you-there-renderer");
        if (!isDialogActive(dialog)) return;

        dialog.querySelector("yt-button-renderer")?.click();
        document.querySelector("video")?.play();
    };

    new MutationObserver(autoResume).observe(
        document.querySelector("ytmusic-popup-container"),
        { childList: true, subtree: true },
    );
})();
