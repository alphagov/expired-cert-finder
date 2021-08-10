from setuptools import setup, find_namespace_packages

from pathlib import Path

from pkg_resources import parse_requirements


with Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in parse_requirements(requirements_txt)
    ]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="expired-cert-finder",
    version="1.0.1",
    author="Government Digital Service",
    description="A tool for discovering expiring or expired certificates in a directory",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alphagov/expired-cert-finder",
    packages=find_namespace_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'expired-cert-finder=expired_cert_finder.cli:run',
        ],
    },
    install_requires=install_requires
)
