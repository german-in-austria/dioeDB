/* global jQuery loadMitErhebungen setMitErhebungen resetBeeinflussung stepForwardClick informantenAntwortenUpdate backwardClick stepBackwardClick fastForwardClick resetReihungAntworten erhInfAufgabenClick erhInfAufgabenChange ausgewaehlteAufgabeChange antwortAudioBereichChange setAudioPlayer erhInfAufgabenSpeichernClick formularChanged progressClick playPauseClick fastBackwardClick forwardClick antwortenSpeichernClick tagEbenenOptionUpdateAll Mousetrap sforwardClick sbackwardClick antwortReihungHochRunterClick updateAinformantErhebung addAntwort antwortLoeschenClick familienHinzufuegenKnopfUpdate */
/* Variablen */
var unsavedAntworten = 0;
var unsavedEIAufgabe = 0;

(function ($) {
	jQuery(document).ready(function ($) {
		/* Inits */
		loadMitErhebungen();
		setMitErhebungen();
		resetBeeinflussung();
		resetReihungAntworten();
		setAudioPlayer();

		/* Tastenkürzel */
		Mousetrap.bind('ctrl+e', function (e) { return false; });
		Mousetrap.bind('ctrl+s', function (e) { $('#antwortensave').click(); return false; });
		Mousetrap.bind('ctrl+d', function (e) { $('#addantwort').click(); return false; });
		Mousetrap.bind('ctrl+space', function (e) { $('#audio-play-pause').click(); return false; });
		Mousetrap.bind('ctrl+1', function (e) { $('#audio-fast-backward').click(); return false; });
		Mousetrap.bind('ctrl+2', function (e) { $('#audio-step-backward').click(); return false; });
		Mousetrap.bind('ctrl+3', function (e) { $('#audio-backward').click(); return false; });
		Mousetrap.bind('ctrl+4', function (e) { $('#audio-forward').click(); return false; });
		Mousetrap.bind('ctrl+5', function (e) { $('#audio-step-forward').click(); return false; });
		Mousetrap.bind('ctrl+6', function (e) { $('#audio-fast-forward').click(); return false; });
		Mousetrap.bind('ctrl+x', function (e) { sforwardClick(); });
		Mousetrap.bind('ctrl+y', function (e) { sbackwardClick(); });

		/* On */
		/* Allgemein */
		window.onbeforeunload = function () {
			if (unsavedAntworten !== 0 || unsavedEIAufgabe !== 0) {
				return 'Es gibt noch ungespeicherte Veränderungen! Wirklich verwerfen?';
			}
		};
		$(document).on('change', '#mitErhebungen', setMitErhebungen);
		$(document).on('change', '#ainformantErhebung', updateAinformantErhebung);
		/* Formular */
		$(document).on('click', '.antwort .antwortreihunghoch:not(.disabled), .antwort .antwortreihungrunter:not(.disabled)', antwortReihungHochRunterClick);
		$(document).on('change', '.antwort input,.antwort textarea,select.tagebene', formularChanged);
		$(document).on('change', 'input[name="start_Antwort"], input[name="stop_Antwort"]', antwortAudioBereichChange);
		$(document).on('change', '#selaufgabe select:not(.noupdate)', ausgewaehlteAufgabeChange);
		$(document).on('change', '#erhinfaufgaben', setAudioPlayer);
		$(document).on('click', '#erhinfaufgaben', erhInfAufgabenClick);
		$(document).on('change', 'input[name="ist_bfl"]', resetBeeinflussung);
		$(document).on('change', '#start_ErhInfAufgaben, #stop_ErhInfAufgaben', erhInfAufgabenChange);
		$(document).on('click', '#eiaufgsave:not(.disabled)', erhInfAufgabenSpeichernClick);
		$(document).on('click', '#antwortensave:not(.disabled)', antwortenSpeichernClick);
		$(document).on('click', '#addantwort', addAntwort);
		$(document).on('click', '.delantwort', antwortLoeschenClick);
		/* Audio */
		$(document).on('click', '#aufgabenprogress, #inferhebungprogress', progressClick);
		$(document).on('click', '#audio-play-pause', playPauseClick);
		$(document).on('click', '#audio-fast-backward', fastBackwardClick);
		$(document).on('click', '#audio-fast-forward', fastForwardClick);
		$(document).on('click', '#audio-backward', backwardClick);
		$(document).on('click', '#audio-forward', forwardClick);
		$(document).on('click', '#audio-step-backward', stepBackwardClick);
		$(document).on('click', '#audio-step-forward', stepForwardClick);
		$(document).on('click', '#audio-step-forward', informantenAntwortenUpdate);
	});
})(jQuery);

/* Funktionen */
function lmfabcLoaded () {
	addAntwort();
	resetBeeinflussung();
	tagEbenenOptionUpdateAll();
	setAudioPlayer();
	familienHinzufuegenKnopfUpdate();
}
