tabellenjson = JSON.parse(tabellen);

var d3svg = 			d3.select('#d3Diagramm').append("svg").attr('id','d3svg')

var d3Tabellen =	d3svg.append('g').attr('id','d3Tabellen')

var d3Tabelle =		d3Tabellen.selectAll('.d3Tabelle')
														.data(tabellenjson)
															.enter().append("g").classed('d3Tabelle', true).attr('id',function(d){ return d.db_table; })
															.attr('transform',function(d,i){ return 'translate('+d.xt+','+d.yt+')'; })

var d3Titel =			d3Tabelle.append("g").classed('d3TabelleTitel', true) // .attr('title',function(d){ return titelErstellen({'verbose_name':d.verbose_name,'app':d.app,'model':d.model,'db_table':d.db_table}); })
d3Titel.append('text').text(function(d){ return d.model+" ("+d.count+")"; })

var d3Inhalt =		d3Tabelle.selectAll('.d3TabelleFelder')
														.data(function(d) { return d.get_fields; })
												 			.enter().append("g").classed('d3TabelleFelder', true).attr('id',function(d){ return d3.select(this.parentNode).datum().db_table+'__'+d.field_name; }) // .attr('title',function(d){ return titelErstellen(d); })
															.attr('transform',function(d,i){ return 'translate(0,'+(25+i*17)+')'; })
															.each(function(d,i){
																if(d.related_db_table) {
																	d3Tabellen.insert('line','*:first-child').datum({
														                    'from': d3.select('#'+d.related_db_table).node(),
														                    'to': this.parentNode,
																								'field':this,
														                }).attr("class", "line")
													                 	.attr("x1", d3.select('#'+d.related_db_table).datum().xt)
														                .attr('y1', d3.select('#'+d.related_db_table).datum().yt)
																						.attr("x2", d3.select(this.parentNode).datum().xt)
																						.attr("y2", d3.select(this.parentNode).datum().yt)
																}
															})
d3Inhalt.append('text')
				.text(function(d){ return d.field_name; })

d3Tabelle.insert('rect','*:first-child').attr('x',-10).attr('y',-20).attr('width',function(d,i){ return this.parentNode.getBBox().width+20; }).attr('height',function(d,i){ return this.parentNode.getBBox().height+12; })
d3Titel.insert('rect','*:first-child').attr('x',-9).attr('y',-19).attr('width',function(d,i){ return this.parentNode.parentNode.getBBox().width-2; }).attr('height',function(d,i){ return this.parentNode.getBBox().height+10; })
d3Inhalt.insert('rect','*:first-child').attr('x',-9).attr('y',-14).attr('width',function(d,i){ return this.parentNode.parentNode.getBBox().width-2; }).attr('height',function(d,i){ return this.parentNode.getBBox().height; })

var zoom = d3.zoom().scaleExtent([0.2, 3]).on("zoom", function () {
              	d3Tabellen.attr("transform", d3.event.transform)
      				})

function zoomZuUebersicht() {
	var sBox = d3svg.node().getBoundingClientRect()
	var bBox = d3Tabellen.node().getBBox()
	var aScale = 1
	var tScaleX = sBox.width/bBox.width
	var tScaleY = sBox.height/bBox.height
	if(tScaleX<1) { aScale = tScaleX-0.015; };
	if(tScaleY<1 && tScaleY<tScaleX) { aScale = tScaleY-0.015; };
	var tx = (sBox.width/2)-(bBox.x+(bBox.width/2))*aScale
	var ty = (sBox.height/2)-(bBox.y+(bBox.height/2))*aScale
	return d3.zoomIdentity.translate(tx, ty).scale(aScale)
}
d3svg.call(zoom.transform, zoomZuUebersicht);
d3svg.call(zoom)

/* Position der Tabellen speichern */
$(document).on('click','#diagrammSpeichern:not(.loading)',function(e){
	if(confirm("Wirklich die Positionen speichern?")) {
		aelement = this
		$(aelement).addClass('loading')
		var adata = []
		d3Tabelle.each(function(d,i){
							adata.push({'app':d.app,'model':d.model,'xt':d.xt,'yt':d.yt})
						})
		$.post(aurl, { csrfmiddlewaretoken: csrf, speichere: 'positionen', positionen: JSON.stringify(adata) } , function(d,e,f,g=aelement) {
			if(d!='OK') {
				alert(d)
				console.log(d)
			}
			$(g).removeClass('loading')
		}).fail(function(d,e,f,g=aelement) {
			alert( "error" )
			$(g).removeClass('loading')
			console.log(d)
		})
	}
});

/* Zentrieren und Zoomen */
$(document).on('click','#diagrammZentrieren',function(e){
	d3svg.call(zoom.transform, zoomZuUebersicht);
	d3svg.call(zoom)
});




/* Funktionen */
var d3TabelleDrag = d3.drag().container(function(){ return this.parentNode.parentNode;}).subject(this)
	  .on('start',function (d) {
			d3.select(this.parentNode).moveToFront();
	    if (d.x1){
        d.x1 =  d3.event.x - d.xt;
        d.y1 =  d3.event.y - d.yt;
	    }else{
        d.x1 = d3.event.x - d.xt;
        d.y1 = d3.event.y - d.yt;
	    }
	  })
    .on('drag',function(d){
			d3Parent = d3.select(this.parentNode)
      d3Parent.attr("transform", "translate(" + (d3.event.x - d.x1)  + "," + (d3.event.y - d.y1) + ")");
      d.xt = d3.event.x - d.x1;
      d.yt = d3.event.y - d.y1;
			d3Tabellen.selectAll('line.line').each(function(){
				var d3This = d3.select(this)
				if(d3Parent.node()==d3This.datum().from) {
					d3This.attr("x1", d.xt).attr("y1", d.yt)
				} else if(d3Parent.node()==d3This.datum().to) {
					d3This.attr("x2", d.xt).attr("y2", d.yt)
				}
			})
    });
d3Titel.call(d3TabelleDrag);

function verbundeneTabelle(d) {
	d3Tabelle.selectAll('.d3TabelleFelder').classed('active', false)
	d3.select('#d3Diagramm').selectAll('.d3Tabelle').classed('active', false)
	if(d.related_db_table) {
		d3.select(this).classed('active', true)
		d3.select("#"+d.related_db_table).classed('active', true)
	};
}

function titelErstellen(d) {
	var o = '';
	for (var p in d) {
		o = o+p+' = "'+d[p]+'"\n';
	}
	return o;
}

d3.selection.prototype.moveToFront = function() {
  return this.each(function(){
    this.parentNode.appendChild(this);
  });
};
d3.selection.prototype.moveToBack = function() {
  return this.each(function() {
    var firstChild = this.parentNode.firstChild;
    if (firstChild) {
        this.parentNode.insertBefore(this, firstChild);
    }
  });
};
