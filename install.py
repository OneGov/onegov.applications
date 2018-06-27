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
    bucket_key = f'onegov-applications-{version}'

    # true if this is the install stage
    # (in the future we should have TRAVIS_STAGE)
    is_install_stage = os.environ.get('STAGE') == 'install'

    # the build directory
    current_dir = os.environ['TRAVIS_BUILD_DIR']

    def __init__(self):
        session = boto3.session.Session(self.access_key, self.secret_key)
        self.s3 = session.resource('s3', endpoint_url=self.endpoint)

        self.requirements_txt = NamedTemporaryFile('r+')

        os.chdir(self.current_dir)

    def pip_install(self, arguments):
        os.system((
            f'pip install -c {self.requirements_txt.name} {arguments} '
            f'--no-binary pillow'
        ))

    def run(self):
        if not self.is_install_stage:
            self.download_requirements()

        # upgrade virtual env
        os.system('pip install --upgrade pip')
        os.system('pip install --upgrade setuptools')

        # install testing (cannot be constrained)
        url = 'git+git://github.com/OneGov/onegov_testing#egg=onegov_testing'
        os.system(f'pip install {url}')

        # install application
        with open('onegov/applications/applications.json') as f:
            applications = json.load(f)

        for application in applications:
            self.pip_install(application['tests'])

        # seems to be required for onegov.core to be importable (weird, works
        # in a vanilla virtual env without tests)
        self.pip_install('-e .')

        if self.is_install_stage:
            self.upload_requirements()

    def upload_requirements(self):
        requirements = subprocess.check_output(('pip', 'freeze'))
        requirements = (line.strip() for line in requirements.splitlines())
        requirements = (line.decode('utf-8') for line in requirements if line)
        requirements = (
            line for line in requirements if 'onegov.applications' not in line)

        requirements = '\n'.join(requirements)

        print(f"Requirements for {self.version}:")
        print(requirements)

        self.s3.create_bucket(Bucket=self.bucket).put_object(
            ACL='private',
            Body=requirements.encode('utf-8'),
            Key=self.bucket_key,
            Expires=datetime.today() + timedelta(days=30)
        )

    def download_requirements(self):
        obj = self.s3.Object(self.bucket, self.bucket_key)

        self.requirements_txt.write(obj.get()['Body'].read().decode('utf-8'))
        self.requirements_txt.flush()
        self.requirements_txt.seek(0)


if __name__ == '__main__':
    Installer().run()
