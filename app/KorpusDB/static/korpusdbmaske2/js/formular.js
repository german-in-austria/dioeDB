/* On */
function antwortenSpeichernClick(e){
  var saveit = 1
  if(!checkEbenen()) { saveit=0; };
  if(saveit==1) {
    var sAntworten = []
    $('.antwort').each(function() {
      var sAntwort = {}
      if($(this).hasClass('delit')) {
        sAntwort['delit'] = 1
      }
      $(this).find('input,textarea').each(function() {
        if($(this).attr('type')=='checkbox') {
          sAntwort[$(this).attr('name')]=$(this).is(':checked')
        } else {
          if($(this).attr('name') == 'start_Antwort' || $(this).attr('name') == 'stop_Antwort') {
            sAntwort[$(this).attr('name')]=durationToSeconds($(this).val())
          } else {
            sAntwort[$(this).attr('name')]=$(this).val()
          }
        }
      })
      sAntworten.push(sAntwort)
    })
    $.post(aurl+$('input[name="von_Inf"]').first().val()+'/'+$('input[name="zu_Aufgabe"]').first().val()+'/',{ csrfmiddlewaretoken: csrf , save: 'Aufgaben' , aufgaben: JSON.stringify(sAntworten) }, function(d) {
      unsavedAntworten=0
      $('#aufgabencontent').html(d)
      informantenAntwortenUpdate()
      familienHinzufuegenKnopfUpdate()
    }).fail(function(d) {
      alert( "error" )
      console.log(d)
    })
  }
}
function antwortAudioBereichChange(e){
  $(this).val(secondsToDuration(durationToSeconds($(this).val())))
  setAudioMarks()
}
function ausgewaehlteAufgabeChange(e){
  $('#selaufgabe').submit()
}


/* Funktionen */
function loadMitErhebungen() {
	if (typeof(Storage) !== "undefined") {
		if (localStorage.KorpusDBmitErhebung && localStorage.KorpusDBmitErhebung == 1) {
			$('#mitErhebungen').prop('checked', true);
		} else {
			$('#mitErhebungen').prop('checked', false);
		}
	}
	setMitErhebungen()
}
function setMitErhebungen() {
	if($('#mitErhebungen').is(':checked')) {
		$('#ainformant>option.noErheb').hide()
		if (typeof(Storage) !== "undefined") { localStorage.setItem("KorpusDBmitErhebung", 1); }
	} else {
		$('#ainformant>option.noErheb').show()
		if (typeof(Storage) !== "undefined") { localStorage.setItem("KorpusDBmitErhebung", 0); }
	}
}
function updateAinformantErhebung() {
	if($('#ainformantErhebung').val() == 0) {
		$('#ainformantErhebung').parents('.lmfa').find('.lmfa-l .lmfabc').parent().removeClass('ainferh-hide')
	} else {
		var aval = $('#ainformantErhebung').val()
		$('#ainformantErhebung').parents('.lmfa').find('.lmfa-l .lmfabc').each(function(){
			if(aval.match(new RegExp("(?:^|,)"+$(this).data('erhebungen')+"(?:,|$)"))) {
				$(this).parent().removeClass('ainferh-hide')
			} else {
				$(this).parent().addClass('ainferh-hide')
			}
		})
	}
}
function formularChanged(){
  unsavedAntworten = 1
  $('#antwortensave').removeClass('disabled')
}
function erhInfAufgabeChanged(){
  unsavedEIAufgabe=1
  $('#eiaufgsave').removeClass('disabled')
}
function informantenAntwortenUpdate() {
  $.post(aurl+'0/0/',{ csrfmiddlewaretoken: csrf , infantreset: 1 , aauswahl: $('select[name="aauswahl"]').val() , ainformant: $('select[name="ainformant"]').val() , aerhebung: $('select[name="aerhebung"]').val() , aaufgabenset: $('select[name="aaufgabenset"]').val() , aaufgabe: $('select[name="aaufgabe"]').val() }, function(d) {
    $('ul.lmfa-l').html(d)
		updateAinformantErhebung()
  }).fail(function(d) {
    alert( "error" )
    console.log(d)
  })
}
