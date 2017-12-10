tabellenjson = JSON.parse(tabellen);

var d3Tabelle =	d3.select('#d3Diagramm')
									.selectAll('.d3Tabelle')
									.data(tabellenjson)
										.enter().append("div").attr('class','d3Tabelle').attr('id',function(d){ return d.db_table; })

var d3Titel =		d3Tabelle.append("div").attr('class','d3TabelleTitel').attr('title',function(d){ return titelErstellen({'verbose_name':d.verbose_name,'app':d.app,'model':d.model,'db_table':d.db_table}); })
													.text(function(d){ return d.model+" ("+d.count+")"; })

var d3Inhalt =	d3Tabelle.selectAll('.d3TabelleFelder')
													.data(function(d) { return d.get_fields; })
												 		.enter().append("div").attr('class','d3TabelleFelder').attr('id',function(d){ return d.field_name; }).attr('title',function(d){ return titelErstellen(d); })
															.text(function(d){ return d.field_name; })
															.on("mouseover", verbundeneTabelle)



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
