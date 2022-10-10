console_scripts = [
    "pycontacts=pycontacts.main:main",
]
dev_requires = [
    "pypitools",
    "Sphinx",
    "black",
]
install_requires = [
    "httplib2",
    "google-api-python-client",
    "google-auth-httplib2",
    "google-auth-oauthlib",
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
