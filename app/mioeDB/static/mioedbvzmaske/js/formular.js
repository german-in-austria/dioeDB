/* global jQuery alert csrf aurl */

(function ($) {
	jQuery(document).ready(function ($) {
		$(document).on('change', '#menue-mioe-ort, #menue-mioe-vz', function (e) {
			console.log('Ort: ', $('#menue-mioe-ort').val(), $('#menue-mioe-ort').val() > 0, 'VZ: ', $('#menue-mioe-vz').val(), $('#menue-mioe-vz').val() > 0);
			if (!$('.mcon').hasClass('loading')) {
				$('.mcon').addClass('loading').html('Lade ...');
				// Speicherdaten ermitteln
				$.post(aurl, { csrfmiddlewaretoken: csrf, getmask: 1, aMioeOrtId: $('#menue-mioe-ort').val(), aVzId: $('#menue-mioe-vz').val() }, function (d) {
					$('.mcon').removeClass('loading');
					let aData = JSON.parse(d);
					if (aData.status === 'success') {
						vzdRendering(aData.html);
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
				let sVzData = [];
				$('.vzd-line').each(function () {
					let aVzDataSet = $(this);
					let sVzDataSet = {};
					sVzDataSet.datenPk = aVzDataSet.find('.vzd-daten-pk').val();
					sVzDataSet.artId = aVzDataSet.find('.vzd-art').val();
					sVzDataSet.artAnzahl = aVzDataSet.find('.vzd-anzahl').val();
					sVzDataSet.artKommentar = aVzDataSet.find('.vzd-kommentar').val();
					sVzData.push(sVzDataSet);
				});
				$.post(aurl, { csrfmiddlewaretoken: csrf, getmask: 1, aMioeOrtId: $('#menue-mioe-ort').val(), aVzId: $('#menue-mioe-vz').val(), sVzData: JSON.stringify(sVzData), save: 1 }, function (d) {
					$('.mcon').removeClass('loading');
					let aData = JSON.parse(d);
					if (aData.status === 'success') {
						vzdRendering(aData.html);
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
		$(document).on('change keyup', '.vzd-anzahl', function (e) {
			$('#antwortensave').removeClass('disabled');
			vzdAnzahlChanged();
		});
		$(document).on('change keyup', '.vzd-kommentar', function (e) {
			$('#antwortensave').removeClass('disabled');
			if (getShowAbivz()) {
				setShowAbivz(true);
			}
		});
		$(document).on('click', '#vzd-show-abivz', function (e) {
			setShowAbivz($('#vzd-show-abivz > span').hasClass('glyphicon-eye-open'));
		});
		function vzdAnzahlChanged () {
			$('#statinfo').removeClass('alert-info alert-danger alert-warning').html('');
			let aSum = [0, 0];
			let aLineEmpty = [false, false];
			let sDg = 0;
			$('.vzd-anzahl:not(.vzd-gesamt)').each(function () {
				if ($(this).parents('tr').hasClass('vzd-varietaet')) { sDg = 0; };
				if ($(this).parents('tr').hasClass('vzd-religion')) { sDg = 1; };
				let aVal = $(this).val();
				if (aVal > 0 || aVal === '0') {
					aSum[sDg] += parseInt(aVal);
				} else {
					aLineEmpty[sDg] = true;
				}
			});
			let gSum = $('.vzd-gesamt').val();
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
		function vzdRendering (content) {
			$('.mcon').html('');
			$('.mcon').html(content);
			setTimeout(vzdAnzahlChanged, 250);
			$('.mcon .vzd-line.vzd-varietaet').first().before('<tr><td colspan="3"><h4>Varietäten</h4></td></tr>');
			$('.mcon .vzd-line.vzd-religion').first().before('<tr><td colspan="3"><h4>Religionen</h4></td></tr>');
			setShowAbivz(getShowAbivz());
		}
		function getShowAbivz () {
			let showAbivz = false;
			$('.vzd-kommentar').each(function () {
				if ($(this).val()) {
					showAbivz = true;
				}
			});
			if (showAbivz) {
				$('#vzd-show-abivz').addClass('hidden');
			} else {
				$('#vzd-show-abivz').removeClass('hidden');
			}
			return showAbivz;
		}
		function setShowAbivz (show) {
			if (show) {
				$('#vzd-show-abivz > span').removeClass('glyphicon-eye-open').addClass('glyphicon-eye-close');
				$('.vzd-hide-abivz').removeClass('hidden');
			} else {
				$('.vzd-hide-abivz').addClass('hidden');
				$('#vzd-show-abivz > span').removeClass('glyphicon-eye-close').addClass('glyphicon-eye-open');
			}
		}
	});
})(jQuery);
