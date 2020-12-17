/* global jQuery alert csrf aurl */

(function ($) {
	jQuery(document).ready(function ($) {
		$(document).on('change', '#menue-mioe-inst', function (e) {
			console.log('INST: ', $('#menue-mioe-inst').val(), $('#menue-mioe-inst').val() > 0);
			if (!$('.mcon').hasClass('loading')) {
				$('.mcon').addClass('loading').html('Lade ...');
				// Speicherdaten ermitteln
				$.post(aurl, { csrfmiddlewaretoken: csrf, getmask: 1, aInstId: $('#menue-mioe-inst').val() }, function (d) {
					$('.mcon').removeClass('loading');
					let aData = JSON.parse(d);
					if (aData.status === 'success') {
						instdRendering(aData.html);
					} else {
						alert('Es ist ein Fehler aufgetreten:\n\n' + aData.error);
						console.log(d);
					}
				}).fail(function (d) {
					var aError = d['responseText'].split('\n', 10);
					alert('Es ist ein Fehler aufgetreten:\n\n' + aError[0] + '\n' + aError[1] + '\n' + aError[2]);
					console.log(d);
					$('.mcon').removeClass('loading');
				});
			}
		});
		$(document).on('click', '#antwortensave:not(.disabled)', function (e) {
			if (!$('.mcon').hasClass('loading')) {
				$('.mcon').addClass('loading');
				$('#antwortensave').addClass('disabled');
				let sInstData = [];
				$('.instd-line').each(function () {
					let aInstDataSet = $(this);
					let sInstDataSet = {};
					sInstDataSet.datenPk = aInstDataSet.find('.instd-daten-pk').val();
					sInstDataSet.artId = aInstDataSet.find('.instd-art').val();
					sInstDataSet.artAnzahl = aInstDataSet.find('.instd-anzahl').val();
					sInstDataSet.artKommentar = aInstDataSet.find('.instd-kommentar').val();
					sInstData.push(sInstDataSet);
				});
				$.post(aurl, { csrfmiddlewaretoken: csrf, getmask: 1, aInstId: $('#menue-mioe-inst').val(), sInstData: JSON.stringify(sInstData), save: 1 }, function (d) {
					$('.mcon').removeClass('loading');
					let aData = JSON.parse(d);
					if (aData.status === 'success') {
						instdRendering(aData.html);
					} else {
						alert('Es ist ein Fehler aufgetreten:\n\n' + aData.error);
						console.log(d);
					}
				}).fail(function (d) {
					var aError = d['responseText'].split('\n', 10);
					alert('Es ist ein Fehler aufgetreten:\n\n' + aError[0] + '\n' + aError[1] + '\n' + aError[2]);
					console.log(d);
					$('.mcon').removeClass('loading');
					$('#antwortensave').removeClass('disabled');
				});
			}
		});
		$(document).on('change keyup', '.instd-anzahl', function (e) {
			$('#antwortensave').removeClass('disabled');
			instdAnzahlChanged();
		});
		$(document).on('change keyup', '.instd-kommentar', function (e) {
			$('#antwortensave').removeClass('disabled');
			if (getShowAbiinst()) {
				setShowAbiinst(true);
			}
		});
		$(document).on('click', '#instd-show-abiinst', function (e) {
			setShowAbiinst($('#instd-show-abiinst > span').hasClass('glyphicon-eye-open'));
		});
		function instdAnzahlChanged () {
			$('#statinfo').removeClass('alert-info alert-danger alert-warning').html('');
			let aSum = [0, 0];
			let aLineEmpty = [false, false];
			let sDg = 0;
			$('.instd-anzahl:not(.instd-gesamt)').each(function () {
				if ($(this).parents('tr').hasClass('instd-varietaet')) { sDg = 0; };
				if ($(this).parents('tr').hasClass('instd-religion')) { sDg = 1; };
				let aVal = $(this).val();
				if (aVal > 0 || aVal === '0') {
					aSum[sDg] += parseInt(aVal);
				} else {
					aLineEmpty[sDg] = true;
				}
			});
			let gSum = $('.instd-gesamt').val();
			if (gSum > 0 || gSum === '0') {
				let alertClass = 'alert-info';
				let alertText = ['Varietäten: ', 'Religionen: '];
				for (var i = 0; i < 2; i++) {
					gSum = parseInt(gSum);
					if (aSum[i] === gSum) {
						if (!aLineEmpty[i]) {
							alertText[i] += 'Alles OK.';
						} else {
							if (alertClass !== 'alert-danger') { alertClass = 'alert-warning'; };
							alertText[i] += 'Es wurden nicht alle Zeilen ausgefüllt!';
						}
					} else {
						alertClass = 'alert-danger';
						alertText[i] += '"Gesamt": <b>' + gSum + '</b> entspricht nicht der Summe: <b>' + aSum[i] + '</b> (Differenz: ' + (aSum[i] - gSum) + ')';
					}
				}
				$('#statinfo').addClass(alertClass).html(alertText[0] + '<br>' + alertText[1]);
			} else {
				$('#statinfo').addClass('alert-danger').html('Es wurde kein "Gesamt" angeben! (Reihung 1)');
			}
		}
		function instdRendering (content) {
			$('.mcon').html('');
			$('.mcon').html(content);
			setTimeout(instdAnzahlChanged, 250);
			$('.mcon .instd-line.instd-varietaet').first().before('<tr><td colspan="3"><h4>Varietäten</h4></td></tr>');
			$('.mcon .instd-line.instd-religion').first().before('<tr><td colspan="3"><h4>Religionen</h4></td></tr>');
			setShowAbiinst(getShowAbiinst());
		}
		function getShowAbiinst () {
			let showAbiinst = false;
			$('.instd-kommentar').each(function () {
				if ($(this).val()) {
					showAbiinst = true;
				}
			});
			if (showAbiinst) {
				$('#instd-show-abiinst').addClass('hidden');
			} else {
				$('#instd-show-abiinst').removeClass('hidden');
			}
			return showAbiinst;
		}
		function setShowAbiinst (show) {
			if (show) {
				$('#instd-show-abiinst > span').removeClass('glyphicon-eye-open').addClass('glyphicon-eye-close');
				$('.instd-hide-abiinst').removeClass('hidden');
			} else {
				$('.instd-hide-abiinst').addClass('hidden');
				$('#instd-show-abiinst > span').removeClass('glyphicon-eye-close').addClass('glyphicon-eye-open');
			}
		}
	});
})(jQuery);
