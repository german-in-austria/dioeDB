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
      format: 'DD.MM.YYYY'
    });
    $('.datetimeinput').datetimepicker({
      locale: 'de',
      format: 'DD.MM.YYYY HH:MM'
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
