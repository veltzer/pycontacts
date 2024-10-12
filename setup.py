import setuptools


def get_readme():
    with open("README.rst") as f:
        return f.read()


setuptools.setup(
    # the first three fields are a must according to the documentation
    name="pycontacts",
    version="0.0.14",
    packages=[
        "pycontacts",
    ],
    # from here all is optional
    description="Interact with google contacts",
    long_description=get_readme(),
    long_description_content_type="text/x-rst",
    author="Mark Veltzer",
    author_email="mark.veltzer@gmail.com",
    maintainer="Mark Veltzer",
    maintainer_email="mark.veltzer@gmail.com",
    keywords=[
        "google",
        "contacts",
        "python",
    ],
    url="https://veltzer.github.io/pycontacts",
    download_url="https://github.com/veltzer/pycontacts",
    license="MIT",
    platforms=[
        "python3",
    ],
    install_requires=[
        "httplib2",
        "pygooglehelper",
        "gdata-python3",
        "pytconf",
        "pylogconf",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.11",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={"console_scripts": [
        "pycontacts=pycontacts.main:main",
    ]},
)
