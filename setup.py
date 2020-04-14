from setuptools import setup, find_packages

BUILDBOTVERSION = '2.7.0'

setup(
    name='buildworker-scripts',
    version='0.1.0',
    packages=find_packages(),
    license='MIT',
    author='Matt Madison',
    author_email='matt@madison.systems',
    entry_points={
        'console_scripts': [
            'store-artifacts = autobuilder.scripts.store_artifacts:main',
        ]
    },
    include_package_data=True,
    package_data={
        'autobuilder': ['templates/*.txt']
    },
    install_requires=['aws-secretsmanager-caching',
                      'boto3', 'botocore']
)
