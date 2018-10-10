/* global csrf jQuery alert unsavedAntworten unsavedEIAufgabe lmfabcLoaded confirm */
(function ($) {
	jQuery(document).ready(function ($) {
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
	});
})(jQuery);
