#!/usr/bin/python

import json
import os

from travispy import TravisPy


def upgrade_virtualenv():
    os.system('pip install --upgrade pip')
    os.system('pip install --upgrade setuptools')
    os.system('pip --version')


def install_testing():
    url = 'git+git://github.com/OneGov/onegov_testing.git#egg=onegov_testing'
    os.system('pip install {}'.format(url))


def install_applications():
    with open('onegov/applications/applications.json') as f:
        applications = json.load(f)

    for application in applications:
        os.system('pip install {} -c requirements.txt'.format(
            application['tests']))

    os.system('pip install .[test] -c requirements.txt')


def load_requirements(path, github_token, current_build_id, current_job_id):
    """ Load the requirements produced by the install stage and store it
    as a requirements.txt file. This way we can be sure that all test jobs
    as well as the deployment stage share the exact same requirements.

    Excludes the onegov.applications line as it makes no sense to useit.

    If this *is* the install stage the constraints.txt will be empty.

    """
    requirements = []

    api = TravisPy.github_auth(github_token)
    build = api.build(current_build_id)

    install_job = next((
        job for job in build.jobs
        if (
            job.config['stage'].lower() == 'install' and
            job.id != int(current_job_id)
        )
    ), None)

    if install_job:
        in_block = False

        for line in install_job.log.body.splitlines():
            if in_block and 'onegov.applications' not in line:
                requirements.append(line)
            if '<requirements>' in line:
                in_block = True
            if '</requirements>' in line:
                break

    with open(os.path.join(path, 'requirements.txt'), 'w') as f:
        f.writelines(requirements)


if __name__ == '__main__':
    upgrade_virtualenv()
    install_testing()
    load_requirements(
        os.environ['TRAVIS_BUILD_DIR'],
        os.environ['TRAVIS_GITHUB_TOKEN'],
        os.environ['TRAVIS_BUILD_ID'],
        os.environ['TRAVIS_JOB_ID']
    )
    install_applications()
