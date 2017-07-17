(function($){jQuery(document).ready(function($){

	$(document).on('click','.filetree a',function(e){
    e.preventDefault()
    $.post('/korpusdb/dateien/',{ csrfmiddlewaretoken: csrf , getDirContent: $(this).data('fullpath') }, function(d) {
      $('.mcon').html(d)
    }).fail(function(d) {
      alert( "error" + d )
      console.log(d)
    })
  });
});})(jQuery);
