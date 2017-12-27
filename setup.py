import setuptools

setuptools.setup(
    name='pycontacts',
    version='0.0.4',
    description='pycontacts is a collection of utilities to help interact with google contacts',
    long_description='pycontacts helps you with various google contacts tasks',
    url='https://veltzer.github.io/pycontacts',
    download_url='https://github.com/veltzer/pycontacts',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    maintainer='Mark Veltzer',
    maintainer_email='mark.veltzer@gmail.com',
    license='MIT',
    platforms=['python3'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='google contacts python',
    packages=setuptools.find_packages(),
    install_requires=[
        'google-api-python-client',  # main client library
    ],
    entry_points={
        'console_scripts': [
            'pgc_list=pycontacts.list:main',
        ],
    },
)
