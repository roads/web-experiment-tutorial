import os

# Server Information
username = '<serverusername>'
password = '<serveruserpassword>'
ipaddr = '<ipaddress>
port = 22

# Website Information
website = 'db-tutorial'
htdocsUrl = 'https://www.yoururl.com/' + website
htdocsPath = '/var/www/html/' + website

# Experiment Configuration
expConfig = {
	'codeVersion' : 'v0',
	'website' : website,
	'htdocsUrl' : htdocsUrl,
	'nTrial' : 10,
	'debugOn' : True,
	'doRecord' : True
}
