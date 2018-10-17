/* global jQuery csrf alert confirm aurl $ unsavedAntworten:true unsavedEIAufgabe:true tagEbenenOptionUpdateAll familienHinzufuegenKnopfUpdate checkEbenen getTagsObject */

(function ($) {
	jQuery(document).ready(function ($) {
		/* Inits */

		/* On */
		/* Formular */
		$(document).on('click', '#antwortensave:not(.disabled)', antwortenSpeichernClick);
	});
})(jQuery);

/* Formular geladen */
function lmfabcLoaded () {
	tagEbenenOptionUpdateAll();
	familienHinzufuegenKnopfUpdate();
}

/* On */
function antwortenSpeichernClick (e) {
	if (confirm('Änderungen werden automatisch an allen betroffenen Antworten durchgeführt!\nWirklich speichern?')) {
		var saveit = 1;
		if (!checkEbenen()) { saveit = 0; };
		if (saveit === 1) {
			var sAufgabenmoeglichkeiten = [];
			$('#antwortensave').attr('disabled', true);
			$('.antwortmoeglichkeit').each(function () {
				var sAufgabenmoeglichkeit = {};
				$(this).find('input,textarea').each(function () {
					if ($(this).attr('type') === 'checkbox') {
						sAufgabenmoeglichkeit[$(this).attr('name')] = $(this).is(':checked');
					} else {
						sAufgabenmoeglichkeit[$(this).attr('name')] = $(this).val();
					}
				});
				sAufgabenmoeglichkeit['tags'] = getTagsObject($(this));
				sAufgabenmoeglichkeiten.push(sAufgabenmoeglichkeit);
			});
			$.post(aurl + 0 + '/' + $('input[name="id_Aufgabe"]').first().val() + '/', { csrfmiddlewaretoken: csrf, save: 'AufgabenmoeglichkeitenTags', aufgabenmoeglichkeiten: JSON.stringify(sAufgabenmoeglichkeiten) }, function (d) {
				unsavedAntworten = 0;
				$('#antwortensave').attr('disabled', false);
				$('#aufgabencontent').html(d);
				tagEbenenOptionUpdateAll();
				familienHinzufuegenKnopfUpdate();
			}).fail(function (d) {
				$('#antwortensave').attr('disabled', false);
				alert('error');
				console.log(d);
			});
		}
	}
}
