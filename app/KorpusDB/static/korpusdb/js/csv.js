(function($){jQuery(document).ready(function($){
	$(document).on('change','#csv-select-tree',function(e){
		$('.mcon').html('Lade ...')
		$.post('/korpusdb/csv/',{ csrfmiddlewaretoken: csrf, csvSelDir:$(this).val(), csvSelDirCol:1}, function(d) {
			if(d.substring(0, 6)=='Fehler') {
				alert(d)
			} else {
				$('.csvselectcol').html(d)
			}
			$('.mcon').html('')
		}).fail(function(d) {
			alert( "error: " + d )
			console.log(d)
			$('.mcon').html('')
		})
	});
	$(document).on('change','#csv-select-file',function(e){
		$('.mcon').html('Lade ...')
		if($(this).val().length < 1) {
			$('.mcon').html('')
			$('#csv-file-info').remove()
		} else {
			$.post('/korpusdb/csv/',{ csrfmiddlewaretoken: csrf, csvSelFile:$(this).val(), csvSelDir:$('#csv-select-tree').val()}, function(d) {
				if(d.substring(0, 6)=='Fehler') {
					alert(d)
				} else {
					$('.csvselectcol').html($(d).find('.csvselectcol').html())
					$('.mcon').html($(d).find('.mcon').html())
				}
			}).fail(function(d) {
				alert( "error: " + d )
				console.log(d)
				$('.mcon').html('')
			})
		}
	});
});})(jQuery);
