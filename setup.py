from setuptools import find_packages, setup

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="clope",
    version="0.1",
    description="Python package for interacting with the Cantaloupe/Seed vending system. Primarily the Spotlight API.",
    author="Jordan Maynor",
    author_email="jmaynor@pepsimidamerica.com",
    packages=find_packages(),
    install_requires=required,
)
