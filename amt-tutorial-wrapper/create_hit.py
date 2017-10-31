import os
import sys
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
import boto.mturk.qualification

def main():
	configName = sys.argv[1]
	website = 'amt-tutorial'

	configPath = os.path.join(website, '_%s.config.py' % (configName))
	cfg = {}
	# execfile(configPath, cfg) 	# Load dictionary with key-value pairs in configuration file (Python 2)
	with open(configPath) as f:
		code = compile(f.read(), configPath, 'exec')
		exec(code, cfg)

	tc = cfg['turkConfig']
	if tc['live']:
		# Live HIT
		print("Are you sure you want to create a live HIT (yes/no)?")
		# r = raw_input() # python 2
		r = input()
		if (r == 'yes') or (r == 'y'):
			hitId = create_hit(cfg)

			print("Created HIT {0}".format(hitId))
			with open('hitid.txt','a') as f:
				f.write(hitId)
				f.write('\n')

		else:
			print('Did not create HIT')
	else:
		# Sandbox HIT
		hitId = create_hit(cfg)

		print("Created HIT {0}".format(hitId))
		with open('hitid.txt','a') as f:
			f.write(hitId)
			f.write('\n')

def create_hit(cfg):

	mtc = connect_mtc(cfg)
	tc = cfg['turkConfig']

	quals = boto.mturk.qualification.Qualifications()
	if tc['live']:
		for qual in tc['quals']:
			quals.add(getattr(boto.mturk.qualification, qual[0])(*qual[1:]))


	# create question

	question = ExternalQuestion(tc['questionUrl'], tc['questionFrameHeight'])
	r = mtc.create_hit(question=question,
					max_assignments=tc['maxAssignments'],
					title=tc['hitTitle'],
					description=tc['hitDescription'],
					keywords=tc['hitKeywords'],
					duration=tc['hitDurationSec'],
					reward=tc['hitRewardDollar'],
					qualifications=quals)

	mtc.close()

	hitId = r[0].HITId

	return hitId

def connect_mtc(cfg):
	awsHost = 'mechanicalturk.amazonaws.com' if cfg['turkConfig']['live'] else \
			  'mechanicalturk.sandbox.amazonaws.com'

	mtc = MTurkConnection(aws_access_key_id=cfg['turkConfig']['awsAccessId'],
					      aws_secret_access_key=cfg['turkConfig']['awsSecretKey'],
						  host=awsHost)
	return mtc

if __name__ == "__main__":
	main()
