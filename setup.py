import setuptools

import sys
if not sys.version_info[0] == 3:
    sys.exit("Sorry, only python version 3 is supported")

setuptools.setup(
    name='pycontacts',
    version='0.0.1',
    description='pycontacts is a collection of utilities to help interact with google contacts',
    long_description='pycontacts helps you with various google contacts tasks',
    url='https://veltzer.github.io/pycontacts',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License'
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='google contacts python',
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
    install_requires=[
        'google-api-python-client',  # main client library
    ],
    entry_points={
        'console_scripts': [
            'pgc_list=pycontacts.list:main',
        ],
    },
)
