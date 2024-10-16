var script = document.createElement('script');

if (window.trustedTypes && window.trustedTypes.createPolicy) {
    const policy = window.trustedTypes.createPolicy('default', {
        createScriptURL: (url) => url
    });
    script.src = policy.createScriptURL('qrc:///qtwebchannel/qwebchannel.js');
} else {
    script.src = 'qrc:///qtwebchannel/qwebchannel.js';
}

script.onload = function() {
    new QWebChannel(qt.webChannelTransport, function(channel) {
        window.backend = channel.objects.backend;

        var lastState = '';
        var lastTrackInfo = {
            title: '',
            author: '',
            thumbnailUrl: ''
        };
        var lastLikeStatus = '';

        function updateVideoState() {
            var player = document.getElementById('player');
            var newState = 'NoVideo';
            if (player) {
                var video = document.getElementsByTagName('video')[0];
                if (video) {
                    newState = (video.readyState === 4) ? (video.paused ? 'VideoPaused' : 'VideoPlaying') : 'NoVideo';
                }
            }
            if (newState !== lastState) {
                backend.video_state_changed(newState);
                lastState = newState;
            }
            updateTrackInfo();
        }

        function getThumbnailUrl() {
            var thumbnailElement = document.querySelector('#song-image #img');
            if (thumbnailElement) {
                if (thumbnailElement.src && !thumbnailElement.src.startsWith('data:image/gif')) {
                    return thumbnailElement.src;
                }
            }

            var fallbackElement = document.querySelector('.thumbnail-image-wrapper .image.style-scope.ytmusic-player-bar');
            if (fallbackElement) {
                return fallbackElement.src;
            }

            return '';
        }

        function updateTrackInfo() {
            var titleElement = document.querySelector('.title.style-scope.ytmusic-player-bar');
            var authorElement = document.querySelector('.byline.style-scope.ytmusic-player-bar');
            var thumbnailUrl = getThumbnailUrl();

            var trackInfo = {
                title: titleElement ? titleElement.textContent.trim() : '',
                author: authorElement ? authorElement.textContent.trim() : '',
                thumbnailUrl: thumbnailUrl || ''
            };

            if (trackInfo.title !== lastTrackInfo.title || trackInfo.author !== lastTrackInfo.author || trackInfo.thumbnailUrl !== lastTrackInfo.thumbnailUrl) {
                backend.track_info_changed(trackInfo.title, trackInfo.author, trackInfo.thumbnailUrl);
                lastTrackInfo = trackInfo;
            }

            updateLikeStatus();
        }

        function updateLikeStatus() {
            var likeButton = document.querySelector('ytmusic-like-button-renderer#like-button-renderer');
            if (likeButton) {
                var likeStatus = likeButton.getAttribute('like-status');
                if (likeStatus && likeStatus !== lastLikeStatus) {
                    likeStatus = likeStatus.toLowerCase().charAt(0).toUpperCase() + likeStatus.slice(1).toLowerCase();
                    backend.like_status_changed(likeStatus);
                    lastLikeStatus = likeStatus;
                }
            }
        }     

        var likeObserver = new MutationObserver(updateLikeStatus);
        var likeButton = document.querySelector('ytmusic-like-button-renderer#like-button-renderer');
        if (likeButton) {
            likeObserver.observe(likeButton, { attributes: true, attributeFilter: ['like-status'] });
        }

        var observer = new MutationObserver(updateVideoState);
        observer.observe(document.body, { childList: true, subtree: true });

        updateVideoState();
    });
};
document.head.appendChild(script);