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
						$('.mcon').html('');
						$('.mcon').html(aData.html);
						setTimeout(vzdAnzahlChanged, 250);
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
					sVzDataSet.artAbwBez = aVzDataSet.find('.vzd-abw-bez').val();
					sVzData.push(sVzDataSet);
				});
				$.post(aurl, { csrfmiddlewaretoken: csrf, getmask: 1, aMioeOrtId: $('#menue-mioe-ort').val(), aVzId: $('#menue-mioe-vz').val(), sVzData: JSON.stringify(sVzData), save: 1 }, function (d) {
					$('.mcon').removeClass('loading');
					let aData = JSON.parse(d);
					if (aData.status === 'success') {
						$('.mcon').html('');
						$('.mcon').html(aData.html);
						setTimeout(vzdAnzahlChanged, 250);
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
		$(document).on('change keyup', '.vzd-abw-bez', function (e) {
			$('#antwortensave').removeClass('disabled');
		});
		function vzdAnzahlChanged () {
			$('#statinfo').removeClass('alert-info alert-danger alert-warning').html('');
			let aSum = 0;
			let aLineEmpty = false;
			$('.vzd-anzahl:not(.vzd-gesamt)').each(function () {
				let aVal = $(this).val();
				if (aVal > 0 || aVal === '0') {
					aSum += parseInt(aVal);
				} else {
					aLineEmpty = true;
				}
			});
			let gSum = $('.vzd-gesamt').val();
			if (gSum > 0 || gSum === '0') {
				gSum = parseInt(gSum);
				if (aSum === gSum) {
					if (!aLineEmpty) {
						$('#statinfo').addClass('alert-info').html('Alles OK.');
					} else {
						$('#statinfo').addClass('alert-warning').html('Es wurden nicht alle Zeilen ausgefüllt!');
					}
				} else {
					$('#statinfo').addClass('alert-danger').html('"Gesamt": <b>' + gSum + '</b> entspricht nicht der Summe: <b>' + aSum + '</b> (Differenz: ' + (aSum - gSum) + ')');
				}
			} else {
				$('#statinfo').addClass('alert-danger').html('Es wurde kein "Gesamt" angeben! (Reihung 1)');
			}
		}
	});
})(jQuery);
