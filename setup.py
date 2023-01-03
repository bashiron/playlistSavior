from setuptools import setup


setup(
    name='playlist-savior',
    version='1.0.0',
    description='Playlist Preservation Program',
    long_description='<detailed description>',
    author='bashiron',
    mantainer='luciano01amoruso@gmail.com',
    url='<future github url>',
    # python_requires='<?>',
    py_modules=['cli'],
    install_requires=[
        'cachetools==5.2.0',
        'certifi==2022.9.24',
        'charset-normalizer==2.1.1',
        'click==8.1.3',
        'google-api-core==2.10.2',
        'google-api-python-client==2.64.0',
        'google-auth==2.12.0',
        'google-auth-httplib2==0.1.0',
        'googleapis-common-protos==1.56.4',
        'httplib2==0.20.4',
        'idna==3.4',
        'loguru==0.6.0',
        'protobuf==4.21.7',
        'psycopg==3.1.4',
        'psycopg-pool==3.1.4',
        'pyasn1==0.4.8',
        'pyasn1-modules==0.2.8',
        'pyparsing==3.0.9',
        'python-dotenv==0.21.0',
        'requests==2.28.1',
        'rsa==4.9',
        'six==1.16.0',
        'typing_extensions==4.4.0',
        'uritemplate==4.1.1',
        'urllib3==1.26.12'
    ],
    entry_points='''
        [console_scripts]
        savior=src.cli:cli
    '''
)
