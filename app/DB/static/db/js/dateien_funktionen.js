/* global $  csrf alert confirm formatBytes FormData localStorage */
function refreshTree () {
	var aseltreeobj = $('.filetree ul li>a.selected').data('rename');
	if (!aseltreeobj) {
		aseltreeobj = $('.filetree ul li>a.selected').data('fullpath');
	}
	$.post('/db/dateien/', { csrfmiddlewaretoken: csrf, getTree: 1 }, function (d, e, f, g = aseltreeobj) {
		$('.filetree').html(d);
		$('.filetree ul li>a').each(function () {
			if ($(this).data('fullpath') === g) {
				$(this).addClass('selected').click();
			}
		});
		if ($('.filetree ul li>a.selected').length < 1) {
			$('.mcon').html('');
		}
	}).fail(function (d) {
		alert('Es ist ein Fehler aufgetreten: ' + d);
		console.log(d);
	});
}

function loadDir (athis) {
	var aelement = athis;
	$(aelement).addClass('loading');
	$.post('/db/dateien/', { csrfmiddlewaretoken: csrf, getDirContent: $(athis).data('fullpath') }, function (d, e, f, g = aelement) {
		$('.mcon').html(d);
		$('.filetree a.selected').removeClass('selected');
		$(g).removeClass('loading').addClass('selected');
		updateFileView();
	}).fail(function (d, e, f, g = aelement) {
		alert('Es ist ein Fehler aufgetreten: ' + d);
		$(g).removeClass('loading');
		console.log(d);
	});
}

function mkDir (athis) {
	var aelement = athis;
	$(aelement).addClass('loading');
	var newDir = window.prompt('Name des Verzeichnisses:', '');
	if (newDir) {
		$.post('/db/dateien/', { csrfmiddlewaretoken: csrf, makeDir: newDir, baseDir: $(athis).parents('.dateien').data('verzeichnis') }, function (d, e, f, g = aelement) {
			$(g).removeClass('loading');
			if (d !== 'OK') {
				alert(d);
			}
			refreshTree();
		}).fail(function (d, e, f, g = aelement) {
			alert('Es ist ein Fehler aufgetreten: ' + d);
			$(g).removeClass('loading');
			console.log(d);
			refreshTree();
		});
	}
}

function editDir (athis) {
	var aelement = athis;
	$(aelement).addClass('loading');
	var fullpath = $(athis).siblings('a').data('fullpath');
	var subname = $(athis).siblings('a').data('subname');
	var newDir = window.prompt('Verzeichnis umbennenen:\nUm das Verzeichnis zu löschen "löschen" schreiben.\nDas löschen ist endgültig und unwiederruflich!', subname);
	if (newDir && newDir !== subname && newDir.length > 0) {
		if (newDir === 'löschen') {
			var newFullPath = 'löschen';
			var cText = 'Soll das Verzeichnis "' + fullpath + '" wirklich gelöscht werden?';
		} else {
			newFullPath = fullpath.substr(0, fullpath.length - subname.length) + newDir;
			cText = 'Soll das Verzeichnis "' + fullpath + '" wirklich in "' + newFullPath + '" umbenannt werden?';
		}
		if (confirm(cText) === true) {
			if (newDir) {
				$.post('/db/dateien/', {csrfmiddlewaretoken: csrf, renameDir: newDir, subname: subname, fullpath: fullpath}, function (d, e, f, g = aelement, h = newFullPath) {
					$(g).removeClass('loading');
					if (d !== 'OK') {
						alert(d);
					}
					if (h !== 'löschen') {
						$(g).siblings('a').data('rename', h);
					}
					refreshTree();
				}).fail(function (d, e, f, g = aelement) {
					alert('Es ist ein Fehler aufgetreten: ' + d);
					$(g).removeClass('loading');
					console.log(d);
					refreshTree();
				});
			}
		}
	}
}
function uploadFile (dfunc = function () {}, efunc = function () {}) {
	if (!window.File || !window.FileReader || !window.FileList || !window.Blob) {
		alert('Die Datei APIs werden von Ihrem Browser nicht vollständig unterstützt!');
		return;
	}
	var input = document.getElementById('dateienupload');
	if (!input) {
		alert('Fehler ... Dateienfeld konnte nicht gefunden werden!');
	}	else if (!input.files) {
		alert('Ihr Browser ist nicht kompatibel!');
	}	else if (!input.files[0]) {
		return;
	}
	else {
		var atext = '';
		var adg = 0;
		var asize = 0;
		$.each(input.files, function (key, value) {
			atext += value['name'] + '-' + formatBytes(value['size']) + '\n';
			asize += value['size'];
			adg += 1;
		});
		if (adg !== 1) {
			atext += '\nSollen diese Dateien(' + formatBytes(asize) + ') hochgeladen werden?';
		} else {
			atext += '\nSoll diese Datei(' + formatBytes(asize) + ') hochgeladen werden?';
		}
		if (confirm(atext) === true) {
			var formdata = new FormData($('#dateienuploadform')[0]);
			$('#dateiuploadfortschritt').show();
			$.ajax({
				type: 'POST',
				url: $('#dateienuploadform').attr('action'),
				data: formdata,
				processData: false,
				contentType: false,
				success: function (d, textStatus, jqXHR) {
					if (d !== 'OK') {
						alert(d);
						console.log(d);
						efunc();
					} else {
						dfunc();
						alert('Dateien erfolgreich hochgeladen!');
					}
					$('#dateiuploadfortschritt').hide();
				},
				error: function (d, textStatus, jqXHR) {
					alert('Fehler: ' + textStatus);
					console.log('Upload Fehler!');
					console.log(d);
					console.log(textStatus);
					efunc();
					$('#dateiuploadfortschritt').hide();
				},
				xhr: function () {
					var xhr = new window.XMLHttpRequest();
					xhr.upload.addEventListener('progress', function (evt) {
						if (evt.lengthComputable) {
							var percentComplete = evt.loaded / evt.total;
							percentComplete = parseInt(percentComplete * 100);
							$('#dateiuploadfortschritt .progress-bar').css('width', percentComplete + '%').html(percentComplete + ' %');
						}
					}, false);
					return xhr;
				}
			});
		}
	}
}
function deleteFile (athis) {
	var aelement = athis;
	$(aelement).addClass('loading');
	if (confirm('Soll die Datei "' + $(athis).parents('.fileobject').data('file-name') + '" unwiederruflich gelöscht werden?') === true) {
		$.post('/db/dateien/', { csrfmiddlewaretoken: csrf, delFile: $(athis).parents('.fileobject').data('file-fullpath') }, function (d, e, f, g = aelement) {
			$(g).removeClass('loading');
			if (d !== 'OK') {
				alert(d);
			}
			$('.filetree ul li>a.selected').click();
		}).fail(function (d, e, f, g = aelement) {
			alert('Es ist ein Fehler aufgetreten: ' + d);
			$(g).removeClass('loading');
			console.log(d);
			$('.filetree ul li>a.selected').click();
		});
	}
}

function renameFile (athis) {
	var aelement = athis;
	$(aelement).addClass('loading');
	var fullpath = $(athis).parents('.fileobject').data('file-fullpath');
	var filename = $(athis).parents('.fileobject').data('file-name');
	var newFilename = window.prompt('Datei umbennenen:', filename);
	if (newFilename && newFilename !== filename && newFilename.length > 3) {
		var newFullPath = fullpath.substr(0, fullpath.length - filename.length) + newFilename;
		var cText = 'Soll die Datei "' + fullpath + '" wirklich in "' + newFullPath + '" umbenannt werden?';
		if (confirm(cText) === true) {
			if (newFilename) {
				$.post('/db/dateien/', { csrfmiddlewaretoken: csrf, renameFile: newFilename, filename: filename, fullpath: fullpath }, function (d, e, f, g = aelement, h = newFullPath) {
					$(g).removeClass('loading');
					if (d !== 'OK') {
						alert(d);
					}
					$('.filetree ul li>a.selected').click();
				}).fail(function (d, e, f, g = aelement) {
					alert('Es ist ein Fehler aufgetreten: ' + d);
					$(g).removeClass('loading');
					console.log(d);
					$('.filetree ul li>a.selected').click();
				});
			}
		}
	}
}

function changeFileView (athis) {
	if (typeof(Storage) !== 'undefined') {
		if ($('button.dateien-ansicht>.glyphicon').hasClass('glyphicon-th')) {
			localStorage.setItem('fileview', 1);
		} else {
			localStorage.setItem('fileview', 0);
		}
		updateFileView();
	}
}

function updateFileView () {
	if (typeof(Storage) !== 'undefined') {
		if (localStorage.fileview && parseInt(localStorage.fileview) === 1) {
			$('button.dateien-ansicht>.glyphicon').addClass('glyphicon-th-list').removeClass('glyphicon-th');
			$('.dateienliste').addClass('listview').removeClass('iconview');
		} else {
			$('button.dateien-ansicht>.glyphicon').addClass('glyphicon-th').removeClass('glyphicon-th-list');
			$('.dateienliste').addClass('iconview').removeClass('listview');
		}
	}
}
