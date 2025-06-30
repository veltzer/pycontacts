""" python deps for this project """

import config.shared

scripts: dict[str,str] = {
    "pycontacts": "pycontacts.main:main",
}

install_requires: list[str] = [
    "httplib2",
    "pygooglehelper",
    # "google-api-python-client",
    "gdata-python3",
    "pytconf",
    "pylogconf",
]
build_requires: list[str] = config.shared.PBUILD
test_requires: list[str] = config.shared.PTEST
requires = install_requires + build_requires + test_requires
