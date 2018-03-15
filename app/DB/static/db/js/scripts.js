/* global jQuery csrf alert setMaps makeModal setSearchfields makeScrollTo getLmfadl loadElement viewurl post fxinputs confirm reloadMenu onSelobjModal onSeleobjbtnnone onSeleobjbtn onSeleobjSelbtn onSelobjOsmModal onSelobjOsmModal onSeleosmbtnnone onSeleosmbtn */

(function ($) {
	jQuery(document).ready(function ($) {
		/* Initialisieren */
		setSearchfields();
		makeScrollTo();
		setMaps();

		/* "on" Sachen */
			/* Kategorien */
		$(document).on('click', '.lmfa li:not(.open)>.lmfabc', function (e) {	/* Kategorie öffnen und ggf. Laden */
			e.preventDefault();
			$(this).parent().addClass('open');
			if (!$(this).hasClass('loading')) { getLmfadl(this); }
		});
		$(document).on('click', '.lmfa li.open>.lmfabc', function (e) {	/* Kategorie schließen */
			e.preventDefault();
			$(this).parent().removeClass('open');
		});
			/* Elemente */
		$(document).on('click', '.lmfa li>.lmfabcl', function (e) {	/* Element laden */
			e.preventDefault();
			loadElement(this);
		});
		$(document).on('click', '.viewobj:not(.loading)', function (e) {	/* Modal mit Element laden */
			makeModal('Lade ...', 'Datensatz wird geladen ...', 'viewobjmodal');
			var aelement = this;
			$(aelement).addClass('loading');
			$.post(viewurl + $(aelement).data('appname') + '/' + $(aelement).data('tabname'), { csrfmiddlewaretoken: csrf, gettableview: $(aelement).data('obj-pk') }, function (d, e, f, g = aelement) {
				if ($('#js-modal.viewobjmodal').length > 0) {
					$('#js-modal.viewobjmodal .modal-title').html($('<div>' + d + '</div>').find('.titel').html());
					$('#js-modal.viewobjmodal .modal-body').html($('<div>' + d + '</div>').find('.content').html());
				}
				$(g).removeClass('loading');
				$('#js-modal.viewobjmodal').on('shown.bs.modal', function () { setMaps(); });
				console.log('viewobj - ' + $(g).data('appname') + '/' + $(g).data('tabname') + ', ' + $(g).data('obj-pk') + ' - Geladen');
			}).fail(function (d, e, f, g = aelement) {
				alert('error');
				$(g).removeClass('loading');
				console.log(d);
			});
		});
		$(document).on('click', '.viewverweise:not(.loading)', function (e) {	/* Modal mit Liste von Verweisen laden */
			e.preventDefault();
			makeModal('Lade ...', 'Datensatz wird geladen ...', 'viewvlistmodal');
			var aelement = this;
			$(aelement).addClass('loading');
			$.post(viewurl + $(aelement).data('appname') + '/' + $(aelement).data('tabname'), { csrfmiddlewaretoken: csrf, getverweisliste: $(aelement).data('obj-pk'), fieldname: $(aelement).data('fieldname') }, function (d, e, f, g = aelement) {
				if ($('#js-modal.viewvlistmodal').length > 0) {
					$('#js-modal.viewvlistmodal .modal-title').html($('<div>' + d + '</div>').find('.titel').html());
					$('#js-modal.viewvlistmodal .modal-body').html($('<div>' + d + '</div>').find('.content').html());
				}
				$(g).removeClass('loading');
				console.log('viewobj - ' + $(g).data('appname') + '/' + $(g).data('tabname') + ', ' + $(g).data('obj-pk') + ' - Geladen');
			}).fail(function (d, e, f, g = aelement) {
				alert('error');
				$(g).removeClass('loading');
				console.log(d);
			});
		});
		$(document).on('click', '.openobj', function (e) {	/* Element in neuem Fenster laden */
			post(viewurl + $(this).data('appname') + '/' + $(this).data('tabname'), { csrfmiddlewaretoken: csrf, loadpk: $(this).data('obj-pk') }, '_blank');
		});
			/* Formular */
		$(document).on('click', '.newobj:not(.loading)', function (e) {	/* Leeres Formular laden */
			var aelement = this;
			$(aelement).addClass('loading');
			$.post(viewurl + $(aelement).data('appname') + '/' + $(aelement).data('tabname'), { csrfmiddlewaretoken: csrf, gettableeditform: 0 }, function (d, e, f, g = aelement) {
				$(g).siblings().find('.usedby').html('');
				$(g).siblings().find('.form-view').html(d);
				$(g).siblings('h2').html($('<div>' + d + '</div>').find('#newformtitel').html());
				$(g).remove();
				fxinputs();
				console.log('newobj - ' + $(g).data('appname') + '/' + $(g).data('tabname') + ', Geladen');
			}).fail(function (d, e, f, g = aelement) {
				alert('error');
				$(g).removeClass('loading');
				console.log(d);
			});
		});
		$(document).on('click', '.delobj:not(.loading)', function (e) {	/* Element löschen */
			var aelement = this;
			$(aelement).addClass('loading');
			if (confirm('Soll der Eintrag wirklich gelöscht werden?')) {
				$.post(viewurl + $(aelement).data('appname') + '/' + $(aelement).data('tabname'), { csrfmiddlewaretoken: csrf, delobj: $(aelement).data('obj-pk') }, function (d, e, f, g = aelement) {
					var atarget = $(g).parents('.mcon').children('div');
					reloadMenu();
					atarget.html(d);
					console.log('delobj - ' + $(g).data('appname') + '/' + $(g).data('tabname') + ', ' + $(g).data('obj-pk') + ' - Geladen');
				}).fail(function (d, e, f, g = aelement) {
					alert('error');
					$(g).removeClass('loading');
					console.log(d);
				});
			}
		});
		$(document).on('click', '.editobj:not(.loading)', function (e) {	/* Formular für Element laden */
			var aelement = this;
			$(aelement).addClass('loading');
			$('.newobj').remove();
			$.post(viewurl + $(aelement).data('appname') + '/' + $(aelement).data('tabname'), { csrfmiddlewaretoken: csrf, gettableeditform: $(aelement).data('obj-pk') }, function (d, e, f, g = aelement) {
				$(g).parents('.form-view').html(d);
				$(g).removeClass('loading');
				fxinputs();
				console.log('editobj - ' + $(g).data('appname') + '/' + $(g).data('tabname') + ', ' + $(g).data('obj-pk') + ' - Geladen');
			}).fail(function (d, e, f, g = aelement) {
				alert('error');
				$(g).removeClass('loading');
				console.log(d);
			});
		});
		$(document).on('click', '.seleobj:not(.loading)', function (e) {		/* Modal mit ForeignKey Select laden */
			onSelobjModal(this);
		});
		$(document).on('click', '#seleobjbtnnone', function (e) {	/* Auswahl aufheben (ForeignKey) */
			onSeleobjbtnnone(this);
		});
		$(document).on('click', '#seleobjbtn', function (e) {	/* Auswahl setzen (ForeignKey) */
			onSeleobjbtn(this);
		});
		$(document).on('change', 'select.foreignkeyselect', function (e) {	/* Auswahl setzen (ForeignKey in Select) */
			onSeleobjSelbtn(this);
		});
		$(document).on('click', '.seleobjosm:not(.loading)', function (e) {	/* Modal mit OpenStreetMap Select laden */
			onSelobjOsmModal(this);
		});
		$(document).on('click', '#seleosmbtnnone', function (e) {	/* Auswahl aufheben (osm ForeignKey) */
			onSeleosmbtnnone(this);
		});
		$(document).on('click', '#seleosmbtn', function (e) {	/* Auswahl setzen (osm ForeignKey) */
			onSeleosmbtn(this);
		});
		$(document).on('click', '#saveobj:not(.loading)', function (e) {	/* Formular speichern */
			var aelement = this;
			$(aelement).addClass('loading');
			$(this).parents('.form-view').find(':input').each(function () {
				if ($(this).val() === 'None') { $(this).val(''); }
			});
			$.post(viewurl + $(aelement).data('appname') + '/' + $(aelement).data('tabname'), $(this).parents('.form-view').find(':input').serializeArray(), function (d, e, f, g = aelement) {
				if ($('<div>' + d + '</div>').find('.content').length > 0) {
					atarget = $(g).parents('.mcon').children('div');
					reloadMenu($('<div>' + d + '</div>').find('.editobj').data('obj-pk'));
					$(g).parents('.content').parent().html(d);
				} else {
					$(g).parents('.form-view').html(d);
				}
				$(g).removeClass('loading');
				setMaps();
				console.log('saveobj - ' + $(g).data('appname') + '/' + $(g).data('tabname') + ', ' + $(g).data('obj-pk') + ' - Geladen');
			}).fail(function (d, e, f, g = aelement) {
				alert('error');
				$(g).removeClass('loading');
				console.log(d);
			});
		});
	});
})(jQuery);

/* Funktionen */
