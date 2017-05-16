/* Variablen */
var audio = new Audio('');
var audioisnewset = 1
var audiomarks = []

/* On */
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
	audio.currentTime = durationToSeconds($('#start_ErhInfAufgaben').val())
}
function fastForwardClick(e){
	audio.currentTime = durationToSeconds($('#stop_ErhInfAufgaben').val())
}
function backwardClick(e){
	audio.currentTime = audio.currentTime-10
}
function forwardClick(e){
	audio.currentTime = audio.currentTime+10
}
function stepBackwardClick(e){
	if(audiomarks.length>0) {
		gtt=0
		gtts=999999999999999
		for (i = 0; i < audiomarks.length; ++i) {
			if(audiomarks[i]<(audio.currentTime-1)&&audiomarks[i]>gtt) { gtt = audiomarks[i]; }
			if(audiomarks[i]<gtts) { gtts = audiomarks[i]; }
		}
		if(gtt==0) { gtt=gtts; }
		audio.currentTime = gtt
	}
}
function stepForwardClick(e){
	if(audiomarks.length>0) {
		gtt=999999999999999
		gtts=0
		for (i = 0; i < audiomarks.length; ++i) {
			if(audiomarks[i]>(audio.currentTime)&&audiomarks[i]<gtt) { gtt = audiomarks[i]; }
			if(audiomarks[i]>gtts) { gtts = audiomarks[i]; }
		}
		if(gtt==999999999999999) { gtt=gtts; }
		audio.currentTime = gtt
	}
}

/* Funktionen */
function durationToSeconds(hms) {
	var a = hms.split(':'); var s = 0.0
	if(a.length>2) { s+=parseFloat(a[a.length-3]) * 60 * 60; }
	if(a.length>1) { s+=parseFloat(a[a.length-2]) * 60; }
	if(a.length>0) { s+=parseFloat(a[a.length-1]); }
	return s
}
function secondsToDuration(sec) {
	var h = parseInt(sec / 3600)
	sec %= 3600;
	var m = parseInt(sec / 60)
	var s = sec % 60
	return ("0" + h).slice(-2) + ':' + ("0" + m).slice(-2) + ':' + ("0" + s.toFixed(6)).slice(-9)
}
function setAudioMarks() {
	audiomarks = []
	$('#aufgabenprogress .markarea,#inferhebungprogress .markarea').remove()
	if($('.antwort').length>0) {
		aeltuasErh = durationToSeconds($('#start_ErhInfAufgaben').val())
		aeltuaeErh = durationToSeconds($('#stop_ErhInfAufgaben').val())
		aeltualErh = aeltuaeErh-aeltuasErh
		$('#inferhebungprogress').append('<div class="markarea" style="left:'+(100/audio.duration*(aeltuasErh))+'%;width:'+(100/audio.duration*(aeltuaeErh-aeltuasErh))+'%"></div>')
		$('.antwort').each(function() {
			asSec = durationToSeconds($(this).find('input[name="start_Antwort"]').val())
			aeSec = durationToSeconds($(this).find('input[name="stop_Antwort"]').val())
			if(asSec>0 && aeSec>0 && aeSec>asSec && aeSec>=aeltuasErh && aeSec<=aeltuaeErh) {
				audiomarks.push(asSec)
				audiomarks.push(aeSec)
				console.log(asSec+' - '+aeSec)
				$('#aufgabenprogress').append('<div class="markarea" style="left:'+(100/aeltualErh*(asSec-aeltuasErh))+'%;width:'+(100/aeltualErh*(aeSec-asSec))+'%"></div>')
			}
		})
	}
	audiomarks.sort()
}
function setAudioPlayer() {
	if($('#audioplayer').children().length>0) {
		aopt = $('#erhinfaufgaben option:selected')
		$('#start_ErhInfAufgaben').val(secondsToDuration(durationToSeconds(aopt.data('start_aufgabe'))))
		$('#stop_ErhInfAufgaben').val(secondsToDuration(durationToSeconds(aopt.data('stop_aufgabe'))))
		$('#aufgabenprogress .pb-starttime').html(secondsToDuration(durationToSeconds(aopt.data('start_aufgabe'))))
		$('#aufgabenprogress .pb-endtime').html(secondsToDuration(durationToSeconds(aopt.data('stop_aufgabe'))))
		var audiofile = audiodir+aopt.data('audiofile')+'.mp3'
		if(audiofile.length>2) {
			audio.src=audiofile
			audio.load()
			audioisnewset = 1
		}
	}
	unsavedEIAufgabe=0
	$('#eiaufgsave').addClass('disabled')
	setAudioMarks()
}
function progressBarUpdate() {
	$('.pb-akttime').html(secondsToDuration(audio.currentTime))
	if(audioisnewset==0) {
		$('#inferhebungprogress .progress-bar').css('width',(100/audio.duration*audio.currentTime)+'%')
		aeltuasErh = durationToSeconds($('#start_ErhInfAufgaben').val())
		aeltuaeErh = durationToSeconds($('#stop_ErhInfAufgaben').val())
		if(audio.currentTime>=aeltuasErh && audio.currentTime<=aeltuaeErh) {
			$('#aufgabenprogress .progress-bar').css('width',(100/(aeltuaeErh-aeltuasErh)*(audio.currentTime-aeltuasErh))+'%')
		} else if(audio.currentTime<aeltuasErh) {
			$('#aufgabenprogress .progress-bar').css('width','0%')
		} else {
			$('#aufgabenprogress .progress-bar').css('width','100%')
		}
	}
}
setInterval(progressBarUpdate, 50);
audio.addEventListener("durationchange", function() {
	$('#inferhebungprogress .pb-endtime').html(secondsToDuration(audio.duration))
}, false);
audio.addEventListener("play", function() {
	if(audioisnewset==1) {
		setTimeout(function() { audio.currentTime = durationToSeconds($('#erhinfaufgaben option:selected').data('start_aufgabe')); setAudioMarks(); }, 100)
		audioisnewset = 0
	}
	$('#aufgabenprogress .progress-bar, #inferhebungprogress .progress-bar').addClass('active')
	$('#audio-play-pause .glyphicon').addClass('glyphicon-pause').removeClass('glyphicon-play')
}, false);
audio.addEventListener("pause", function() {
	$('#aufgabenprogress .progress-bar, #inferhebungprogress .progress-bar').removeClass('active')
	$('#audio-play-pause .glyphicon').addClass('glyphicon-play').removeClass('glyphicon-pause')
}, false);
