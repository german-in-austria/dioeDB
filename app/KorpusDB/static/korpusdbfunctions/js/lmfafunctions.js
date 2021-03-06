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
				$('.mcon').addClass('loading');
				$.post($(this).attr('href'), { csrfmiddlewaretoken: csrf }, function (d) {
					$('.mcon').removeClass('loading');
					$('.mcon').html(d);
					lmfabcLoaded();
				}).fail(function (d) {
					$('.mcon').removeClass('loading');
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
	setMitDaten();
}
function setMitDaten (e) {
	if ($('#mitDaten').is(':checked')) {
		$('option.noData').hide();
		if (typeof (Storage) !== 'undefined') { localStorage.setItem('KorpusDBmitDaten', 'on'); }
	} else {
		$('option.noData').show();
		if (typeof (Storage) !== 'undefined') { localStorage.setItem('KorpusDBmitDaten', 'off'); }
	}
}
