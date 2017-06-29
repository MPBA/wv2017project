from distutils.core import setup

setup(
    name='chainEN',
    version='1.0',
    description='Notarizes files on the bitcoin blockchain.',
    author='Elliot and Nunzio',
    author_email='elliot.gorokhovsky@gmail.com',
    url='https://xxxxxx',
    data_files=[('config', 'chainEN/config.json')],
    packages=['chainEN'],
    install_requires=['redis']
)
