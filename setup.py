import pathlib
from setuptools import setup, find_packages

# How to use:
# https://packaging.python.org/tutorials/packaging-projects/
# Basically run this command in your python interpreter:
# setup.py sdist bdist_wheel

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="hwglance",
    version="1.0.9",
    description="hwglance: Glance at your computer status",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/NamasteJasutin/hwglance",
    author="NamasteJasutin",
    author_email="justin.duijn@outlook.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "hwglance=hwglance.__console__:main",
        ]
    },
)