(function($){jQuery(document).ready(function($){
  /* On */
  $(document).on('click','a.select-auswertung',function(e){	/* Auswertung auswählen */
    e.preventDefault()
    post(asurl, { csrfmiddlewaretoken: csrf, auswertung: $(this).data('auswertung') })
  })
  $(document).on('click','#seiten-auswertung>a',function(e){	/* Seite auswählen */
    e.preventDefault()
    var aelement = $(this)
    $.post(asurl, makeQuery({ getdatalist: 1, aseite: $(aelement).data('seite') }) , function(d,e,f,g=aelement) {
      $('#liste-auswertung').html(d)
      console.log('datenliste - '+$(g).data('seite')+' - Geladen')
    }).fail(function(d,e,f,g=aelement) {
      alert( "error" )
      console.log(d)
    })
  })
  $(document).on('click','#download-auswertung',function(e){	/* Auswertung herunterladen */
    e.preventDefault()
    post(asurl, makeQuery({ download: $(this).data('type') }))
  })
  $(document).on('click','.order-col-auswertung',function(e){	/* Auswertung sortieren */
    e.preventDefault()
    var aelement = $(this)
    $.post(asurl, makeQuery({ getdatalist: 1, orderby: $(this).data('orderby') }) , function(d,e,f,g=aelement) {
      $('#liste-auswertung').html(d)
      console.log('orderliste - '+$(g).data('orderby')+' - Geladen')
    }).fail(function(d,e,f,g=aelement) {
      alert( "error" )
      console.log(d)
    })
  })

  /* Funktionen */
  function makeQuery(adata) {
    xdata = adata
    if(typeof xdata.csrfmiddlewaretoken == 'undefined') { xdata.csrfmiddlewaretoken = csrf; };
    if(typeof xdata.auswertung == 'undefined') { xdata.auswertung = $('#view-auswertung').data('auswertung'); };
    if(typeof xdata.aseite == 'undefined') { xdata.aseite = $('#data-auswertung').data('seite'); };
    if(typeof xdata.orderby == 'undefined') { xdata.orderby = $('#data-auswertung').data('orderby'); };
    return xdata
  }
});})(jQuery);
