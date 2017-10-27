import os

username = '<serverusername>'
password = '<serveruserpassword>'
ipaddr = '159.203.207.54'
port = 22
website = 'db-tutorial'

htdocsUrl = 'https://www.mozerlab.us/' + website
htdocsPath = '/var/www/html/' + website

turkConfig = {
	'live' : False,
}

submitUrl = 'https://www.mturk.com/mturk/externalSubmit' if turkConfig['live'] else \
			'https://workersandbox.mturk.com/mturk/externalSubmit'

defaultGameConfig = {
	'codeVersion' : 'v0',
	'website' : website,
	'htdocsUrl' : htdocsUrl,
	'submitUrl' : submitUrl,
	'nScreen' : 5,
	'doRecord': True,
	'debugOn' : True
}

expMode ='valid'
