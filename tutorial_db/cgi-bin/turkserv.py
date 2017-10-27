#!/usr/bin/python
import os
import sys
import json
import portalocker
import datetime
import apputils
import cgitb
from string import Template

# This file consitutes the AWS question URL (pointed to by the config file)

# cgitb.enable()

def main():
	cfg = {}
	execfile('config.python', cfg)
	
	form = apputils.getFieldStorageValues()
	
	inMturk = 'hitId' in form and 'assignmentId' in form and 'workerId' in form and (form['hitId'] and
				form['assignmentId'] and form['workerId'])
			
	if inMturk:
		if form['assignmentId'] != 'ASSIGNMENT_ID_NOT_AVAILABLE':
			print "Location: %s/consent.html?hitId=%s&assignmentId=%s&workerId=%s" % (cfg['htdocsUrl'], form['hitId'],form['assignmentId'],form['workerId'])
			print
			return
	
	tmpl = Template(readAllText('%s/preview.html' % cfg['htdocsPath']))
	print "Content-type: text/html\n"
	print tmpl.substitute({ 'expTimeMin' : cfg['defaultGameConfig']['expTimeMin'], 
							'htdocsUrl' : cfg['defaultGameConfig']['htdocsUrl'] })
def readAllText(path):
	with open(path, 'r') as f:
		return f.read()


if __name__ == "__main__":
	main()
	