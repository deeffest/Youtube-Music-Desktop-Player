(query) => {
    const input = document.querySelector('ytmusic-search-box input#input');
    if (!input) return;
    input.focus();
    document.execCommand('selectAll');
    document.execCommand('insertText', false, query);
}
