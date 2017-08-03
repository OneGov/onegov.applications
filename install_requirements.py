#!/usr/bin/python

import json
import os

os.system('pip install --upgrade pip')
os.system('pip install --upgrade setuptools')
os.system('pip --version')
os.system('pip install git+git://github.com/OneGov/onegov_testing.git#egg=onegov_testing')

with open('onegov/applications/applications.json') as f:
    applications = json.load(f)

for application in applications:
    os.system('pip install {}'.format(application['tests']))

os.system('pip install .')
