from setuptools import setup

# Read dependencies from requirements.txt
with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="sovax",
    version="1.0",
    py_modules=["sovax"],  # This tells setuptools you're using a single script, not a package
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "sovax = sovax:main"  # maps to main() in sovax.py
        ]
    },
    python_requires=">=3.6",
    description="Passive Recon Tool",
    author="Shashaank Subramannya"
)
