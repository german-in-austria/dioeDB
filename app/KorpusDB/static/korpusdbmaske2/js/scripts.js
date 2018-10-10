/* global jQuery loadMitErhebungen setMitErhebungen formFirstFocus setMitErhebungen updateAinformantErhebung formularChanged ausgewaehlteAufgabeChange antwortenSpeichernClick addAntwortTr delAntwortTr addAntwort delAntwort */
/* Variablen */

(function ($) {
	jQuery(document).ready(function ($) {
		/* Inits */
		loadMitErhebungen();
		setMitErhebungen();
		formFirstFocus();

		/* On */
		/* Allgemein */
		$(document).on('change', '#mitErhebungen', setMitErhebungen);
		$(document).on('change', '#ainformantErhebung', updateAinformantErhebung);
		/* Formular */
		$(document).on('change', '.aufgabeantwort input,.aufgabeantwort textarea', formularChanged);
		$(document).on('change', '#selaufgabe select:not(.noupdate)', ausgewaehlteAufgabeChange);
		$(document).on('click', '#antwortensave:not(.disabled)', antwortenSpeichernClick);
		$(document).on('click', 'tr .addantwort', addAntwortTr);
		$(document).on('click', 'tr .delantwort', delAntwortTr);
		$(document).on('click', '.addantwort.aa234', addAntwort);
		$(document).on('click', '.antwort .delantwort', delAntwort);
	});
})(jQuery);

/* Funktionen */
function lmfabcLoaded () {
	formFirstFocus();
}
