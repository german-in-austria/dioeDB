/* global _ $ csrf Vue performance stdfunctions loadingsaving svgfunctions searchfilter tokensets tagsystemCache */

var preventClose = false;
window.onbeforeunload = function () {
	if (preventClose) {
		return 'Wirklich Tool verlassen?';
	}
};

var annotationsTool = new Vue({
	el: '#annotationsTool',
	delimiters: ['${', '}'],
	http: {
		root: '/annotationsdb/startvue',
		headers: {
			'X-CSRFToken': csrf
		},
		emulateJSON: true
	},
	data: {
		loading: true,
		tagCache: tagsystemCache,
		menue: {
			informantenMitTranskripte: [],
			aInformant: 0,
			aTranskripte: []
		},
		annotationsTool: {
			aPK: 0,
			nNr: 0,
			loaded: true
		},
		unsaved: false,
		aTmNr: 1,
		// Annotations Daten - Start
		aTranskript: {},				// Transkript Informationen - {"n":"01_LE_V2","pk":3,"ut":"10.12.2017- 16:30"}
		aEinzelErhebung: {},		// EinzelErhebung - {"lf":"","e":1,"o":"","pk":65,"af":"1124_173725","b":"","dp":"\\Interviews\\01_LE\\","d":"24.11.2014- 00:00","k":"","trId":3}
		aTokenTypes: {},				// TokenTypes - id: {"n":"word"}
		aInformanten: {},
		aInfLen: 0,
		aSaetze: {},
		aEvents: [],
		tEvents: [],
		aTokens: {},
		aTokenReihung: [],
		aTokenReihungInf: {},
		aTokenTextInf: null,
		aTokenFragmente: {},
		aTokenSets: {},
		delTokenSets: {},
		aAntworten: {},
		// Annotations Daten - Ende
		delAntworten: {},
		zeilenTEvents: [],
		zeilenHeight: 0,
		renderZeilen: [],
		svgTTS: document.getElementById('svg-text-textsize'),
		svgTokenLastView: -1,
		svgZeileSelected: -1,
		svgInfSelected: -1,
		svgSelTokenList: [],
		audioPos: 0,
		audioDuration: 0,
		aInfInfo: undefined,
		tEventInfo: undefined,
		aTokenInfo: undefined,
		aTokenSetInfo: undefined,
		message: null,
		mWidth: 0,
		sHeight: 0,
		getCharWidthCach: {},
		aTokenSetHeight: 20,
		eEventHeight: 40,
		eInfHeight: 63,
		eInfTop: 10,
		zInfWidth: 100,
		showTransInfo: true,
		showTokenInfo: true,
		showTokenSetInfo: true,
		showTokenSetInfos: true,
		showAllgeInfo: false,
		showSuche: false,
		showFilter: false,
		showTagEbene: false,
		previewTagEbene: 0,
		suchen: false,
		suchText: '',
		suchInf: 0,
		suchTokens: [],
		suchTokensInfo: {},
		suchOptText: true,
		suchOptOrtho: true,
		suchOptTextInOrtho: false,
		suchModus: 'token',
		suchModusWild: false,
		selToken: -1,
		selTokenBereich: {'v': -1, 'b': -1},
		selTokenListe: [],
		ctrlKS: false,
		selTokenSet: 0,
		selTokenSetSTMax: 15
	},
	computed: {
	},
	watch: {
		unsaved: function (nVal, oVal) {
			preventClose = nVal;
		},
		mWidth: function (nVal, oVal) {
			if (nVal !== oVal) {
				this.updateZeilenTEvents();
			}
		},
		selToken: function (nVal, oVal) {
			if (nVal > -1) {
				this.svgZeileSelected = this.getZeileOfTEvent(this.getTEventOfAEvent(this.searchByKey(this.aTokens[this.selToken]['e'], 'pk', this.aEvents)));
				this.svgInfSelected = this.aTokens[this.selToken]['i'];
				this.scrollToToken(this.selToken);
			} else {
				this.svgZeileSelected = -1;
				this.svgInfSelected = -1;
			}
		},
		'selTokenBereich.v': function (nVal, oVal) {
			this.checkSelTokenBereich();
		},
		'selTokenBereich.b': function (nVal, oVal) {
			this.checkSelTokenBereich();
		},
		showSuche: searchfilter.wShowSuche,
		showFilter: searchfilter.wShowFilter,
		suchText: searchfilter.wSuchText,
		aTokenInfo: function (nVal, oVal) { this.aTokenInfoChange(nVal, oVal); },
		'aTokenInfo.t': function (nVal, oVal) { this.aTokenInfoChange(nVal, oVal); },
		'aTokenInfo.tt': function (nVal, oVal) { this.aTokenInfoChange(nVal, oVal); },
		'aTokenInfo.o': function (nVal, oVal) { this.aTokenInfoChange(nVal, oVal); },
		'aTokenInfo.le': function (nVal, oVal) { this.aTokenInfoChange(nVal, oVal); },
		'aTokenInfo.to': function (nVal, oVal) { this.aTokenInfoChange(nVal, oVal); },
		'aTokenInfo.changed': function (nVal, oVal) {
			this.modalSperren('#aTokenInfo');
		},
		aTokenSetInfo: function (nVal, oVal) {
			if (this.aTokenSetInfo && oVal) { this.$set(this.aTokenSetInfo, 'changed', true); };
		},
		'aTokenSetInfo.changed': function (nVal, oVal) {
			this.modalSperren('#aTokenSetInfo');
		}
	},
	methods: {
		reset: loadingsaving.reset,
		/* getTranskript: Läd aktuelle Daten des Transkripts für das Annotations Tool */
		getTranskript: loadingsaving.getTranskript,
		/* Änderungen speichern */
		speichern: loadingsaving.speichern,
		/* setInformanten: Informanten setzten */
		setInformanten: function (nInformanten) {
			this.aInformanten = {};
			Object.keys(nInformanten).map(function (key, i) {
				this.aInformanten[key] = nInformanten[key];
				this.aInformanten[key]['i'] = i;
				this.aInformanten[key]['show'] = true;
			}, this);
			this.aInfLen = Object.keys(nInformanten).length;
		},
		/* addTokens: Tokens hinzufügen */
		addTokens: function (nTokens) {
			Object.keys(nTokens).map(function (key, i) {
				this.updateToken(key, nTokens[key]);
			}, this);
		},
		/* addTokenSets: TokenSets hinzufügen */
		addTokenSets: tokensets.addTokenSets,
		/* addAntworten: Antworten hinzufügen */
		addAntworten: function (nAntworten) {
			Object.keys(nAntworten).map(function (key, i) {
				if (nAntworten[key].pt) {
					nAntworten[key].tags = [];
					nAntworten[key].pt.forEach(function (val) {
						nAntworten[key].tags.push({'e': val.e, 'tags': this.processTags(val.t).tags});
					}, this);
					delete nAntworten[key].pt;
				}
				this.setAAntwort(key, nAntworten[key]);
			}, this);
		},
		delAntwort: function (dAntwort) {
			if (dAntwort > 0) {
				this.setAAntwort(dAntwort);
			}
		},
		processTags: function (pTags, pPos = 0, gen = 0) {
			var xTags = [];
			var xPos = pPos;
			var xClose = 0;
			while (xPos < pTags.length && xClose < 1) {
				if (pTags[xPos].c > 0) {
					xClose = pTags[xPos].c;
					pTags[xPos].c -= 1;
					xPos = xPos - 1;
				} else {
					var prData = this.processTags(pTags, xPos + 1);
					var zTags = prData.tags;
					var zPos = prData.pos;
					xTags.push({'id': pTags[xPos].i, 'tag': pTags[xPos].t, 'tags': zTags});
					xPos = zPos + 1;
				}
			}
			return {'tags': xTags, 'pos': xPos};
		},
		setAAntwort: function (key, val = undefined) {
			if (val === undefined) { // Antwort Löschen
				if (this.aAntworten[key]['its'] && this.aTokenSets[this.aAntworten[key]['its']]) {
					delete this.aTokenSets[this.aAntworten[key]['its']].aId;
				}
				if (this.aAntworten[key]['it'] && this.aTokens[this.aAntworten[key]['it']]) {
					delete this.aTokens[this.aAntworten[key]['it']].aId;
				}
				this.delAntworten[key] = this.aAntworten[key];
				delete this.aAntworten[key];
			} else { // Antwort setzen
				if (key === 0 || isNaN(key)) { // Neue Antwort
					key = -1;
					while (this.aAntworten[key]) {
						key -= 1;
					}
					val.saveme = true;
				}
				this.aAntworten[key] = val;
				if (this.aAntworten[key]['its'] && this.aTokenSets[this.aAntworten[key]['its']]) {
					this.aTokenSets[this.aAntworten[key]['its']].aId = parseInt(key);
				}
				if (this.aAntworten[key]['it'] && this.aTokens[this.aAntworten[key]['it']]) {
					this.aTokens[this.aAntworten[key]['it']].aId = parseInt(key);
				}
			}
			return key;
		},
		/* deleteATokenSet: TokenSet löschen */
		deleteATokenSet: tokensets.deleteATokenSet,
		/* updateTokenSetData: TokenSet ändern */
		updateTokenSetData: tokensets.updateTokenSetData,
		/* updateTokenData: Token ändern */
		updateTokenData: function () {
			var aTPK = this.aTokenInfo['pk'];
			$('#aTokenInfo').modal('hide');
			this.aTokens[aTPK].t = this.aTokenInfo.t;
			this.aTokens[aTPK].tt = this.aTokenInfo.tt;
			this.aTokens[aTPK].o = this.aTokenInfo.o;
			this.aTokens[aTPK].le = this.aTokenInfo.le;
			this.aTokens[aTPK].to = this.aTokenInfo.to;
			if (this.aTokenInfo.aId) {
				this.aTokens[aTPK].aId = this.setAAntwort(parseInt(this.aTokenInfo.aId), {'it': aTPK, 'vi': this.aTokenInfo.i, 'tags': ((this.aTokenInfo.tags) ? JSON.parse(JSON.stringify(this.aTokenInfo.tags)) : undefined)});
				this.aAntworten[this.aTokens[aTPK].aId].saveme = true;
			}
			if (this.aTokenInfo.delAntwort && this.aTokenInfo.aId > 0) {
				this.delAntwort(this.aTokenInfo.aId);
			}
			this.aTokens[aTPK].saveme = true;
			this.unsaved = true;
			this.preRenderTEvent(this.getTEventOfAEvent(this.searchByKey(this.aTokenInfo.e, 'pk', this.aEvents)), true);
			this.updateZeilenTEvents();
			this.aTokenInfo = undefined;
			console.log('TokenSet ID ' + aTPK + ' geändert!');
		},
		/* updateToken */
		updateToken: function (key, values) {
			this.aTokens[key] = values;
			if (this.aTokens[key]['fo']) {
				this.updateTokenFragment(key, this.aTokens[key]['fo']);
			}
			if (this.aEvents[this.aTokens[key]['e']]) {
				this.setRerenderEvent(this.aTokens[key]['e']);
			}
		},
		/* updateTokenFragment */
		updateTokenFragment: function (key, fo) {
			if (this.aTokenFragmente[fo]) {
				if (this.aTokenFragmente[fo].indexOf(key) < 0) {
					this.aTokenFragmente[fo].push(key);
				}
			} else {
				this.aTokenFragmente[fo] = [key];
			}
		},
		/* addEvents: Events hinzufügen */
		addEvents: function (nEvents) {
			nEvents.forEach(function (val) {
				this.updateEvent(0, val);
			}, this);
		},
		/* updateEvent */
		updateEvent: function (index = 0, values) {
			if (index === 0) {
				Object.keys(values.tid).map(function (key) {
					values.tid[key].forEach(function (val) {
						this.aTokenReihung.push(val);
						if (!this.aTokenReihungInf[key]) { this.aTokenReihungInf[key] = []; }
						this.aTokenReihungInf[key].push(val);
					}, this);
				}, this);
				index = this.aEvents.push({}) - 1;
				this.aEvents[index] = values;
				this.setRerenderEvent(index);
			} else {
				index = parseInt(index);
				this.aEvents[index] = values;
				this.setRerenderEvent(index);
			}
			// tEvetns erstellen/updaten
			var newTEvent = true;
			Object.keys(this.tEvents).map(function (key) {
				if (this.tEvents[key]) {
					if (this.tEvents[key]['s'] === this.aEvents[index]['s'] && this.tEvents[key]['e'] === this.aEvents[index]['e']) {
						Object.keys(this.aEvents[index].tid).map(function (xKey, i) {
							this.tEvents[key]['eId'][xKey] = index;
							this.tEvents[key]['rerender'] = true;
						}, this);
						newTEvent = false;
					}
				}
			}, this);
			if (newTEvent) {
				var atEvent = {
					s: this.aEvents[index]['s'],
					e: this.aEvents[index]['e'],
					as: this.durationToSeconds(this.aEvents[index]['s']),
					ae: this.durationToSeconds(this.aEvents[index]['e']),
					al: 0,
					rerender: true,
					eId: {}
				};
				atEvent['al'] = atEvent['ae'] - atEvent['as'];
				Object.keys(this.aEvents[index].tid).map(function (key, i) {
					atEvent['eId'][key] = index;
				}, this);
				var tEvIndex = this.tEvents.push({}) - 1;
				this.tEvents[tEvIndex] = atEvent;
			}
		},
		/* setRerenderEvent */
		setRerenderEvent: function (key) {
			this.debouncedPrerenderEvents();
		},
		debouncedPrerenderEvents: _.debounce(function () {
			var t0 = performance.now();
			this.tEvents.forEach(function (val, key) {
				this.preRenderTEvent(key);
			}, this);
			this.debouncedSVGHeight();
			this.updateZeilenTEvents();
			var t1 = performance.now();
			console.log('debouncedPrerenderEvents: ' + Math.ceil(t1 - t0) + ' ms');
		}, 100),
		debouncedSVGHeight: _.debounce(function () {
			this.scrollRendering();
		}, 50),
		preRenderTEvent: svgfunctions.preRenderTEvent,
		sizeTEvent: svgfunctions.sizeTEvent,
		updateInfShow: function () {
			this.updateZeilenTEvents();
			this.debouncedSVGHeight();
		},
		/* updateZeilenTEvents */
		updateZeilenTEvents: svgfunctions.updateZeilenTEvents,
		uzteEndDataUpdate: svgfunctions.uzteEndDataUpdate,
		/* getTokenString */
		getTokenString: function (tId, field, bfield = false) {
			var aTxt = this.getTokenFragment(tId, field, bfield);
			var space = ((this.aTokens[tId]['tt'] === 2) || (this.aTokens[tId]['fo'] > 0 || aTxt[0] === '_') ? '' : '\u00A0');
			if (aTxt[0] === '_') {
				aTxt = aTxt.substr(1);
			};
			return space + aTxt;
		},
		/* getTokenFragment */
		getTokenFragment (tId, field, bfield = false) {
			var aTtxt = this.aTokens[tId][field];
			if (bfield && !aTtxt) {
				aTtxt = this.aTokens[tId][bfield];
			}
			if (this.aTokenFragmente[tId] && this.aTokenFragmente[tId].length === 1) {
				this.aTokenFragmente[tId].forEach(function (val) {
					var nTtxt = this.aTokens[val][field];
					if (bfield && !nTtxt) {
						nTtxt = this.aTokens[val][bfield];
					}
					var aPos = aTtxt.lastIndexOf(nTtxt);
					if (aPos > 0) {
						aTtxt = aTtxt.substr(0, aPos);
					}
				}, this);
				return aTtxt;
			}
			return aTtxt;
		},
		/* scrollRendering */
		scrollRendering: svgfunctions.scrollRendering,
		/* getMenue: Läd aktuelle Daten für das Menü */
		getMenue: loadingsaving.getMenue,
		/* Events */
		/* setAudioPos */
		setAudioPos: function (aPos) {
			this.audioPos = aPos;
		},
		setATokenInfo: function (aVal, aKey) {
			console.log('setATokenInfo', aKey, aVal);
			this.aTokenInfo[aKey] = aVal;
			this.$set(this.aTokenInfo, 'changed', true);
		},
		setATokenSetInfo: function (aVal, aKey) {
			console.log('setATokenSetInfo', aKey, aVal);
			this.aTokenSetInfo[aKey] = aVal;
			this.$set(this.aTokenSetInfo, 'changed', true);
		},
		setAudioDuration: function (aPos) {
			this.audioDuration = aPos;
		},
		ctrlKey: function () {
			this.ctrlKS = true;
		},
		/* showTEventInfos */
		showTEventInfos: function (event, tId) {
			if (event.ctrlKey) {
				var rect = event.target.getBoundingClientRect();
				console.log(this.$refs.audioplayer);
				this.$refs.audioplayer.setAudioPosBySec(this.tEvents[tId].as + ((this.tEvents[tId].ae - this.tEvents[tId].as) / rect.width * (event.clientX - rect.left)));
				this.ctrlKS = true;
			} else {
				this.tEventInfo = tId;
				setTimeout(function () { $('#tEventInfo').modal('show'); }, 20);
			}
		},
		/* showaInfInfos */
		showaInfInfos: function (iId) {
			this.aInfInfo = iId;
			setTimeout(function () { $('#aInformantenInfo').modal('show'); }, 20);
		},
		/* showaTokenSetInfos */
		showaTokenSetInfos: tokensets.showaTokenSetInfos,
		/* showaTokenInfos */
		showaTokenInfos: function (eTok, direkt = false, e = undefined) {
			if (direkt || (this.selToken === eTok && (!e || (!e.ctrlKey && !e.shiftKey)))) {
				// console.log('Token auswählen', eTok, direkt, e);
				this.aTokens[eTok]['viewed'] = true;
				this.svgTokenLastView = eTok;
				this.aTokenInfo = JSON.parse(JSON.stringify(this.aTokens[eTok]));
				if (this.aTokenInfo.aId && this.aAntworten[this.aTokenInfo.aId].tags) {
					this.aTokenInfo.tags = JSON.parse(JSON.stringify(this.aAntworten[this.aTokenInfo.aId].tags));
				}
				this.aTokenInfo['pk'] = eTok;
				this.aTokenInfo['e-txt'] = this.aEvents[this.searchByKey(this.aTokens[eTok]['e'], 'pk', this.aEvents)]['s'];
				let aVToken = eTok;
				let aBToken = eTok;
				let aVTokenOrg;
				let aBTokenOrg;
				if (aVToken) {
					this.aTokenInfo['satzView'] = [];
					if (!aBToken) { aBToken = aVToken; };
					aVTokenOrg = aVToken;
					aBTokenOrg = aBToken;
					// this.aTokenInfo['satzView'].push({text: aVToken + ' - ' + aBToken, class: 'test'});
					// Satzanfang und -ende ermitteln
					if (this.aTokens[aVToken].s) {
						let aTokPos = this.aTokenReihungInf[this.aTokens[aVToken].i].indexOf(aVToken);
						if (aTokPos > -1) {
							while (aTokPos > 0 && this.aTokens[this.aTokenReihungInf[this.aTokens[aVToken].i][aTokPos]] && this.aTokens[this.aTokenReihungInf[this.aTokens[aVToken].i][aTokPos]].s === this.aTokens[aVToken].s) {
								aTokPos -= 1;
							}
							if (this.aTokens[this.aTokenReihungInf[this.aTokens[aVToken].i][aTokPos + 1]]) {
								aVToken = this.aTokenReihungInf[this.aTokens[aVToken].i][aTokPos + 1];
							}
						}
					}
					if (this.aTokens[aBToken].s) {
						let aTokPos = this.aTokenReihungInf[this.aTokens[aBToken].i].indexOf(aBToken);
						if (aTokPos > -1) {
							while (aTokPos < this.aTokenReihungInf[this.aTokens[aBToken].i].length && this.aTokens[this.aTokenReihungInf[this.aTokens[aBToken].i][aTokPos]] && this.aTokens[this.aTokenReihungInf[this.aTokens[aBToken].i][aTokPos]].s === this.aTokens[aBToken].s) {
								aTokPos += 1;
							}
							if (this.aTokens[this.aTokenReihungInf[this.aTokens[aBToken].i][aTokPos - 1]]) {
								aBToken = this.aTokenReihungInf[this.aTokens[aBToken].i][aTokPos - 1];
							}
						}
					}
					// this.aTokenInfo['satzView'].push({text: aVToken + ' - ' + aBToken, class: 'test'});
					let aTokPosV = this.aTokenReihungInf[this.aTokens[aVToken].i].indexOf(aVToken);
					if (aTokPosV > -1) {
						aTokPosV -= 10;
						if (aTokPosV < 0) { aTokPosV = 0; };
						if (this.aTokens[this.aTokenReihungInf[this.aTokens[aVToken].i][aTokPosV]]) {
							aVToken = this.aTokenReihungInf[this.aTokens[aVToken].i][aTokPosV];
						}
					}
					let aTokPosB = this.aTokenReihungInf[this.aTokens[aBToken].i].indexOf(aBToken);
					if (aTokPosB > -1) {
						aTokPosB += 10;
						if (aTokPosB > this.aTokenReihungInf[this.aTokens[aBToken].i].length - 1) { aTokPosB = this.aTokenReihungInf[this.aTokens[aBToken].i].length - 1; };
						if (this.aTokens[this.aTokenReihungInf[this.aTokens[aVToken].i][aTokPosB]]) {
							aBToken = this.aTokenReihungInf[this.aTokens[aVToken].i][aTokPosB];
						}
					}
					// this.aTokenInfo['satzView'].push({text: aVToken + ' - ' + aBToken, class: 'test'});
					if (aVTokenOrg !== aVToken) {
						let aTokPos = this.aTokenReihungInf[this.aTokens[aVTokenOrg].i].indexOf(aVToken);
						let aText = '';
						let aOrtho = '';
						while (aTokPos < this.aTokenReihungInf[this.aTokens[aVTokenOrg].i].length && this.aTokenReihungInf[this.aTokens[aBToken].i][aTokPos] !== aVTokenOrg) {
							let aTok = this.aTokens[this.aTokenReihungInf[this.aTokens[aBToken].i][aTokPos]];
							aText += ' ' + aTok.t;
							aOrtho += ' ' + aTok.o || aTok.t;
							aTokPos += 1;
						}
						this.aTokenInfo['satzView'].push({text: aText, ortho: aOrtho, class: 'before'});
					}
					if (aVTokenOrg && aBTokenOrg) {
						let aTokPos = this.aTokenReihungInf[this.aTokens[aVTokenOrg].i].indexOf(aVTokenOrg);
						let aText = '';
						let aOrtho = '';
						while (aTokPos < this.aTokenReihungInf[this.aTokens[aVTokenOrg].i].length && this.aTokenReihungInf[this.aTokens[aVTokenOrg].i][aTokPos] !== aBTokenOrg) {
							let aTok = this.aTokens[this.aTokenReihungInf[this.aTokens[aVTokenOrg].i][aTokPos]];
							aText += ' ' + aTok.t;
							aOrtho += ' ' + aTok.o || aTok.t;
							aTokPos += 1;
						}
						if (this.aTokenReihungInf[this.aTokens[aVTokenOrg].i][aTokPos] === aBTokenOrg) {
							let aTok = this.aTokens[this.aTokenReihungInf[this.aTokens[aVTokenOrg].i][aTokPos]];
							aText += ' ' + aTok.t;
							aOrtho += ' ' + aTok.o || aTok.t;
						}
						this.aTokenInfo['satzView'].push({text: aText, ortho: aOrtho, class: 'active'});
					}
					console.log(aVToken + ' - ' + aBToken);
				}
				if (aBTokenOrg !== aBToken) {
					let aTokPos = this.aTokenReihungInf[this.aTokens[aBTokenOrg].i].indexOf(aBTokenOrg) + 1;
					let aText = '';
					let aOrtho = '';
					while (aTokPos < this.aTokenReihungInf[this.aTokens[aBTokenOrg].i].length && this.aTokenReihungInf[this.aTokens[aBToken].i][aTokPos] !== aBToken) {
						let aTok = this.aTokens[this.aTokenReihungInf[this.aTokens[aBTokenOrg].i][aTokPos]];
						aText += ' ' + aTok.t;
						aOrtho += ' ' + aTok.o || aTok.t;
						aTokPos += 1;
					}
					if (this.aTokenReihungInf[this.aTokens[aBTokenOrg].i][aTokPos] === aBToken) {
						let aTok = this.aTokens[this.aTokenReihungInf[this.aTokens[aBTokenOrg].i][aTokPos]];
						aText += ' ' + aTok.t;
						aOrtho += ' ' + aTok.o || aTok.t;
					}
					this.aTokenInfo['satzView'].push({text: aText, ortho: aOrtho, class: 'after'});
				}
				// this.aTokenInfo['satzView'] = [{text: 'test', ortho: 'test Ortho', class: 'test'}];
				setTimeout(function () { $('#aTokenInfo').modal('show'); }, 20);
			} else if (e) {
				if (e.shiftKey) {
					if (this.selTokenBereich.v === -1) {
						this.selTokenBereich.v = this.selToken;
						if (eTok !== this.selToken) {
							this.selTokenBereich.b = eTok;
						}
					} else {
						this.selTokenBereich.b = eTok;
					}
				} else if (e.ctrlKey) {
					if (this.selTokenBereich.v > -1 && this.selTokenBereich.b > -1 && this.selTokenListe.length === 0) {
						(this.svgSelTokenList.slice()).forEach(function (val) {
							this.updateSelTokenListe(val);
						}, this);
					} else if (this.selTokenListe.length === 0) {
						this.updateSelTokenListe(this.selToken);
					}
					this.updateSelTokenListe(eTok);
					this.ctrlKS = true;
					this.selTokenBereich = {'v': -1, 'b': -1};
				} else {
					this.selTokenBereich = {'v': -1, 'b': -1};
					this.selTokenListe = [];
					this.svgSelTokenList = [];
				}
			}
			this.selToken = eTok;
		},
		/* aTokenTextInf erstellen/updaten */
		updateATokenTextInf: function () {
			this.aTokenTextInf = null;
			if (this.aTokenReihungInf) {
				var t0 = performance.now();
				this.aTokenTextInf = {};
				Object.keys(this.aTokenReihungInf).forEach(function (aInfKey) {
					if (!this.aTokenTextInf[aInfKey]) {
						this.aTokenTextInf[aInfKey] = {'text': '', 'ortho': '', 'text_in_ortho': '', 'tokens': {}};
					}
					this.aTokenReihungInf[aInfKey].forEach(function (aTokenId) {
						[{'prop': 'text', 'o1': 't', 'o2': false}, {'prop': 'ortho', 'o1': 'o', 'o2': 't'}, {'prop': 'text_in_ortho', 'o1': 'to', 'o2': false}].forEach(function (aField) {
							let vPos = this.aTokenTextInf[aInfKey][aField.prop].length;
							let aTxt = this.getTokenString(aTokenId, aField.o1, aField.o2).replace(String.fromCharCode(160), ' ');
							let bPos = vPos + aTxt.length - 1;
							this.aTokenTextInf[aInfKey][aField.prop] += aTxt;
							if (!this.aTokenTextInf[aInfKey].tokens[aTokenId]) {
								this.aTokenTextInf[aInfKey].tokens[aTokenId] = {};
							}
							this.aTokenTextInf[aInfKey].tokens[aTokenId][aField.prop] = {'v': vPos, 'b': bPos};
						}, this);
					}, this);
				}, this);
				console.log('updateATokenTextInf: ' + Math.ceil(performance.now() - t0) + ' ms');
			}
			console.log(this.aTokenTextInf);
		},
		modalSperren: function (modalID) {
			$(modalID).off('keyup.dismiss.bs.modal');
			$(modalID).off('keydown.dismiss.bs.modal');
			$(modalID).data('bs.modal').options.backdrop = 'static';
			$(modalID + ' button.close').hide();
		},
		/* Funktion zur ermittlung der Breite von Buchstaben im SVG-Element */
		getCharWidth: svgfunctions.getCharWidth,
		/* Funktion zur ermittlung der Breite von Texten im SVG-Element */
		getTextWidth: svgfunctions.getTextWidth,
		/* Sonsitge Funktionen: */
		objectKeyFilter: stdfunctions.objectKeyFilter,
		objectSubValueFilter: stdfunctions.objectSubValueFilter,
		searchByKey: stdfunctions.searchByKey,
		getFirstObjectOfValueInPropertyOfArray: stdfunctions.getFirstObjectOfValueInPropertyOfArray,
		/* Zeit umrechnen */
		durationToSeconds: stdfunctions.durationToSeconds,
		secondsToDuration: stdfunctions.secondsToDuration,
		/* Events */
		/* Fenstergröße */
		resizeWindow: function () {
			this.mWidth = $('#annotationsvg').width();
			this.sHeight = $('#svgscroller').height();
		},
		/* Tastatur */
		focusCatchKeyUp: function (e) {
			if (e.keyCode === 39) { // rechts
				e.preventDefault();
				if (e.shiftKey && this.selTokenBereich.v === -1) {
					this.selTokenBereich.v = this.selToken;
				}
				if (e.ctrlKey && !this.ctrlKS) {
					this.updateSelTokenListe(this.selToken);
				}
				this.selectNextToken();
				if (e.shiftKey) {
					this.selTokenBereich.b = this.selToken;
				} else {
					this.selTokenBereich = {'v': -1, 'b': -1};
				}
				if (e.ctrlKey) {
					this.updateSelTokenListe(this.selToken);
					this.ctrlKS = true;
				}
			} else if (e.keyCode === 37) { // links
				e.preventDefault();
				if (e.shiftKey && this.selTokenBereich.v === -1) {
					this.selTokenBereich.v = this.selToken;
				}
				if (e.ctrlKey && !this.ctrlKS) {
					this.updateSelTokenListe(this.selToken);
				}
				this.selectPrevToken();
				if (e.shiftKey) {
					this.selTokenBereich.b = this.selToken;
				} else {
					this.selTokenBereich = {'v': -1, 'b': -1};
				}
				if (e.ctrlKey) {
					this.updateSelTokenListe(this.selToken);
					this.ctrlKS = true;
				}
			} else if (e.keyCode === 40) { // unten
				e.preventDefault();
				this.selTokenBereich = {'v': -1, 'b': -1};
				this.selectNextInf();
			} else if (e.keyCode === 38) { // oben
				e.preventDefault();
				this.selTokenBereich = {'v': -1, 'b': -1};
				this.selectPrevInf();
			} else if (e.ctrlKey && e.keyCode === 13) { // Enter
				if (this.selTokenSet !== 0) {
					this.showaTokenSetInfos(this.selTokenSet, true);
				}
				this.ctrlKS = true;
			} else if (e.keyCode === 13) { // Enter
				e.preventDefault();
				if (this.selToken > -1) {
					this.showaTokenInfos(this.selToken, true);
				}
			} else if (e.keyCode === 17) { // Strg
				if (!this.ctrlKS) {
					this.updateSelTokenListe(this.selToken);
				}
				this.ctrlKS = false;
			} else {
				console.log('focusCatchKeyUp: ' + e.keyCode);
			}
			e.target.value = '';
		},
		focusCatchKeyDown: function (e) {
			if (e.ctrlKey && e.keyCode === 70) { // Strg + F
				e.preventDefault();
				this.focusSuchText();
				this.showSuche = true;
			} else if (e.keyCode === 114) { // F3
				e.preventDefault();
				this.naechsterSuchToken(!e.shiftKey);
			} else if (e.ctrlKey && e.keyCode === 68) { // Strg + D
				e.preventDefault();
				this.ctrlKS = true;
				this.selTokenBereich = {'v': -1, 'b': -1};
				this.selTokenListe = [];
				this.svgSelTokenList = [];
			} else if (e.ctrlKey && e.keyCode === 65) { // Strg + A
				this.ctrlKS = true;
				if (this.selToken) {
					if (this.aTokens[this.selToken].tokenSets && this.aTokens[this.selToken].tokenSets.length > 0) {
						if (!e.shiftKey) {
							if (this.aTokens[this.selToken].tokenSets.indexOf(this.selTokenSet) < this.aTokens[this.selToken].tokenSets.length - 1) {
								this.selTokenSet = this.aTokens[this.selToken].tokenSets[this.aTokens[this.selToken].tokenSets.indexOf(this.selTokenSet) + 1];
							} else {
								this.selTokenSet = this.aTokens[this.selToken].tokenSets[0];
							}
						} else {
							if (this.aTokens[this.selToken].tokenSets.indexOf(this.selTokenSet) > 0) {
								this.selTokenSet = this.aTokens[this.selToken].tokenSets[this.aTokens[this.selToken].tokenSets.indexOf(this.selTokenSet) - 1];
							} else {
								this.selTokenSet = this.aTokens[this.selToken].tokenSets[this.aTokens[this.selToken].tokenSets.length - 1];
							}
						}
					}
				}
			} else if (e.ctrlKey && e.keyCode === 81) { // Strg + Q
				this.ctrlKS = true;
				this.selTokenSet = 0;
			}
		},
		sucheCatchKeyUp: searchfilter.sucheCatchKeyUp,
		sucheCatchKeyDown: searchfilter.sucheCatchKeyDown,
		focusFocusCatch: function () {
			$('#focuscatch').focus();
		},
		focusSuchText: function () {
			$('#suchtext').focus();
		},
		/* Nächstes Token auswählen */
		selectNextToken: function () {
			this.selToken = this.tokenNextPrev(this.selToken);
		},
		/* Vorherigen Token auswählen */
		selectPrevToken: function () {
			this.selToken = this.tokenNextPrev(this.selToken, false);
		},
		/* Nächsten Informanten/Zeile auswählen */
		selectNextInf: function () {
			this.infNextPrev();
		},
		/* Vorherigen Informanten/Zeile auswählen */
		selectPrevInf: function () {
			this.infNextPrev(false);
		},
		infNextPrev: function (next = true) {
			if (this.tEvents[0]) {
				var aTId = this.selToken;
				if (aTId < 0) {
					this.selToken = this.tokenNextPrev(-1, next);
				} else {
					var aIId = this.aTokens[aTId]['i'];
					var aZAEKey = this.getTEventOfAEvent(this.searchByKey(this.aTokens[aTId]['e'], 'pk', this.aEvents));
					var aZAE = this.tEvents[aZAEKey];
					var aZTE = this.zeilenTEvents[this.getZeileOfTEvent(aZAEKey)];
					var aInfAv = Object.keys(this.objectKeyFilter(this.aInformanten, aZTE['iId']));
					var nTokSel = -1;
					if (String(aInfAv[((next) ? aInfAv.length - 1 : 0)]) !== String(aIId)) {
						var nIId = this.wertNachWert(Object.keys(aZAE['eId']), String(aIId), next);
						if (nIId === undefined) {
							nIId = this.wertNachWert(Object.keys(this.aInformanten), String(aIId), next);
							var aTEvents = this.listeNachWert(aZTE['eId'], aZAEKey, next);
							aTEvents.some(function (tEKey, tI) {
								if (this.tEvents[tEKey]['eId'][nIId]) {
									var tmpAE = this.aEvents[this.tEvents[tEKey]['eId'][nIId]]['tid'][nIId];
									nTokSel = tmpAE[((next) ? 0 : tmpAE.length - 1)];
									return true;
								}
							}, this);
						} else {
							nTokSel = this.aEvents[aZAE['eId'][nIId]]['tid'][nIId][0];
						}
					}
					if (nTokSel < 0) {
						var tmpZTE = this.zeilenTEvents[this.getZeileOfTEvent(aZAEKey) + ((next) ? 1 : -1)];
						if (tmpZTE) {
							var tmpZTEeId = tmpZTE['eId'];
							var tmpTEeId = this.tEvents[tmpZTEeId[((next) ? 0 : tmpZTEeId.length - 1)]]['eId'];
							if (next) {
								var tmpAEtid = this.aEvents[tmpTEeId[Object.keys(tmpTEeId)[0]]]['tid'];
								nTokSel = tmpAEtid[Object.keys(tmpAEtid)[0]][0];
							} else {
								var tmpTEeIdK = Object.keys(tmpTEeId);
								var tmpAEtidR = this.aEvents[tmpTEeId[tmpTEeIdK[tmpTEeIdK.length - 1]]]['tid'];
								var tmpAEtidK = Object.keys(tmpAEtidR);
								var tmpAEtidS = tmpAEtidR[tmpAEtidK[tmpAEtidK.length - 1]];
								nTokSel = tmpAEtidS[tmpAEtidS.length - 1];
							}
						}
					}
					if (nTokSel < 0) {
						nTokSel = this.tokenNextPrev(-1, next);
					}
					this.selToken = nTokSel;
				}
			}
		},
		/* Nächster/Vorheriger Token (next = true next else prev) */
		tokenNextPrev: function (aTId, next = true) {
			var nTId = -1;
			if (this.tEvents[0]) {
				if (aTId < 0) {	// Erster/Letzer Token
					return ((next) ? this.aTokenReihung[0] : this.aTokenReihung[this.aTokenReihung.length - 1]);
				} else {	// Nächster/Vorheriger Token
					var aIId = this.aTokens[aTId]['i'];
					var aTRI = this.aTokenReihungInf[aIId];
					var aTRIiO = aTRI.indexOf(aTId);
					return ((next)
												? ((aTRIiO < aTRI.length - 1) ? aTRI[aTRIiO + 1] : this.tokenNextPrev(-1, next))
												: ((aTRIiO > 0) ? aTRI[aTRIiO - 1] : this.tokenNextPrev(-1, next)));
				}
			}
			return nTId;
		},
		/* Zu Token scrollen */
		scrollToToken: svgfunctions.scrollToToken,
		/* Funktionen für Tokenauswahl */
		getTEventOfAEvent: function (aEId) {
			var nKey = -1;
			this.tEvents.some(function (val, key) {
				Object.keys(val['eId']).some(function (xKey, i) {
					if (val['eId'][xKey] === aEId) {
						nKey = key;
						return true;
					}
				}, this);
				return (nKey > -1);
			}, this);
			return nKey;
		},
		getZeileOfTEvent: function (aTEId) {
			var nKey = -1;
			this.zeilenTEvents.some(function (val, key) {
				if (val['eId'].indexOf(aTEId) > -1) {
					nKey = key;
					return true;
				}
			}, this);
			return nKey;
		},
		/* Suchen: */
		suche: searchfilter.suche,
		naechsterSuchToken: searchfilter.naechsterSuchToken,
		/* Wandelt aktuelle Auswahl in Token Set um */
		selToTokenSet: tokensets.selToTokenSet,
		/* TokenSet Bereich neu setzen */
		setATokenSetBereich: tokensets.setATokenSetBereich,
		/* TokenSet Liste Token hinzufügen/entfernen */
		toggleATokenSetListe: tokensets.toggleATokenSetListe,
		updateATokenSets: tokensets.updateATokenSets,
		checkSelTokenBereich: tokensets.checkSelTokenBereich,
		updateSelTokenListe: tokensets.updateSelTokenListe,
		reRenderSelToken: tokensets.reRenderSelToken,
		sucheZuAuswahlListe: searchfilter.sucheZuAuswahlListe,
		/* Properties von Objekt filtern */
		filterProperties: stdfunctions.filterProperties,
		listeNachWert: stdfunctions.listeNachWert,
		wertNachWert: stdfunctions.wertNachWert,
		listeNachWertLoop: stdfunctions.listeNachWertLoop,
		/* Sortiert und Filtert vorgegebene Liste mit Event IDs chronologisch nach aTokenReihung. */
		sortEventIdListe: function (aEListe) {
			var nEListe = [];
			this.aTokenReihung.forEach(function (val) {
				if (aEListe.indexOf(val) >= 0) {
					nEListe.push(val);
				}
			}, this);
			return nEListe;
		},
		listeWerteInListe: stdfunctions.listeWerteInListe,
		tokenCountByInf: function (aTRI) {
			var output = '';
			Object.keys(this.aInformanten).map(function (iKey, iI) {
				output += this.aInformanten[iKey].k + ': ' + ((aTRI[iKey]) ? aTRI[iKey].length.toLocaleString() : '0') + '\n';
			}, this);
			return output;
		},
		sortTokenSets: tokensets.sortTokenSets,
		aTokenInfoChange: function (nVal, oVal) {
			if (this.aTokenInfo && oVal !== undefined) { this.$set(this.aTokenInfo, 'changed', true); };
		},
		hasSubProp: stdfunctions.hasSubProp,
		getValOfSubProp: stdfunctions.getValOfSubProp
	},
	mounted: function () {
		document.getElementById('svgscroller').addEventListener('scroll', this.scrollRendering);
		window.addEventListener('resize', this.resizeWindow);
		this.resizeWindow();
		this.getMenue();
		tagsystemCache.getBase();
		/* Wenn Modal angezeigt wird */
		$(document).on('shown.bs.modal', '.modal', function (e) {
			if ($(this).data('focus')) {
				$($(this).data('focus')).focus();
			}
		});
		/* Wenn Modal ausgeblendet wurde */
		$(document).on('hidden.bs.modal', '.modal', function (e) {
			if ($(this).data('unset')) {
				annotationsTool[$(this).data('unset')] = undefined;
			}
			annotationsTool.focusFocusCatch();
		});
	},
	created: function () {
		this.debouncedSuche = _.debounce(this.suche, 500);
		this.debouncedUpdateInfShow = _.debounce(this.updateInfShow, 100);
		this.debouncedUpdateATokenSets = _.debounce(this.updateATokenSets, 100);
		this.debouncedupdateZeilenTEvents = _.debounce(this.updateZeilenTEvents, 50);
	},
	beforeDestroy: function () {
		document.getElementById('svgscroller').removeEventListener('scroll', this.scrollRendering);
		window.removeEventListener('resize', this.resizeWindow);
	}
});
