#!/usr/bin/python
import os
import sys
import json
import portalocker
import datetime
import cgitb
import apputils

# cgitb.enable()		# enable gci traceback
def main():

	cfg = {}						# Initialize dictionary
	execfile('config.python', cfg)	# Import key-value pairs from config file
	

	form = apputils.getFieldStorageValues()	# Grab key-value pairs from incoming post
	
	# Check if in mTurk by seeing if appropriate fields exist
	inMturk = 'hitId' in form and 'assignmentId' in form and 'workerId' in form and (form['hitId'] and
				form['assignmentId'] and form['workerId'])
	
	if inMturk:
		gameConfig = get_exp_config(form, cfg)
	else:
		gameConfig = get_free_config(form, cfg)
	
	print "Content-type: application/json\n\n"
	print json.dumps(gameConfig)
	
def get_free_config(form, cfg):
	gameConfig = cfg['defaultGameConfig'].copy()
	gameConfig.update(form)
	gameConfig['mode'] = '';
	return gameConfig
	
def get_exp_config(form, cfg):
	gameConfig = cfg['defaultGameConfig'].copy()
	gameConfig.update(form)
	gameConfig['mode'] = 'turkExp'
	return gameConfig


if __name__ == "__main__":
	main()
	