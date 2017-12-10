tabellenjson = JSON.parse(tabellen);

var d3Tabelle =	d3.select('#d3Diagramm')
									.selectAll('.d3Tabelle')
									.data(tabellenjson)
										.enter().append("div").attr('class','d3Tabelle').attr('id',function(d){ return d.db_table; })

var d3Titel =		d3Tabelle.append("div").attr('class','d3TabelleTitel').attr('title',function(d){ return makeTitel({'verbose_name':d.verbose_name,'app':d.app,'model':d.model,'db_table':d.db_table}); })
													.text(function(d){ return d.model+" ("+d.count+")"; })

var d3content =	d3Tabelle.selectAll('.d3TabelleFelder')
													.data(function(d) { return d.get_fields; })
												 		.enter().append("div").attr('class','d3TabelleFelder').attr('id',function(d){ return d.field_name; }).attr('title',function(d){ return makeTitel(d); })
															.text(function(d){ return d.field_name; })



function makeTitel(d) {
	var o = '';
	for (var p in d) {
		o = o+p+' = "'+d[p]+'"\n';
	}
	return o;
}
