/* global jQuery Mousetrap */

var unsavedAntworten = 0;
var unsavedEIAufgabe = 0;

(function ($) {
	jQuery(document).ready(function ($) {
		/* Tastenkürzel */
		Mousetrap.bind('ctrl+e', function (e) { return false; });
		Mousetrap.bind('ctrl+s', function (e) { $('#antwortensave').click(); return false; });
		Mousetrap.bind('ctrl+d', function (e) { $('#addantwort').click(); return false; });

		/* ungespeicherte Daten retten */
		window.onbeforeunload = function () {
			if (unsavedAntworten !== 0 || unsavedEIAufgabe !== 0) {
				return 'Es gibt noch ungespeicherte Veränderungen! Wirklich verwerfen?';
			}
		};
	});
})(jQuery);
