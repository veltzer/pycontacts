console_scripts = [
    "pycontacts=pycontacts.main:main",
]
dev_requires = [
    "pypitools",
    "black",
]
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
