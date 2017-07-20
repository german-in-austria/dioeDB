(function($){jQuery(document).ready(function($){
	function refreshTree() {
		aseltreeobj = $('.filetree ul li>a.selected').data('rename')
		if(!aseltreeobj) {
			aseltreeobj = $('.filetree ul li>a.selected').data('fullpath')
		}
		$.post('/korpusdb/dateien/',{ csrfmiddlewaretoken: csrf , getTree: 1 }, function(d,e,f,g=aseltreeobj) {
			$('.filetree').html(d)
			$('.filetree ul li>a').each(function(){
				if($(this).data('fullpath')==g) {
					$(this).addClass('selected').click()
				}
			})
			if($('.filetree ul li>a.selected').length<1) {
				$('.mcon').html('')
			}
		}).fail(function(d) {
			alert( "error: " + d )
			console.log(d)
		})
	}
	$(document).on('click','.filetree a',function(e){
    e.preventDefault()
		aelement = this
		$(aelement).addClass('loading')
    $.post('/korpusdb/dateien/',{ csrfmiddlewaretoken: csrf , getDirContent: $(this).data('fullpath') }, function(d,e,f,g=aelement) {
      $('.mcon').html(d)
			$('.filetree a.selected').removeClass('selected')
			$(g).removeClass('loading').addClass('selected')
    }).fail(function(d,e,f,g=aelement) {
      alert( "error: " + d )
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
		aelement = this
		$(aelement).addClass('loading')
		newDir = window.prompt("Name des Verzeichnisses:","");
		if(newDir) {
	    $.post('/korpusdb/dateien/',{ csrfmiddlewaretoken: csrf , makeDir:newDir, baseDir:$(this).parents('.dateien').data('verzeichniss')}, function(d,e,f,g=aelement) {
				$(g).removeClass('loading')
				if(d!='OK') {
					alert(d)
				}
				refreshTree()
	    }).fail(function(d,e,f,g=aelement) {
	      alert( "error: " + d )
				$(g).removeClass('loading')
	      console.log(d)
				refreshTree()
	    })
		}
	});
	$(document).on('click','.filetree button.treeeditbtn',function(e){
		aelement = this
		$(aelement).addClass('loading')
		fullpath = $(this).siblings('a').data('fullpath')
		subname = $(this).siblings('a').data('subname')
		newDir = window.prompt("Verzeichniss umbennenen:\nUm das Verzeichniss zu löschen \"löschen\" schreiben.\nDas löschen ist endgültig und unwiederruflich!",subname);
		if(newDir && newDir != subname && newDir.length > 0) {
			if(newDir == "löschen") {
				newFullPath = 'löschen'
				cText = 'Soll das Verzeichniss "'+fullpath+'" wirklich gelöscht werden?'
			} else {
				newFullPath = fullpath.substr(0, fullpath.length - subname.length)+newDir
				cText = 'Soll das Verzeichniss "'+fullpath+'" wirklich in "'+newFullPath+'" umbenannt werden?'
			}
			if (confirm(cText) == true) {
				if(newDir) {
					$.post('/korpusdb/dateien/',{ csrfmiddlewaretoken: csrf , renameDir:newDir, subname:subname, fullpath:fullpath}, function(d,e,f,g=aelement,h=newFullPath) {
						$(g).removeClass('loading')
						if(d!='OK') {
							alert(d)
						}
						if(h!="löschen") {
							$(g).siblings('a').data('rename',h)
						}
						refreshTree()
					}).fail(function(d,e,f,g=aelement) {
						alert( "error: " + d )
						$(g).removeClass('loading')
						console.log(d)
						refreshTree()
					})
				}
			}
		}
	});
	$(document).on('click','button.dateien-hochladen',function(e){
		console.log('hochladen - '+$(this).parents('.dateien').data('verzeichniss'))
	});
});})(jQuery);
