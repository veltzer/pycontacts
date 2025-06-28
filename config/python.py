""" python deps for this project """

console_scripts: list[str] = [
    "pycontacts=pycontacts.main:main",
]
config_requires: list[str] = [
    "pyclassifiers",
]
install_requires: list[str] = [
    "httplib2",
    "pygooglehelper",
    # "google-api-python-client",
    "gdata-python3",
    "pytconf",
    "pylogconf",
]
build_requires: list[str] = [
    "pymakehelper",
    "pydmt",
]
test_requires: list[str] = [
    "pylint",
    "pytest",
    "pytest-cov",
    "mypy",
]
requires = config_requires + install_requires + build_requires + test_requires
