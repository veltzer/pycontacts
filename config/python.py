console_scripts = [
    "pycontacts=pycontacts.main:main",
]
dev_requires = [
    "pypitools",
    "black",
]
config_requires = []
install_requires = [
    "httplib2",
    "pygooglehelper",
    # "google-api-python-client",
    "gdata-python3",
    "pytconf",
    "pylogconf",
]
make_requires = [
    "pymakehelper",
    "pydmt",
    "pyclassifiers",
]
test_requires = [
    "pylint",
    "pytest",
    "pytest-cov",
    "flake8",
    "mypy",
]
requires = config_requires + install_requires + make_requires + test_requires
