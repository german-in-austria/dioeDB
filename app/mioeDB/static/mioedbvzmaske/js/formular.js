/* global jQuery onSelobjModal */

(function ($) {
	jQuery(document).ready(function ($) {
		$(document).on('change', '#menue-mioe-ort', function (e) {	/* Bei Änderung von Speziellen Suchfeldern -> Suche aktuallisieren */
			console.log($('#menue-mioe-ort').val());
		});
	});
})(jQuery);
