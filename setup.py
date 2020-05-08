import pathlib
from setuptools import setup

from pandas2pgfplots import __version__ as version

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pandas2pgfplots",
    version=version,
    description="Library for pgfplots plots from pandas DataFrames",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/xblahoud/pandas2pgfplots",
    author="Fanda Blahoudek",
    author_email="fandikb+dev@gmail.com",
    license="MIT",
    python_requires=">=3.6.0",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["pandas2pgfplots"],
    install_requires=[
        'pandas>=0.24',
    ]
)
