/* global csrf aurl alert confirm tabellen $ d3 */
var tabellenjson = JSON.parse(tabellen);

var d3svg = 			d3.select('#d3Diagramm').append('svg').attr('id', 'd3svg');

var d3Tabellen =	d3svg.append('g').attr('id', 'd3Tabellen');

var d3Tabelle =		d3Tabellen.selectAll('.d3Tabelle')
														.data(tabellenjson)
															.enter().append('g').classed('d3Tabelle', true).attr('id', function (d) { return d.db_table; })
															.attr('transform', function (d, i) { return 'translate(' + d.xt + ',' + d.yt + ')'; });

var d3Titel =			d3Tabelle.append('g').classed('d3TabelleTitel', true).attr('title', function (d) { return titelErstellen({'verbose_name': d.verbose_name, 'app': d.app, 'model': d.model, 'db_table': d.db_table}); });
d3Titel.append('text').text(function (d) { return d.model + ' (' + d.count + ')'; });

var d3Inhalt =		d3Tabelle.selectAll('.d3TabelleFelder')
														.data(function (d) { return d.get_fields; })
															.enter().append('g').classed('d3TabelleFelder', true).attr('id', function (d) { return d3.select(this.parentNode).datum().db_table + '__' + d.field_name; }).attr('title', function (d) { return titelErstellen(d); })
															.attr('transform', function (d, i) { return 'translate(0,' + (25 + i * 17) + ')'; })
															.each(function (d, i) {
																if (d.related_db_table) {
																	var aFrom = d3.select('#' + d.related_db_table);
																	d3Tabellen.insert('path', '*:first-child').datum({
																		'from': aFrom.node(),
																		'to': this.parentNode,
																		'field': this
																	}).attr('class', 'line');
																}
															});
d3Inhalt.append('text')
			.text(function (d) { return d.field_name; });
d3Tabelle.selectAll('.d3TabelleFelder')
			.on('click', feldClick)
			.on('mouseenter', feldMouseEnter)
			.on('mouseleave', feldMouseLeave);

d3Tabelle.insert('rect', '*:first-child').attr('x', -10).attr('y', -20).attr('width', function (d, i) { var aw = this.parentNode.getBBox().width + 20; d.cx = aw / 2 - 5; return aw; }).attr('height', function (d, i) { var ah = this.parentNode.getBBox().height + 12; d.cy = ah / 2 - 10; return ah; });
updateAlleLinien();
d3Titel.insert('rect', '*:first-child').attr('x', -9).attr('y', -19).attr('width', function (d, i) { return this.parentNode.parentNode.getBBox().width - 2; }).attr('height', function (d, i) { return this.parentNode.getBBox().height + 10; });
d3Inhalt.insert('rect', '*:first-child').attr('x', -9).attr('y', -14).attr('width', function (d, i) { return this.parentNode.parentNode.getBBox().width - 2; }).attr('height', function (d, i) { return this.parentNode.getBBox().height; });

var zoom = d3.zoom().scaleExtent([0.2, 3]).on('zoom', function () {
	d3Tabellen.attr('transform', d3.event.transform);
});

d3Tabelle.on('mouseenter', tabelleMouseEnter)
			.on('mouseleave', tabelleMouseLeave);

function tabelleMouseEnter () {
	var aTabelle = this;
	var d3Linien = d3Tabellen.selectAll('.line');
	d3Linien.each(function () {
		var aThis = d3.select(this);
		if (aThis.datum().from === aTabelle) {
			aThis.classed('vonTabelle', true);
			d3.select(aThis.datum().field).classed('zeigendesFeld', true);
			d3.select(aThis.datum().to).classed('zeigendeTabelle', true);
		} else if (aThis.datum().to === aTabelle) {
			aThis.classed('zuTabelle', true);
			d3.select(aThis.datum().from).classed('zielTabelle', true);
		}
	});
}
function tabelleMouseLeave () {
	d3Tabellen.selectAll('.line').classed('vonTabelle', false).classed('zuTabelle', false).classed('aktivesFeld', false);
	d3Tabelle.selectAll('.d3TabelleFelder').classed('zeigendesFeld', false);
	d3Tabelle.classed('zeigendeTabelle', false).classed('zielTabelle', false);
}
function feldClick () {
	console.log('click ...');
}
function feldMouseEnter () {
	var aFeld = this;
	d3Tabellen.selectAll('.line').each(function () {
		var aThis = d3.select(this);
		if (aThis.datum().field === aFeld) {
			aThis.classed('aktivesFeld', true);
		}
	});
}
function feldMouseLeave () {
	d3Tabellen.selectAll('.line').classed('aktivesFeld', false);
}

function zoomZuUebersicht () {
	var sBox = d3svg.node().getBoundingClientRect();
	var bBox = d3Tabellen.node().getBBox();
	var aScale = 1;
	var tScaleX = sBox.width / bBox.width;
	var tScaleY = sBox.height / bBox.height;
	if (tScaleX < 1) { aScale = tScaleX - 0.015; };
	if (tScaleY < 1 && tScaleY < tScaleX) { aScale = tScaleY - 0.015; };
	var tx = (sBox.width / 2) - (bBox.x + (bBox.width / 2)) * aScale;
	var ty = (sBox.height / 2) - (bBox.y + (bBox.height / 2)) * aScale;
	return d3.zoomIdentity.translate(tx, ty).scale(aScale);
}
d3svg.call(zoom.transform, zoomZuUebersicht);
d3svg.call(zoom);

/* Position der Tabellen speichern */
$(document).on('click', '#diagrammSpeichern:not(.loading)', function (e) {
	if (confirm('Wirklich die Positionen speichern?')) {
		var aelement = this;
		$(aelement).addClass('loading');
		var adata = [];
		d3Tabelle.each(function (d, i) {
			adata.push({'app': d.app, 'model': d.model, 'xt': d.xt, 'yt': d.yt});
		});
		$.post(aurl, { csrfmiddlewaretoken: csrf, speichere: 'positionen', positionen: JSON.stringify(adata) }, function (d, e, f, g = aelement) {
			if (d !== 'OK') {
				alert(d);
				console.log(d);
			}
			$(g).removeClass('loading');
		}).fail(function (d, e, f, g = aelement) {
			alert('error');
			$(g).removeClass('loading');
			console.log(d);
		});
	}
});

/* Zentrieren und Zoomen */
$(document).on('click', '#diagrammZentrieren', function (e) {
	d3svg.call(zoom.transform, zoomZuUebersicht);
	d3svg.call(zoom);
});

$(document).ready(function () {
	$('#d3Tabellen g.d3TabelleFelder, #d3Tabellen g.d3TabelleTitel').tooltip({
		'container': 'body',
		'placement': 'right',
		'html': true
	});
});

/* Funktionen */
var d3TabelleDrag = d3.drag().container(function () { return this.parentNode.parentNode; }).subject(this)
		.on('start', function (d) {
			d3.select(this.parentNode).moveToFront();
			if (d.x1) {
				d.x1 = d3.event.x - d.xt;
				d.y1 = d3.event.y - d.yt;
			} else {
				d.x1 = d3.event.x - d.xt;
				d.y1 = d3.event.y - d.yt;
			}
		})
		.on('drag', function (d) {
			var d3Parent = d3.select(this.parentNode);
			d3Parent.attr('transform', 'translate(' + (d3.event.x - d.x1) + ',' + (d3.event.y - d.y1) + ')');
			d.xt = d3.event.x - d.x1;
			d.yt = d3.event.y - d.y1;
			d3Tabellen.selectAll('.line').each(function () {
				var d3LinieDatum = d3.select(this).datum();
				if (d3Parent.node() === d3LinieDatum.from || d3Parent.node() === d3LinieDatum.to) {
					updateLinie(d3.select(this));
				}
			});
		});
d3Titel.call(d3TabelleDrag);

function updateAlleLinien () {
	d3Tabellen.selectAll('.line').each(function () {
		updateLinie(d3.select(this));
	});
}
function updateLinie (d3Linie) {
	var aFrom = d3.select(d3Linie.datum().from).datum();
	var aTo = d3.select(d3Linie.datum().to).datum();
	d3Linie.attr('d', stepLine(aFrom.xt + aFrom.cx, aFrom.yt + aFrom.cy, aTo.xt + aTo.cx, aTo.yt + aTo.cy));
}

// function verbundeneTabelle (d) {
// 	d3Tabelle.selectAll('.d3TabelleFelder').classed('active', false);
// 	d3.select('#d3Diagramm').selectAll('.d3Tabelle').classed('active', false);
// 	if (d.related_db_table) {
// 		d3.select(this).classed('active', true);
// 		d3.select('#' + d.related_db_table).classed('active', true);
// 	}
// }

function titelErstellen (d) {
	var o = '';
	for (var p in d) {
		o = o + p + ' = "' + d[p] + '"<br>';
	}
	return o;
}

d3.selection.prototype.moveToFront = function () {
	return this.each(function () {
		this.parentNode.appendChild(this);
	});
};
d3.selection.prototype.moveToBack = function () {
	return this.each(function () {
		var firstChild = this.parentNode.firstChild;
		if (firstChild) {
			this.parentNode.insertBefore(this, firstChild);
		}
	});
};

function stepLine (x1, y1, x2, y2) {
	var l = [];
	var mx = x1 + (x2 - x1) / 2;
	l.push('M', x1, y1);
	l.push('L', mx, y1);
	l.push('L', mx, y2);
	l.push('L', x2, y2);
	return l.join(' ');
}
