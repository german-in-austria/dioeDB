/* Variablen */
var unsavedAntworten = 0;
var unsavedEIAufgabe = 0;

(function($){jQuery(document).ready(function($){
	/* Inits */
	resetBeeinflussung()
	resetReihungTags()
	resetReihungAntworten()
	setAudioPlayer()
	tagEbenenOptionUpdateAll()

	/* Tastenkürzel */
	Mousetrap.bind('ctrl+e', function(e) { return false; })
	Mousetrap.bind('ctrl+s', function(e) { $('#antwortensave').click(); return false; })
	Mousetrap.bind('ctrl+d', function(e) { $('#addantwort').click(); return false; })
	Mousetrap.bind('ctrl+space', function(e) { $('#audio-play-pause').click(); return false; })
	Mousetrap.bind('ctrl+q', function(e) { $('#audio-fast-backward').click(); return false; })
	Mousetrap.bind('ctrl+w', function(e) { $('#audio-fast-forward').click(); return false; })
	Mousetrap.bind('ctrl+2', function(e) { $('#audio-backward').click(); return false; })
	Mousetrap.bind('ctrl+3', function(e) { $('#audio-forward').click(); return false; })
	Mousetrap.bind('ctrl+1', function(e) { $('#audio-step-backward').click(); return false; })
	Mousetrap.bind('ctrl+4', function(e) { $('#audio-step-forward').click(); return false; })

	/* On */
	/* Allgemein */
	window.onbeforeunload = function () {
		if(unsavedAntworten!=0 || unsavedEIAufgabe!=0) {
			return 'Es gibt noch ungespeicherte Veränderungen! Wirklich verwerfen?'
		}
	}
	$(document).on('click','.lmfabc',function(e){
		e.preventDefault()
		if((unsavedAntworten==0 && unsavedEIAufgabe==0) || confirm('Es gibt noch ungespeicherte veränderungen! Wirklich verwerfen?')) {
			unsavedAntworten=0
			unsavedEIAufgabe=0
			$('.lmfabc').removeClass('open')
			$(this).addClass('open')
			$.post($(this).attr('href'),{ csrfmiddlewaretoken: csrf }, function(d) {
				$('.mcon').html(d)
				addAntwort()
				resetBeeinflussung()
				tagEbenenOptionUpdateAll()
				setAudioPlayer()
				familienHinzufuegenKnopfUpdate()
			}).fail(function(d) {
				alert( "error" )
				console.log(d)
			})
		}
	})
	/* Formular */
	$(document).on('click','.antwort .antwortreihunghoch:not(.disabled), .antwort .antwortreihungrunter:not(.disabled)',antwortReihungHochRunterClick)
	$(document).on('change','.antwort input,.antwort textarea,select.tagebene',formularChanged)
	$(document).on('change','input[name="start_Antwort"], input[name="stop_Antwort"]',antwortAudioBereichChange)
	$(document).on('change','#selaufgabe select',ausgewaehlteAufgabeChange)
	$(document).on('change','#erhinfaufgaben',setAudioPlayer)
	$(document).on('click','#erhinfaufgaben',erhInfAufgabenClick)
	$(document).on('change','input[name="ist_bfl"]',resetBeeinflussung)
	$(document).on('change','#start_ErhInfAufgaben, #stop_ErhInfAufgaben',erhInfAufgabenChange)
	$(document).on('click','#eiaufgsave:not(.disabled)',erhInfAufgabenSpeichernClick)
	$(document).on('click','#antwortensave:not(.disabled)',antwortenSpeichernClick)
	$(document).on('click','#addantwort',addAntwort)
	$(document).on('click','.delantwort',antwortLoeschenClick)
	/* Tags */
	$(document).mouseup(closeTagSelect)
	$(document).on('click','.antwort .ptagsleft, .antwort .ptagsright',moveTagLeftRightClick)
	$(document).on('click','.ant-ftag',openNewTagSelectClick)
	$(document).on('click','.ant-ctag',openTagPresetSelectClick)
	$(document).on('click','.ant-tag',openChangeTagSelectClick)
	$(document).on('click','.edittag .ptagsbtn:not(.ptagsleft,.ptagsright)',tagAendernLoeschenClick)
	$(document).on('click','.newtag .ptagsbtn',tagHinzufuegenClick)
	$(document).on('click','.pretags .pretagsbtn',tagPresetHinzufuegenClick)
	$(document).on('click','.add-tag-line',addTagLineClick)
	$(document).on('change','select.tagebene',tagEbeneChange)
	$(document).on('mouseenter','button.ant-ftag',function(){$(this).siblings('button.ant-tag').addClass('addhover')})
	$(document).on('mouseleave','button.ant-ftag',function(){$(this).siblings('button.ant-tag').removeClass('addhover')})
	/* Audio */
	$(document).on('click','#aufgabenprogress, #inferhebungprogress',progressClick)
	$(document).on('click','#audio-play-pause',playPauseClick)
	$(document).on('click','#audio-fast-backward',fastBackwardClick)
	$(document).on('click','#audio-fast-forward',fastForwardClick)
	$(document).on('click','#audio-backward',backwardClick)
	$(document).on('click','#audio-forward',forwardClick)
	$(document).on('click','#audio-step-backward',stepBackwardClick)
	$(document).on('click','#audio-step-forward',stepForwardClick)
	$(document).on('click','#audio-step-forward',informantenAntwortenUpdate)

});})(jQuery);
