(function($){jQuery(document).ready(function($){
	$(document).on('click','.filetree a',function(e){
		e.preventDefault()
		loadDir(this)
	});
	$(document).on('click','.filetree button.treebtn.opend',function(e){
		$(this).removeClass('opend').addClass('closed');
		$(this).siblings('ul').hide('fast');
	});
	$(document).on('click','.filetree button.treebtn.closed',function(e){
		$(this).removeClass('closed').addClass('opend');
		$(this).siblings('ul').show('fast');
	});
	$(document).on('click','button.dateien-neuesverzeichniss',function(e){
		mkDir(this)
	});
	$(document).on('click','.filetree button.treeeditbtn',function(e){
		editDir(this)
	});
	$(document).on('click','button.dateien-hochladen',function(e){
		$('#dateienupload').click()
	});
	$(document).on('change','#dateienupload',function(e){
		uploadFile(function(){$('.filetree ul li>a.selected').click();})
	});
	$(document).on('click','button.dateien-dateiloeschen',function(e){
		deleteFile(this)
	});
	$(document).on('click','button.dateien-dateiumbenennen',function(e){
		renameFile(this)
	});

});})(jQuery);
