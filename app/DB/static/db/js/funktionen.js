/* global jQuery $ makeModal csrf viewurl setSearchfields makeScrollTo alert L makeSearch */

/* Funktionen */
/* jQuery */
(function ($) {
	$.fn.progenyWithoutAncestors = function (notAncestors, aFind) {	/* Finde alle "aFind" die nicht Nachkommen von "notAncestors" sind */
		var $found = $();
		var $currentSet = this;
		while ($currentSet.length) {
			$currentSet = $currentSet.not(notAncestors);
			var $cfound = $currentSet.filter(aFind);
			if ($cfound.length) {
				var $curfound = $currentSet.filter(aFind);
				if ($found.length) {
					$found = $found.add($curfound);
				} else {
					$found = $curfound;
				}
				$currentSet = $currentSet.not($curfound).children();
			} else {
				$currentSet = $currentSet.children();
			}
		}
		return $found;
	};
})(jQuery);

	/* Allgemein */
function fxinputs () {
	$('.dateinput').datetimepicker({
		locale: 'de',
		format: 'DD.MM.YYYY',
		showClear: true
	});
	$('.datetimeinput').datetimepicker({
		locale: 'de',
		format: 'DD.MM.YYYY HH:mm',
		showClear: true,
		stepping: 1
	});
	$('input.durationinput').each(function () {
		if ($(this).val()) { $(this).val(secondsToDuration(durationToSeconds($(this).val()))); };
	});
	$('label').each(function () {
		if ($(this).text() && $(this).text().indexOf('(HTML)') > -1) {
			let eto = $(this).siblings('div');
			if (eto) {
				eto = eto.children('textarea');
				if (eto) {
					eto.hide();
					// eto.after('<div data-tiny-editor>' + eto.val() + '</div>');
					const div = document.createElement("div");
		      div.dataset["tinyEditor"] = "";
					// div.dataset["formatblock"] = "no";
					div.dataset["fontname"] = "no";
					div.dataset["forecolor"] = "no";
					div.dataset["justifyleft"] = "no";
					div.dataset["justifycenter"] = "no";
					div.dataset["justifyright"] = "no";
					div.dataset["insertorderedlist"] = "no";
					div.dataset["insertunorderedlist"] = "no";
					div.dataset["outdent"] = "no";
					div.dataset["indent"] = "no";
					div.dataset["removeFormat"] = "no";
					let aVal = eto.val().trim();
					div.innerHTML = aVal;
		      eto[0].after(div);
		      window.__tinyEditor.transformToEditor(div);
					div.addEventListener('input', e => {
						// console.log(e, 'x', $(e.target))
						$(e.target).siblings('textarea').val(e.target.innerHTML);
					});
					console.log($(this), eto, div);
				}
			}
		}
	})
}

/* Elemente */
function onSelobjModal (athis) {													/* Modal mit ForeignKey Select laden */
	makeModal('Lade ...', 'Datensatz wird geladen ...', 'viewobjmodal');
	var aelement = athis;
	$('.seleobj,.seleobjosm').removeClass('lsel');
	$(aelement).addClass('loading lsel');
	$.post(viewurl + $(aelement).data('appname') + '/' + $(aelement).data('tabname'), { csrfmiddlewaretoken: csrf, getforeignkeysel: $(aelement).data('obj-pk') }, function (d, e, f, g = aelement) {
		if ($('#js-modal.viewobjmodal').length > 0) {
			$('#js-modal.viewobjmodal .modal-dialog').addClass('modal-xlg');
			$('#js-modal.viewobjmodal .modal-title').html('Datensatz auswählen:');
			$('#js-modal.viewobjmodal .modal-body').html(d);
			$('#js-modal.viewobjmodal .modal-footer').html('<button id="seleobjbtnnone" type="button" class="btn btn-warning">Auswahl aufheben</button><button id="seleobjbtn" type="button" class="btn btn-primary">Auswählen</button><button id="closeobjbtn" type="button" class="btn btn-default">Schließen</button>');
			$('#js-modal.viewobjmodal .modal-body,#js-modal.viewobjmodal .modal-body>.row').css({'height': $(window).height() * 0.8, 'overflow': 'hidden', 'padding': '0px', 'margin': '0px'});
			setSearchfields();
			makeScrollTo();
			setTimeout(setMaps, 500);
		}
		$(g).removeClass('loading');
		setTimeout(function () { $('#js-modal.viewobjmodal .lmfasf').focus(); }, 500);
		console.log('seleobj - ' + $(g).data('appname') + '/' + $(g).data('tabname') + ', ' + $(g).data('obj-pk') + ' - Geladen');
	}).fail(function (d, e, f, g = aelement) {
		var aError = d['responseText'].split('\n', 10);
		alert('Es ist ein Fehler aufgetreten:\n\n' + aError[0] + '\n' + aError[1] + '\n' + aError[2]);
		$(g).removeClass('loading');
		console.log(d);
	});
}

/* Audioplayer */
function durationToSeconds (hms) {
	var s = 0.0;
	if (hms && hms.indexOf(':') > -1) {
		var a = hms.split(':');
		if (a.length > 2) { s += parseFloat(a[a.length - 3]) * 60 * 60; }
		if (a.length > 1) { s += parseFloat(a[a.length - 2]) * 60; }
		if (a.length > 0) { s += parseFloat(a[a.length - 1]); }
	} else {
		s = parseFloat(hms);
		if (isNaN(s)) { s = 0.0; }
	}
	return s;
}
function secondsToDuration (sec) {
	var v = '';
	if (sec < 0) { sec = -sec; v = '-'; }
	var h = parseInt(sec / 3600);
	sec %= 3600;
	var m = parseInt(sec / 60);
	var s = sec % 60;
	return v + ('0' + h).slice(-2) + ':' + ('0' + m).slice(-2) + ':' + ('0' + s.toFixed(6)).slice(-9);
}

/* OpenStreetMap */
var map;
var locationStyle = { 'color': '#ff7800', 'weight': 5, 'opacity': 0.65 };
var geojsonLayer;
function getOsmDatenbankEintrag (OrtPK, OrtName, osmId, osmType) {
	$('#osmDatenbank').html('Auswahl: <span id="osmAusgewaehlt" data-ortpk="' + OrtPK + '" data-orte-osm-id="' + osmId + '" data-orte-osm-type="' + osmType + '">' + OrtName + '</span> (PK: ' + OrtPK + ')');
}
function geojsonLayerSet (data, oid, amap) {
	if (geojsonLayer) { amap.removeLayer(geojsonLayer); }
	geojsonLayer = L.geoJSON(data.geojson, {style: locationStyle}).addTo(amap);
	if (data.geojson.type === 'Point') {
		amap.setView(new L.LatLng(data.lat, data.lon), 11);
	} else {
		amap.fitBounds(geojsonLayer.getBounds());
	};
	if (oid > 0) { /* Datenbankeintrag vorhanden */
		getOsmDatenbankEintrag(oid, data.display_name, data.osm_id, data.osm_type);
	} else { /* Datenbankeintrag erstellen? */
		$('#osmDatenbank').html('<div class="important-box">Datensatz für <b>"' + data.display_name + '"</b> erstellen? <a href="#" id="osmDatensatzErstellen" class="btn btn-primary btn-fx" data-osm-id="' + data.osm_id + '" data-osm-type="' + data.osm_type + '" data-ort-namelang="' + data.display_name + '" data-lat="' + data.lat + '" data-lon="' + data.lon + '">Ja</a></div>');
	}
}
var osmapin;
function setMaps () {
	if ($('#osmapin').length > 0) {
		var aelement = $('#osmapin');
		osmapin = new L.Map('osmapin');
		var osmUrl = '//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
		var osmAttribution = 'Map data &copy; <a href="//openstreetmap.org">OpenStreetMap</a> contributors';
		var osmin = new L.TileLayer(osmUrl, {maxZoom: 18, attribution: osmAttribution});
		osmapin.setView(new L.LatLng(aelement.data('lat'), aelement.data('lon')), 12).addLayer(osmin);
		if (aelement.data('osm-id')) {
			$.getJSON('//nominatim.openstreetmap.org/reverse?format=json&polygon_geojson=1&osm_type=' + aelement.data('osm-type').charAt(0).toUpperCase() + '&osm_id=' + encodeURI(aelement.data('osm-id')), function (data, b, c, d = aelement) {
				geojsonLayerSet(data, aelement.data('obj-pk'), osmapin);
			}).fail(function (data, b, c, d = aelement) {
				var aError = data['responseText'].split('\n', 10);
				alert('Es ist ein Fehler aufgetreten:\n\n' + aError[0] + '\n' + aError[1] + '\n' + aError[2]);
				console.log(data);
			});
		}
	}
}
$(document).on('click', '#osmDatensatzErstellen:not(.loading)', function (e) {
	e.preventDefault();
	var aData = $('#osmDatensatzErstellen');
	$('#osmDatensatzErstellen').addClass('loading');
	$.post(viewurl + 'PersonenDB/tbl_orte', { csrfmiddlewaretoken: csrf, savepk: 0, saveform: 1, osm_id: aData.data('osm-id'), osm_type: aData.data('osm-type'), ort_namelang: aData.data('ort-namelang'), lat: aData.data('lat'), lon: aData.data('lon') }, function (d) {
		var newOrtPK = $('<div>' + d + '</div>').find('.editobj').data('obj-pk');
		aData = $('#osmDatensatzErstellen');
		$('#osm' + aData.data('osm-id') + aData.data('osm-type')).data('OrtPK', newOrtPK).addClass('indatenbank');
		getOsmDatenbankEintrag(newOrtPK, aData.data('ort-namelang'), aData.data('osm-id'), aData.data('osm-type'));
		console.log('saveobj - Ort - ' + newOrtPK);
		setMaps();
	}).fail(function (d) {
		var aError = d['responseText'].split('\n', 10);
		alert('Es ist ein Fehler aufgetreten:\n\n' + aError[0] + '\n' + aError[1] + '\n' + aError[2]);
		$('#osmDatensatzErstellen').removeClass('loading');
		console.log(d);
	});
});
function onSelobjOsmModal (athis) {											/* Modal mit OpenStreetMap Select laden */
	$('.seleobj,.seleobjosm').removeClass('lsel');
	$(athis).addClass('lsel');
	makeModal('Ort auswählen ...', '<div id="osmap"></div><br><div class="row"><div class="col-md-6"><div class="form-inline"><div class="form-group"><input type="text" class="form-control" id="osmOrt"></div><button id="osmSuche" type="submit" class="btn btn-default">Ort suchen</button></div></div><div class="col-md-6" id="osmDatenbank"></div></div><br><div id="osmWahl"></div>', 'viewosmmodal');
	$('#js-modal.viewosmmodal .modal-footer').html('<button id="seleosmbtnnone" type="button" class="btn btn-warning">Auswahl aufheben</button><button id="seleosmbtn" type="button" class="btn btn-primary">Auswählen</button><button id="closeosmbtn" type="button" class="btn btn-default">Schließen</button>');
	$('#js-modal.viewosmmodal').on('hidden.bs.modal', function () { map.remove(); });
	$('#js-modal.viewosmmodal').on('shown.bs.modal', function () {
		map = new L.Map('osmap');
		var osmUrl = '//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
		var osmAttribution = 'Map data &copy; <a href="//openstreetmap.org">OpenStreetMap</a> contributors';
		var osm = new L.TileLayer(osmUrl, {maxZoom: 18, attribution: osmAttribution});
		map.setView(new L.LatLng(48.2083537, 16.3725042), 12).addLayer(osm);
		if ($(athis).data('obj-pk')) {
			$.post('/db/search', { csrfmiddlewaretoken: csrf, getort: $(athis).data('obj-pk') }, function (d) {
				if (d.substr(0, 2) === 'OK') {
					var aortdata = jQuery.parseJSON(d.substr(2));
					console.log(aortdata);
					map.setView(new L.LatLng(aortdata.lat, aortdata.lon), 12);
					$.getJSON('//nominatim.openstreetmap.org/reverse?format=json&polygon_geojson=1&osm_type=' + aortdata.osm_type.charAt(0).toUpperCase() + '&osm_id=' + encodeURI(aortdata.osm_id), function (data, b, c, d = aortdata) {
						geojsonLayerSet(data, aortdata.pk, map);
					}).fail(function (data) {
						var aError = d['responseText'].split('\n', 10);
						alert('Es ist ein Fehler aufgetreten:\n\n' + aError[0] + '\n' + aError[1] + '\n' + aError[2]);
						console.log(data);
					});
				} else {
					var aError = d['responseText'].split('\n', 10);
					alert('Es ist ein Fehler aufgetreten:\n\n' + aError[0] + '\n' + aError[1] + '\n' + aError[2]);
					console.log(d);
				}
			}).fail(function (d) {
				var aError = d['responseText'].split('\n', 10);
				alert('Es ist ein Fehler aufgetreten:\n\n' + aError[0] + '\n' + aError[1] + '\n' + aError[2]);
				$('.osmAuswahl').removeClass('loading');
				console.log(d);
			});
		}
		$('#osmOrt').focus();
	});
}
function onSeleosmbtnnone (athis) {	/* Auswahl aufheben (osm ForeignKey) */
	var aseltar = $('.seleobjosm.lsel').parents('.form-control-static');
	aseltar.find('.seleobj, .seleobjosm, .openobj, .viewobj').data('obj-pk', 0);
	aseltar.find('input[type="hidden"]').val('None');
	aseltar.children('span').addClass('grey').html('Keine Eingabe vorhanden');
	aseltar.find('.openobj, .viewobj').addClass('hidden');
	$('#js-modal').modal('hide');
	aseltar.find('.seleobjosm').focus();
}
function onSeleosmbtn (athis) {	/* Auswahl setzen (osm ForeignKey) */
	if ($('#osmAusgewaehlt').length > 0) {
		var aseltar = $('.seleobjosm.lsel').parents('.form-control-static');
		aseltar.find('.seleobj, .seleobjosm, .openobj, .viewobj').data('obj-pk', $('#osmAusgewaehlt').data('ortpk'));
		aseltar.find('input[type="hidden"]').val($('#osmAusgewaehlt').data('ortpk'));
		aseltar.children('span').removeClass('grey').html($('#osmAusgewaehlt').text());
		aseltar.find('.openobj, .viewobj').removeClass('hidden');
		$('#js-modal').modal('hide');
		aseltar.find('.seleobjosm').focus();
	} else {
		alert('Es wurde keine Auswahl getroffen!');
	}
}
function osmSuche () {	/* OpenStreetMap Suche ausführen */
	var osmOrt = $('#osmOrt').val();
	$('#osmSuche,#osmOrt').addClass('loading');
	if ($('#osmDatensatzErstellen').length > 0) { $('#osmDatenbank').html(''); }
	if (geojsonLayer) { map.removeLayer(geojsonLayer); }
	$.getJSON('//nominatim.openstreetmap.org/search?format=json&limit=10&q=' + encodeURI(osmOrt), function (data) {
		var osmOrte = ''; var osmOrteDB = [];
		$.each(data, function (key, val) {
			if (val.osm_id && val.type !== 'river' && val.type !== 'canal' && val.type !== 'aerodrome') {
				osmOrte += '<li><a href="#" title="' + val.type + '" class="osmAuswahl loading" id="osm' + val.osm_id + val.osm_type + '" data-orte-osm-id="' + val.osm_id + '" data-orte-osm-type="' + val.osm_type + '" data-orte-lat="' + val.lat + '" data-orte-lon="' + val.lon + '" data-display-name="' + val.display_name + '">' + ((val.icon) ? '<img src="' + val.icon + '">' : '<span class="noosmicon">?</span>') + ' ' + val.display_name + '</a></li>';
				osmOrteDB.push({osm_id: val.osm_id, osm_type: val.osm_type});
			}
		});
		if (osmOrte.length > 0) {
			$('#osmWahl').html('<ul>' + osmOrte + '</ul>');
			$.post('/db/search', { csrfmiddlewaretoken: csrf, sucheorte: 1, suchorte: JSON.stringify(osmOrteDB) }, function (d) {
				$('.osmAuswahl').removeClass('loading');
				if (d.substr(0, 2) === 'OK') {
					var ifirst = 1;
					$.each(jQuery.parseJSON(d.substr(2)), function (key, val) {
						if (val.ort_pk > 0) {
							$('#osm' + val.osm_id + val.osm_type).data('OrtPK', val.ort_pk).addClass('indatenbank');
							if (ifirst === 1) {
								$('#osm' + val.osm_id + val.osm_type).click();
								ifirst = 0;
							}
						}
					});
				} else {
					var aError = d['responseText'].split('\n', 10);
					alert('Es ist ein Fehler aufgetreten:\n\n' + aError[0] + '\n' + aError[1] + '\n' + aError[2]);
					console.log(d);
				}
			}).fail(function (d) {
				var aError = d['responseText'].split('\n', 10);
				alert('Es ist ein Fehler aufgetreten:\n\n' + aError[0] + '\n' + aError[1] + '\n' + aError[2]);
				$('.osmAuswahl').removeClass('loading');
				console.log(d);
			});
		} else {
			$('#osmWahl').html('<p>Kein Ort gefunden!</p>');
		}
		$('#osmSuche,#osmOrt').removeClass('loading');
	}).fail(function (data) {
		var aError = data['responseText'].split('\n', 10);
		alert('Es ist ein Fehler aufgetreten:\n\n' + aError[0] + '\n' + aError[1] + '\n' + aError[2]);
		$('#osmSuche,#osmOrt').removeClass('loading');
		console.log(data);
	});
}
$(document).on('click', '#osmSuche:not(.loading)', function () {
	osmSuche();
});
$(document).on('keypress', '#osmOrt:not(.loading)', function (e) {
	if (e.which === 13) {
		osmSuche();
	}
});
$(document).on('click', '#closeosmbtn', function () {
	var aseltar = $('.seleobjosm.lsel').parents('.form-control-static');
	$('#js-modal').modal('hide');
	aseltar.find('.seleobjosm').focus();
});
$(document).on('click', '#closeobjbtn', function () {
	var aseltar = $('.seleobj.lsel').parents('.form-control-static');
	$('#js-modal').modal('hide');
	aseltar.find('.seleobj').focus();
});
$(document).on('click', '.osmAuswahl:not(.loading)', function (e) {	/* Auswahl anzeigen */
	e.preventDefault();
	if ($(this).data('orte-data')) {
		geojsonLayerSet($(this).data('orte-data'), $(this).data('OrtPK'), map);
	} else {
		$(this).addClass('loading');
		map.panTo(new L.LatLng($(this).data('orte-lat'), $(this).data('orte-lon')));
		var aelement = $(this);
		$.getJSON('//nominatim.openstreetmap.org/reverse?format=json&polygon_geojson=1&osm_type=' + $(this).data('orte-osm-type').charAt(0).toUpperCase() + '&osm_id=' + encodeURI($(this).data('orte-osm-id')), function (data, b, c, d = aelement) {
			d.data('orte-data', data);
			geojsonLayerSet(data, aelement.data('OrtPK'), map);
			d.removeClass('loading');
		}).fail(function (data, b, c, d = aelement) {
			var aError = data['responseText'].split('\n', 10);
			alert('Es ist ein Fehler aufgetreten:\n\n' + aError[0] + '\n' + aError[1] + '\n' + aError[2]);
			d.removeClass('loading');
			console.log(data);
		});
	}
});
function onSeleobjbtnnone (athis) {	/* Auswahl aufheben (ForeignKey) */
	var aseltar = $('.seleobj.lsel').parents('.form-control-static');
	aseltar.find('.seleobj, .seleobjosm, .viewobj, .openobj').data('obj-pk', 0);
	aseltar.find('input[type="hidden"],select.foreignkeyselect').val('None').trigger('change');
	aseltar.children('span').addClass('grey').html('Keine Eingabe vorhanden');
	aseltar.find('.viewobj, .openobj').addClass('hidden');
	$('#js-modal').modal('hide');
	aseltar.find('.seleobj').focus();
}
function onSeleobjbtn (athis) {	/* Auswahl setzen (ForeignKey) */
	var aselobj = $(athis).parents('.modal-content');
	if (aselobj.find('.lmfabcl.open').data('lmfabcl-id') > 0) {
		var aseltar = $('.seleobj.lsel').parents('.form-control-static');
		aseltar.find('.seleobj, .seleobjosm, .viewobj, .openobj').data('obj-pk', aselobj.find('.lmfabcl.open').data('lmfabcl-id'));
		aseltar.find('input[type="hidden"],select.foreignkeyselect').val(aselobj.find('.lmfabcl.open').data('lmfabcl-id')).trigger('change');
		aseltar.children('span').removeClass('grey').html(aselobj.find('.lmfabcl.open').html());
		aseltar.find('.viewobj, .openobj').removeClass('hidden');
		$('#js-modal').modal('hide');
		aseltar.find('.seleobj').focus();
	} else {
		alert('Es wurde keine Auswahl getroffen!');
	}
}
function onSeleobjSelbtn (athis) {	/* Auswahl setzen (ForeignKey in Select) */
	var aseltar = $(athis).parents('.form-control-static');
	aseltar.find('.viewobj, .openobj').removeClass('hidden');
	var aselpk = $(athis).val();
	var aselpki = aselpk;
	if (aselpk === '' || aselpk === 'None') { aselpk = 0; aselpki = 'None'; aseltar.find('.viewobj, .openobj').addClass('hidden'); }
	console.log(aselpk);
	aseltar.find('.seleobj, .seleobjosm, .viewobj, .openobj').data('obj-pk', aselpk);
	aseltar.find('input[type="hidden"]').val(aselpki);
}
function loadElement (aElement, afurl, aid, alf, extradata) {	/* Element laden */
	$(aElement).addClass('loading');
	if (!afurl) {
		afurl = viewurl + $(aElement).parents('.lmfa').data('lmfa-app') + '/' + $(aElement).parents('.lmfa').data('lmfa-tabelle');
	}
	if (!aid) {
		aid = $(aElement).data('lmfabcl-id');
	}
	$.post(afurl, $.extend({}, { csrfmiddlewaretoken: csrf, gettableview: aid }, extradata), function (d, e, f, g = aElement, h = alf) {
		$(g).parents('.lmfa').find('li>.lmfabcl.open').removeClass('open');
		$(g).removeClass('loading').addClass('open');
		if ($(g).length > 0) {
			$($(g).parents('.lmfa').data('lmfa-target')).html(d);
		} else {
			$($('.lmfa').data('lmfa-target')).html(d);
		}
		console.log('lmfabcl - ' + $(g).data('lmfabcl-id') + ' - Geladen');
		if (h) {
			if (aid > 0) {
				h(aid);
			} else {
				h();
			}
		}
		$('.text-ellipsis').each(function () {
			$(this).prop('title', $(this).text());
		});
		setMaps();
	}).fail(function (d, e, f, g = aElement) {
		var aError = d['responseText'].split('\n', 10);
		alert('Es ist ein Fehler aufgetreten:\n\n' + aError[0] + '\n' + aError[1] + '\n' + aError[2]);
		$(g).removeClass('loading');
		console.log(d);
	});
}
function getLmfadl (aElement, apk = 0) {	/* Liste der Elemente laden */
	if ($(aElement).siblings('.lmfa-dl').length < 1) {
		$(aElement).addClass('loading');
		$.post(viewurl + $(aElement).parents('.lmfa').data('lmfa-app') + '/' + $(aElement).parents('.lmfa').data('lmfa-tabelle'), { csrfmiddlewaretoken: csrf, getlmfadl: $(aElement).data('lmfabc') }, function (d, e, f, g = aElement, h = apk) {
			$(g).removeClass('loading');
			$(g).parent().append(d);
			console.log('lmfal - ' + $(g).data('lmfabc') + ' - Geladen');
			if (h > 0) {
				console.log(h);
				$('.lmfabcl[data-lmfabcl-id="' + h + '"]').addClass('open').parent().parent().parent().addClass('open');
			}
			makeSearch($(aElement).parents('.lmfa'), redo = 1);
		}).fail(function (d, e, f, g = aElement) {
			var aError = d['responseText'].split('\n', 10);
			alert('Es ist ein Fehler aufgetreten:\n\n' + aError[0] + '\n' + aError[1] + '\n' + aError[2]);
			$(g).removeClass('loading');
			console.log(d);
		});
	}
}
function reloadMenu (aid) {
	$.post(viewurl + $('.lmfa').data('lmfa-app') + '/' + $('.lmfa').data('lmfa-tabelle'), { csrfmiddlewaretoken: csrf, getlmfal: true }, function (d, e, f, g = aid) {
		var loomp = [];
		$('.lmfa-l>.open>.lmfabc').each(function () {
			loomp.push($(this).data('lmfabc'));
		});
		$('.lmfa-l').replaceWith(d);
		$.each(loomp, function () {
			getLmfadl($('.lmfa-l>li>.lmfabc[data-lmfabc="' + this + '"]'), g);
			$('.lmfa-l>li>.lmfabc[data-lmfabc="' + this + '"]').parent().addClass('open');
		});
	}).fail(function (d, e, f) {
		var aError = d['responseText'].split('\n', 10);
		alert('Es ist ein Fehler aufgetreten:\n\n' + aError[0] + '\n' + aError[1] + '\n' + aError[2]);
		console.log(d);
	});
}
		/* Formular */
function resetEinblendbareFelder () {
	if ($('.feld-blenden .glyphicon').hasClass('glyphicon-eye-open')) {
		$('.feld-einblendbar').removeClass('hidden');
	} else {
		$('.feld-einblendbar').addClass('hidden');
	}
}
