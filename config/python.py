import config.project

package_name = config.project.project_name

console_scripts = [
    "pycontacts=pycontacts.main:main",
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

test_requires = [
    "pylint",
    "pytest",
    "pytest-cov",
    "flake8",
    "pymakehelper",
]

dev_requires = [
    "pyclassifiers",
    "pypitools",
    "pydmt",
    "Sphinx",
    "black",
]

python_requires = ">=3.9"
test_os = ["ubuntu-20.04"]
test_python = ["3.9"]
