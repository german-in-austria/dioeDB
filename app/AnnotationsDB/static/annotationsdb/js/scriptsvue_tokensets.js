/* global _ $ confirm alert */

const tokensets = {
	/* addTokenSets: TokenSets hinzufügen */
	addTokenSets: function (nTokenSets) {
		Object.keys(nTokenSets).map(function (key, i) {
			this.aTokenSets[key] = nTokenSets[key];
		}, this);
		this.debouncedUpdateATokenSets();
	},

	/* deleteATokenSet: TokenSet löschen */
	deleteATokenSet: function (delTokenSetID, direkt = false, aDirekt = false) {
		if (direkt || confirm('Soll das TokenSet ID ' + delTokenSetID + ' gelöscht werden?')) {
			$('#aTokenSetInfo').modal('hide');
			if (this.aTokenSets[delTokenSetID].aId && ((aDirekt) || confirm('Soll die dazugehörige Antwort auch gelöscht werden?'))) {
				this.setAAntwort(this.aTokenSets[delTokenSetID].aId);
			}
			this.delTokenSets[delTokenSetID] = this.aTokenSets[delTokenSetID];
			delete this.aTokenSets[delTokenSetID];
			this.unsaved = true;
			this.aTokenSetInfo = undefined;
			this.selTokenSet = 0;
			this.updateATokenSets();
			this.focusFocusCatch();
			console.log('TokenSet ID ' + delTokenSetID + ' gelöscht!');
		}
	},

	/* updateTokenSetData: TokenSet ändern */
	updateTokenSetData: function () {
		var aTSPK = this.aTokenSetInfo['pk'];
		$('#aTokenSetInfo').modal('hide');
		if (this.aTokenSetInfo.aId) {
			this.aTokenSets[aTSPK].aId = this.setAAntwort(parseInt(this.aTokenSetInfo.aId), {'its': aTSPK, 'vi': this.aTokens[(this.aTokenSetInfo.t || this.aTokenSetInfo.tx)[0]].i, 'tags': ((this.aTokenSetInfo.tags) ? JSON.parse(JSON.stringify(this.aTokenSetInfo.tags)) : undefined)});
			this.aAntworten[this.aTokenSets[aTSPK].aId].saveme = true;
		}
		if (this.aTokenSetInfo.delAntwort && this.aTokenSetInfo.aId > 0) {
			this.delAntwort(this.aTokenSetInfo.aId);
		}
		this.unsaved = true;
		this.updateATokenSets();
		this.aTokenSetInfo = undefined;
		console.log('TokenSet ID ' + aTSPK + ' geändert!');
	},

	/* showaTokenSetInfos */
	showaTokenSetInfos: function (eTokSet, direkt = false, e = undefined) {
		if (direkt || (this.selTokenSet === eTokSet && (!e || (!e.ctrlKey && !e.shiftKey)))) {
			this.aTokenSetInfo = JSON.parse(JSON.stringify(this.aTokenSets[eTokSet]));
			if (this.aTokenSetInfo.aId && this.aAntworten[this.aTokenSetInfo.aId].tags) {
				this.aTokenSetInfo.tags = JSON.parse(JSON.stringify(this.aAntworten[this.aTokenSetInfo.aId].tags));
			}
			this.aTokenSetInfo['pk'] = eTokSet;
			let aVToken;
			let aBToken;
			let aVTokenOrg;
			let aBTokenOrg;
			if (this.aTokenSetInfo.ivt) {
				aVToken = this.aTokenSetInfo.ivt;
			}
			if (this.aTokenSetInfo.ibt) {
				aBToken = this.aTokenSetInfo.ibt;
			}
			if (this.aTokenSetInfo.t) {
				aVToken = this.aTokenSetInfo.t[0];
				aBToken = this.aTokenSetInfo.t[this.aTokenSetInfo.t.length - 1];
			}
			if (aVToken) {
				this.aTokenSetInfo['satzView'] = [];
				if (!aBToken) { aBToken = aVToken; };
				aVTokenOrg = aVToken;
				aBTokenOrg = aBToken;
				// this.aTokenSetInfo['satzView'].push({text: aVToken + ' - ' + aBToken, class: 'test'});
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
				// this.aTokenSetInfo['satzView'].push({text: aVToken + ' - ' + aBToken, class: 'test'});
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
				// this.aTokenSetInfo['satzView'].push({text: aVToken + ' - ' + aBToken, class: 'test'});
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
					this.aTokenSetInfo['satzView'].push({text: aText, ortho: aOrtho, class: 'before'});
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
					this.aTokenSetInfo['satzView'].push({text: aText, ortho: aOrtho, class: 'active'});
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
				this.aTokenSetInfo['satzView'].push({text: aText, ortho: aOrtho, class: 'after'});
			}
			// this.aTokenSetInfo['satzView'] = [{text: 'test', ortho: 'test Ortho', class: 'test'}];
			setTimeout(function () { $('#aTokenSetInfo').modal('show'); }, 20);
		} else {
			this.selTokenSet = ((this.selTokenSet === eTokSet) ? 0 : eTokSet);
			if (e.ctrlKey) { this.ctrlKS = true; };
		}
	},

	/* Wandelt aktuelle Auswahl in Token Set um */
	selToTokenSet: function () {
		var aTokSetId = -1;
		while (this.aTokenSets[aTokSetId]) {
			aTokSetId -= 1;
		}
		if (this.selTokenBereich.v >= 0 && this.selTokenBereich.b >= 0) {
			this.aTokenSets[aTokSetId] = {'ivt': this.selTokenBereich.v, 'ibt': this.selTokenBereich.b, 'ok': false, 'saveme': true};
			this.unsaved = true;
			this.selTokenBereich = {'v': -1, 'b': -1};
			this.svgSelTokenList = [];
		} else if (this.selTokenListe.length > 0) {
			this.aTokenSets[aTokSetId] = {'t': this.selTokenListe.slice(), 'ok': false, 'saveme': true};
			this.unsaved = true;
			this.selTokenListe = [];
			this.svgSelTokenList = [];
		}
		this.updateATokenSets();
		this.focusFocusCatch();
	},

	/* TokenSet Bereich neu setzen */
	setATokenSetBereich: function (aTokenSetId, aTokenId, feld, direkt = false) {
		if (this.aTokens[aTokenId].i !== this.aTokens[this.aTokenSets[aTokenSetId].ivt].i) {
			alert('Der Token muss den selben Informanten haben!');
			return;
		}
		if (feld === 'ivt') {
			if (this.aTokenReihung.indexOf(this.aTokenSets[aTokenSetId].ibt) <= this.aTokenReihung.indexOf(aTokenId)) {
				alert('Der "Von Token" muss vor dem "Bis Token" liegen!');
				return;
			} else {
				if (direkt || confirm('Den "Von Token" von Token Set ID ' + aTokenSetId + ' wirklich neu setzen?')) {
					this.aTokenSets[aTokenSetId].ivt = aTokenId;
				} else { return; };
			}
		} else if (feld === 'ibt') {
			if (this.aTokenReihung.indexOf(this.aTokenSets[aTokenSetId].ivt) >= this.aTokenReihung.indexOf(aTokenId)) {
				alert('Der "Bis Token" muss nach dem "Von Token" liegen!');
				return;
			} else {
				if (direkt || confirm('Den "Bis Token" von Token Set ID ' + aTokenSetId + ' wirklich neu setzen?')) {
					this.aTokenSets[aTokenSetId].ibt = aTokenId;
				} else { return; };
			}
		}
		this.aTokenSets[aTokenSetId].ok = false;
		this.aTokenSets[aTokenSetId].saveme = true;
		this.unsaved = true;
		this.updateATokenSets();
		this.focusFocusCatch();
	},

	/* TokenSet Liste Token hinzufügen/entfernen */
	toggleATokenSetListe: function (aTokenSetId, aTokenId, direkt = false) {
		if (this.aTokens[aTokenId].i !== this.aTokens[this.aTokenSets[aTokenSetId].t[0]].i) {
			alert('Der Token muss den selben Informanten haben!');
			return;
		}
		if (this.aTokenSets[aTokenSetId].t.indexOf(aTokenId) > -1) {
			if (this.aTokenSets[aTokenSetId].t.length < 2) {
				alert('TokenSets müssen mindestens einen Token enthalten!');
				return;
			}
			if (direkt || confirm('Den Token "' + this.aTokens[aTokenId].t + '" ID ' + aTokenId + ' aus Token Set ID ' + aTokenSetId + ' wirklich löschen?')) {
				this.aTokenSets[aTokenSetId].t.splice(this.aTokenSets[aTokenSetId].t.indexOf(aTokenId), 1);
			} else { return; };
		} else {
			if (direkt || confirm('Den Token "' + this.aTokens[aTokenId].t + '" ID ' + aTokenId + ' zu Token Set ID ' + aTokenSetId + ' hinzufügen?')) {
				this.aTokenSets[aTokenSetId].t.push(aTokenId);
			} else { return; };
		}
		this.aTokenSets[aTokenSetId].ok = false;
		this.aTokenSets[aTokenSetId].saveme = true;
		this.unsaved = true;
		this.updateATokenSets();
		this.focusFocusCatch();
	},

	updateATokenSets: function () {
		console.log('updateATokenSets');
		// Verbindung bei Tokens zu TokenSets überprüfen ob die Tokens noch verwendet werden
		Object.keys(this.aTokens).map(function (tId, iI) {
			if (this.aTokens[tId].tokenSets) {
				_.remove(this.aTokens[tId].tokenSets, (n) => {
					return (!this.aTokenSets[n] || !this.aTokenSets[n].ok);
				});
				if (this.aTokens[tId].tokenSets.length < 1) {
					delete this.aTokens[tId].tokenSets;
				}
			}
		}, this);
		// TokenSets aktuallisieren/berechnen
		Object.keys(this.aTokenSets).map(function (aTokSetId, iI) {
			if (!this.aTokenSets[aTokSetId].ok) {
				var aTokSetIdInt = parseInt(aTokSetId);
				if (this.aTokenSets[aTokSetId].ivt) {
					var aInf = this.aTokens[this.aTokenSets[aTokSetId].ivt].i;
					if (this.aTokenReihungInf[aInf].indexOf(this.aTokenSets[aTokSetId].ivt >= 0 && this.aTokenReihungInf[aInf].indexOf(this.aTokenSets[aTokSetId].ibt >= 0))) {
						if (this.aTokenSets[aTokSetId].ivt > this.aTokenSets[aTokSetId].ibt) {
							var temp = this.aTokenSets[aTokSetId].ivt;
							this.aTokenSets[aTokSetId].ivt = this.aTokenSets[aTokSetId].ibt;
							this.aTokenSets[aTokSetId].ibt = temp;
						}
						var aList = JSON.parse(JSON.stringify(this.aTokenReihungInf[aInf]));
						this.aTokenSets[aTokSetId].tx = aList.splice(aList.indexOf(this.aTokenSets[aTokSetId].ivt), aList.indexOf(this.aTokenSets[aTokSetId].ibt) + 1 - aList.indexOf(this.aTokenSets[aTokSetId].ivt));
						this.aTokenSets[aTokSetId].ok = this.aTokenSets[aTokSetId].tx.length > 0;
					}
				} else if (this.aTokenSets[aTokSetId].t && this.listeWerteInListe(this.aTokenSets[aTokSetId].t, this.aTokenReihung)) {
					this.aTokenSets[aTokSetId].t = this.sortEventIdListe(this.aTokenSets[aTokSetId].t);
					this.aTokenSets[aTokSetId].ok = this.aTokenSets[aTokSetId].t.length > 0;
				}
				// Verwendeten Tokens aktuelles TokenSet zuweisen
				var xt = this.aTokenSets[aTokSetId].t || this.aTokenSets[aTokSetId].tx;
				if (xt && this.aTokenSets[aTokSetId].ok) {
					xt.forEach(function (tId) {
						if (!this.aTokens[tId].tokenSets) {
							this.aTokens[tId].tokenSets = [];
						}
						if (this.aTokens[tId].tokenSets.indexOf(aTokSetIdInt) < 0) {
							this.aTokens[tId].tokenSets.push(aTokSetIdInt);
						}
						this.aTokens[tId].tokenSets = this.sortTokenSets(this.aTokens[tId].tokenSets);
					}, this);
				}
			}
		}, this);
		this.updateZeilenTEvents();
	},

	checkSelTokenBereich: function () {
		if (this.selTokenBereich.v >= 0 && this.selTokenBereich.b >= 0) {
			var aInf = this.aTokens[this.selTokenBereich.v].i;
			if ((aInf !== this.aTokens[this.selTokenBereich.b].i) || this.selTokenBereich.v === this.selTokenBereich.b) {
				this.selTokenBereich = {'v': -1, 'b': -1};
				this.svgSelTokenList = [];
				return true;
			}
			this.selTokenListe = [];
			var aList = JSON.parse(JSON.stringify(this.aTokenReihungInf[aInf]));
			var sTBv = this.selTokenBereich.v;
			var sTBb = this.selTokenBereich.b;
			if (sTBv > sTBb) { var temp = sTBv; sTBv = sTBb; sTBb = temp; }
			this.svgSelTokenList = aList.splice(aList.indexOf(sTBv), aList.indexOf(sTBb) + 1 - aList.indexOf(sTBv));
		} else {
			if (this.selTokenListe.length < 1) {
				this.svgSelTokenList = [];
			}
		}
	},
	updateSelTokenListe: function (eTok = undefined) {
		if (eTok !== undefined) {
			this.selTokenBereich = {'v': -1, 'b': -1};
			if (this.selTokenListe.indexOf(eTok) > -1) {
				this.selTokenListe.splice(this.selTokenListe.indexOf(eTok), 1);
			} else {
				if (this.selTokenListe.length < 1 || this.aTokens[eTok].i === this.aTokens[this.selTokenListe[0]].i) {
					this.selTokenListe.push(eTok);
				} else {
					this.selTokenListe = [];
				}
			}
		}
		this.svgSelTokenList = this.selTokenListe;
	},

	reRenderSelToken: function () {
		var tSelToken = this.selToken;
		this.selToken = -1;
		this.$nextTick(() => { this.selToken = tSelToken; });
	},

	sortTokenSets: function (tokSets) {
		return tokSets.slice().sort((a, b) => {
			var xa = this.aTokenReihung.indexOf((this.aTokenSets[a].t || this.aTokenSets[a].tx)[0]);
			var xb = this.aTokenReihung.indexOf((this.aTokenSets[b].t || this.aTokenSets[b].tx)[0]);
			if (xa > xb) { return 1; }
			if (xa < xb) { return -1; }
			var aTSa = this.aTokenSets[a].t || this.aTokenSets[a].tx;
			var aTSb = this.aTokenSets[b].t || this.aTokenSets[b].tx;
			xa = this.aTokenReihung.indexOf(aTSa[aTSa.length - 1]);
			xb = this.aTokenReihung.indexOf(aTSb[aTSb.length - 1]);
			if (xa < xb) { return 1; }
			if (xa > xb) { return -1; }
			if (this.aTokenSets[a].t && this.aTokenSets[b].tx) { return 1; }
			if (this.aTokenSets[a].tx && this.aTokenSets[b].t) { return -1; }
			return 0;
		});
	}
};
