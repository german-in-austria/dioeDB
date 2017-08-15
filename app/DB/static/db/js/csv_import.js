(function($){jQuery(document).ready(function($){
	$(document).on('change','#dateienupload',function(e){
		uploadFile(function(){$('a.lmfabcl.open').click();})
	});
	$(document).on('click','a.csvdateiselect:not(.loading)',function(e){
		e.preventDefault()
		makeModal('Lade ...','CSV Datei wird geladen ...','csvviewmodal')
		aelement = this
		$(aelement).addClass('loading')
		$.post(asurl, { csrfmiddlewaretoken: csrf, csvviewer: $(aelement).data('pk') } , function(d,e,f,g=aelement) {
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
