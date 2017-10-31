import os

# Server Information
username = '<serverusername>'
password = '<serveruserpassword>'
ipaddr = '159.203.207.54'
port = 22

# Website Information
website = 'server-tutorial'
htdocsUrl = 'https://www.mozerlab.us/' + website
htdocsPath = '/var/www/html/' + website

# Experiment Configuration
expConfig = {
	'codeVersion' : 'v0',
	'website' : website,
	'htdocsUrl' : htdocsUrl,
	'nTrial' : 10,
	'debugOn' : True
}
