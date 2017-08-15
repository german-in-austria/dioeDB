(function($){jQuery(document).ready(function($){
	$(document).on('change','#dateienupload',function(e){
		uploadFile(function(){$('a.lmfabcl.open').click();})
	});
	$(document).on('click','a.csvdateiselect',function(e){
		e.preventDefault()
		
	});
});})(jQuery);
