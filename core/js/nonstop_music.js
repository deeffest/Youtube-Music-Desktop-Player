// ==UserScript==
// @match        https://music.youtube.com/*
// ==/UserScript==

function isDialogActive(dialog) {
    const parentDialog = dialog?.closest("tp-yt-paper-dialog");
    return parentDialog && !parentDialog.hasAttribute("aria-hidden");
}

function autoResume() {
    const dialog = document.querySelector("ytmusic-you-there-renderer");

    if (dialog && isDialogActive(dialog)) {
        const confirmButton = dialog.querySelector("yt-button-renderer");
        if (confirmButton) {
            confirmButton.click();
        }

        const video = document.querySelector("video");
        if (video) {
            video.play();
        }
    }
}

const nonstopMusicObserver = new MutationObserver(autoResume);
nonstopMusicObserver.observe(
    document.querySelector("ytmusic-popup-container"),
    {
        childList: true,
        subtree: true,
    },
);
