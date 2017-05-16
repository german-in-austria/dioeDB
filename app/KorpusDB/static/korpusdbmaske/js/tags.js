/* On */
function closeTagSelect(e) {	/* Tag Select Fenster schließen wenn ausserhalb geklickt wird */
	var container = $(".seltags")
	if (!container.is(e.target) && container.has(e.target).length === 0) { container.remove(); }
}
function openNewTagSelectClick(e){
	var apos = $(this).position()
	$(this).after('<div class="tags seltags newtag" style="left:'+apos.left+'px;">'+$('#xtags').html()+'</div>')
	filterSeltags(this,1)
	$(this).blur()
}
function openChangeTagSelectClick(e){
	var apos = $(this).position()
	$(this).after('<div class="tags seltags edittag" style="left:'+apos.left+'px;" data-reihung="'+$(this).data('reihung')+'">'+$('#xtags').html()+'</div>')
	$('.seltags').find('.ptagsbtn[data-pk="' + $(this).data('id_tag') + '"]').addClass('active')
	filterSeltags(this,0)
	$(this).blur()
}
function moveTagLeftRightClick(e){
	var aselobj = $(this).parents('.seltags')
	var targettag
	$(this).parents('.reihung-tags').find('.ant-tag').each(function(){
		if($(this).data('reihung') == aselobj.data('reihung')) {
			targettag = $(this)
		}
	})
	$(this).parents('.seltags').remove()
	if($(this).hasClass('ptagsleft')) {
		targettag.insertBefore(targettag.prev('.ant-tag:not(.delit)'))
	} else {
		targettag.insertAfter(targettag.next('.ant-tag:not(.delit)'))
	}
	unsavedAntworten = 1
	$('#antwortensave').removeClass('disabled')
	resetReihungTags()
}
function openTagPresetSelectClick(e){
	var apos = $(this).position()
	$(this).after('<div class="tags seltags pretags" style="left:'+apos.left+'px;">'+$('#pretags').html()+'</div>')
	$(this).blur()
}
function tagAendernLoeschenClick(e){
	var aselobj = $(this).parents('.seltags')
	var othis=this
	if($(othis).data('pk')!=0 || ($(othis).data('pk')==0 && confirm('Soll dieser "AntwortenTag" tatsächlich gelöscht werden?'))) {
		$(this).parents('.reihung-tags').find('.ant-tag').each(function(){
			if($(this).data('reihung') == aselobj.data('reihung')) {
				if($(othis).data('pk')==0 || ($(this).siblings('.r-tag-familie:visible').length==0 || confirm('Sollen die "Children" tatsächlich gelöscht werden?'))) {
					//$(this).data('id_tag',$(othis).data('pk')).html($(othis).html())
					orgPk = $(this).data('pk')
					if($(othis).data('pk')==0) {
						if($(this).data('pk')==0) {
							$(this).parent().remove()
						} else {
							$(this).data('id_tag',0).parent().hide().find('.ant-tag').data('id_tag',0).addClass('delit')
						}
					} else {
						$(this).siblings('.r-tag-familie').hide().find('.ant-tag').attr('data-id_tag',0).addClass('delit')
						$(this).parent().replaceWith('<div class="'+$(othis).parent().data('classes')+'" data-generation="'+$(othis).parent().data('generation')+'" data-pk="'+$(othis).parent().data('pk')+'"><button class="ant-tag" data-id_tag="'+$(othis).data('pk')+'" data-pk="'+orgPk+'">'+$(othis).html()+'</button>'+$('<div></div>').append($(this).siblings('.r-tag-familie')).html()+'</div>')
					}
				}
			}
		})
	}
	aselobj.remove()
	resetReihungTags()
	familienHinzufuegenKnopfUpdate()
	unsavedAntworten = 1
	$('#antwortensave').removeClass('disabled')
}
function tagHinzufuegenClick(e){
	var aselobj = $(this).parents('.seltags')
	$(this).parents('.tags.seltags').siblings('.ant-ftag').before('<div class="'+$(this).parent().data('classes')+'" data-generation="'+$(this).parent().data('generation')+'" data-pk="'+$(this).parent().data('pk')+'"><button class="ant-tag" data-id_tag="'+$(this).data('pk')+'" data-pk="0">'+$(this).html()+'</button></div>')
	aselobj.remove()
	resetReihungTags()
	familienHinzufuegenKnopfUpdate()
	unsavedAntworten = 1
	$('#antwortensave').removeClass('disabled')
}
function tagPresetHinzufuegenClick(e){
	var aselobj = $(this).parents('.seltags')
	aselobj.siblings('.r-tag-familie').append(JSON.parse('"'+$(this).data('html')+'"'))
	aselobj.remove()
	resetReihungTags()
	familienHinzufuegenKnopfUpdate()
	unsavedAntworten = 1
	$('#antwortensave').removeClass('disabled')
}
function addTagLineClick(e){
	$(this).parents('.add-tag-line-line').before($(this).parents('.tag-forms').find('div.tag-vorlage').html())
}
function tagEbeneChange(e){
	tagEbeneColor(this)
	tagEbenenOptionUpdateCluster(this)
}

/* Funktionen */
function resetReihungTags() {
	$('.reihung-tags').each(function(){
		var areihung = 1
		$(this).find('.ant-tag:not(.delit)').each(function(){
			$(this).data('reihung',areihung)
			areihung+=1
		})
	})
}
function getTagsObject(athis) {
	var tags = []
	athis.find('.ant-tag').each(function() {
		tags.push({'reihung':$(this).data('reihung') , 'id_tag':$(this).data('id_tag') , 'pk':$(this).data('pk'), 'id_TagEbene':$(this).parents('.tag-line').find('select.tagebene').val() })
	})
	return tags
}
function checkEbenen(){
	var isok = true
	$('.tag-forms>.tag-line select.tagebene').each(function() {
		if($(this).val()==0) {
			if ($(this).parents('.tag-line').find('.ant-tag').length>0) {
				if(!confirm('Sollen alle Tags der Ebenen ohne Auswahl gelöscht werden?')) {
					isok = false
				}
				return false
			}
		}
	})
	return isok
}
function tagEbeneColor(athis) {
	if($(athis).val()==0) {
		$(athis).parents('.tag-line').css('background-color','#fcc')
	} else {
		$(athis).parents('.tag-line').css('background-color','transparent')
	}
}
function tagEbenenOptionUpdateAll() {
	$('.tag-forms select.tagebene').each(function(){
		tagEbenenOptionUpdate(this)
	})
}
function tagEbenenOptionUpdateCluster(athis) {
	$(athis).parents('.tag-forms').find('select.tagebene').each(function(){
		tagEbenenOptionUpdate(this)
	})
}
function tagEbenenOptionUpdate(athis) {
	var notThis = $(athis).parents('.tag-forms').find('select.tagebene').not($(athis))
	$(athis).find('option').removeAttr('disabled').each(function(){
		var asVal = $(this).val()
		if(asVal != 0) {
			if(notThis.filter(function(){return this.value==asVal}).length>0) {
				$(this).attr('disabled','disabled')
			}
		}
	})
}
function familienHinzufuegenKnopfUpdate() {
	$('button.ant-ftag').remove()
	$('.r-tag-familie-pchilds').append('<button class="ant-ftag"><span class="glyphicon glyphicon-plus" aria-hidden="true"></span></button>')
}
function filterSeltags(athis,addtag) {
	if(addtag==0) {
		athis = $(athis).parent().siblings('.ant-ftag')
	} else {
		athis = $(athis)
	}
	var avEbene = athis.parents('.tag-line').find('select.tagebene').val()
	if(athis.parent().data('generation')=="None") {
		var avGeneration = 0
	} else {
		var avGeneration = athis.parent().data('generation')+1
	}
	var avPk = athis.parent().data('pk')
	$('.tags.seltags .tag-familie').each(function(){
		if(avPk>0) {
			if($(this).parents('.tag-familie').length>0) {
				if($(this).data('pk')==avPk) {
					$(this).addClass('show-familie').parents('.tag-familie').removeClass('hidden-familie')
				} else {
					$(this).addClass('hidden-familie')
				}
			} else {
				if($(this).data('pk')==avPk) {
					$(this).addClass('show-familie')
				} else {
					$(this).addClass('hidden-familie')
				}
			}
		}
		if($(this).data('ebenen')) {
			if($(this).data('ebenen').split(",").indexOf(avEbene)<0) {
				$(this).addClass('hidden-ebene')
			}
		}
		if($(this).data('generation')!=avGeneration && $(this).data('generation')!="None") {
			if($(this).data('generation')<avGeneration) {
				$(this).addClass('hidden-parent').children('button.ptagsbtn').attr('disabled','disabled')
			} else {
				$(this).addClass('hidden-child')
			}
		}
	})
}
