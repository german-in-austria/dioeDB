/* global jQuery alert csrf aurl */

(function ($) {
	jQuery(document).ready(function ($) {
		$(document).on('change', '#menue-mioe-ort, #menue-mioe-vz', function (e) {	/* Bei Änderung von Speziellen Suchfeldern -> Suche aktuallisieren */
			console.log('Ort: ', $('#menue-mioe-ort').val(), $('#menue-mioe-ort').val() > 0, 'VZ: ', $('#menue-mioe-vz').val(), $('#menue-mioe-vz').val() > 0);
			if (!$('.mcon').hasClass('loading')) {
				$('.mcon').addClass('loading').html('Lade ...');
				$.post(aurl, { csrfmiddlewaretoken: csrf, getmask: 1, aMioeOrtId: $('#menue-mioe-ort').val(), aVzId: $('#menue-mioe-vz').val() }, function (d) {
					$('.mcon').removeClass('loading');
					$('.mcon').html(d);
				}).fail(function (d) {
					var aError = d['responseText'].split('\n', 10);
					alert('Es ist ein Fehler aufgetreten:\n\n' + aError[0] + '\n' + aError[1] + '\n' + aError[2]);
					console.log(d);
					$('.mcon').removeClass('loading').html('');
				});
			}
		});
		// $(document).on('click', '.m-lvzd', function (e) {
		// 	e.preventDefault();
		// 	if (!$('#vz-liste').hasClass('loading')) {
		// 		$('#vz-liste > .lmfabcl-nf').removeClass('open');
		// 		$(this).addClass('open');
		// 		$('#vz-liste').addClass('loading');
		// 		$('.mcon').addClass('loading').html('Lade ...');
		// 		$.post(aurl, { csrfmiddlewaretoken: csrf, getmask: $(this).data('vzid') }, function (d) {
		// 			$('#vz-liste, .mcon, #vz-liste > .lmfabcl-nf').removeClass('loading');
		// 			$(this).removeClass('loading');
		// 			$('.mcon').html(d);
		// 		}).fail(function (d) {
		// 			var aError = d['responseText'].split('\n', 10);
		// 			alert('Es ist ein Fehler aufgetreten:\n\n' + aError[0] + '\n' + aError[1] + '\n' + aError[2]);
		// 			console.log(d);
		// 			$('#vz-liste, #vz-liste > .lmfabcl-nf').removeClass('loading');
		// 			$('.mcon').removeClass('loading').html('');
		// 		});
		// 		console.log($(this).data('vzid'), 'laden ...');
		// 	}
		// });
	});
})(jQuery);
