/* global csrf $ jQuery alert unsavedAntworten unsavedEIAufgabe lmfabcLoaded confirm localStorage */
(function ($) {
	jQuery(document).ready(function ($) {
		loadMitDaten();
		$(document).on('change', '#selaufgabe select:not(.noupdate)', function () { $('#selaufgabe').submit(); });
		$(document).on('click', '.lmfabc', function (e) {
			e.preventDefault();
			if ((unsavedAntworten === 0 && unsavedEIAufgabe === 0) || confirm('Es gibt noch ungespeicherte veränderungen! Wirklich verwerfen?')) {
				unsavedAntworten = 0;
				unsavedEIAufgabe = 0;
				$('.lmfabc').removeClass('open');
				$(this).addClass('open');
				$.post($(this).attr('href'), { csrfmiddlewaretoken: csrf }, function (d) {
					$('.mcon').html(d);
					lmfabcLoaded();
				}).fail(function (d) {
					alert('error');
					console.log(d);
				});
			}
		});
		$(document).on('change', '#mitDaten', setMitDaten);
	});
})(jQuery);

function loadMitDaten () {
	if (typeof (Storage) !== 'undefined') {
		if (localStorage.KorpusDBmitDaten && localStorage.KorpusDBmitDaten === 'on') {
			$('#mitDaten').prop('checked', true);
		} else {
			$('#mitDaten').prop('checked', false);
		}
	}
	setMitDaten(null, localStorage.KorpusDBmitDaten);
}
function setMitDaten (e, fd = null) {
	if ($('#mitDaten').is(':checked') || fd) {
		$('option.noData').hide();
		if (typeof (Storage) !== 'undefined') { localStorage.setItem('KorpusDBmitDaten', 'on'); }
	} else {
		$('option.noData').show();
		if (typeof (Storage) !== 'undefined') { localStorage.setItem('KorpusDBmitDaten', 'off'); }
	}
}
