from setuptools import setup

setup(
    name='access_logger',
    version='0.0.1',
    description='Access logging is a request/response logging package for Django projects',
    url='https://github.com/nasir15/AccessLogger.git',
    author='Nasir Khan',
    author_email='nasirfareed15@gmail.com',
    license='public',
    packages=['access_logger'],
    zip_safe=False,
    install_requires=['Django'],
)
