document.addEventListener('keydown', function(event) {
    if (event.code === 'Space' && !event.target.matches('input, textarea')) {
        event.preventDefault();
        const playPauseButton = document.querySelector('.play-pause-button');
        if (playPauseButton) {
            playPauseButton.click();
        }
    }
    if (event.code === 'ArrowLeft' && !event.ctrlKey) {
        const video = document.querySelector('video');
        if (video) {
            video.currentTime = Math.max(0, video.currentTime - 10);
        }
    }
    if (event.code === 'ArrowRight' && !event.ctrlKey) {
        const video = document.querySelector('video');
        if (video) {
            video.currentTime = Math.min(video.duration, video.currentTime + 10);
        }
    }
    if (event.code === 'ArrowRight' && event.ctrlKey) {
        const nextButton = document.querySelector('.next-button');
        if (nextButton) {
            nextButton.click();
        }
    }
    if (event.code === 'ArrowLeft' && event.ctrlKey) {
        const prevButton = document.querySelector('.previous-button');
        if (prevButton) {
            prevButton.click();
        }
    }
})