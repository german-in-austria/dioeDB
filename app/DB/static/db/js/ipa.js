(function($){jQuery(document).ready(function($){

	var ipakeys = {
		'a':	['X', 'X2', 'X3', 'X4'],
		'ab':	['Y', 'Y2', 'Y3'],
		'b':	['Z', 'Z2', 'Z3', 'Z4', 'Z5', 'Z6']
	};

	$(document).on('keyup', 'input[data-ipa="true"]', function (e) {
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
			$('#ipaselector').remove();
			var ipaselectorhtml = '<div id="ipaselector">';
			$.each(akeyselects, function (i, val) {
				ipaselectorhtml += '<div class="clearfix"><div class="ipakey">' + val['k'] + '</div>';
				$.each(val['a'], function (i2, kval) {
					ipaselectorhtml += '<button class="ipavals">' + kval + '</button>';
				});
				ipaselectorhtml += '</div>';
			});
			ipaselectorhtml += '</div>';
			$(this).parent().css('position', 'relative').append(ipaselectorhtml);

		} else {
			console.log(e.key);
		}
	});

});})(jQuery);
