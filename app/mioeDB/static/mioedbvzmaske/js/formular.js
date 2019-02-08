/* global jQuery */

(function ($) {
	jQuery(document).ready(function ($) {
		$(document).on('change', '#menue-mioe-ort', function (e) {	/* Bei Änderung von Speziellen Suchfeldern -> Suche aktuallisieren */
			if (!$('#vz-liste').hasClass('loading')) {
				console.log($('#menue-mioe-ort').val(), 'laden ...');
			}
		});
	});
})(jQuery);
