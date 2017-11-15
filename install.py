#!/usr/bin/python

import boto3
import json
import os
import subprocess

from datetime import datetime, timedelta
from tempfile import NamedTemporaryFile


class Installer(object):

    # the version of onegov.applications
    version = os.environ['TRAVIS_TAG']

    # the place where artifacts are stored
    access_key = os.environ['S3_ACCESS_KEY']
    secret_key = os.environ['S3_SECRET_KEY']
    endpoint = 'https://objects.cloudscale.ch'

    # the bucket where build artifacts needed between the stages are stored
    bucket = 'artifacts'
    bucket_key = 'onegov-applications-{}'.format(version)

    # true if this is the install stage
    # (in the future we should have TRAVIS_STAGE)
    is_install_stage = os.environ.get('STAGE') == 'install'

    # the build directory
    current_dir = os.environ['TRAVIS_BUILD_DIR']

    def __init__(self):
        session = boto3.session.Session(self.access_key, self.secret_key)

        self.s3 = session.resource('s3', endpoint_url=self.endpoint)
        self.s3.create_bucket(Bucket=self.bucket)

        self.requirements_txt = NamedTemporaryFile('r+')
        os.chdir(self.current_dir)

    def pip_install(self, arguments):
        os.system('pip install -c {} {}'.format(
            self.requirements_txt.name,
            arguments))

    def run(self):
        if not self.is_install_stage:
            self.load_requirements()

        # upgrade virtual env
        os.system('pip install --upgrade pip')
        os.system('pip install --upgrade setuptools')

        # install testing
        self.pip_install(
            'git+git://github.com/OneGov/onegov_testing.git#egg=onegov_testing'
        )

        # install application
        with open('onegov/applications/applications.json') as f:
            applications = json.load(f)

            for application in applications:
                self.pip_install(application['tests'])

            self.pip_install('.[test]')

        if self.is_install_stage:
            self.save_requirements()

    def save_requirements(self):
        requirements = subprocess.check_output(('pip', 'freeze'))
        requirements = (line.strip() for line in requirements.splitlines())
        requirements = (line.decode('utf-8') for line in requirements if line)
        requirements = list(requirements)

        for ix, requirement in enumerate(requirements):
            if 'onegov.applications' in requirement:
                requirements[ix] = 'onegov.applications=={}'.format(
                    self.version)

        requirements = '\n'.join(requirements)

        print("Requirements for {}:".format(self.version))
        print(requirements)

        self.s3.put_object(
            ACL='private',
            Bucket=self.bucket,
            Body=requirements.encode('utf-8'),
            Key=self.bucket_key,
            Expires=datetime.today() + timedelta(days=30)
        )

    def load_requirements(self):
        obj = self.s3.Object(self.bucket, self.bucket_id)

        self.requirements_txt.write(obj.get()['Body'].decode('utf-8'))
        self.requirements_txt.flush()
        self.requirements_txt.seek(0)


if __name__ == '__main__':
    Installer().run()
