tabellenjson = JSON.parse(tabellen);

var d3svg = 			d3.select('#d3Diagramm').append("svg").attr('id','d3svg')

var d3Tabellen =	d3svg.call(d3.zoom().on("zoom", function () {
              d3Tabellen.attr("transform", d3.event.transform)
      })).append('g').attr('id','d3Tabellen')

var d3Tabelle =		d3Tabellen.selectAll('.d3Tabelle')
														.data(tabellenjson)
															.enter().append("g").attr('class','d3Tabelle').attr('id',function(d){ return d.db_table; })
															.attr('transform',function(d,i){ d.xt=(50+i*200); d.yt=100; return 'translate('+d.xt+','+d.yt+')'; })

var d3Titel =			d3Tabelle.append("g").attr('class','d3TabelleTitel') // .attr('title',function(d){ return titelErstellen({'verbose_name':d.verbose_name,'app':d.app,'model':d.model,'db_table':d.db_table}); })
d3Titel.append('text').text(function(d){ return d.model+" ("+d.count+")"; })

var d3Inhalt =		d3Tabelle.selectAll('.d3TabelleFelder')
														.data(function(d) { return d.get_fields; })
												 			.enter().append("g").attr('class','d3TabelleFelder').attr('id',function(d){ return d3.select(this.parentNode).datum().db_table+'__'+d.field_name; }) // .attr('title',function(d){ return titelErstellen(d); })
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
	d3Tabelle.selectAll('.d3TabelleFelder').attr('class','d3TabelleFelder')
	d3.select('#d3Diagramm').selectAll('.d3Tabelle').attr('class','d3Tabelle')
	if(d.related_db_table) {
		d3.select(this).attr('class','d3TabelleFelder active')
		d3.select("#"+d.related_db_table).attr('class','d3Tabelle active')
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
