/* global jQuery alert csrf aurl */

(function ($) {
	jQuery(document).ready(function ($) {
		$(document).on('change', '#menue-mioe-ort', function (e) {	/* Bei Änderung von Speziellen Suchfeldern -> Suche aktuallisieren */
			if (!$('#vz-liste').hasClass('loading')) {
				$('#vz-liste').addClass('loading').html('Lade ...');
				$.post(aurl, { csrfmiddlewaretoken: csrf, getmenue: $(this).val() }, function (d) {
					$('#vz-liste').removeClass('loading').html('');
					let aData = JSON.parse(d);
					if (aData.success === 'success') {
						$.each(aData.mioeOrte, function (aKey, aVal) {
							$('#vz-liste').append('<a href="#" class="m-lvzd lmfabc-nf" title="' + aVal.title + '\nErhebungs Datum' + aVal.erheb_datum + '" data-vzid="' + aVal.id + '">' + aVal.title + '</a>');
						});
					}
				}).fail(function (d) {
					var aError = d['responseText'].split('\n', 10);
					alert('Es ist ein Fehler aufgetreten:\n\n' + aError[0] + '\n' + aError[1] + '\n' + aError[2]);
					console.log(d);
					$('#vz-liste').removeClass('loading').html('');
				});
				console.log($('#menue-mioe-ort').val(), 'laden ...');
			}
		});
		$(document).on('click', '.m-lvzd', function (e) {
			e.preventDefault();
			console.log($(this).data('vzid'));
		});
	});
})(jQuery);
