/* global jQuery Audio Mousetrap $ audiodir confirm formularChanged */
/* Variablen */
var audio = new Audio('');
var audioisnewset = 1;
var audiomarks = [];
var audiomarksObj = [];
var playing = false;

(function ($) {
	jQuery(document).ready(function ($) {
		/* Tastenkürzel */
		Mousetrap.bind('ctrl+space', function (e) { $('#audio-play-pause').click(); return false; });
		Mousetrap.bind('ctrl+1', function (e) { $('#audio-fast-backward').click(); return false; });
		Mousetrap.bind('ctrl+2', function (e) { $('#audio-step-backward').click(); return false; });
		Mousetrap.bind('ctrl+3', function (e) { $('#audio-backward').click(); return false; });
		Mousetrap.bind('ctrl+4', function (e) { $('#audio-forward').click(); return false; });
		Mousetrap.bind('ctrl+5', function (e) { $('#audio-step-forward').click(); return false; });
		Mousetrap.bind('ctrl+6', function (e) { $('#audio-fast-forward').click(); return false; });
		Mousetrap.bind('ctrl+x', function (e) { sforwardClick(); });
		Mousetrap.bind('ctrl+y', function (e) { sbackwardClick(); });

		/* Audio */
		$(document).on('click', '#aufgabenprogress, #inferhebungprogress', progressClick);
		$(document).on('click', '#audio-play-pause', playPauseClick);
		$(document).on('click', '#audio-fast-backward', fastBackwardClick);
		$(document).on('click', '#audio-fast-forward', fastForwardClick);
		$(document).on('click', '#audio-backward', backwardClick);
		$(document).on('click', '#audio-forward', forwardClick);
		$(document).on('click', '#audio-step-backward', stepBackwardClick);
		$(document).on('click', '#audio-step-forward', stepForwardClick);
		$(document).on('click', '.get-audio-position-btn', getAudioPositionBtn);
	});
})(jQuery);

/* On */
function progressClick (e) {
	var parentOffset = $(this).parent().offset();
	var azpos = (e.pageX - parentOffset.left - 15) / $(this).width();
	var aspos = durationToSeconds($(this).find('.pb-starttime').html());
	var aepos = durationToSeconds($(this).find('.pb-endtime').html());
	audio.currentTime = aspos + ((aepos - aspos) * azpos);
}
function playPauseClick (e) {
	var aappgi = $(this).find('.glyphicon');
	if (aappgi.hasClass('glyphicon-play')) {
		audio.play();
	} else {
		audio.pause();
	}
}
function fastBackwardClick (e) {
	audio.currentTime = durationToSeconds($('#start_ErhInfAufgaben').val()) - syncDiff($('#erhinfaufgaben option:selected'));
}
function fastForwardClick (e) {
	audio.currentTime = durationToSeconds($('#stop_ErhInfAufgaben').val()) - syncDiff($('#erhinfaufgaben option:selected'));
}
function backwardClick (e) {
	audio.currentTime = audio.currentTime - 5;
}
function forwardClick (e) {
	audio.currentTime = audio.currentTime + 5;
}
function sbackwardClick (e) {
	audio.currentTime = audio.currentTime - 1;
}
function sforwardClick (e) {
	audio.currentTime = audio.currentTime + 1;
}
function stepBackwardClick (e) {
	if (audiomarks.length > 0) {
		var gtt = 0;
		var gtts = 999999999999999;
		for (var i = 0; i < audiomarks.length; ++i) {
			if (audiomarks[i] < (audio.currentTime - 1) && audiomarks[i] > gtt) { gtt = audiomarks[i]; };
			if (audiomarks[i] < gtts) { gtts = audiomarks[i]; };
		}
		if (gtt === 0) { gtt = gtts; };
		audio.currentTime = gtt;
	}
}
function stepForwardClick (e) {
	if (audiomarks.length > 0) {
		if ($('#audio-loop').val() === 'loopAntwort' && audiomarksObj.length > 0) {
			for (let i = 0; i < audiomarksObj.length; ++i) {
				if (audio.currentTime >= audiomarksObj[i].s && audio.currentTime <= audiomarksObj[i].e) {
					if (audiomarksObj[i + 1]) {
						audio.currentTime = audiomarksObj[i + 1].s;
						break;
					}
				}
			}
		} else {
			var gtt = 999999999999999;
			var gtts = 0;
			for (let i = 0; i < audiomarks.length; ++i) {
				if (audiomarks[i] > (audio.currentTime) && audiomarks[i] < gtt) { gtt = audiomarks[i]; };
				if (audiomarks[i] > gtts) { gtts = audiomarks[i]; };
			}
			if (gtt === 999999999999999) { gtt = gtts; };
			audio.currentTime = gtt;
		}
	}
}
function getAudioPositionBtn (e) {
	var aVal = durationToSeconds($(this).siblings('.audio-position-input').val());
	if (audio.currentTime >= 0 && (aVal === 0 || confirm('Soll die aktuelle Zeit überschrieben werden?'))) {
		$(this).siblings('.audio-position-input').val(secondsToDuration(audio.currentTime));
	}
	setAudioMarks();
	formularChanged();
}

/* Funktionen */
function durationToSeconds (hms) {
	var s = 0.0;
	if (hms && hms.indexOf(':') > -1) {
		var a = hms.split(':');
		if (a.length > 2) { s += parseFloat(a[a.length - 3]) * 60 * 60; };
		if (a.length > 1) { s += parseFloat(a[a.length - 2]) * 60; };
		if (a.length > 0) { s += parseFloat(a[a.length - 1]); };
	} else {
		s = parseFloat(hms);
		if (isNaN(s)) { s = 0.0; };
	}
	return s;
}
function secondsToDuration (sec) {
	var v = '';
	if (sec < 0) { sec = -sec; v = '-'; };
	var h = parseInt(sec / 3600);
	sec %= 3600;
	var m = parseInt(sec / 60);
	var s = sec % 60;
	return v + ('0' + h).slice(-2) + ':' + ('0' + m).slice(-2) + ':' + ('0' + s.toFixed(6)).slice(-9);
}
function syncDiff (adata) {
	if (durationToSeconds(adata.data('sync_time')) > 0) {
		return durationToSeconds(adata.data('time_beep')) - durationToSeconds(adata.data('sync_time'));
	}
	return 0;
}
function setAudioMarks () {
	audiomarks = [];
	audiomarksObj = [];
	$('#aufgabenprogress .markarea,#inferhebungprogress .markarea').remove();
	if ($('.antwort').length > 0) {
		var aeltuasErh = durationToSeconds($('#start_ErhInfAufgaben').val()) - syncDiff($('#erhinfaufgaben option:selected'));
		var aeltuaeErh = durationToSeconds($('#stop_ErhInfAufgaben').val()) - syncDiff($('#erhinfaufgaben option:selected'));
		var aeltualErh = aeltuaeErh - aeltuasErh;
		$('#inferhebungprogress').append('<div class="markarea" style="left:' + (100 / audio.duration * (aeltuasErh)) + '%;width:' + (100 / audio.duration * (aeltuaeErh - aeltuasErh)) + '%"></div>');
		$('.antwort').each(function () {
			var asSec = durationToSeconds($(this).find('input[name="start_Antwort"]').val());
			var aeSec = durationToSeconds($(this).find('input[name="stop_Antwort"]').val());
			if (asSec > 0 && aeSec > 0 && aeSec > asSec && aeSec >= aeltuasErh && aeSec <= aeltuaeErh) {
				audiomarks.push(asSec);
				audiomarks.push(aeSec);
				if (asSec < aeSec) {
					audiomarksObj.push({s: asSec, e: aeSec})
				}
				console.log(asSec + ' - ' + aeSec);
				$('#aufgabenprogress').append('<div class="markarea" style="left:' + (100 / aeltualErh * (asSec - aeltuasErh)) + '%;width:' + (100 / aeltualErh * (aeSec - asSec)) + '%"></div>');
			}
		});
	}
	audiomarks.sort();
	audiomarksObj.sort((a, b) => (a.s > b.s) ? 1 : ((b.s > a.s) ? -1 : 0));
}
function setAudioPlayer () {
	if ($('#audioplayer').children().length > 0) {
		var aopt = $('#erhinfaufgaben option:selected');
		$('#start_ErhInfAufgaben').val(secondsToDuration(durationToSeconds(aopt.data('start_aufgabe'))));
		$('#stop_ErhInfAufgaben').val(secondsToDuration(durationToSeconds(aopt.data('stop_aufgabe'))));
		$('#sync_time_ErhInfAufgaben').html(secondsToDuration(durationToSeconds(aopt.data('sync_time'))));
		$('#time_beep_ErhInfAufgaben').html(secondsToDuration(durationToSeconds(aopt.data('time_beep'))));
		$('#syncdiff_ErhInfAufgaben').html(secondsToDuration(-syncDiff(aopt)));
		$('#aufgabenprogress .pb-starttime').html(secondsToDuration(durationToSeconds(aopt.data('start_aufgabe')) - syncDiff(aopt)));
		$('#aufgabenprogress .pb-endtime').html(secondsToDuration(durationToSeconds(aopt.data('stop_aufgabe')) - syncDiff(aopt)));
		var aaudiofile = aopt.data('audiofile');
		audio.pause();
		audio.currentTime = 0;
		if (aaudiofile) {
			if (aaudiofile.substr(0, 1) === '/' && audiodir.substr(-1) === '/') { aaudiofile = aaudiofile.substr(1); };
			var audiofile = audiodir + aaudiofile;
			if (audiofile.length > 2) {
				console.log(audiofile);
				audio.src = audiofile;
				audio.load();
			}
			$('#audio-play-pause, #audio-fast-backward, #audio-fast-forward, #audio-backward, #audio-forward, #audio-step-backward, #audio-step-forward').removeAttr('disabled').removeClass('disabled');
		} else {
			$('#audio-play-pause, #audio-fast-backward, #audio-fast-forward, #audio-backward, #audio-forward, #audio-step-backward, #audio-step-forward').attr('disabled', 'disabled').addClass('disabled');
		}
		audioisnewset = 1;
		$('#inferhebungprogress .progress-bar,#aufgabenprogress .progress-bar').css('width', '0%');
	}
	unsavedEIAufgabe=0;
	$('#eiaufgsave').addClass('disabled');
	setAudioMarks();
}
function progressBarUpdate () {
	$('.pb-akttime').html(secondsToDuration(audio.currentTime));
	if (audioisnewset === 0) {
		$('#inferhebungprogress .progress-bar').css('width', (100 / audio.duration * audio.currentTime) + '%');
		var aeltuasErh = durationToSeconds($('#start_ErhInfAufgaben').val()) - syncDiff($('#erhinfaufgaben option:selected'));
		var aeltuaeErh = durationToSeconds($('#stop_ErhInfAufgaben').val()) - syncDiff($('#erhinfaufgaben option:selected'));
		if (audio.currentTime >= aeltuasErh && audio.currentTime <= aeltuaeErh) {
			$('#aufgabenprogress .progress-bar').css('width', (100 / (aeltuaeErh - aeltuasErh) * (audio.currentTime - aeltuasErh)) + '%');
		} else if (audio.currentTime < aeltuasErh) {
			$('#aufgabenprogress .progress-bar').css('width', '0%');
		} else {
			$('#aufgabenprogress .progress-bar').css('width', '100%');
		}
	}
	if (playing) {
		if ($('#audio-loop').val() === 'loop' || ($('#audio-loop').val() === 'loopAntwort' && audiomarksObj.length === 0)) {
			if (audio.currentTime > durationToSeconds($('#stop_ErhInfAufgaben').val()) - syncDiff($('#erhinfaufgaben option:selected'))) {
				audio.currentTime = durationToSeconds($('#start_ErhInfAufgaben').val()) - syncDiff($('#erhinfaufgaben option:selected'));
			}
		} else if ($('#audio-loop').val() === 'loopAntwort' && audiomarksObj.length > 0) {
			var newTime = audiomarksObj[0].s;
			for (var i = 0; i < audiomarksObj.length; ++i) {
				if (audio.currentTime >= audiomarksObj[i].s && audio.currentTime <= audiomarksObj[i].e) {
					newTime = -1;
				} else if (newTime >= 0 && audio.currentTime >= audiomarksObj[i].e) {
					newTime = audiomarksObj[i].s;
				}
			}
			if (newTime >= 0) {
				audio.currentTime = newTime;
			}
		}
	}
}
setInterval(progressBarUpdate, 50);
audio.addEventListener('durationchange', function () {
	$('#inferhebungprogress .pb-endtime').html(secondsToDuration(audio.duration));
}, false);
audio.addEventListener('play', function () {
	if (audioisnewset === 1) {
		setTimeout(function () { audio.currentTime = durationToSeconds($('#erhinfaufgaben option:selected').data('start_aufgabe')) - syncDiff($('#erhinfaufgaben option:selected')); setAudioMarks(); }, 100);
		audioisnewset = 0;
	}
	$('#aufgabenprogress .progress-bar, #inferhebungprogress .progress-bar').addClass('active');
	playing = true;
	$('#audio-play-pause .glyphicon').addClass('glyphicon-pause').removeClass('glyphicon-play');
}, false);
audio.addEventListener('pause', function () {
	$('#aufgabenprogress .progress-bar, #inferhebungprogress .progress-bar').removeClass('active');
	playing = false;
	$('#audio-play-pause .glyphicon').addClass('glyphicon-play').removeClass('glyphicon-pause');
}, false);
