(function($){jQuery(document).ready(function($){

	$(document).on('click','.filetree a',function(e){
    e.preventDefault()
		aelement = this
		$(aelement).addClass('loading')
    $.post('/korpusdb/dateien/',{ csrfmiddlewaretoken: csrf , getDirContent: $(this).data('fullpath') }, function(d,e,f,g=aelement) {
      $('.mcon').html(d)
			$('.filetree a.selected').removeClass('selected')
			$(g).removeClass('loading').addClass('selected')
    }).fail(function(d,e,f,g=aelement) {
      alert( "error" + d )
			$(g).removeClass('loading')
      console.log(d)
    })
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
		
		console.log('neuesverzeichniss - '+$(this).parents('.dateien').data('verzeichniss'))
	});
	$(document).on('click','button.dateien-hochladen',function(e){
		console.log('hochladen - '+$(this).parents('.dateien').data('verzeichniss'))
	});
});})(jQuery);
