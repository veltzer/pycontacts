"""
dependencies for this project
"""


def populate(d):
    d.requirements3 = [
        'google-api-python-client',
        # 'gdata-python-client',
    ]


def get_deps():
    return [
        __file__,  # myself
    ]
