from setuptools import setup, find_packages

setup(
    name='sovax',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'pyfiglet',
        'dnspython',
        'beautifulsoup4',
        'python-whois'
    ],
    entry_points={
        'console_scripts': [
            'sovax = sovax.sovax:main'
        ]
    },
)

