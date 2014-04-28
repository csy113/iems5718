function htmlEscape(str) {
	return String(str)
		.replace(/(<([^>]+)>)/ig,"")
		.replace(/&/g, '&amp;')
		.replace(/"/g, '&quot;')
		.replace(/'/g, '&#39;')
		.replace(/</g,
				'&lt;')
		.replace(/>/g,
				'&gt;');
}
