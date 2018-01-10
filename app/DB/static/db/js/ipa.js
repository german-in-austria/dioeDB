(function($){jQuery(document).ready(function($){

	var ipakeys = {
		'a':	['X', 'X2', 'X3', 'X4'],
		'ab':	['Y', 'Y2', 'Y3'],
		'b':	['Z', 'Z2', 'Z3', 'Z4', 'Z5', 'Z6']
	};

	$(document).on('blur', '#ipaselector .ipavals, input[data-ipa="true"]', function (e) {
		setTimeout(function () {
			if ($('#ipaselector').find(':focus').length < 1) {
				$('#ipaselector').remove();
			};
		}, 25);
	});
	$(document).on('keyup', 'input[data-ipa="true"]', function (e) {
		if (e.key !== 'Tab') {
			$('#ipaselector').remove();
			if (e.key.length === 1 && this.selectionStart === this.selectionEnd) {
				var akeyselects = [];
				if (this.selectionStart > 1) {
					var alkey = this.value.substring(this.selectionStart - 2, this.selectionStart);
					if (ipakeys[alkey]) {
						akeyselects.push({'k': alkey, 'a': ipakeys[alkey]});
					};
				};
				var akey = this.value.substring(this.selectionStart - 1, this.selectionStart);
				if (akey && ipakeys[akey]) {
					akeyselects.push({'k': akey, 'a': ipakeys[akey]});
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
		var aKey = $(this).parent().data('ipa-key');
		var aVal = $(this).data('ipa-val');
		var oText = aTarget.val();
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

});})(jQuery);