/* global */

const stdfunctions = {
	objectKeyFilter: function (obj, key) {
		var nObj = {};
		Object.keys(obj).map(function (iKey, iI) {
			if (key.indexOf(iKey) >= 0) {
				nObj[iKey] = obj[iKey];
			}
		}, this);
		return nObj;
	},
	objectSubValueFilter: function (obj, key, value) {
		var nObj = {};
		Object.keys(obj).map(function (iKey, iI) {
			if (obj[iKey][key] === value) {
				nObj[iKey] = obj[iKey];
			}
		}, this);
		return nObj;
	},
	searchByKey: function (value, key, list) {
		for (var i = 0; i < list.length; i++) {
			if (list[i][key] === value) {
				return i;
			}
		}
	},

	/* Zeit umrechnen */
	durationToSeconds: function (hms) {
		var s = 0.0;
		if (hms && hms.indexOf(':') > -1) {
			var a = hms.split(':');
			if (a.length > 2) { s += parseFloat(a[a.length - 3]) * 60 * 60; }
			if (a.length > 1) { s += parseFloat(a[a.length - 2]) * 60; }
			if (a.length > 0) { s += parseFloat(a[a.length - 1]); }
		} else {
			s = parseFloat(hms);
		}
		return ((isNaN(s)) ? 0.0 : s);
	},
	secondsToDuration: function (sec, fix = 6) {
		var v = '';
		if (sec < 0) { sec = -sec; v = '-'; }
		var h = parseInt(sec / 3600);
		sec %= 3600;
		var m = parseInt(sec / 60);
		var s = sec % 60;
		return v + ('0' + h).slice(-2) + ':' + ('0' + m).slice(-2) + ':' + ('0' + s.toFixed(fix)).slice(-(3 + fix));
	},

	/* Properties von Objekt filtern */
	filterProperties: function (obj, props) {
		var output = {};
		Object.keys(obj).map(function (key, i) {
			if (props.indexOf(key) > -1) {
				output[key] = obj[key];
			}
		}, this);
		return output;
	},
	listeNachWert: function (liste, val, next = true) {
		var aList = ((next) ? liste.slice() : liste.slice().reverse());
		if (aList.indexOf(val) < aList.length - 1) {
			aList.splice(0, aList.indexOf(val) + 1);
			return aList;
		}
		return [];
	},
	wertNachWert: function (list, val, next = true) {
		var aList = ((next) ? list : list.slice().reverse());
		if (aList.indexOf(val) < aList.length - 1) {
			return aList[aList.indexOf(val) + 1];
		}
		return undefined;
	},
	listeNachWertLoop: function (liste, val, next = true) {
		var aList = ((next) ? liste.slice() : liste.slice().reverse());
		if (val && aList.indexOf(val) > -1 && aList.indexOf(val) < aList.length - 1) {
			if (aList.indexOf(val) > 0) {
				aList = aList.concat(aList.splice(0, aList.indexOf(val) + 1));
			} else {
				aList.splice(0, 1);
			}
		}
		return aList;
	},
	getFirstObjectOfValueInPropertyOfArray (arr, property, value, returnObj) {
		let rObj = ((returnObj) ? {} : null);
		if (Array.isArray(arr)) {
			arr.some(function (aVal, aKey) {
				if (aVal[property] && aVal[property] === value) {
					rObj = aVal;
					return true;
				}
			});
		}
		return rObj;
	},
	hasSubProp (obj, propertys, retVal = false) {		// Ermitten ob Property in einem verschachtelten Objekt existiert
		var out = null;
		if ((typeof propertys === 'string') && (propertys !== null) && propertys.length > 0) {
			var aObj = obj;
			propertys.split('.').some(function (property) {
				if ((typeof aObj === 'object') && (aObj !== null)) {
					if (aObj.hasOwnProperty(property)) {
						out = true;
						aObj = aObj[property];
					} else {
						out = null;
						return true;
					}
				} else {
					out = null;
					return true;
				}
			});
		}
		return ((retVal) ? ((out) ? aObj : null) : out);
	},
	getValOfSubProp (obj, propertys) {		// Gibt Wert eines Property eines verschachtelten Objekts zurück
		return this.hasSubProp(obj, propertys, true);
	},
	listeWerteInListe: function (aListe, bListe) {
		var cListe = aListe.slice();
		bListe.some(function (val) {
			var ap = cListe.indexOf(val);
			if (ap >= 0) {
				cListe.splice(ap, 1);
				return (cListe.length === 0);
			}
		}, this);
		return (cListe.length === 0);
	}
};
