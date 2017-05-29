(function($){jQuery(document).ready(function($){
  /* Funktion für Standarddaten hinzufügen!!! für post Anfragen, damit alle Optionen immer mitgeschickt werden !!!!
      <!-- Hier hin !!!
   */
  $(document).on('click','a.select-auswertung',function(e){	/* Auswertung auswählen */
    e.preventDefault()
    post(asurl, { csrfmiddlewaretoken: csrf, auswertung: $(this).data('auswertung') })
  })
  $(document).on('click','#seiten-auswertung>a',function(e){	/* Seite auswählen */
    e.preventDefault()
    var aelement = $(this)
    $.post(asurl, { csrfmiddlewaretoken: csrf, auswertung: $('#view-auswertung').data('auswertung'), getdatalist: 1, aseite: $(aelement).data('seite') } , function(d,e,f,g=aelement) {
      $('#liste-auswertung').html(d)
      console.log('datenliste - '+$(g).data('seite')+' - Geladen')
    }).fail(function(d,e,f,g=aelement) {
      alert( "error" )
      console.log(d)
    })
  })
  $(document).on('click','#download-auswertung',function(e){	/* Auswertung herunterladen */
    e.preventDefault()
    post(asurl, { csrfmiddlewaretoken: csrf, auswertung: $('#view-auswertung').data('auswertung'), download: $(this).data('type') })
  })
});})(jQuery);
