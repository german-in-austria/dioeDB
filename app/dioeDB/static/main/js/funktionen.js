/* Allgemein */
function post(path, params, target, method) { method = method || "post"; var form = document.createElement("form"); form.setAttribute("method", method); form.setAttribute("action", path); if(target) { form.setAttribute("target", target); }; for(var key in params) { if(params.hasOwnProperty(key)) { var hiddenField = document.createElement("input"); hiddenField.setAttribute("type", "hidden"); hiddenField.setAttribute("name", key); hiddenField.setAttribute("value", params[key]); form.appendChild(hiddenField); };}; document.body.appendChild(form); form.submit(); };
function openUrlInNewWindow(url) {
	var win = window.open(url, '_blank');
	if (win) {
		win.focus();
	} else {
		alert('Please allow popups for this website');
	}
}
function makeScrollTo() {
$('.lmfa .scrollto').each(function() {
  $(this).removeClass('scrollto').parents('.lmfa').scrollTop($(this).offset().top-250)
})
}
function makeModal(atitel,abody,aclass='') {						/* Modal erstellen */
amodal = '<div id="js-modal" class="modal fade '+aclass+'" tabindex="-1" role="dialog"><div class="modal-dialog modal-lg"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-label="Schließen"><span aria-hidden="true">&times;</span></button>' +
     '<h4 class="modal-title">'+atitel+'</h4></div>' +
     '<div class="modal-body">'+abody+'</div>' +
     '<div class="modal-footer"><button type="button" class="btn btn-default" data-dismiss="modal">Schließen</button></div>' +
     '</div></div></div>'
$('#js-modal').remove()
$('body').append(amodal)
$('#js-modal').modal('show').on('hidden.bs.modal', function (e) {
  $('#js-modal').remove()
})
}
function formatBytes(a,b){if(0==a)return"0 Bytes";var c=1e3,d=b||2,e=["Bytes","KB","MB","GB","TB","PB","EB","ZB","YB"],f=Math.floor(Math.log(a)/Math.log(c));return parseFloat((a/Math.pow(c,f)).toFixed(d))+" "+e[f]}
