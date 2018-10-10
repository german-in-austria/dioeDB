/* global jQuery loadMitErhebungen setMitErhebungen resetBeeinflussung informantenAntwortenUpdate resetReihungAntworten erhInfAufgabenClick erhInfAufgabenChange ausgewaehlteAufgabeChange antwortAudioBereichChange setAudioPlayer erhInfAufgabenSpeichernClick formularChanged antwortenSpeichernClick tagEbenenOptionUpdateAll antwortReihungHochRunterClick updateAinformantErhebung addAntwort antwortLoeschenClick familienHinzufuegenKnopfUpdate */
/* Variablen */

(function ($) {
	jQuery(document).ready(function ($) {
		/* Inits */
		loadMitErhebungen();
		setMitErhebungen();
		resetBeeinflussung();
		resetReihungAntworten();
		setAudioPlayer();

		/* On */
		/* Allgemein */
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
