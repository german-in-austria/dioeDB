function refreshTree() {
	aseltreeobj = $('.filetree ul li>a.selected').data('rename')
	if(!aseltreeobj) {
		aseltreeobj = $('.filetree ul li>a.selected').data('fullpath')
	}
	$.post('/db/dateien/',{ csrfmiddlewaretoken: csrf , getTree: 1 }, function(d,e,f,g=aseltreeobj) {
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

function loadDir(athis) {
	aelement = athis
	$(aelement).addClass('loading')
	$.post('/db/dateien/',{ csrfmiddlewaretoken: csrf , getDirContent: $(athis).data('fullpath') }, function(d,e,f,g=aelement) {
		$('.mcon').html(d)
		$('.filetree a.selected').removeClass('selected')
		$(g).removeClass('loading').addClass('selected')
	}).fail(function(d,e,f,g=aelement) {
		alert( "error: " + d )
		$(g).removeClass('loading')
		console.log(d)
	})
}

function mkDir(athis){
	aelement = athis
	$(aelement).addClass('loading')
	newDir = window.prompt("Name des Verzeichnisses:","");
	if(newDir) {
		$.post('/db/dateien/',{ csrfmiddlewaretoken: csrf , makeDir:newDir, baseDir:$(athis).parents('.dateien').data('verzeichniss')}, function(d,e,f,g=aelement) {
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
}

function editDir(athis){
	aelement = athis
	$(aelement).addClass('loading')
	fullpath = $(athis).siblings('a').data('fullpath')
	subname = $(athis).siblings('a').data('subname')
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
				$.post('/db/dateien/',{ csrfmiddlewaretoken: csrf , renameDir:newDir, subname:subname, fullpath:fullpath}, function(d,e,f,g=aelement,h=newFullPath) {
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
}
function uploadFile(dfunc = function(){},efunc = function(){}){
	if(!window.File || !window.FileReader || !window.FileList || !window.Blob) {
		alert('Die Datei APIs werden von Ihrem Browser nicht vollständig unterstützt!')
		return
	}
	input = document.getElementById('dateienupload')
	if(!input) {
		alert("Fehler ... Dateienfeld konnte nicht gefunden werden!")
	}
	else if(!input.files) {
		alert("Ihr Browser ist nicht kompatibel!")
	}
	else if(!input.files[0]) {
		return
	}
	else {
		var atext = '', adg = 0, asize = 0
		$.each( input.files, function( key, value ) {
			atext+= value["name"]+"-"+formatBytes(value["size"])+"\n"
			asize+= value["size"]
			adg+=1
		});
		if(adg!=1) {
			atext+= "\nSollen diese Dateien("+formatBytes(asize)+") hochgeladen werden?"
		} else {
			atext+= "\nSoll diese Datei("+formatBytes(asize)+") hochgeladen werden?"
		}
		if (confirm(atext) == true) {
			var formdata = new FormData($('#dateienuploadform')[0]);
			$('#dateiuploadfortschritt').show()
			$.ajax({
				type: "POST",
				url: $('#dateienuploadform').attr('action'),
				data: formdata,
				processData: false,
				contentType: false,
				success: function(d, textStatus, jqXHR) {
					if(d!='OK') {
						alert(d)
						console.log(d)
						efunc()
					} else {
						dfunc()
						alert( "Dateien erfolgreich hochgeladen!" )
					}
					$('#dateiuploadfortschritt').hide()
				},
				error: function(d, textStatus, jqXHR) {
					alert( "Fehler: " + textStatus )
					console.log('Upload Fehler!')
					console.log(d)
					console.log(textStatus)
					efunc()
					$('#dateiuploadfortschritt').hide()
				},
				xhr: function() {
					var xhr = new window.XMLHttpRequest();
					xhr.upload.addEventListener("progress", function(evt) {
						if (evt.lengthComputable) {
							var percentComplete = evt.loaded / evt.total;
							percentComplete = parseInt(percentComplete * 100);
							$('#dateiuploadfortschritt .progress-bar').css("width",percentComplete+"%").html(percentComplete+" %")
						}
					}, false);
					return xhr;
				},
			});
		}
	}
}
function deleteFile(athis){
	aelement = athis
	$(aelement).addClass('loading')
	if (confirm('Soll die Datei "'+$(athis).siblings('a.filelink').data('file-name')+'" unwiederruflich gelöscht werden?') == true) {
		$.post('/db/dateien/',{ csrfmiddlewaretoken: csrf , delFile:$(athis).siblings('a.filelink').data('file-fullpath')}, function(d,e,f,g=aelement) {
			$(g).removeClass('loading')
			if(d!='OK') {
				alert(d)
			}
			$('.filetree ul li>a.selected').click()
		}).fail(function(d,e,f,g=aelement) {
			alert( "error: " + d )
			$(g).removeClass('loading')
			console.log(d)
			$('.filetree ul li>a.selected').click()
		})
	}
}

function renameFile(athis){
	aelement = athis
	$(aelement).addClass('loading')
	fullpath = $(athis).siblings('a').data('file-fullpath')
	filename = $(athis).siblings('a').data('file-name')
	newFilename = window.prompt("Datei umbennenen:",filename);
	if(newFilename && newFilename != filename && newFilename.length > 3) {
		newFullPath = fullpath.substr(0, fullpath.length - filename.length)+newFilename
		cText = 'Soll die Datei "'+fullpath+'" wirklich in "'+newFullPath+'" umbenannt werden?'
		if (confirm(cText) == true) {
			if(newFilename) {
				$.post('/db/dateien/',{ csrfmiddlewaretoken: csrf , renameFile:newFilename, filename:filename, fullpath:fullpath}, function(d,e,f,g=aelement,h=newFullPath) {
					$(g).removeClass('loading')
					if(d!='OK') {
						alert(d)
					}
					$('.filetree ul li>a.selected').click()
				}).fail(function(d,e,f,g=aelement) {
					alert( "error: " + d )
					$(g).removeClass('loading')
					console.log(d)
					$('.filetree ul li>a.selected').click()
				})
			}
		}
	}
}
