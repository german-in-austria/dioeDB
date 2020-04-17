/* global jQuery asurl loadElement */
(function ($) {
	jQuery(document).ready(function ($) {
		$(document).on('click', '#fxerhinfaufgabebtn:not(.loading)', function () {
			$(this).addClass('loading disabled');
			loadElement($('.lmfa .lmfabcl.open'), asurl, undefined, undefined, {'erhinfaufgabefxfunction': 1});
		});
		$(document).on('click', '#fxantwortenmitsaetzenbtn:not(.loading)', function () {
			$(this).addClass('loading disabled');
			loadElement($('.lmfa .lmfabcl.open'), asurl, undefined, undefined, {'antwortenmitsaetzenfxfunction': 1});
		});
		$(document).on('click', '#fxstxsmbtn:not(.loading)', function () {
			$(this).addClass('loading disabled');
			loadElement($('.lmfa .lmfabcl.open'), asurl, undefined, undefined, {'stxsmfxfunction': 1});
		});
	});
})(jQuery);
