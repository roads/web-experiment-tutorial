# Example usage: python3 deploy_website.py birds-16
from __future__ import division
import os
import sys
import shutil
import paramiko
import tarfile
import json

def main():

	website = 'server-tutorial'
	configName = sys.argv[1]

	print('Deploying {0}_{1} to server...'.format(website, configName))

	configPath = os.path.join(website, '_%s.config.py' % (configName))
	cfg = {} 					# Initialize dictionary data type for cofiguration file
	# execfile(configPath, cfg) 	# Load dictionary with key-value pairs in configuration file (Python 2)
	with open(configPath) as f:
		code = compile(f.read(), configPath, 'exec')
		exec(code, cfg)

	# This filter omits files that don't start with '_', i.e. the various configuration files
	def filterf(f):
		fileName =  os.path.basename(f.name)
		if fileName.startswith('_'):
			return None
		return f

	# Packing up all files for transfer to server
	# Description:
	# w:gz - ppen for gzip compressed writing.
	# arcname specifies an alternative name for the file in the archive
	print('    Compressing files to tar ball...')
	with tarfile.open('frontend.tar.gz', 'w:gz') as tar:
		tar.add(website, arcname=website, filter = filterf)				# add all website files except files starting with "_"
		tar.add('cgi-bin', arcname=website + '/cgi-bin')				# placing cgi-bin inside website folder
		tar.add(configPath, arcname=website + '/cgi-bin/config.python') # placing config file inside cgi-bin folder (NOTE .python)

	# Upload to server and unpack
	print('    Uploading to server ...')
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(cfg['ipaddr'],
				port=cfg['port'],
				username=cfg['username'],
				password=cfg['password'])
	sftp = ssh.open_sftp()
	sftp.put('frontend.tar.gz', 'frontend.tar.gz')
	sftp.close()

	# Extract and some cleanup
	print('    Decompressing tar bar ...')
	stdin,stdout,stderr = ssh.exec_command('cd ~; rm -rf %s; tar -xzf frontend.tar.gz; rm frontend.tar.gz' % website)
	# To root, remove website directory if it exists (suppress output), extract from tar ball, remove tarball
	# SEE http://www.cyberciti.biz/faq/unpack-tgz-linux-command-line/ for tar extraction options
	print(stderr.readlines())

	# Move htdocs
	print('    Moving htdocs to appropriate server location ...')
	stdin, stdout, stderr = ssh.exec_command('cd ~; rm -rf {1}; mv {0} {1}; chmod 755 {1}/cgi-bin/*.py'.format(website, cfg['htdocsPath']))
	# Command Description:
	# to root, remove directory at htdocsPath (e.g., '/var/www/bdroads.com/public_html/similarity_9birds')
	# set permissions 755 of all python files in htdocsPath/cgi-bin
	# set permissions 755 of all php files in htdocsPath/php
	# SEE: http://www.computerhope.com/unix/uchmod.htm
	# move website to htdocsPath
	# NOTE: because the config file ends with .python (NOT .py), its permissions are 644
	print(stderr.readlines())

	ssh.close()

	# Remove tar ball on local machine
	os.remove('frontend.tar.gz')

	print('DONE\n')


if __name__ == "__main__":
	main()
