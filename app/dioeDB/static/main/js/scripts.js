(function($){jQuery(document).ready(function($){
	$(document).on('click','.show-hide-unused-cols',function(e){
		$('.hide-unused-cols').toggleClass('all')
		$(this).find('span').toggleClass('glyphicon-eye-close glyphicon-eye-open')
	});
	function CheckSysStatus() {
		if(sysstatus['sperre']) {
			alert(sysstatus['wartung']['stitel']+"\n\n"+sysstatus['wartung']['stext']+"\n\nWartungstermin: "+sysstatus['wartung']['zeit']+"\nBisherige Dauer: "+(-sysstatus['wartung']['restzeit'])+" Minuten")
			if(!isstartseite) {
				post("/", { csrfmiddlewaretoken: csrf})
			}
		} else if(typeof sysstatus['wartung'] != "undefined") {
			alert(sysstatus['wartung']['titel']+"\n\n"+sysstatus['wartung']['text']+"\n\nWartungstermin: "+sysstatus['wartung']['zeit']+"\nRestzeit: "+sysstatus['wartung']['restzeit']+" Minuten")
		}
	}
	CheckSysStatus()
	function NewCheckSysStatus() {
		$.post(sysstatusurl, { csrfmiddlewaretoken: csrf } , function(d) {
			sysstatus = jQuery.parseJSON(d)
			CheckSysStatus()
		}).fail(function(d) {
			alert( "Verbindungsfehler!\n\n Konnte den Systemstatus nicht abrufen!" )
		})
	}
	setInterval(NewCheckSysStatus, 600000); /* 600000 = 10 Minuten */
});})(jQuery);
