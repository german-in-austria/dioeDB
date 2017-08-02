(function($){jQuery(document).ready(function($){
	$(document).on('change','#csv-select-tree',function(e){
		$.post('/korpusdb/csv/',{ csrfmiddlewaretoken: csrf , csvSelDir:$(this).val(), csvSelDirCol:1}, function(d) {
			if(d.substring(0, 6)=='Fehler') {
				alert(d)
			} else {
				$('.csvselectcol').html(d)
			}
		}).fail(function(d) {
			alert( "error: " + d )
			console.log(d)
		})
	});
});})(jQuery);
