function urlMatchesOneOfPatterns(url, patterns) {
    for (var i = 0; i < patterns.length; i++) {
        var pattern = patterns[i];
        if (url.match(pattern)) {
            return true;
        }
    }

    return false;
}
var UptoboxModule = {
    canHandleUrl: function(url) {
        var validPatterns = [
            ".*uptobox.com.*"
        ];
        return urlMatchesOneOfPatterns(url, validPatterns);
    },
    getMediaType: function() {
        return 'video';
    },
    getPluginPath: function(url, getAddOnVersion, callback) {
        var videoId = url.match('(https|http)://([^_&/#\?]+\.)?uptobox.com/([^_&/#\?]+)')[3];
        callback('plugin://plugin.video.vstream/?site=cHosterGui&function=play&title=++Revenge++%28SD%29+%5BCOLOR+violet%5DUptobox%5B%2FCOLOR%5D&sHosterIdentifier=uptobox&sTitle=++Revenge++%28SD%29+%5BCOLOR+violet%5DUptobox%5B%2FCOLOR%5D&siteUrl='+videoId+'&sFav=play&sMediaUrl='+videoId+'&sCat=4&sId=cHosterGui&sFileName=++Revenge++%28SD%29&sType=5');
    }
};

var allModules = [
	UptoboxModule,
];
