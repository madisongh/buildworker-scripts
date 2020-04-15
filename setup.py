from setuptools import setup, find_packages

setup(
    name='buildworker-scripts',
    version='0.1.0',
    packages=find_packages(),
    license='MIT',
    author='Matt Madison',
    author_email='matt@madison.systems',
    url='https://github.com/madisongh/buildworker-scripts',
    entry_points={
        'console_scripts': [
            'store-artifacts = buildworker_scripts.scripts.store_artifacts:main',
        ]
    },
    install_requires=['aws-secretsmanager-caching',
                      'boto3', 'botocore']
)
