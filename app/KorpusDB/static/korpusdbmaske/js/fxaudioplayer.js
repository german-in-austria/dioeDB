/* Variablen */
var audio = new Audio('');
var audioisnewset = 1;
var audiomarks = [];

(function($){jQuery(document).ready(function($){
	/* Tastenkürzel */
	Mousetrap.bind('ctrl+e', function(e) { return false; })
	Mousetrap.bind('ctrl+space', function(e) { $('#audio-play-pause').click(); return false; })
	Mousetrap.bind('ctrl+1', function(e) { $('#audio-fast-backward').click(); return false; })
	Mousetrap.bind('ctrl+2', function(e) { $('#audio-step-backward').click(); return false; })
	Mousetrap.bind('ctrl+3', function(e) { $('#audio-backward').click(); return false; })
	Mousetrap.bind('ctrl+4', function(e) { $('#audio-forward').click(); return false; })
	Mousetrap.bind('ctrl+5', function(e) { $('#audio-step-forward').click(); return false; })
	Mousetrap.bind('ctrl+6', function(e) { $('#audio-fast-forward').click(); return false; })
	Mousetrap.bind('ctrl+x', function(e) { sforwardClick() })
	Mousetrap.bind('ctrl+y', function(e) { sbackwardClick() })
	/* On */
	$(document).on('click','#audioprogress',progressClick)
	$(document).on('click','#audio-play-pause',playPauseClick)
	$(document).on('click','#audio-fast-backward',fastBackwardClick)
	$(document).on('click','#audio-fast-forward',fastForwardClick)
	$(document).on('click','#audio-backward',backwardClick)
	$(document).on('click','#audio-forward',forwardClick)
	$(document).on('click','#audio-step-backward',stepBackwardClick)
	$(document).on('click','#audio-step-forward',stepForwardClick)
});})(jQuery);

/* On Funktionen */
function progressClick(e){
	var parentOffset = $(this).parent().offset();
	azpos = (e.pageX - parentOffset.left - 15) / $(this).width()
	aspos = durationToSeconds($(this).find('.pb-starttime').html())
	aepos = durationToSeconds($(this).find('.pb-endtime').html())
	audio.currentTime = aspos + ((aepos-aspos) * azpos)
}
function playPauseClick(e){
	var aappgi = $(this).find('.glyphicon')
	if(aappgi.hasClass('glyphicon-play')) {
		audio.play();
	} else {
		audio.pause();
	}
}
function fastBackwardClick(e){
	console.log('letzter Marker')
}
function fastForwardClick(e){
	console.log('nächster Marker')
}
function stepBackwardClick(e){
	audio.currentTime = audio.currentTime-30
}
function stepForwardClick(e){
	audio.currentTime = audio.currentTime+30
}
function backwardClick(e){
	audio.currentTime = audio.currentTime-5
}
function forwardClick(e){
	audio.currentTime = audio.currentTime+5
}
function sbackwardClick(e){
	audio.currentTime = audio.currentTime-1
}
function sforwardClick(e){
	audio.currentTime = audio.currentTime+1
}

/* Funktionen */
function setAudioPlayer() {
	audio.pause()
	audio.currentTime = 0
	if($('#audioplayer').children().length>0) {
		var aaudiofile = $(fxAudioDir).val()+$(fxAudioFile).val()
		if(aaudiofile.substr(0,1)=='/' && audiodir.substr(-1)=='/') { aaudiofile = aaudiofile.substr(1) };
		var audiofile = audiodir+aaudiofile
		if(audiofile.length>2) {
			audio.src=audiofile
			audio.load()
			audioisnewset = 1
		}
	}
	// setAudioMarks()
}
function progressBarUpdate() {
	$('.pb-akttime').html(secondsToDuration(audio.currentTime))
	if(audioisnewset==0) {
		$('#audioprogress .progress-bar').css('width',(100/audio.duration*audio.currentTime)+'%')
	}
}
setInterval(progressBarUpdate, 50);
audio.addEventListener("durationchange", function() {
	$('#audioprogress .pb-endtime').html(secondsToDuration(audio.duration))
}, false);
audio.addEventListener("play", function() {
	if(audioisnewset==1) {
		audioisnewset = 0
	}
	$('#audioprogress .progress-bar').addClass('active')
	$('#audio-play-pause .glyphicon').addClass('glyphicon-pause').removeClass('glyphicon-play')
}, false);
audio.addEventListener("pause", function() {
	$('#audioprogress .progress-bar').removeClass('active')
	$('#audio-play-pause .glyphicon').addClass('glyphicon-play').removeClass('glyphicon-pause')
}, false);
