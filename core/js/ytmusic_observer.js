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

        function updateTrackInfo() {
            var titleElement = document.querySelector('.title.ytmusic-player-bar');
            var authorElement = document.querySelector('.byline.ytmusic-player-bar');
            var thumbnailElement = document.querySelector('.image.ytmusic-player-bar');

            var trackInfo = {
                title: titleElement ? titleElement.textContent : '',
                author: authorElement ? authorElement.textContent : '',
                thumbnailUrl: thumbnailElement ? thumbnailElement.src : ''
            };

            if (trackInfo.title !== lastTrackInfo.title || trackInfo.author !== lastTrackInfo.author || trackInfo.thumbnailUrl !== lastTrackInfo.thumbnailUrl) {
                backend.track_info_changed(trackInfo.title, trackInfo.author, trackInfo.thumbnailUrl);
                lastTrackInfo = trackInfo;
            }
        }

        var observer = new MutationObserver(updateVideoState);
        observer.observe(document.body, { childList: true, subtree: true });

        updateVideoState();
    });
};
document.head.appendChild(script);