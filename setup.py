import setuptools


def get_readme():
    with open('README.rst') as f:
        return f.read()


setuptools.setup(
    # the first three fields are a must according to the documentation
    name="pycontacts",
    version="0.0.11",
    packages=[
        'pycontacts',
    ],
    # from here all is optional
    description="pycontacts is a collection of utilities to help interact with google contacts",
    long_description=get_readme(),
    long_description_content_type="text/x-rst",
    author="Mark Veltzer",
    author_email="mark.veltzer@gmail.com",
    maintainer="Mark Veltzer",
    maintainer_email="mark.veltzer@gmail.com",
    keywords=[
        'google',
        'contacts',
        'python',
    ],
    url="https://veltzer.github.io/pycontacts",
    download_url="https://github.com/veltzer/pycontacts",
    license="MIT",
    platforms=[
        'python3',
    ],
    install_requires=[
        'httplib2',
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'gdata-python3',
        'pytconf',
        'pylogconf',
    ],
    extras_require={
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
    data_files=[
    ],
    entry_points={"console_scripts": [
        'pycontacts=pycontacts.main:main',
    ]},
    python_requires=">=3.6",
)
