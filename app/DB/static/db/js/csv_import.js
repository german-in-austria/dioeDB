(function($){jQuery(document).ready(function($){
	$(document).on('change','#dateienupload',function(e){
		uploadFile(function(){$('a.lmfabcl.open').click();})
	});
	$(document).on('click','a.csvdateiselect:not(.loading), button.csvdateiselectimport:not(.loading)',function(e){
		e.preventDefault()
		aelement = this
		if($(aelement).hasClass('csvdateiselectimport')) {
			impDat = 1
			$('#js-modal.csvviewmodal .modal-body').html('Import läuft ...')
		} else {
			impDat = 0
			makeModal('Lade ...','CSV Datei wird geladen ...','csvviewmodal')
		}
		$(aelement).addClass('loading')
		$.post(asurl, { csrfmiddlewaretoken: csrf, csvviewer: $(aelement).data('pk'), importData: impDat } , function(d,e,f,g=aelement) {
			if($('#js-modal.csvviewmodal').length>0) {
				$('#js-modal.csvviewmodal .modal-title').html($('<div>'+d+'</div>').find('.modal-title').html())
				$('#js-modal.csvviewmodal .modal-body').html($('<div>'+d+'</div>').find('.modal-body').html())
				$('#js-modal.csvviewmodal .modal-footer').html($('<div>'+d+'</div>').find('.modal-footer').html())
			}
			$(g).removeClass('loading')
			$('#js-modal.csvviewmodal').on('shown.bs.modal',function(){ setMaps() })
		}).fail(function(d,e,f,g=aelement) {
			alert( "error" )
			$(g).removeClass('loading')
			console.log(d)
		})
	});
});})(jQuery);
