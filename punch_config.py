__config_version__ = 1

GLOBALS = {
    'serializer': '{{year}}.{{month}}.{{build}}',
}

FILES = ['setup.py']

VERSION = [
    {
        'name': 'year',
        'type': 'date',
        'fmt': 'YYYY'
    },
    {
        'name': 'month',
        'type': 'date',
        'fmt': 'MM'
    },
    {
        'name': 'build',
        'type': 'integer',
        'start_value': 0
    }
]

VCS = {
    'name': 'git',
    'commit_message': "Release {{ new_version }}",
}

ACTIONS = {
    'build': {
        'type': 'conditional_reset',
        'field': 'build',
        'update_fields': ['year', 'month']
    }
}
