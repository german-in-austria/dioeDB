/* global jQuery openUrlInNewWindow */

(function ($) {
	jQuery(document).ready(function ($) {
		$(document).on('click', 'a#linkwb', function (e) {
			e.preventDefault();
			openUrlInNewWindow('https://regionalsprache.de/Wenkerbogen/WenkerbogenViewer.aspx?WbNr=' + $('#fid_num_wb_1_1').val());
		});
	});
})(jQuery);
