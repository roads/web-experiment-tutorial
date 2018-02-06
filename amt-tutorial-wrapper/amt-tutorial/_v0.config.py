import os

# Server Information
username = '<serverusername>'
password = '<serveruserpassword>'
ipaddr = '<ipadress>'
port = 22

# Website Information<
website = 'amt-tutorial'
htdocsUrl = 'https://www.yoururl.com/' + website
htdocsPath = '/var/www/html/' + website

# BEGIN NEW CODE
# AMT Configuration
dollarPerHour = 6.00
expTimeMin = 1.0
hitRewardDollar = (expTimeMin / 60.0 ) * dollarPerHour;
turkConfig = {
	'live' : False,
	'questionUrl' : '%s/cgi-bin/turkserv.py' % (htdocsUrl),
	'questionFrameHeight' : 600,
	'hitTitle' : "Identify a letter as rapidly as possible.",
	'hitDescription' : 'Identify a letter as rapidly as possible.',
	'hitKeywords' : "experiment, psychology",
	'hitDurationSec' :  1800,
	'hitRewardDollar' : hitRewardDollar,
	'maxAssignments' : 1,
	'awsAccessId' : 'AFAKEACCESSKEY',
	'awsSecretKey' : 'AFAKESECRETKEY',
	'quals' : 	[
		['NumberHitsApprovedRequirement', 'GreaterThanOrEqualTo', 100],
		['PercentAssignmentsApprovedRequirement', 'GreaterThanOrEqualTo', 90],
		['LocaleRequirement', 'EqualTo', 'US']
	]
}
submitUrl = 'https://www.mturk.com/mturk/externalSubmit' if turkConfig['live'] else \
			'https://workersandbox.mturk.com/mturk/externalSubmit'
# END NEW CODE

# Experiment Configuration
expConfig = {
	'codeVersion' : 'v0',
	'website' : website,
	'htdocsUrl' : htdocsUrl,
	'nTrial' : 10,
	'debugOn' : True,
	'doRecord' : True,
	'submitUrl' : submitUrl,
	'expTimeMin' : expTimeMin
}
