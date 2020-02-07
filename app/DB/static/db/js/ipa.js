/* global jQuery */

var ipaKeys = {
	'a':	['a', 'ɑ', 'ɐ', 'ɒ'],
	'b':	['b', 'b̥', 'β', 'β̥'],
	'p':	['p', 'pʰ', 'p̚'],
	'd':	['d', 'd̥'],
	't':	['t', 'tʰ', 't̚'],
	'e':	['e', 'ɛ', 'ə'],
	'ä':	['ɛː', 'æ'],
	'f':	['f', 'v̥'],
	'g':	['g', 'g̥'],
	'k':	['k', 'kʰ', 'k͡χ', 'k̚'],
	'h':	['ʰ'],
	'i':	['i', 'ɪ'],
	'l':	['l', 'ɭ', 'ɫ'],
	'm':	['m', 'ɱ'],
	'n':	['n', 'ŋ', 'ⁿ', 'n̩'],
	'o':	['o', 'ɔ'],
	'oa':	['ɔɐ̯', 'ɔo̯'],
	'ö':	['ø', 'œ'],
	'r':	['ʁ', 'ʀ', 'ɹ', 'ɾ'],
	'z':	['z', 'z̥'],
	'sch': ['ʃ', 'ʒ̥', 'ʒ'],
	'u':	['u', 'ʊ', 'ue̯'],
	'ü':	['y', 'ʏ', 'ʏɐ̯'],
	'w':	['v', 'β', 'β̥'],
	'ch':	['ç', 'x', 'χ', 'ɣ̥', 'ʝ̥'],
	'ei':	['aɛ̯', 'æe̯', 'æː'],
	'au':	['aɔ̯', 'ao̯', 'ɒ'],
	'eu':	['ɔe̯'],
	'ie':	['ɪɐ̯'],
	'ia':	['ɪɐ̯'],
	'pf':	['p͡f', 'b̥͡f'],
	'ts':	['t͡s', 'd̥͡s'],
	'1':	['̯', '̃', '͡', '̚', '̥'],
	'0':	['̯', 'ʰ', 'ⁿ', '̃', 'ː', '͡', '̝', '̞', 'ʔ'],
	':':	['ː'],
	'.':	['̩', '̥', '̝', '̞'],
	'?':	['?', 'ʔ']
};

(function ($) {
	jQuery(document).ready(function ($) {
		$(document).on('blur', '#ipaselector .ipavals, input[data-ipa="true"]', function (e) {
			setTimeout(function () {
				if ($('#ipaselector').find(':focus').length < 1) {
					$('#ipaselector').remove();
				};
			}, 25);
		});
		$(document).on('keyup', 'input[data-ipa="true"]', function (e) {
			if (e.key !== 'Tab' && e.key !== 'Shift') {
				$('#ipaselector').remove();
				if (e.key.length === 1 && this.selectionStart === this.selectionEnd) {
					var akeyselects = [];
					if (e.key === '!') {
						for (var key in ipaKeys) {
							if (!ipaKeys.hasOwnProperty(key)) continue;
							akeyselects.push({'k': key, 'a': ipaKeys[key]});
						};
					} else {
						var alkey = '';
						if (this.selectionStart > 2) {
							alkey = this.value.substring(this.selectionStart - 3, this.selectionStart);
							if (ipaKeys[alkey]) {
								akeyselects.push({'k': alkey, 'a': ipaKeys[alkey]});
							};
						};
						if (this.selectionStart > 1) {
							alkey = this.value.substring(this.selectionStart - 2, this.selectionStart);
							if (ipaKeys[alkey]) {
								akeyselects.push({'k': alkey, 'a': ipaKeys[alkey]});
							};
						};
						var akey = this.value.substring(this.selectionStart - 1, this.selectionStart);
						if (akey && ipaKeys[akey]) {
							akeyselects.push({'k': akey, 'a': ipaKeys[akey]});
						};
					};
					if (akeyselects.length > 0) {
						var ipaselectorhtml = '<div id="ipaselector" data-ipa-selstart="' + this.selectionStart + '">';
						$.each(akeyselects, function (i, val) {
							ipaselectorhtml += '<div class="clearfix" data-ipa-key="' + val['k'] + '"><div class="ipakey">' + val['k'] + '</div>';
							$.each(val['a'], function (i2, kval) {
								ipaselectorhtml += '<button class="ipavals" data-ipa-val="' + kval + '">' + kval + '</button>';
							});
							ipaselectorhtml += '</div>';
						});
						ipaselectorhtml += '</div>';
						$(this).parent().css('position', 'relative').append(ipaselectorhtml);
					};
				};
			};
		});
		$(document).on('click', '#ipaselector .ipavals', function (e) {
			var aTarget = $('#ipaselector').siblings('input[data-ipa="true"]');
			var aSelStart = $('#ipaselector').data('ipa-selstart');
			var aKey = $(this).parent().data('ipa-key').toString();
			var aVal = $(this).data('ipa-val').toString();
			var oText = aTarget.val().toString();
			aTarget.val(oText.substring(0, aSelStart - aKey.length) + aVal + oText.substring(aSelStart, oText.length));
			aTarget.focus();
			if (aTarget[0].setSelectionRange) {
				var nSelPos = aSelStart + aVal.length - aKey.length;
				aTarget[0].setSelectionRange(nSelPos, nSelPos);
			};
		});
		$(document).on('keyup', '#ipaselector .ipavals', function (e) {
			if (e.key === 'Escape') {
				var aTarget = $('#ipaselector').siblings('input[data-ipa="true"]');
				var aSelStart = $('#ipaselector').data('ipa-selstart');
				aTarget.focus();
				if (aTarget[0].setSelectionRange) {
					aTarget[0].setSelectionRange(aSelStart, aSelStart);
				};
			};
		});
	});
})(jQuery);
