(function($){jQuery(document).ready(function($){
  $(document).on('click','a.resetidseq:not(.loading)',function(e){				/* resetidseq */
		e.preventDefault()
    aelement = this
    $.post($(this).attr("href"), { csrfmiddlewaretoken: csrf } , function(d,e,f,g=aelement) {
      $(g).removeClass('loading')
      if(d['error']) {
        $(g).addClass('error')
        alert(d['error'])
      } else if(d['success']=='success') {
        $(g).addClass('success')
      } else {
        $(g).addClass('error')
        alert( "error" )
      }
      console.log(d)
    }).fail(function(d,e,f,g=aelement) {
      alert( "error" )
      $(g).removeClass('loading').addClass('error')
      console.log(d)
    })
		console.log('resetidseq')
	})
});})(jQuery);
