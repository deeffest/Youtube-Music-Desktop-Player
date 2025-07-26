// ==UserScript==
// @match        https://music.youtube.com/*
// ==/UserScript==

var style = document.createElement("style");

style.textContent = `
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background-color: transparent;
    }

    ::-webkit-scrollbar-corner {
        background-color: transparent;
    }

    ::-webkit-scrollbar-thumb {
        background-color: rgba(100, 100, 100, 0.6);
        border-radius: 8px;
        border: 2px solid transparent;
        background-clip: padding-box;
        transition: background-color 0.3s ease;
    }

    ::-webkit-scrollbar-thumb:hover {
        background-color: rgba(136, 136, 136, 0.8);
    }
`;

document.head.appendChild(style);
