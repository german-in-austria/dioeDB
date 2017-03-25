/* Funktionen */
	/* jQuery */
(function($) {
  $.fn.progenyWithoutAncestors = function(notAncestors,aFind) {	/* Finde alle "aFind" die nicht Nachkommen von "notAncestors" sind */
    var $found = $(), $currentSet = this
    while ($currentSet.length) {
    	$currentSet = $currentSet.not(notAncestors)
			$cfound = $currentSet.filter(aFind)
			if($cfound.length) {
				$curfound = $currentSet.filter(aFind)
				if($found.length) {
					$found = $found.add($curfound)
				} else {
					$found = $curfound
				}
				$currentSet = $currentSet.not($curfound).children()
			} else {
				$currentSet = $currentSet.children()
			}
    }
		return $found
  }
})(jQuery);
  /* Allgemein */
  function fxinputs() {
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
  }
	/* Elemente */
function onSelobjModal(athis) {													/* Modal mit ForeignKey Select laden */
	makeModal('Lade ...','Datensatz wird geladen ...','viewobjmodal')
	aelement = athis
	$('.seleobj').removeClass('lsel')
	$(aelement).addClass('loading lsel')
	$.post(viewurl+$(aelement).data('appname')+"/"+$(aelement).data('tabname'), { csrfmiddlewaretoken: csrf, getforeignkeysel: $(aelement).data('obj-pk') } , function(d,e,f,g=aelement) {
		if($('#js-modal.viewobjmodal').length>0) {
			$('#js-modal.viewobjmodal .modal-dialog').addClass('modal-xlg')
			$('#js-modal.viewobjmodal .modal-title').html('Datensatz auswählen:')
			$('#js-modal.viewobjmodal .modal-body').html(d)
			$('#js-modal.viewobjmodal .modal-footer').prepend('<button id="seleobjbtnnone" type="button" class="btn btn-warning">Auswahl aufheben</button><button id="seleobjbtn" type="button" class="btn btn-primary">Auswählen</button>')
			$('#js-modal.viewobjmodal .modal-body,#js-modal.viewobjmodal .modal-body>.row').css({'height': $(window).height() * 0.8,'overflow':'hidden','padding':'0px','margin':'0px'});
			setSearchfields()
			makeScrollTo()
		}
		$(g).removeClass('loading')
		console.log('seleobj - '+$(g).data('appname')+"/"+$(g).data('tabname')+', '+$(g).data('obj-pk')+' - Geladen')
	}).fail(function(d,e,f,g=aelement) {
		alert( "error" )
		$(g).removeClass('loading')
		console.log(d)
	})
}
/* OpenStreetMap */
var map
var locationStyle = {"color": "#ff7800", "weight": 5, "opacity": 0.65 }
var geojsonLayer
function getOsmDatenbankEintrag(OrtPK) {
  $('#osmDatenbank').html('Auswahl ... '+OrtPK)
  /* ToDo: Daten auswählen? */
}
function geojsonLayerSet(data,oid) {
  if(geojsonLayer) { map.removeLayer(geojsonLayer); }
  geojsonLayer = L.geoJSON(data.geojson,{style:locationStyle}).addTo(map)
  if(data.geojson.type == 'Point') {
    map.setView(new L.LatLng(data.lat,data.lon),11)
  } else {
    map.fitBounds(geojsonLayer.getBounds())
  };
  if(oid>0) { /* Datenbankeintrag vorhanden */
     getOsmDatenbankEintrag(oid)
  } else { /* Datenbankeintrag erstellen? */
    $('#osmDatenbank').html('Datensatz für <b>"'+data.display_name+'"</b> erstellen? <a href="#" id="osmDatensatzErstellen" data-osm-id="'+data.osm_id+'" data-osm-type="'+data.osm_type+'" data-ort-namelang="'+data.display_name+'" data-lat="'+data.lat+'" data-lon="'+data.lon+'">Ja</a>')
  }
}
$(document).on('click', '#osmDatensatzErstellen:not(.loading)', function(e) {
  e.preventDefault()
  aData = $('#osmDatensatzErstellen')
  $('#osmDatensatzErstellen').addClass('loading')
  $.post(viewurl+'PersonenDB/tbl_orte', { csrfmiddlewaretoken: csrf, savepk: 0, saveform: 1, osm_id: aData.data('osm-id'), osm_type: aData.data('osm-type'), ort_namelang: aData.data('ort-namelang'), lat: aData.data('lat'), lon: aData.data('lon') } , function(d) {
    var newOrtPK = $('<div>'+d+'</div>').find('.editobj').data('obj-pk')
    $('#osm'+$('#osmDatensatzErstellen').data('osm-id')+$('#osmDatensatzErstellen').data('osm-type')).data('OrtPK',newOrtPK).addClass('indatenbank')
    getOsmDatenbankEintrag(newOrtPK)
    console.log('saveobj - Ort - '+newOrtPK)
  }).fail(function(d) {
    alert( "error" )
    $('#osmDatensatzErstellen').removeClass('loading')
    console.log(d)
  })
})
function onSelobjOsmModal(athis) {											/* Modal mit OpenStreetMap Select laden */
 	makeModal('Ort auswählen ...','<div id="osmap"></div><br><div class="row"><div class="col-md-6"><div class="form-inline"><div class="form-group"><input type="text" class="form-control" id="osmOrt"></div><button id="osmSuche" type="submit" class="btn btn-default">Ort suchen</button></div></div><div class="col-md-6" id="osmDatenbank"></div></div><br><div id="osmWahl"></div>','viewosmmodal')
  $('#js-modal.viewosmmodal').on('hidden.bs.modal',function(){ map.remove(); })
  $('#js-modal.viewosmmodal').on('shown.bs.modal',function(){
    map = new L.Map('osmap');
    var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      osmAttribution = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
      osm = new L.TileLayer(osmUrl, {maxZoom: 18, attribution: osmAttribution});
    map.setView(new L.LatLng(48.2083537,16.3725042), 12).addLayer(osm);
    // ToDo: Vorhandenen Wert laden!

  })
}
function osmSuche() {                                   /* OpenStreetMap Suche ausführen */
  var osmOrt = $('#osmOrt').val();
  $('#osmSuche,#osmOrt').addClass('loading')
  if($('#osmDatensatzErstellen').length>0) { $('#osmDatenbank').html('') }
  if(geojsonLayer) { map.removeLayer(geojsonLayer); }
  $.getJSON('http://nominatim.openstreetmap.org/search?format=json&limit=10&q=' + encodeURI(osmOrt), function(data) {
    var osmOrte = ''; var osmOrteDB = [];
    $.each(data, function(key, val) {
      if(val.osm_id) {
        osmOrte+='<li><a href="#" title="'+val.type+'" class="osmAuswahl loading" id="osm'+val.osm_id+val.osm_type+'" data-orte-osm-id="'+val.osm_id+'" data-orte-osm-type="'+val.osm_type+'" data-orte-lat="'+val.lat+'" data-orte-lon="'+val.lon+'">'+((val.icon)?'<img src="'+val.icon+'">':'<span class="noosmicon">?</span>')+' '+val.display_name+'</a></li>';
        osmOrteDB.push({osm_id:val.osm_id,osm_type:val.osm_type})
      }
    })
    if(osmOrte.length > 0) {
      $('#osmWahl').html('<ul>'+osmOrte+'</ul>')
      $.post('/db/search', { csrfmiddlewaretoken: csrf, sucheorte: 1, suchorte: JSON.stringify(osmOrteDB) } , function(d) {
        $('.osmAuswahl').removeClass('loading')
        if(d.substr(0,2)=='OK') {
          var ifirst = 1
          $.each(jQuery.parseJSON(d.substr(2)), function(key, val) {
            if(val.ort_pk>0) {
              $('#osm'+val.osm_id+val.osm_type).data('OrtPK',val.ort_pk).addClass('indatenbank')
              if(ifirst == 1) {
                $('#osm'+val.osm_id+val.osm_type).click();
                ifirst = 0
              }
            }
          })
        } else {
          alert( "error" )
          console.log(d)
        }
      }).fail(function(d) {
        alert( "error" )
        $('.osmAuswahl').removeClass('loading')
        console.log(d)
      })
    } else {
      $('#osmWahl').html('<p>Kein Ort gefunden!</p>')
    }
    $('#osmSuche,#osmOrt').removeClass('loading')
  }).fail(function(data) {
		alert( "error" )
		$('#osmSuche,#osmOrt').removeClass('loading')
		console.log(data)
	})
}
$(document).on('click', '#osmSuche:not(.loading)', function() {
  osmSuche()
})
$(document).on('keypress','#osmOrt:not(.loading)',function(e){
  if(e.which === 13){
    osmSuche()
  }
})
$(document).on('click', '.osmAuswahl:not(.loading)', function(e) {    /* Auswahl anzeigen */
  e.preventDefault()
  if($(this).data('orte-data')) {
    geojsonLayerSet($(this).data('orte-data'),$(this).data('OrtPK'));
  } else {
    $(this).addClass('loading')
    map.panTo(new L.LatLng($(this).data('orte-lat'),$(this).data('orte-lon')));
    aelement = $(this);
    $.getJSON('http://nominatim.openstreetmap.org/reverse?format=json&polygon_geojson=1&osm_type='+$(this).data('orte-osm-type').charAt(0).toUpperCase()+'&osm_id=' + encodeURI($(this).data('orte-osm-id')), function(data,b,c,d=aelement) {
      d.data('orte-data',data)
      geojsonLayerSet(data,aelement.data('OrtPK'))
      d.removeClass('loading')
    }).fail(function(data,b,c,d=aelement) {
  		alert( "error" )
  		d.removeClass('loading')
  		console.log(data)
  	})
  }
})
function onSeleobjbtnnone(athis) {											/* Auswahl aufheben (ForeignKey) */
	aseltar = $('.seleobj.lsel').parents('.form-control-static')
	aseltar.children('.seleobj, .viewobj, .openobj').data('obj-pk',0)
	aseltar.children('input[type="hidden"]').val(0)
	aseltar.children('span').addClass('grey').html('Keine Eingabe vorhanden')
	aseltar.children('.viewobj, .openobj').addClass('hidden')
	$('#js-modal').modal('hide')
}
function onSeleobjbtn(athis) {													/* Auswahl setzen (ForeignKey) */
	aselobj = $(athis).parents('.modal-content')
	if(aselobj.find('.lmfabcl.open').data('lmfabcl-id')>0) {
		aseltar = $('.seleobj.lsel').parents('.form-control-static')
		aseltar.children('.seleobj, .viewobj, .openobj').data('obj-pk',aselobj.find('.lmfabcl.open').data('lmfabcl-id'))
		aseltar.children('input[type="hidden"]').val(aselobj.find('.lmfabcl.open').data('lmfabcl-id'))
		aseltar.children('span').removeClass('grey').html(aselobj.find('.lmfabcl.open').html())
		aseltar.children('.viewobj, .openobj').removeClass('hidden')
		$('#js-modal').modal('hide')
	} else {
		alert('Es wurde keine Auswahl getroffen!')
	}
}
function loadElement(aElement,afurl,aid,alf) {									/* Element laden */
	$(aElement).addClass('loading')
	if(!afurl) {
		afurl = viewurl+$(aElement).parents('.lmfa').data('lmfa-app')+'/'+$(aElement).parents('.lmfa').data('lmfa-tabelle')
	}
	if(!aid) {
		aid = $(aElement).data('lmfabcl-id')
	}
	$.post(afurl, { csrfmiddlewaretoken: csrf, gettableview: aid } , function(d,e,f,g=aElement,h=alf) {
		$(g).parents('.lmfa').find('li>.lmfabcl.open').removeClass('open')
		$(g).removeClass('loading').addClass('open')
		if($(g).length>0) {
			$($(g).parents('.lmfa').data('lmfa-target')).html(d)
		} else {
			$($('.lmfa').data('lmfa-target')).html(d)
		}
		console.log('lmfabcl - '+$(g).data('lmfabcl-id')+' - Geladen')
		if(h) {
			if(aid>0) {
				h(aid)
			} else {
				h()
			}
		}
    $('.text-ellipsis').each(function(){
      $(this).prop('title',$(this).text())
    })
	}).fail(function(d,e,f,g=aElement) {
		alert( "error" )
		$(g).removeClass('loading')
		console.log(d)
	})
}
function getLmfadl(aElement,apk=0) {								/* Liste der Elemente laden */
if ($(aElement).siblings('.lmfa-dl').length<1) {
	$(aElement).addClass('loading')
	$.post(viewurl+$(aElement).parents('.lmfa').data('lmfa-app')+'/'+$(aElement).parents('.lmfa').data('lmfa-tabelle'), { csrfmiddlewaretoken: csrf, getlmfadl: $(aElement).data('lmfabc') } , function(d,e,f,g=aElement,h=apk) {
		$(g).removeClass('loading')
		$(g).parent().append(d)
		console.log('lmfal - '+$(g).data('lmfabc')+' - Geladen')
		if(h>0) {
			console.log(h)
			$('.lmfabcl[data-lmfabcl-id="'+h+'"]').addClass('open').parent().parent().parent().addClass('open')
		}
		makeSearch($(aElement).parents('.lmfa'),redo=1)
	}).fail(function(d,e,f,g=aElement) {
		alert( "error" )
		$(g).removeClass('loading')
		console.log(d)
	})
}
}
function reloadMenu(aid) {
	$.post(viewurl+$('.lmfa').data('lmfa-app')+'/'+$('.lmfa').data('lmfa-tabelle'), { csrfmiddlewaretoken: csrf, getlmfal: true } , function(d,e,f,g=aid) {
		loomp = []
		$('.lmfa-l>.open>.lmfabc').each(function() {
			loomp.push($(this).data('lmfabc'))
		})
		$('.lmfa-l').replaceWith(d)
		$.each(loomp, function() {
			getLmfadl($('.lmfa-l>li>.lmfabc[data-lmfabc="'+this+'"]'),g)
			$('.lmfa-l>li>.lmfabc[data-lmfabc="'+this+'"]').parent().addClass('open')
		})
	}).fail(function(d,e,f) {
		alert( "error" )
		console.log(d)
	})
}
		/* Formular */
function resetEinblendbareFelder() {
	if($('.feld-blenden .glyphicon').hasClass('glyphicon-eye-open')) {
		$('.feld-einblendbar').removeClass('hidden')
	} else {
		$('.feld-einblendbar').addClass('hidden')
	}
}
