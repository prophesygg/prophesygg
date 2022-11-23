from setuptools import setup, find_packages

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="prophesygg",
    version="0.0.1",
    packages=find_packages(exclude=['tests*']),
    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=[],
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": []
    },
    # metadata to display on PyPI
    author="Prophesy.gg Team",
    author_email="contact@prophesy.gg",
    description="Prophesy.gg",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.prophesy.gg",
)