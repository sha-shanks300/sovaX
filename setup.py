from setuptools import setup, find_packages

setup(
    name="sovax",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pyfiglet",
        "dnspython"
    ],
    entry_points={
        "console_scripts": [
            "sovax = sovax.__main__:main"
        ]
    },
    python_requires=">=3.6",
    description="Passive Recon Tool",
    author="Shashaank Subramannya"
)
