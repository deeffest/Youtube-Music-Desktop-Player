var style = document.createElement('style');

style.textContent = `
    ::-webkit-scrollbar {
        width: 10px;
    }    
    ::-webkit-scrollbar:horizontal {
        height: 10px;
    }
    ::-webkit-scrollbar-corner {
        background-color: transparent;
    }
    ::-webkit-scrollbar-track {
        background-color: transparent;
    }
    ::-webkit-scrollbar-thumb {
        background-color: #666;
    }
    ::-webkit-scrollbar-thumb:hover {
        background-color: #888;
    }
`;

document.head.appendChild(style);

document.addEventListener('selectstart', function(e) {
    e.preventDefault();
});