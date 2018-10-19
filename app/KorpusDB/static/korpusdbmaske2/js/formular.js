/* global jQuery csrf alert confirm aurl $ setAudioMarks secondsToDuration durationToSeconds unsavedAntworten:true unsavedEIAufgabe:true tagEbenenOptionUpdateAll familienHinzufuegenKnopfUpdate getTagsObject resetReihungTags */

(function ($) {
	jQuery(document).ready(function ($) {
		/* Inits */
		formFirstFocus();

		/* On */
		/* Allgemein */
		$(document).on('change', '#ainformantErhebung', updateAinformantErhebung);
		/* Formular */
		$(document).on('change', '.aufgabeantwort input,.aufgabeantwort textarea,select.tagebene', formularChanged);
		$(document).on('click', '#antwortensave:not(.disabled)', antwortenSpeichernClick);
		$(document).on('click', 'tr .addantwort', addAntwortTr);
		$(document).on('click', 'tr .delantwort', delAntwortTr);
		$(document).on('click', '.addantwort.aa234', addAntwort);
		$(document).on('click', '.antwort .delantwort', delAntwort);
	});
})(jQuery);

/* Formular geladen */
function lmfabcLoaded () {
	tagEbenenOptionUpdateAll();
	familienHinzufuegenKnopfUpdate();
	resetReihungTags();
	formFirstFocus();
}

/* On */
function antwortenSpeichernClick (e) {
	var saveit = 1;
	if (saveit === 1) {
		var sAntworten = [];
		$('#antwortensave').attr('disabled', true);
		$('.aufgabeantwort').each(function () {
			var sAntwort = {};
			var subdg, laufpk, lantpk, ldg;
			subdg = laufpk = lantpk = ldg = -1;
			if ($(this).hasClass('delit')) {
				sAntwort['delit'] = 1;
			}
			$(this).find('input,textarea').each(function () {
				if ($(this).parents('.vorlage').length === 0) {
					var aAntwort;
					if ($(this).attr('type') === 'checkbox') {
						aAntwort = $(this).is(':checked');
					} else {
						aAntwort = $(this).val();
					}
					var amkl = $(this).parents('.antwortmoeglichkeiten-line');
					var adiv = $(this).parents('.antwort');
					if (amkl.length > 0) {
						if (laufpk !== amkl.data('aufgabenm-pk') || lantpk !== amkl.data('antworten-pk') || ldg !== amkl.data('dg')) {
							subdg = subdg + 1;
							if (!sAntwort.hasOwnProperty('sub')) { sAntwort['sub'] = []; };
							if (!sAntwort['sub'].hasOwnProperty(subdg)) { sAntwort['sub'][subdg] = {}; };
							sAntwort['sub'][subdg]['tags'] = getTagsObject(amkl);
							laufpk = amkl.data('aufgabenm-pk');
							lantpk = amkl.data('antworten-pk');
							ldg = amkl.data('dg');
						}
						sAntwort['sub'][subdg]['sys_aufgabenm_pk'] = amkl.data('aufgabenm-pk');
						sAntwort['sub'][subdg]['sys_antworten_pk'] = amkl.data('antworten-pk');
						sAntwort['sub'][subdg]['dg'] = amkl.data('dg');
						if (amkl.hasClass('delit')) {
							sAntwort['sub'][subdg]['delit'] = 1;
						}
						sAntwort['sub'][subdg][$(this).attr('name')] = aAntwort;
					} else if (adiv.length > 0) {
						if (ldg !== adiv.data('dg')) {
							subdg = subdg + 1;
							ldg = adiv.data('dg');
						}
						if (!sAntwort.hasOwnProperty('sub')) { sAntwort['sub'] = []; };
						if (!sAntwort['sub'].hasOwnProperty(subdg)) { sAntwort['sub'][subdg] = {}; };
						sAntwort['sub'][subdg]['dg'] = adiv.data('dg');
						if (adiv.hasClass('delit')) {
							sAntwort['sub'][subdg]['delit'] = 1;
						}
						sAntwort['sub'][subdg][$(this).attr('name')] = aAntwort;
					} else {
						sAntwort[$(this).attr('name')] = aAntwort;
					}
				}
			});
			sAntworten.push(sAntwort);
		});
		console.log(sAntworten);
		$.post(aurl + $('input[name="von_Inf"]').first().val() + '/' + $('input[name="zu_Aufgabe"]').first().val() + '/', { csrfmiddlewaretoken: csrf, save: 'Aufgaben', aufgaben: JSON.stringify(sAntworten) }, function (d) {
			unsavedAntworten = 0;
			$('#antwortensave').attr('disabled', false);
			$('#aufgabencontent').html(d);
			informantenAntwortenUpdate();
			tagEbenenOptionUpdateAll();
			familienHinzufuegenKnopfUpdate();
			formFirstFocus();
		}).fail(function (d) {
			$('#antwortensave').attr('disabled', false);
			alert('error');
			console.log(d);
		});
	}
}
function antwortAudioBereichChange (e) {
	$(this).val(secondsToDuration(durationToSeconds($(this).val())));
	setAudioMarks();
}

/* Funktionen */
function updateAinformantErhebung () {
	if ($('#ainformantErhebung').val() === 0) {
		$('#ainformantErhebung').parents('.lmfa').find('.lmfa-l .lmfabc').parent().removeClass('ainferh-hide');
	} else {
		var aval = $('#ainformantErhebung').val();
		$('#ainformantErhebung').parents('.lmfa').find('.lmfa-l .lmfabc').each(function () {
			if (aval.match(new RegExp('(?:^|,)' + $(this).data('erhebungen') + '(?:,|$)'))) {
				$(this).parent().removeClass('ainferh-hide');
			} else {
				$(this).parent().addClass('ainferh-hide');
			}
		});
	}
}
function formularChanged () {
	unsavedAntworten = 1;
	$('#antwortensave').removeClass('disabled');
}
function erhInfAufgabeChanged () {
	unsavedEIAufgabe = 1;
	$('#eiaufgsave').removeClass('disabled');
}
function informantenAntwortenUpdate () {
	$.post(aurl + '0/0/', { csrfmiddlewaretoken: csrf, infantreset: 1, aauswahl: $('select[name="aauswahl"]').val(), ainformant: $('select[name="ainformant"]').val(), aphaenomen: $('select[name="aphaenomen"]').val(), aerhebung: $('select[name="aerhebung"]').val(), aaufgabenset: $('select[name="aaufgabenset"]').val(), aaufgabe: $('select[name="aaufgabe"]').val() }, function (d) {
		$('ul.lmfa-l').html(d);
		updateAinformantErhebung();
		formFirstFocus();
	}).fail(function (d) {
		alert('error');
		console.log(d);
	});
}
function formFirstFocus () {
	$('.aufgabeantwort input:visible,.aufgabeantwort textarea:visible').first().focus();
}
function addAntwortTr () {
	var vorlage = $(this).parents('tr').next();
	vorlage.data('dg', vorlage.data('dg') + 1);
	$(this).parents('tr').before(vorlage.clone().removeClass('vorlage').data('dg', vorlage.data('dg')));
	formularChanged();
}
function delAntwortTr () {
	if (confirm('Wirklich löschen?')) {
		$(this).parents('tr').addClass('delit');
		formularChanged();
	}
}
function addAntwort () {
	var vorlage = $(this).siblings('.antwort.vorlage');
	vorlage.data('dg', vorlage.data('dg') + 1);
	$(this).before(vorlage.clone().removeClass('vorlage').data('dg', vorlage.data('dg')));
	resetReihungTags();
	formularChanged();
}
function delAntwort () {
	if (confirm('Wirklich löschen?')) {
		$(this).parents('.antwort').addClass('delit');
		resetReihungTags();
		formularChanged();
	}
}
