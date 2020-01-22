/* global $ performance */

const svgfunctions = {
	preRenderTEvent: function (key, rerender = false) {
		if (rerender || this.tEvents[key]['rerender']) {
			this.tEvents[key]['svgWidth'] = this.sizeTEvent(key);
			this.tEvents[key]['rerender'] = false;
		}
	},
	sizeTEvent: function (key) {
		var mW = 0;
		Object.keys(this.aInformanten).map(function (iKey, iI) {	// Informanten durchzählen
			Object.keys(this.tEvents[key]['eId']).map(function (eKey, eI) {
				if (eKey === iKey) {
					var aW = 0;
					this.aEvents[this.tEvents[key]['eId'][eKey]]['tid'][iKey].forEach(function (aTokenId) {
						var t1W = this.getTextWidth(this.getTokenString(aTokenId, 't'), false);
						var t2W = this.getTextWidth(this.getTokenString(aTokenId, 'o', 't'), false);
						var tW = ((t1W > t2W) ? t1W : t2W) + 1.5;
						this.aTokens[aTokenId]['svgLeft'] = aW + 2;
						this.aTokens[aTokenId]['svgWidth'] = tW + 2;
						aW += tW;
					}, this);
					if (aW > mW) {
						mW = aW;
					}
				}
			}, this);
		}, this);
		return mW + 2;
	},
	/* updateZeilenTEvents */
	updateZeilenTEvents: function () {
		var t0 = performance.now();
		var aWidth = this.zInfWidth;
		this.zeilenTEvents = [];
		var aZTEv = 0;
		this.zeilenTEvents[aZTEv] = {'eId': [], 'eH': 0, 'iId': [], 'eT': 0, 'tId': {'all': []}, 'tsId': {'all': []}, 'tsH': {'all': 0}, 'tsT': {}, 'tsIdZ': {}, 'tsZi': {}};
		var eTop = 0;
		this.zeilenHeight = 0;
		this.tEvents.forEach(function (val, key) {
			this.tEvents[key]['svgLeft'] = aWidth - this.zInfWidth;
			aWidth += val['svgWidth'] + 0.5;
			if (aWidth < this.mWidth - 25) {
				this.zeilenTEvents[aZTEv]['eId'].push(key);
			} else {
				this.uzteEndDataUpdate(aZTEv);
				this.zeilenHeight += this.zeilenTEvents[aZTEv]['eH'];
				eTop = this.zeilenTEvents[aZTEv]['eT'] + this.zeilenTEvents[aZTEv]['eH'];
				aWidth = this.zInfWidth + val['svgWidth'];
				aZTEv++;
				this.tEvents[key]['svgLeft'] = 0;
				this.zeilenTEvents[aZTEv] = {'eId': [key], 'eH': 0, 'iId': [], 'eT': eTop, 'tId': {'all': []}, 'tsId': {'all': []}, 'tsH': {'all': 0}, 'tsT': {}, 'tsIdZ': {}, 'tsZi': {}};
			}
		}, this);
		this.uzteEndDataUpdate(aZTEv);
		this.zeilenHeight += this.zeilenTEvents[aZTEv]['eH'];
		this.scrollRendering();
		var t1 = performance.now();
		console.log('updateZeilenTEvents: ' + Math.ceil(t1 - t0) + ' ms');
	},
	/* scrollRendering */
	scrollRendering: function () {
		var sPos = $('.mcon.vscroller').scrollTop();
		var sePos = sPos + this.sHeight + 75;
		var aTop = 0;
		var aBottom = 0;
		var cRenderZeilen = [];
		this.zeilenTEvents.some(function (val, key) {
			aBottom = aTop + val['eH'];
			if (sePos >= aTop && sPos <= aBottom) {
				cRenderZeilen.push(key);
			}
			aTop += val['eH'];
			return aTop > sePos;
		}, this);
		if (this.renderZeilen !== cRenderZeilen) {
			this.renderZeilen = cRenderZeilen;
		}
	},
	/* Funktion zur ermittlung der Breite von Buchstaben im SVG-Element */
	getCharWidth: function (zeichen) {
		if (this.getCharWidthCach[zeichen]) {
			return this.getCharWidthCach[zeichen];
		} else {
			if (this.svgTTS) {
				this.svgTTS.textContent = zeichen;
				this.getCharWidthCach[zeichen] = this.svgTTS.getBBox().width;
				if (this.getCharWidthCach[zeichen] === 0) {
					this.svgTTS.textContent = 'X' + zeichen + 'X';
					this.getCharWidthCach[zeichen] = this.svgTTS.getBBox().width - this.getCharWidth('X') * 2;
				}
				return this.getCharWidthCach[zeichen];
			}
		}
	},
	/* Funktion zur ermittlung der Breite von Texten im SVG-Element */
	getTextWidth: function (text, cached = true) {
		if (cached) {
			var w = 0;
			var i = text.length;
			while (i--) {
				w += this.getCharWidth(text.charAt(i));
			}
			if (w) {
				return w;
			}
		} else {
			if (this.svgTTS) {
				this.svgTTS.textContent = text;
				return this.svgTTS.getBBox().width;
			}
		}
	},

	uzteEndDataUpdate: function (aZTEv) {
		// console.log(this.zeilenTEvents[aZTEv]);
		this.zeilenTEvents[aZTEv]['eId'].forEach(function (val, key) {
			var tEvent = this.tEvents[val];
			Object.keys(tEvent['eId']).map(function (iKey, iI) {
				if (this.aInformanten[iKey].show) {
					if (this.zeilenTEvents[aZTEv]['iId'].indexOf(iKey) < 0) {
						this.zeilenTEvents[aZTEv]['iId'].push(iKey);
					}
					var aEvent = this.aEvents[tEvent['eId'][iKey]];
					aEvent['tid'][iKey].forEach(function (aTokenId, tidKey) {
						if (!this.zeilenTEvents[aZTEv]['tId'][iKey]) {
							this.zeilenTEvents[aZTEv]['tId'][iKey] = [];
						}
						if (this.zeilenTEvents[aZTEv]['tId']['all'].indexOf(aTokenId) < 0) {
							this.zeilenTEvents[aZTEv]['tId']['all'].push(aTokenId);
							this.zeilenTEvents[aZTEv]['tId'][iKey].push(aTokenId);
							if (this.aTokens[aTokenId]['tokenSets']) {
								this.aTokens[aTokenId]['tokenSets'].forEach(function (aTokenSetId, tsidKey) {
									if (this.zeilenTEvents[aZTEv]['tsId']['all'].indexOf(aTokenSetId) < 0) {
										if (!this.zeilenTEvents[aZTEv]['tsId'][iKey]) {
											this.zeilenTEvents[aZTEv]['tsId'][iKey] = [];
										}
										this.zeilenTEvents[aZTEv]['tsId']['all'].push(aTokenSetId);
										this.zeilenTEvents[aZTEv]['tsId'][iKey].push(aTokenSetId);
									}
								}, this);
							}
						}
					}, this);
				}
			}, this);
		}, this);
		Object.keys(this.aInformanten).map(function (iKey, iI) {
			var tsIdZp = 0;
			if (this.zeilenTEvents[aZTEv]['iId'].indexOf(iKey) > -1) {
				var aZteStart = this.aTokenReihung.indexOf(this.zeilenTEvents[aZTEv]['tId'][iKey][0]);
				var aZteEnde = this.aTokenReihung.indexOf(this.zeilenTEvents[aZTEv]['tId'][iKey][this.zeilenTEvents[aZTEv]['tId'][iKey].length - 1]);
				if (this.zeilenTEvents[aZTEv]['tsId'][iKey]) {
					this.zeilenTEvents[aZTEv]['tsIdZ'][iKey] = [];
					this.zeilenTEvents[aZTEv]['tsZi'][iKey] = {};
					// TokenSets sortieren:
					this.zeilenTEvents[aZTEv]['tsId'][iKey] = this.sortTokenSets(this.zeilenTEvents[aZTEv]['tsId'][iKey]);
					// TokenSets in Zeilen laden:
					if (!this.zeilenTEvents[aZTEv]['tsIdZ'][iKey]) { this.zeilenTEvents[aZTEv]['tsIdZ'][iKey] = []; };
					this.zeilenTEvents[aZTEv]['tsId'][iKey].some(function (tsId) {
						// TokenSets sortieren:
						var aSetT = (this.aTokenSets[tsId].t || this.aTokenSets[tsId].tx);
						var atSetStart = this.aTokenReihung.indexOf(aSetT[0]);
						var atSetEnde = this.aTokenReihung.indexOf(aSetT[aSetT.length - 1]);
						var aDeep = this.zeilenTEvents[aZTEv]['tsIdZ'][iKey].length;
						this.zeilenTEvents[aZTEv]['tsIdZ'][iKey].some(function (y, yD) {
							var aOk = true;
							y.forEach(function (x) {
								var tSet = (this.aTokenSets[x].t || this.aTokenSets[x].tx);
								if (atSetStart <= this.aTokenReihung.indexOf(tSet[tSet.length - 1]) && atSetEnde >= this.aTokenReihung.indexOf(tSet[0])) {
									aOk = false;
									return true;
								}
							}, this);
							if (aOk) {
								aDeep = yD;
								return true;
							}
						}, this);
						if (!this.zeilenTEvents[aZTEv]['tsIdZ'][iKey][aDeep]) {
							this.zeilenTEvents[aZTEv]['tsIdZ'][iKey][aDeep] = [];
						}
						this.zeilenTEvents[aZTEv]['tsIdZ'][iKey][aDeep].push(tsId);
						// Zusätzliche Daten für SVG Darstellung der Token Sets hinzufügen:
						this.zeilenTEvents[aZTEv]['tsZi'][iKey][tsId] = {};
						this.zeilenTEvents[aZTEv]['tsZi'][iKey][tsId]['sT'] = ((atSetStart < aZteStart) ? undefined : aSetT[0]);
						this.zeilenTEvents[aZTEv]['tsZi'][iKey][tsId]['eT'] = ((atSetEnde > aZteEnde) ? undefined : aSetT[aSetT.length - 1]);
						if (this.aTokenSets[tsId].tx) {
							this.zeilenTEvents[aZTEv]['tsZi'][iKey][tsId]['sX'] = ((atSetStart < aZteStart) ? undefined : (this.tEvents[this.getTEventOfAEvent(this.searchByKey(this.aTokens[aSetT[0]].e, 'pk', this.aEvents))].svgLeft + this.aTokens[aSetT[0]].svgLeft));
							this.zeilenTEvents[aZTEv]['tsZi'][iKey][tsId]['eX'] = ((atSetEnde > aZteEnde) ? undefined : (this.tEvents[this.getTEventOfAEvent(this.searchByKey(this.aTokens[aSetT[aSetT.length - 1]].e, 'pk', this.aEvents))].svgLeft + this.aTokens[aSetT[aSetT.length - 1]].svgLeft + this.aTokens[aSetT[aSetT.length - 1]].svgWidth));
						} else {
							this.zeilenTEvents[aZTEv]['tsZi'][iKey][tsId]['sX'] = ((atSetStart < aZteStart) ? undefined : (this.tEvents[this.getTEventOfAEvent(this.searchByKey(this.aTokens[aSetT[0]].e, 'pk', this.aEvents))].svgLeft + this.aTokens[aSetT[0]].svgLeft + (this.aTokens[aSetT[0]].svgWidth / 2)));
							this.zeilenTEvents[aZTEv]['tsZi'][iKey][tsId]['eX'] = ((atSetEnde > aZteEnde) ? undefined : (this.tEvents[this.getTEventOfAEvent(this.searchByKey(this.aTokens[aSetT[aSetT.length - 1]].e, 'pk', this.aEvents))].svgLeft + this.aTokens[aSetT[aSetT.length - 1]].svgLeft + (this.aTokens[aSetT[aSetT.length - 1]].svgWidth / 2)));
							this.zeilenTEvents[aZTEv]['tsZi'][iKey][tsId]['tX'] = [];
							aSetT.forEach(function (val) {
								if (this.zeilenTEvents[aZTEv]['tId'][iKey].indexOf(val) > -1) {
									var aToken = this.aTokens[val];
									this.zeilenTEvents[aZTEv]['tsZi'][iKey][tsId]['tX'].push(this.tEvents[this.getTEventOfAEvent(this.searchByKey(aToken.e, 'pk', this.aEvents))].svgLeft + aToken.svgLeft + (aToken.svgWidth / 2));
								}
							}, this);
						}
						tsIdZp = this.zeilenTEvents[aZTEv]['tsIdZ'][iKey].length - 1;
					}, this);
					tsIdZp += 1;
					// Sortierung optimieren:
					var dChange = true;
					for (var m = 0; (m < 10 && dChange); m++) {
						dChange = false;
						for (var i = this.zeilenTEvents[aZTEv]['tsIdZ'][iKey].length - 2; i >= 0; i--) {
							this.zeilenTEvents[aZTEv]['tsIdZ'][iKey][i].forEach(function (aVal, aIndex) {
								var aSetT = (this.aTokenSets[aVal].t || this.aTokenSets[aVal].tx);
								var atSetStart = this.aTokenReihung.indexOf(aSetT[0]);
								var atSetEnde = this.aTokenReihung.indexOf(aSetT[aSetT.length - 1]);
								var aOk = true;
								this.zeilenTEvents[aZTEv]['tsIdZ'][iKey][i + 1].some(function (nVal, nIndex) {
									var nSetT = (this.aTokenSets[nVal].t || this.aTokenSets[nVal].tx);
									if (atSetStart <= this.aTokenReihung.indexOf(nSetT[nSetT.length - 1]) && atSetEnde >= this.aTokenReihung.indexOf(nSetT[0])) {
										aOk = false;
										return true;
									}
								}, this);
								if (aOk) {
									dChange = true;
									this.zeilenTEvents[aZTEv]['tsIdZ'][iKey][i + 1].push(this.zeilenTEvents[aZTEv]['tsIdZ'][iKey][i].splice(aIndex, 1)[0]);
								}
							}, this);
						}
					}
				}
				this.zeilenTEvents[aZTEv]['tsT'][iKey] = this.zeilenTEvents[aZTEv]['tsH']['all'];
				this.zeilenTEvents[aZTEv]['tsH'][iKey] = this.aTokenSetHeight * (tsIdZp);
				this.zeilenTEvents[aZTEv]['tsH']['all'] += this.zeilenTEvents[aZTEv]['tsH'][iKey];
			}
		}, this);
		var tsIdZpA = 0;
		if (this.zeilenTEvents[aZTEv]['tsIdZ']) {
			Object.keys(this.zeilenTEvents[aZTEv]['tsIdZ']).map(function (iKey, iI) {
				tsIdZpA += this.zeilenTEvents[aZTEv]['tsIdZ'][iKey].length;
			}, this);
		}
		this.zeilenTEvents[aZTEv]['eH'] = this.eEventHeight + (this.aTokenSetHeight * tsIdZpA) + (this.eInfHeight + this.eInfTop) * this.zeilenTEvents[aZTEv]['iId'].length;
	},
	/* Zu Token scrollen */
	scrollToToken: function (tId) {
		var sTop = $('.mcon.vscroller').scrollTop();
		var sBottom = sTop + this.sHeight + 75;
		var aZTE = this.zeilenTEvents[this.getZeileOfTEvent(this.getTEventOfAEvent(this.searchByKey(this.aTokens[this.selToken]['e'], 'pk', this.aEvents)))];
		var sTo = 0;
		if (aZTE) {
			if (aZTE['eT'] < sTop) {
				sTo = aZTE['eT'] - 20;
				if (sTo < 0) { sTo = 0; }
				$('.mcon.vscroller').stop().animate({scrollTop: sTo}, 250);
			} else if ((aZTE['eT'] + aZTE['eH']) > sBottom) {
				sTo = (aZTE['eT'] + aZTE['eH'] + 20) - (this.sHeight + 75) * 0.8;
				if (sTo < 0) { sTo = 0; }
				$('.mcon.vscroller').stop().animate({scrollTop: sTo}, 250);
			}
		} else {
			console.log(tId, this.selToken, this.aTokens[this.selToken]['e']);
		}
	}
};
