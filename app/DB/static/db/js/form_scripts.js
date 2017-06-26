(function($){jQuery(document).ready(function($){
	/* Initialisieren */
	var necount = 0 /* Neue Elemente Counter */
	setSearchfields()
	makeScrollTo()

	/* "on" Sachen */
		/* Reihung */
	$(document).on('click','.element-reihung-hoch , .element-reihung-runter',function(e){	/* Reihung rauf/runter */
		aformdata = $(this).closest('.formdata')
		if($(this).hasClass('element-reihung-hoch')) {
			aformdata.insertBefore(aformdata.prev('.formdata:not(.hidden)'))
		} else {
			aformdata.insertAfter(aformdata.next('.formdata:not(.hidden)'))
		}
		resetReihung(aformdata.parent().children('.formdata:not(.hidden)'))
	})

		/* Kategorien */
	$(document).on('click','.lmfa li:not(.open)>.lmfabc',function(e){	/* Kategorie öffnen und ggf. Laden */
		e.preventDefault()
		$(this).parent().addClass('open')
		if(!$(this).hasClass('loading')) { getLmfadl(this); }
	})
	$(document).on('click','.lmfa li.open>.lmfabc',function(e){				/* Kategorie schließen */
		e.preventDefault()
		$(this).parent().removeClass('open')
	})
		/* Elemente */
	$(document).on('click','.lmfa li>.lmfabcl',function(e){						/* Element laden */
		e.preventDefault()
		if($(this).parents('.modal').length>0) {
			loadElement(this)
		} else {
			loadElement(this,asurl)
		}
	})
	$(document).on('click','.viewobj:not(.loading)',function(e){		/* Modal mit Element laden */
		makeModal('Lade ...','Datensatz wird geladen ...','viewobjmodal')
		aelement = this
		$(aelement).addClass('loading')
		$.post(viewurl+$(aelement).data('appname')+"/"+$(aelement).data('tabname'), { csrfmiddlewaretoken: csrf, gettableview: $(aelement).data('obj-pk') } , function(d,e,f,g=aelement) {
			if($('#js-modal.viewobjmodal').length>0) {
				$('#js-modal.viewobjmodal .modal-title').html($('<div>'+d+'</div>').find('.titel').html())
				$('#js-modal.viewobjmodal .modal-body').html($('<div>'+d+'</div>').find('.content').html())
			}
			$(g).removeClass('loading')
			$('#js-modal.viewobjmodal').on('shown.bs.modal',function(){ setMaps() })
			console.log('viewobj - '+$(g).data('appname')+"/"+$(g).data('tabname')+', '+$(g).data('obj-pk')+' - Geladen')
		}).fail(function(d,e,f,g=aelement) {
			alert( "error" )
			$(g).removeClass('loading')
			console.log(d)
		})
	})
	$(document).on('click','.viewverweise:not(.loading)',function(e){		/* Modal mit Liste von Verweisen laden */
		e.preventDefault()
		makeModal('Lade ...','Datensatz wird geladen ...','viewvlistmodal')
		aelement = this
		$(aelement).addClass('loading')
		$.post(viewurl+$(aelement).data('appname')+"/"+$(aelement).data('tabname'), { csrfmiddlewaretoken: csrf, getverweisliste: $(aelement).data('obj-pk'), fieldname: $(aelement).data('fieldname') } , function(d,e,f,g=aelement) {
			if($('#js-modal.viewvlistmodal').length>0) {
				$('#js-modal.viewvlistmodal .modal-title').html($('<div>'+d+'</div>').find('.titel').html())
				$('#js-modal.viewvlistmodal .modal-body').html($('<div>'+d+'</div>').find('.content').html())
			}
			$(g).removeClass('loading')
			console.log('viewobj - '+$(g).data('appname')+"/"+$(g).data('tabname')+', '+$(g).data('obj-pk')+' - Geladen')
		}).fail(function(d,e,f,g=aelement) {
			alert( "error" )
			$(g).removeClass('loading')
			console.log(d)
		})
	})
	$(document).on('click','.openobj',function(e){										/* Element in neuem Fenster laden */
		if($(this).data('foreignkeytarget')) {
			oourl = $(this).data('foreignkeytarget')
		} else {
			oourl = viewurl+$(this).data('appname')+"/"+$(this).data('tabname')
		}
		if($(this).data('obj-pk')>0) {
			pdata = { csrfmiddlewaretoken: csrf, loadpk: $(this).data('obj-pk') }
		} else {
			pdata = { csrfmiddlewaretoken: csrf }
		}
		post(oourl, pdata, '_blank')
	})
	$(document).on('click','.seleobj:not(.loading)',function(e){		/* Modal mit ForeignKey Select laden */
		onSelobjModal(this)
	})
	$(document).on('click','#seleobjbtnnone',function(e){						/* Auswahl aufheben (ForeignKey) */
		onSeleobjbtnnone(this)
	})
	$(document).on('click','#seleobjbtn',function(e){								/* Auswahl setzen (ForeignKey) */
		onSeleobjbtn(this)
	})
	$(document).on('change','select.foreignkeyselect',function(e){		/* Auswahl setzen (ForeignKey in Select) */
		onSeleobjSelbtn(this)
	})
	$(document).on('click','.seleobjosm:not(.loading)',function(e){		/* Modal mit OpenStreetMap Select laden */
		onSelobjOsmModal(this)
	})
	$(document).on('click','#seleosmbtnnone',function(e){						/* Auswahl aufheben (osm ForeignKey) */
		onSeleosmbtnnone(this)
	})
	$(document).on('click','#seleosmbtn',function(e){								/* Auswahl setzen (osm ForeignKey) */
		onSeleosmbtn(this)
	})
	$(document).on('change','input.durationinput',function(e){			/* durationinput Update */
		if($(this).val()) { $(this).val(secondsToDuration(durationToSeconds($(this).val()))) }
	})

		/* Formular */
	$(document).on('click','.newobj:not(.loading)',function(e){				/* Leeres Formular laden */
		formularNeu(this)
	})

	$(document).on('click','.editobj:not(.loading)',function(e){			/* Formulareintrag laden */
		necount = 0
		aelement = this
		$(aelement).addClass('loading')
		$('.newobj').remove()
		$.post(asurl, { csrfmiddlewaretoken: csrf, gettableeditform: $(aelement).data('obj-pk') } , function(d,e,f,g=aelement) {
			$(g).parents('.form-view').html(d)
			$(g).removeClass('loading')
			fxinputs()
			$('.form-save').removeClass('hidden')
			setReihung()
			resetEinblendbareFelder()
			console.log('editobj - '+$(g).data('obj-pk')+' - Geladen')
		}).fail(function(d,e,f,g=aelement) {
			alert( "error" )
			$(g).removeClass('loading')
			console.log(d)
		})
	})
	$(document).on('click','.element-hinzufuegen',function(e){				/* Element hinzufügen */
		necount = necount + 1
		newbase = $(this).siblings('.newbase')
		newclone = newbase.clone().removeClass('hidden newbase')
		newclone.find('[id^="fid_"],[id^="collapse"]').each(function() {
			$(this).prop('id',$(this).prop('id')+'_n'+necount)
		})
		newclone.find('[for^="fid_"]').each(function() {
			$(this).prop('for',$(this).prop('for')+'_n'+necount)
		})
		newclone.find('[href^="#collapse"]').each(function() {
			$(this).prop('href',$(this).prop('href')+'_n'+necount)
		})
		newbase.before(newclone)
		setReihung()
		resetReihung($(this).siblings('.formdata:not(.hidden)'))
		fxinputs()
	})
	$(document).on('click','.element-delete',function(e){							/* Element löschen */
		if( confirm('Soll der Eintrag wirklich gelöscht werden?')) {
			aformdata = $(this).closest('.formdata')
			aformdata.addClass('hidden delit')
			resetReihung(aformdata.siblings('.formdata:not(.hidden)'))
		}
	})
	$(document).on('click','.feld-blenden',function(e){								/* Einblendbare Felder umschalten */
		$(this).children('.glyphicon').toggleClass('glyphicon-eye-close glyphicon-eye-open')
		resetEinblendbareFelder()
	})

	function formSaveData(athis) {																		/* Formular Daten, zum speichern, auswerten */
		var adataarray = new Array
		$(athis).progenyWithoutAncestors('.form-fields','.form-list').children('.formdata:not(.newbase)').each(function(){
			acontb = $(this).children().progenyWithoutAncestors('.formdata','.form-fields')
			var adataobj = {'id':$(this).data('id')}
			if($(this).hasClass('delit')) {
				adataobj['delit'] = true
			}
			var afelderarray = {}
		 	acontb.children().progenyWithoutAncestors('.form-fields','.form-savedata').each(function(){
				if($(this).hasClass('dateinput')) {
					aval = $(this).val()
					oval = ''
					if(aval.length > 3) {
						aval = aval.split('.')
						oval = aval[2]+'-'+aval[1]+'-'+aval[0]
					}
					afelderarray[$(this).prop('name')] = {'val':oval,'id':$(this).attr('id')}
				} else if($(this).hasClass('datetimeinput')) {
					aval = $(this).val()
					oval = ''
					if(aval.length > 3) {
						tval = aval.split(' ')
						aval = tval[0].split('.')
						oval = aval[2]+'-'+aval[1]+'-'+aval[0]+' '+tval[1]
					}
					afelderarray[$(this).prop('name')] = {'val':oval,'id':$(this).attr('id')}
				} else if($(this).hasClass('durationinput')) {
					afelderarray[$(this).prop('name')] = {'val':durationToSeconds($(this).val()),'id':$(this).attr('id')}
				} else if($(this).prop('type')=='checkbox') {
					afelderarray[$(this).prop('name')] = {'val':$(this).is(':checked'),'id':$(this).attr('id')}
				} else {
					afelderarray[$(this).prop('name')] = {'val':$(this).val(),'id':$(this).attr('id')}
				}
			})
			adataobj['input'] = afelderarray
			var asubs = acontb.children().progenyWithoutAncestors('.formdata','.form-list')
			if(asubs.length>0) {
				var asubdatas = new Array
				asubs.each(function(){
					var asubdata = formSaveData(this)
					if(asubdata.length>0) {
						asubdatas.push(asubdata)
					}
				})
				if(asubdatas.length>0) {
					adataobj['subs'] = asubdatas
				}
			}
			adataarray.push(adataobj)
		})
		return adataarray
	}
	$(document).on('click','.form-save',function(e){								/* Formular speichern */
		var aformsenddata = [formSaveData($('.form-view'))]
		console.log(aformsenddata)
		aelement = this
		$(aelement).addClass('loading')
		$(this).find(':input').each(function() {
			if($(this).val()=='None') { $(this).val(''); }
		})
		$('.help-block.errtxt').remove()
		$('.form-group.has-error').removeClass('has-error')
		$('.this-wrong').removeClass('this-wrong')
		$('.tab-wrong').removeClass('tab-wrong')
		$.post(asurl, { csrfmiddlewaretoken: csrf, saveform: JSON.stringify(aformsenddata) }, function(d,e,f,g=aelement) {
			if(d.substring(0, 2)=='OK') {
				if(d.substring(2)>0) {
					loadElement($('.lmfa .lmfabcl.open'),asurl,d.substring(2),reloadMenu)
				} else {
					$($('.lmfa').data('lmfa-target')).html('<div id="lmfa-mtarget"><h2 class="titel">'+aktueb+':</h2><br><button class="feld-blenden" title="Ausgeblendete Felder ein-/ausblenden"><span class="glyphicon glyphicon-eye-close" aria-hidden="true"></span></button><button class="newobj" data-appname="'+aappname+'" data-tabname="'+atabname+'" data-obj-pk="0" title="Neues Element erstellen"><span class="glyphicon glyphicon-file" aria-hidden="true"></span></button><button class="form-save hidden" title="Aktuelles Formular speichern"><span class="glyphicon glyphicon-save" aria-hidden="true"></span></button><br><div class="content"><div class="form-horizontal form-view"></div></div></div></div>')
					formularNeu($($('.lmfa').data('lmfa-target')).find('.newobj'))
					reloadMenu()
				}
			} else if (d.substring(0, 6)=='Error:') {
				$.each(jQuery.parseJSON(d.substring(6)), function() {
					if(this[0]=='sys') {
						alert( this[1] )
					} else {
						$(this[0]).closest('.form-group').addClass('has-error')
						if($(this[0]).closest('.tab-pane').length>0) {
							$('#sel'+$(this[0]).closest('.tab-pane').attr('id')).addClass('tab-wrong')
						}
						$(this[0]).addClass('this-wrong').after('<span class="help-block errtxt"><strong>Dieses Feld ist zwingend erforderlich.</strong></span>')
					}
				})
				$('.mcon').scrollTop($('.form-group.has-error').offset().top-150)
			} else {
				console.log(d)
			}
			$(g).removeClass('loading')
		}).fail(function(d,e,f,g=aelement) {
			alert( "error" )
			$(g).removeClass('loading')
			console.log(d)
		})
	})

});})(jQuery);

/* Funktionen */
	/* Reihung */
function setReihung() {														/* Knöpfe für Reihungen hinzufügen */
	$("input[data-process]").each(function(){
		if($(this).data('process') == 'auto:reihung') {
			aformdata = $(this).closest('.formdata')
			if(!(aformdata.hasClass('hidden') || aformdata.hasClass('hatreihung'))) {
				aformdata.addClass('hatreihung')
				aformdata.find('.element-delete').after('<button class="element-btn element-reihung-hoch"><span class="glyphicon glyphicon-chevron-up" aria-hidden="true"></span></button><button class="element-btn element-reihung-runter"><span class="glyphicon glyphicon-chevron-down" aria-hidden="true"></span></button>')
			}
		}
	})
}
function resetReihung(aelemente) {								/* Reihungen aktuallisieren */
	var dg = 0
	aelemente.each(function() {
		dg++
		$(this).find('.aktuelle-reihung').first().html(dg)
		$(this).children('.panel-collapse').children('.panel-body').children('.form-group').find('input[data-process]').add($(this).children('.panel-collapse').children('.panel-body').children('input[data-process]')).each(function(){
			if($(this).data('process') == 'auto:reihung') {
				$(this).val(dg)
			}
		})
	})
}
function formularNeu(aelement) {								/* Leeres Formular laden */
	$(aelement).addClass('loading')
	$.post(asurl, { csrfmiddlewaretoken: csrf, gettableeditform: 0 } , function(d,e,f,g=aelement) {
		$(g).siblings().find('.usedby').html('')
		$(g).siblings().find('.form-view').html(d)
		$(g).siblings('h2').html($('<div>'+d+'</div>').find('#newformtitel').html())
		$(g).remove()
		fxinputs()
		$('.form-save').removeClass('hidden')
		setReihung()
		resetEinblendbareFelder()
		console.log('newobj - '+$(g).data('appname')+"/"+$(g).data('tabname')+', Geladen')
	}).fail(function(d,e,f,g=aelement) {
		alert( "error" )
		$(g).removeClass('loading')
		console.log(d)
	})
}
