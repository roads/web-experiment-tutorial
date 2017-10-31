import cgi

def getFieldStorageValues():
	form = cgi.FieldStorage()
	params = {}
	for key in form.keys():
		params[key] = form[key].value
	return params