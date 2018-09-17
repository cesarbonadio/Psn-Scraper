def replaceByList(text,re):
	for r in re:
		text = text.replace(r[0],r[1])
	return text