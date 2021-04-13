

const background = document.querySelector('#p_background'); // background derived from album cover below
const thumbnail = document.querySelector('#thumbnail'); // album cover 
const song = document.querySelector('#song'); // audio object
const playListRows= document.querySelector(".play-list-row");
//const trackInfoBox= document.querySelector(".track-info-box");
const songArtist = document.querySelector('.song-artist'); // element where track artist appears
const songTitle = document.querySelector('.song-title'); // element where track title appears
const progressBar = document.querySelector('#progress-bar'); // element where progress bar appears
const pPause = document.querySelector('#play-pause'); // element where play and pause image appears
const smallToggleBtn= document.querySelector('.small-toggle-btn');
const largeToggleBtn= document.querySelector(".large-toggle-btn");
const nextTrackBtn= document.querySelector(".next-track-btn");
const previousTrackBtn= document.querySelector(".previous-track-btn");


songIndex = 0;
songs = ['/sidebar_Icon/sMusic copy/player/assets/music/blinding.mp3' , '/sidebar_Icon/sMusic copy/player/assets/music/duniya.mp3', '/sidebar_Icon/sMusic copy/player/assets/music/scam.mp3', '/sidebar_Icon/sMusic copy/player/assets/music/senorita.mp3', '/sidebar_Icon/sMusic copy/player/assets/music/dynamite.mp3',
 '/sidebar_Icon/sMusic copy/player/assets/music/stranger things.mp3', '/sidebar_Icon/sMusic copy/player/assets/music/faded.mp3' ]; // object storing paths for audio objects
thumbnails = ['/sidebar_Icon/sMusic copy/player/assets/images/blinding.png', '/sidebar_Icon/sMusic copy/player/assets/images/duniya.jpg', '/sidebar_Icon/sMusic copy/player/assets/images/scam.jpg', '/sidebar_Icon/sMusic copy/player/assets/images/senorita.jpg', '/sidebar_Icon/sMusic copy/player/assets/images/dynamite.jpg'
, '/sidebar_Icon/sMusic copy/player/assets/images/stranger things.jpg', '/sidebar_Icon/sMusic copy/player/assets/images/faded.jpg' ]; // object storing paths for album covers and backgrounds
songArtists = ['The Weeknd', ' Akhil and Dhvani','Achint','Camila Cabello and Shawn Mendes', 'BTS', 'Kygo','Alan Walker']; // object storing track artists
songTitles = ["Blinding Lights","Duniyaa","Scam 1992","Señorita","Dynamite","Stranger Things","Faded"]; // object storing track titles

// function where pp (play-pause) element changes based on playing boolean value - if play button clicked, change pp.src to pause button and call song.play() and vice versa.
let playing = true;
function playPause() {
    if (playing) {
        const song = document.querySelector('#song'),
        thumbnail = document.querySelector('#thumbnail');

        pPause.src = "./assets/icons/pause.png"
        thumbnail.style.transform = "scale(1.15)";
        
        song.play();
        playing = false;
    } else {
        pPause.src = "./assets/icons/play.png"
        thumbnail.style.transform = "scale(1)"
        
        song.pause();
        playing = true;
    }
}

// automatically play the next song at the end of the audio object's duration
song.addEventListener('ended', function(){
    nextSong();
});

// function where songIndex is incremented, song/thumbnail image/background image/song artist/song title changes to next index value, and playPause() runs to play next track 
function nextSong() {
    songIndex++;
    if (songIndex > 6) {
        songIndex = 0;
    };
    song.src = songs[songIndex];
    thumbnail.src = thumbnails[songIndex];
    background.src = thumbnails[songIndex];

    songArtist.innerHTML = songArtists[songIndex];
    songTitle.innerHTML = songTitles[songIndex];

    playing = true;
    playPause();
}

// function where songIndex is decremented, song/thumbnail image/background image/song artist/song title changes to previous index value, and playPause() runs to play previous track 
function previousSong() {
    songIndex--;
    if (songIndex < 0) {
        songIndex = 6;
    };
    song.src = songs[songIndex];
    thumbnail.src = thumbnails[songIndex];
    p_background.src = thumbnails[songIndex];

    songArtist.innerHTML = songArtists[songIndex];
    songTitle.innerHTML = songTitles[songIndex];

    playing = true;
    playPause();
}

// update progressBar.max to song object's duration, same for progressBar.value, update currentTime/duration DOM
function updateProgressValue() {
    progressBar.max = song.duration;
    progressBar.value = song.currentTime;
    document.querySelector('.currentTime').innerHTML = (formatTime(Math.floor(song.currentTime)));
    if (document.querySelector('.durationTime').innerHTML === "NaN:NaN") {
        document.querySelector('.durationTime').innerHTML = "0:00";
    } else {
        document.querySelector('.durationTime').innerHTML = (formatTime(Math.floor(song.duration)));
    }
};

// convert song.currentTime and song.duration into MM:SS format
function formatTime(seconds) {
    let min = Math.floor((seconds / 60));
    let sec = Math.floor(seconds - (min * 60));
    if (sec < 10){ 
        sec  = `0${sec}`;
    };
    return `${min}:${sec}`;
};

// run updateProgressValue function every 1/2 second to show change in progressBar and song.currentTime on the DOM
setInterval(updateProgressValue, 500);

// function where progressBar.value is changed when slider thumb is dragged without auto-playing audio
function changeProgressBar() {
    song.currentTime = progressBar.value;
};

// //Adding event listeners to playlist clickable elements.
// for (var i = 0; i < elements.playListRows.length; i++) {
//     var smallToggleBtn = elements.playerButtons.smallToggleBtn[i];
//     var playListLink = elements.playListRows[i].children[2].children[0];

//     //Playlist link clicked.
//     playListLink.addEventListener("click", function(e) {
//       e.preventDefault();
//       var selectedTrack = parseInt(this.parentNode.parentNode.getAttribute("data-track-row"));

//       if (selectedTrack !== currentTrack) {
//         resetPlayStatus();
//         currentTrack = null;
//         trackLoaded = false;
//       }

//       if (trackLoaded === false) {
//         currentTrack = parseInt(selectedTrack);
//         setTrack();
//       } else {
//         playBack(this);
//       }
//     }, false);

//     //Small toggle button clicked.
//     smallToggleBtn.addEventListener("click", function(e) {
//       e.preventDefault();
//       var selectedTrack = parseInt(this.parentNode.getAttribute("data-track-row"));

//       if (selectedTrack !== currentTrack) {
//         resetPlayStatus();
//         currentTrack = null;
//         trackLoaded = false;
//       }

//       if (trackLoaded === false) {
//         currentTrack = parseInt(selectedTrack);
//         setTrack();
//       } else {
//         playBack(this);
//       }

//     }, false);
//   }

//   //Audio time has changed so update it.
//   elements.songs.addEventListener("timeupdate", trackTimeChanged, false);

//   //Audio track has ended playing.
//   elements.songs.addEventListener("ended", function(e) {
//     trackHasEnded();
//   }, false);

//   var resetPlayStatus = function() {
//     var smallToggleBtn = elements.playerButtons.smallToggleBtn;

//     elements.playerButtons.largeToggleBtn.children[0].className = "large-play-btn";

//     for (var i = 0; i < smallToggleBtn.length; i++) {
//       if (smallToggleBtn[i].children[0].className === "small-pause-btn") {
//         smallToggleBtn[i].children[0].className = "small-play-btn";
//       }
//     }
//   };