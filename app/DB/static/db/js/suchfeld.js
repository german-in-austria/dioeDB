
	/* "on" Sachen */
		/* Suche */
	$(document).on('click','.lmfa .lmfasfx',function(e){				/* Options Buttons (Suche)*/
		$(this).toggleClass('active')
	})
	$(document).on('keyup','.lmfa .lmfasf',function(e){					/* Bei Eingabe in Suchfeld -> Suche Starten */
		startSearch($(this).parents('.lmfa'))
	})
	$(document).on('click','.lmfa .lmfasfx',function(e){				/* Bei Klick auf Options Buttons -> Suche aktuallisieren */
		makeSearch($(this).parents('.lmfa'),1)
	})
	$(document).on('click','.iwdbtn>.idbtn',function(e){				/* Suchfeld loeschen */
		$(this).siblings('input').val('').focus()
		makeSearch($(this).parents('.lmfa'),1)
	})
	$(document).on('change','.lmfa .fxfselect>select',function(e){			/* Bei Änderung von Speziellen Suchfeldern -> Suche aktuallisieren */
		makeSearch($(this).parents('.lmfa'),1)
	})

	/* Funktionen */
		/* Suche */
	function setSearchfields() {										/* Suchfelder hinzufuegen */
		$('.lmfa').each(function() {
			if($(this).find('.lmfasff').length<1) {
				$(this).prepend('<div class="lmfasff"><div class="iwdbtn"><input type="text" size="20" class="lmfasf" placeholder="Suchen ..."><button class="idbtn" title="Eingabe loeschen!"><span class="glyphicon glyphicon-erase" aria-hidden="true"></span></button></div>'
				+ '<button class="lmfasfx lmfasfe'+(($(this).find('.lmfabc[data-enthaelt="1"]').length>0)?' active':'')+'"'+(($(this).find('.lmfabc[data-enthaelt="1"]').length>0)?' disabled="disabled"':'')+'>Enthält</button><button class="lmfasfx lmfasfa'+(($(this).find('.lmfabc[data-suchein="1"]').length>0)?' active':'')+'"'+(($(this).find('.lmfabc[data-suchein="1"]').length>0)?' disabled="disabled"':'')+'>Alle<span class="hidden-md"> Kategorien</span></button>'
				+ '</div>')
			}
		})
	}
	function startSearch(sElement) {									/* Zeitversetztes suchen starten! */
		sFeld = sElement.find('.lmfasf')
		sFeld.addClass('waiting')
		if(sFeld.data('sTimer')) { clearTimeout(sFeld.data('sTimer')); }
		sFeld.data('sTimer',setTimeout(makeSearch.bind(null, sElement), 250))
	}
	function makeSearch(sElement,redo=0) {								/* Suche durchfuehren */
		var sFeld = sElement.find('.lmfasf')
		sFeld.removeClass('waiting')
		aVal = sFeld.val()
		if(sFeld.data('aVal')!=aVal||redo==1) {
			sFeld.data('aVal',aVal)
			if(aVal.length>0) {
				sElement.addClass('searching')
				sElement.find('.found').removeClass('found')
				sElement.find('.iwdbtn>.idbtn').addClass('active')
				if(sElement.find('.lmfasfe').hasClass('active')) { /* Suche nach Enthaelt */
					sElement.find('.lmfabc').each(function() {
						if($(this).siblings('.lmfa-dl').length>0) { /* Suche in geladener Liste! */
							var aregexp = new RegExp(aVal.replace(/[|\\{}()[\]^$+*?.]/g, '\\$&')+'.*', 'i')
							$(this).siblings('.lmfa-dl').find('.lmfabcl').each(function() {
								if($(this).text().match(aregexp)) {
									$(this).parent().addClass('found')
								} else {
									$(this).parent().removeClass('found')
								}
							})
						}
					})
				} else { /* Suche nach Anfangsbuchstaben */
					var aabc = 'Andere'
					if(/^[a-zA-Zaeoeueaeoeue]*$/.test(aVal.charAt(0))) { aabc = aVal.charAt(0); }
					var sEli = sElement.find('.lmfabc[data-lmfabc="'+aabc+'"]')
					sEli.parent().addClass('open')
					if (sEli.siblings('.lmfa-dl').length<1) {
						getLmfadl(sEli)
					} else {
						var aregexp = new RegExp('^'+aVal.replace(/[|\\{}()[\]^$+*?.]/g, '\\$&')+'.*', 'i')
						sEli.siblings('.lmfa-dl').find('.lmfabcl').each(function() {
							if($(this).text().match(aregexp)) {
								$(this).parent().addClass('found')
							} else {
								$(this).parent().removeClass('found')
							}
						})
					}
				}
			} else {	/* Suche zuruecksetzen */
				sElement.removeClass('searching')
				sElement.find('.found').removeClass('found')
				sElement.find('.iwdbtn>.idbtn').removeClass('active')
			}
			var fxSearch = false
			sElement.find('.fxfselect>select').each(function(){
				var aHideId = 'hide-'+$(this).attr('name')
				var aVal = $(this).val()
				sElement.find('.'+aHideId).removeClass('hide-fx '+aHideId)
				if(aVal!='None') {
					fxSearch = true
					sElement.find('.lmfabcl').each(function() {
						var aVals = new Array
						if(aVal.indexOf('&&') > -1) {
							aVals = aVal.split('&&')
						} else {
							aVals.push(aVal)
						}
						for(i = 0; i < aVals.length; i++) {
							if(aVals[i].indexOf('>') > -1) {
								aValSp = aVals[i].split('>')
								if(!$(this).data('fx-'+aValSp[0])>aValSp[1]) {
									$(this).parent().addClass('hide-fx '+aHideId)
								}
							} else if(aVals[i].indexOf('<') > -1) {
								aValSp = aVals[i].split('<')
								if(!$(this).data('fx-'+aValSp[0])<aValSp[1]) {
									$(this).parent().addClass('hide-fx '+aHideId)
								}
							} else if(aVals[i].indexOf('==') > -1) {
								aValSp = aVals[i].split('==')
								if($(this).data('fx-'+aValSp[0])!=aValSp[1]) {
									$(this).parent().addClass('hide-fx '+aHideId)
								}
							}
						}
					})
				}
			})
			// Refresh Counter!
			reSearch = sElement.hasClass('searching')
			sElement.find('.lmfabc').each(function() {
				if(reSearch||fxSearch==true) {
					$(this).find('span').html('?')
					if($(this).siblings('.lmfa-dl').length>0) {
						if(reSearch) {
							$(this).find('span').html($(this).siblings('.lmfa-dl').children('li.found:not(.hide-fx)').length)
						} else {
							$(this).find('span').html($(this).siblings('.lmfa-dl').children('li:not(.hide-fx)').length)
						}
					}
					if($(this).find('span').text()!='0') {
						$(this).parent().addClass('found').removeClass('hide-fx')
					} else {
						$(this).parent().removeClass('found').addClass('hide-fx')
					}
					if($(this).parents('.lmfa').find('.lmfasfa').hasClass('active')&& $(this).parents('.lmfa').find('.lmfabc.loading').length<1) {
						getLmfadl($(this))
					}
				} else {
					$(this).find('span').html($(this).data('lmfabcc').toLocaleString())
					$(this).parent().removeClass('found hide-fx')
				}
			})
		}
	}
