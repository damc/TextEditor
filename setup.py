from setuptools import setup

setup(
    name='TextEditor',
    author='Damian Czapiewski',
    author_email='damiancz@mailfence.com',
    packages=['screenless'],
    install_requires=['screenless'],
    version='0.1',
    license='MIT',
    description=(
        'Text editor that doesn\'t require the user to look at the computer'
        'screen.'
    )
)