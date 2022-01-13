/*Consts*/
const player = document.getElementById("audio-player");
const timeScale = document.getElementById("input-time");
const volumeScale = document.getElementById("input-volume");
const pTimeCurrent = document.getElementById("p-time-current");
const pDuration = document.getElementById("p-duration");
var mouseDown = 0;

/*ButtonPreviousPage*/
function menuButtonPreviousPageClick(img) {

}
function menuButtonPreviousPageHover(img) {
    img.src = "../static/images/back_hover.png";
}
function menuButtonPreviousPageUnHover(img) {
    img.src = "../static/images/back.png";
}
/*ButtonNextPage*/
function menuButtonNextPageClick(img) {

}
function menuButtonNextPageHover(img) {
    img.src = "../static/images/back_back_hover.png";
}
function menuButtonNextPageUnHover(img) {
    img.src = "../static/images/back_back.png";
}
/*ButtonRandom*/
function playerButtonRandomClick(img) {

}
function playerButtonRandomHover(img) {
    img.src = "../static/images/random_hover.png";
}
function playerButtonRandomUnHover(img) {
    img.src = "../static/images/random.png";
}
/*ButtonPrevious*/
function playerButtonPreviousClick(img) {
    playPrevious();
}
function playerButtonPreviousHover(img) {
    img.src = "../static/images/previous_hover.png";
}
function playerButtonPreviousUnHover(img) {
    img.src = "../static/images/previous.png";
}
/*Button*/
function playerButtonPlayClick(img) {
    if (player.paused) {
        player.play();
        img.src = "../static/images/stop.png";
    } else {
        player.pause();
        img.src = "../static/images/play.png";
    }
}
function playerButtonPlayHover(img) {

}
function playerButtonPlayUnHover(img) {

}
/*ButtonNext*/
function playerButtonNextClick(img) {

}
function playerButtonNextHover(img) {
    img.src = "../static/images/next_hover.png";
}
function playerButtonNextUnHover(img) {
    img.src = "../static/images/next.png";
}
/*ButtonRepeat*/
function playerButtonRepeatClick(img) {
    if (player.loop) {
        img.src = "../static/images/repeat.png";
        player.loop = false;
    } else {
        img.src = "../static/images/repeat_on.png";
        player.loop = true;
    }
}
function playerButtonRepeatHover(img) {
    if (!player.loop) {
        img.src = "../static/images/repeat_hover.png";
    }
}
function playerButtonRepeatUnHover(img) {
    if (!player.loop) {
        img.src = "../static/images/repeat.png";
    }
}

/*Music*/
function loadTrack(track_id, track_artists_id, track_album_id, track_name, track_duration) {
    console.log(track_id);
    player.addEventListener('timeupdate', updateTime);
    player.src = "../api/track/" + track_id + "/";
    player.load();
    document.getElementById("img-player").src = "../static/images/stop.png";
    document.getElementById("img-player-left-picture").src = "../api/album/" + track_album_id + "/image/";

    document.getElementById("p-player-info-title").innerHTML = track_name;
    document.getElementById("p-player-info-title").onclick = function() {
        openAlbum(track_album_id);
    };

    document.getElementById("p-player-info-artist").onclick = function() {
        openArtist(track_artists_id);
    };
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", "/api/artist/" + track_artists_id + "/info", false);
    xmlHttp.send(null);
    document.getElementById("p-player-info-artist").innerHTML = JSON.parse(JSON.parse(xmlHttp.responseText).info).name;

//    for (var i = 0; i < track_artists_id.length; i++) {
//        var xmlHttp = new XMLHttpRequest();
//        xmlHttp.open("GET", "/api/artist/" + track_artists_id[i] + "/info", false);
//        xmlHttp.send(null);
//        var json = JSON.parse(xmlHttp.responseText);
//        document.getElementById("a-player-info-artist").innerHTML += json.name;
//    }
    timeScale.setAttribute("max", Math.round(track_duration));

    player.play();
}

function play() {
    player.currentTime = 0;
}

function playPrevious() {
    if (player.currentTime >= 1) {
        play();
    } else {
        /*load previous*/
    }
}

function playNext() {
    if (player.ended && player.loop) {
        play();
    } else {
        /*load next*/
    }
}

function changeTime() {
    value = timeScale.value;
    if (!mouseDown) {
        player.currentTime = value;
    }
    pTimeCurrent.innerHTML = Math.floor(value / 60).toString() + ":" + (Math.round(value) - 60 * Math.floor(value / 60)).toString().padStart(2, "0");
}

function updateTime() {
    console.log("player.duration = " + player.duration);
    console.log("player.duration / 60 = " + player.duration / 60);
    console.log("player.duration % 60 = " + player.duration % 60);
    if (!mouseDown) {
        timeScale.value = player.currentTime;
        pTimeCurrent.innerHTML = Math.floor(player.currentTime / 60).toString() + ":" + (Math.round(player.currentTime) - 60 * Math.floor(player.currentTime / 60)).toString().padStart(2, "0");
    }
    if (player.duration.toString() == "NaN") {
        pDuration.innerHTML = "0:00";
    } else {
        pDuration.innerHTML = Math.floor(player.duration / 60).toString() + ":" + (Math.round(player.duration) - 60 * Math.floor(player.duration / 60)).toString().padStart(2, "0");
    }
}

function changeVolume() {
    player.volume = volumeScale.value / 100.0;
}

function search(search_text) {
    var main = document.getElementById("div-main");

    if (search_text == "") {
        main.innerHTML = "";
//        main.innerHtml += '<div class="light-1"></div><div class="light-2"></div><div class="light-3"></div>';
        return;
    }

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", "/api/search/?text=" + search_text, false);
    xmlHttp.send(null);
    var json = JSON.parse(xmlHttp.responseText);

    var innerHTML = ""

    if (json.artists.length != 0) {
        innerHTML += "<p class=\"p-main-artists\">Artists:</p><div class=\"div-main-search-artists\">";
        for (var i = 0; i < json.artists.length; i++) {
            var artist_id = json.artists[i][0];
            var artist_name = json.artists[i][1];
            innerHTML += "<div class=\"div-main-search-artist\"><img class=\"img-search-artist\" src=\"../api/artist/" +
                artist_id + "/image/\" onclick=\"openArtist('" + artist_id + "')\">" +
                "<p class=\"p-search-artist\">" + json.artists[i][1] + "</p></div>";
        }
        innerHTML += "</div>";
    }

    if (json.albums.length != 0) {
        innerHTML += "<p class=\"p-main-albums\">Albums:</p><div class=\"div-main-search-albums\">";
        for (var i = 0; i < json.albums.length; i++) {
            var album_id = json.albums[i][0];
            var album_artists_id = JSON.parse(json.albums[i][1]);
            var album_info = JSON.parse(json.albums[i][2]);
            innerHTML += "<div class=\"div-main-search-album\"><img class=\"img-search-album\" src=\"../api/album/" +
                album_id + "/image/\" onclick=\"openAlbum('" + album_id + "')\">" +
                "<p class=\"p-search-album\">" + album_info.name + "</p></div>";
        }
        innerHTML += "</div>";
    }

    if (json.playlists.length != 0) {
        innerHTML += "<div class=\"div-main-search-playlists\"><p class=\"p-main-playlists\">Playlists:</p>";
        for (var i = 0; i < json.playlists.length; i++) {
            var playlist_id = json.playlists[i][0];
            var playlist_authors_id = JSON.parse(json.playlists[i][1]);
            var playlist_info = JSON.parse(json.playlists[i][2]);
            innerHTML += "<div class=\"div-main-search-playlist\"><img class=\"img-search-playlist\" src=\"../api/playlist/" +
                playlist_id + "/image/\">" + "<p class=\"p-search-playlist\">" + playlist_info.name + "</p></div>";
        }
        innerHTML += "</div>";
    }

    if (json.tracks.length != 0) {
        innerHTML += "<div class=\"div-main-search-tracks\"><p class=\"p-main-tracks\">Tracks:</p>";
        for (var i = 0; i < json.tracks.length; i++) {
            var track_id = json.tracks[i][0];
            var track_artists_id = JSON.parse(json.tracks[i][1]);
            var track_album_id = json.tracks[i][2];
            var track_info = JSON.parse(json.tracks[i][3]);
            innerHTML += "<div class=\"div-main-search-track\"><img class=\"img-search-track\" src=\"../api/album/" +
                track_album_id + "/image/\" onclick=\"loadTrack('" + track_id + "', '" +
                track_artists_id + "', '" + track_album_id + "', `" + track_info.name + "`, `" + track_info.duration + "`)\">" +
                "<p class=\"p-search-track\">" + track_info.name + "</p></div>";
        }
        innerHTML += "</div>";
    }

    if (innerHTML.length == 0) {
        innerHTML = "<div class=\"div-main-search-result\">Nothing Found! :(</div>";
    } else {
        innerHTML = "<div class=\"div-main-search-result\"><p class=\"p-search-header\">Best search results:</p></div>" + innerHTML;
    }

    main.innerHTML = innerHTML;
}

function openArtist(artist_id) {
    var main = document.getElementById("div-main");
    main.innerHTML = "";

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", "/api/artist/" + artist_id + "/info/", false);
    xmlHttp.send(null);
    var artist_info = JSON.parse(JSON.parse(xmlHttp.responseText).info);
    console.log("artist_info = " + artist_info);

    //    var xmlHttp = new XMLHttpRequest();
    //    xmlHttp.open("GET", "/api/album/" + album_id + "/info/", false);
    //    xmlHttp.send(null);
    //    var album_info = JSON.parse(xmlHttp.responseText);
    main.innerHTML = "<div class=\"div-main-artist\"><div id=\"div-main-artist-img\" " +
        "class=\"div-main-artist-img\" style=\"background-image: url('/api/artist/" + artist_id +
        "/image/');background-size: cover;\"><p class=\"p-main-artist-name\">" +
        artist_info.name + "</p></div></div>";

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", "/api/artist/" + artist_id + "/tracks/", false);
    xmlHttp.send(null);
    var artist_tracks = JSON.parse(xmlHttp.responseText).tracks;
    console.log(artist_tracks);

    main.innerHTML += "<div id=\"div-main-artist-tracks\" class=\"div-main-artist-tracks\"><p class=\"p-main-tracks\">Tracks:</p></div>";

    for (var i = 0; i < artist_tracks.length; i++) {
        var track_id = artist_tracks[i];

        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open("GET", "/api/track/" + track_id + "/info/", false);
        xmlHttp.send(null);
        var track_info = JSON.parse(xmlHttp.responseText).info;

        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open("GET", "/api/track/" + track_id + "/artists/", false);
        xmlHttp.send(null);
        var track_artists_id = JSON.parse(xmlHttp.responseText).artists;

        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open("GET", "/api/track/" + track_id + "/album/", false);
        xmlHttp.send(null);
        var track_album_id = JSON.parse(xmlHttp.responseText).album;

        main.innerHTML += "<div class=\"div-main-search-track\"><img class=\"img-search-track\" src=\"../api/album/" +
            track_album_id + "/image/\" onclick=\"loadTrack(`" + track_id + "`, `" + track_artists_id + "`, `" +
            track_album_id + "`, `" + track_info.name + "`, `" + track_info.duration + "`)\"><p class=\"p-search-track\">" + track_info.name + "</p></div>"
    }

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", "/api/artist/" + artist_id + "/albums/", false);
    xmlHttp.send(null);
    var artist_albums = JSON.parse(xmlHttp.responseText).albums;
    console.log("artist_albums = " + artist_albums);
}

function openAlbum(album_id) {
    var main = document.getElementById("div-main");
    main.innerHTML = "";

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", "/api/album/" + album_id + "/info/", false);
    xmlHttp.send(null);
    var album_info = JSON.parse(xmlHttp.responseText).info;
    console.log(album_info);

    //    var xmlHttp = new XMLHttpRequest();
    //    xmlHttp.open("GET", "/api/album/" + album_id + "/info/", false);
    //    xmlHttp.send(null);
    //    var album_info = JSON.parse(xmlHttp.responseText);
    main.innerHTML = "<div class=\"div-main-album\"><img src=\"/api/album/" +
        album_id + "/image/\"></div>";

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", "/api/album/" + album_id + "/artists/", false);
    xmlHttp.send(null);
    var album_artists = JSON.parse(xmlHttp.responseText).artists;
    console.log(album_artists);

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", "/api/album/" + album_id + "/tracks/", false);
    xmlHttp.send(null);
    var album_tracks = JSON.parse(xmlHttp.responseText).tracks;
    console.log(album_tracks);
}

window.onload = function() {
    var req = new XMLHttpRequest();
    req.open('GET', document.location, false);
    req.send(null);
    var headers = req.getAllResponseHeaders().toLowerCase();

//    var xmlHttp = new XMLHttpRequest();
//    xmlHttp.open("GET", "/user/" +  + "/last_track_id/", false);
//    xmlHttp.send(null);
//    var last_track_id = JSON.parse(xmlHttp.responseText).last_track_id;
//
//    player.addEventListener('timeupdate', updateTime);
//    player.src = "../api/track/" + last_track_id + "/";
//    player.load();
//    player.pause();
//    timeScale.value = 0;
};

document.body.onmousedown = function(event) {
    if (event.target.id == "input-time") {
        ++mouseDown;
    }
}
document.body.onmouseup = function(event) {
    if (event.target.id == "input-time") {
        --mouseDown;
        player.currentTime = timeScale.value;
    }
}