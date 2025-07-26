// ==UserScript==
// @match        https://music.youtube.com/*
// ==/UserScript==

(function () {
    "use strict";

    const video = document.querySelector('video');

    const origAddSourceBuffer = MediaSource.prototype.addSourceBuffer;
    MediaSource.prototype.addSourceBuffer = function (mime) {
        if (mime.includes("video")) {
            const fakeBuffer = {
                appendBuffer() {
                    this.updating = false;
                    this._updateEnd();
                },
                remove() {},
                abort() {},
                updating: false,
                buffered: {
                    length: 1,
                    start: () => 0,
                    end: () => {
                        const video = document.querySelector('video');
                        return video ? video.duration : 0;
                    },
                },
                addEventListener() {},
                removeEventListener() {},
                dispatchEvent() {
                    return false;
                },
                _updateEnd() {
                    const evt = new Event("updateend");
                    this.dispatchEvent(evt);
                },
            };
            return fakeBuffer;
        }

        return origAddSourceBuffer.call(this, mime);
    };

    const origXHROpen = XMLHttpRequest.prototype.open;
    XMLHttpRequest.prototype.open = function (method, url) {
        if (url.includes("mime=video")) {
            this.abort();
            return;
        }
        return origXHROpen.apply(this, arguments);
    };

    const origFetch = window.fetch;
    window.fetch = async function (...args) {
        const req = args[0];
        const url = typeof req === "string" ? req : req?.url || "";

        if (url.includes("mime=video")) {
            return new Response(null, { status: 204 });
        }

        return origFetch.apply(this, args);
    };
})();
