/* global $ alert confirm */

const loadingsaving = {
	reset: function () {
		this.unsaved = false;
		this.loading = true;
		this.aInfInfo = undefined;
		this.tEventInfo = undefined;
		this.aTokenInfo = undefined;
		this.aTokenSetInfo = undefined;
		this.annotationsTool = {
			aPK: 0,
			nNr: 0,
			loaded: true
		};
		this.aTranskript = {};
		this.aEinzelErhebung = {};
		this.aTokenTypes = {};
		this.aInformanten = {};
		this.aInfLen = 0;
		this.aSaetze = {};
		this.aEvents = [];
		this.tEvents = [];
		this.aTokens = {};
		this.aTokenReihung = [];
		this.aTokenReihungInf = {};
		this.aTokenTextInf = null;
		this.aTokenFragmente = {};
		this.aTokenSets = {};
		this.aAntworten = {};
		this.zeilenTEvents = [];
		this.zeilenHeight = 0;
		this.renderZeilen = [];
		this.svgTTS = document.getElementById('svg-text-textsize');
		this.svgTokenLastView = -1;
		this.selToken = -1;
		this.selTokenSet = 0;
		this.selTokenBereich = {'v': -1, 'b': -1};
		this.selTokenListe = [];
		this.audioPos = 0;
		this.audioDuration = 0;
		this.showSuche = false;
		this.showFilter = false;
		return true;
	},

	/* getTranskript: Läd aktuelle Daten des Transkripts für das Annotations Tool */
	getTranskript: function (aPK, aType = 'start', aNr = 0) {
		if (aType !== 'start' || (!this.unsaved || confirm('Ungespeicherte Daten! Wirklich verwerfen?'))) {
			console.log('Lade Datensatz ' + aNr + '/' + this.aTmNr + ' von Transkript pk: ' + aPK + ' ...');
			if (aType === 'start') {
				$(':focus').blur();
				$('#annotationsvg').focus();
				this.reset();
				this.annotationsTool = {
					aPK: aPK,
					nNr: 0,
					loaded: false
				};
			}
			this.$http.post('',
				{
					getTranskript: aPK,
					aType: aType,
					aNr: aNr
				})
			.then((response) => {
				if (aPK === this.annotationsTool.aPK) {
					if (aType === 'start') {
						this.aTmNr = response.data['aTmNr'];
						this.aTranskript = response.data['aTranskript'];
						this.aEinzelErhebung = response.data['aEinzelErhebung'];
						this.aTokenTypes = response.data['aTokenTypes'];
						this.setInformanten(response.data['aInformanten']);
						this.aSaetze = response.data['aSaetze'];
						this.focusFocusCatch();
						setTimeout(this.selectNextToken, 200);
					}
					this.addTokens(response.data['aTokens']);
					this.addEvents(response.data['aEvents']);
					this.addTokenSets(response.data['aTokenSets']);
					this.addAntworten(response.data['aAntworten']);
					this.loading = false;
					if (this.annotationsTool.nNr === response.data['nNr']) {
						this.$set(this.annotationsTool, 'nNr', response.data['nNr']);
						this.annotationsTool.loaded = true;
						console.log('Alle Datensätze geladen.');
					} else if (this.annotationsTool.loaded === false) {
						this.$set(this.annotationsTool, 'nNr', response.data['nNr']);
						this.getTranskript(this.annotationsTool.aPK, 'next', this.annotationsTool.nNr);
					}
					this.aTokenTextInf = null;
				}
			})
			.catch((err) => {
				console.log(err);
				this.annotationsTool = {
					aPK: 0,
					nNr: 0,
					loaded: false
				};
				alert('Fehler!');
				this.loading = false;
			});
		}
	},

	/* Änderungen speichern */
	speichern: function () {
		console.log('Änderungen speichern');
		var sOK = true;
		var sData = {};
		/* Token für speichern auslesen */
		var sATokens = {};
		Object.keys(this.aTokens).map(function (key, i) {
			if (this.aTokens[key].saveme) {
				sATokens[key] = this.filterProperties(this.aTokens[key], ['a', 't', 'tt', 'tr', 'e', 'to', 'i', 'o', 's', 'sr', 'fo', 'le']);
			}
		}, this);
		if (Object.keys(sATokens).length > 0) {
			sData.aTokens = sATokens;
		}
		/* Token Sets für speichern auslesen */
		var sATokenSets = {};
		Object.keys(this.aTokenSets).map(function (key, i) {
			if (this.aTokenSets[key].saveme) {
				sATokenSets[key] = this.filterProperties(this.aTokenSets[key], ['a', 'ivt', 'ibt', 't']);
			}
		}, this);
		if (Object.keys(sATokenSets).length > 0) {
			sData.aTokenSets = sATokenSets;
		}
		if (Object.keys(this.delTokenSets).length > 0) {
			sData.dTokenSets = this.delTokenSets;
		}
		/* Antworten für speichern auslesen */
		var sAAntworten = {};
		Object.keys(this.aAntworten).map(function (key, i) {
			if (this.aAntworten[key].saveme) {
				sAAntworten[key] = this.filterProperties(this.aAntworten[key], ['vi', 'inat', 'is', 'ibfl', 'it', 'its', 'bds', 'sa', 'ea', 'k']);
				if (this.aAntworten[key].tags) {
					sAAntworten[key].tags = getFlatTags(this.aAntworten[key].tags);
				}
			}
		}, this);
		if (Object.keys(sAAntworten).length > 0) {
			sData.aAntworten = sAAntworten;
		}
		if (Object.keys(this.delAntworten).length > 0) {
			sData.dAntworten = this.delAntworten;
		}
		console.log(sData);
		if (sOK) {
			this.loading = true;
			this.$http.post('',
				{
					speichern: JSON.stringify(sData)
				})
			.then((response) => {
				if (response.data['OK']) {
					console.log(response.data);
					if (response.data['gespeichert']) {
						/* Tokens */
						if (response.data['gespeichert']['aTokens']) {
							Object.keys(response.data['gespeichert']['aTokens']).map(function (key, i) {
								var nToken = response.data['gespeichert']['aTokens'][key];
								if (this.aTokens[key]) {
									delete this.aTokens[key];
								}
								var aKey = ((nToken.nId) ? nToken.nId : key);
								if (nToken.nId) { delete nToken.nId; };
								this.updateToken(aKey, nToken);
								this.preRenderTEvent(this.getTEventOfAEvent(this.searchByKey(nToken.e, 'pk', this.aEvents)), true);
							}, this);
						}
						/* Token Sets */
						if (response.data['gespeichert']['aTokenSets']) {
							Object.keys(response.data['gespeichert']['aTokenSets']).map(function (key, i) {
								var nTokenSet = response.data['gespeichert']['aTokenSets'][key];
								if (this.aTokenSets[key]) {
									delete this.aTokenSets[key];
								}
								var aKey = ((nTokenSet.nId) ? nTokenSet.nId : key);
								this.aTokenSets[aKey] = {};
								this.aTokenSets[aKey].a = nTokenSet.a;
								if (nTokenSet.ivt) { this.aTokenSets[aKey].ivt = nTokenSet.ivt; };
								if (nTokenSet.ibt) { this.aTokenSets[aKey].ibt = nTokenSet.ibt; };
								if (nTokenSet.t) { this.aTokenSets[aKey].t = nTokenSet.t; };
							}, this);
						}
						if (response.data['gespeichert']['dTokenSets']) {
							Object.keys(response.data['gespeichert']['dTokenSets']).map(function (key, i) {
								if (this.aTokenSets[key]) {
									delete this.aTokenSets[key];
								}
								if (this.delTokenSets[key]) {
									delete this.delTokenSets[key];
								}
							}, this);
						}
						/* Antworten */
						if (response.data['gespeichert']['aAntworten']) {
							Object.keys(response.data['gespeichert']['aAntworten']).map(function (key, i) {
								var nAntwort = response.data['gespeichert']['aAntworten'][key];
								if (this.aAntworten[key]) {
									if (this.aAntworten[key]['its'] && this.aTokenSets[this.aAntworten[key]['its']]) {
										delete this.aTokenSets[this.aAntworten[key]['its']].aId;
									}
									if (this.aAntworten[key]['it'] && this.aTokens[this.aAntworten[key]['it']]) {
										delete this.aTokens[this.aAntworten[key]['it']].aId;
									}
									delete this.aAntworten[key];
								}
								var aKey = ((nAntwort.nId) ? nAntwort.nId : key);
								if (nAntwort.nId) {
									delete nAntwort.nId;
								}
								if (nAntwort.pt) {
									nAntwort.tags = [];
									nAntwort.pt.forEach(function (val) {
										nAntwort.tags.push({'e': val.e, 'tags': this.processTags(val.t).tags});
									}, this);
									delete nAntwort.pt;
								}
								this.setAAntwort(aKey, nAntwort);
							}, this);
						}
						if (response.data['gespeichert']['dAntworten']) {
							Object.keys(response.data['gespeichert']['dAntworten']).map(function (key, i) {
								if (this.aAntworten[key]) {
									delete this.aAntworten[key];
								}
								if (this.delAntworten[key]) {
									delete this.delAntworten[key];
								}
							}, this);
						}
						this.updateATokenSets();
						this.updateZeilenTEvents();
						this.focusFocusCatch();
						this.unsaved = false;
					}
				} else {
					alert('Fehler!');
					console.log(response);
				}
				this.loading = false;
			})
			.catch((err) => {
				console.log(err);
				alert('Fehler!');
				this.loading = false;
			});
		}
	},

	/* getMenue: Läd aktuelle Daten für das Menü */
	getMenue: function () {
		this.loading = true;
		this.$http.post('',
			{
				getMenue: 1,
				ainformant: this.menue.aInformant
			})
		.then((response) => {
			this.menue = {
				informantenMitTranskripte: response.data['informantenMitTranskripte'],
				aInformant: response.data['aInformant'],
				aTranskripte: response.data['aTranskripte']
			};
			this.loading = false;
		})
		.catch((err) => {
			console.log(err);
			alert('Fehler!');
			this.loading = false;
		});
	}
};

function getFlatTags (aTags) {
	var fTags = [];
	aTags.forEach(function (val) {
		fTags.push({'e': val.e, 't': getFlatTagsX(val.tags)});
	});
	return fTags;
}
function getFlatTagsX (aTags) {
	var fTags = [];
	aTags.forEach(function (val) {
		var aTag = {'i': val.id, 't': val.tag};
		fTags.push(aTag);
		if (val.tags) {
			getFlatTagsX(val.tags).forEach(function (sval) {
				fTags.push(sval);
			});
		}
	});
	return fTags;
}
