#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="gpt-repository-loader",
    version="0.1.5",
    author="Felvin",
    author_email="team@felvin.com",
    description="A utility to convert a Git repository into a text representation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/felvin-search/gpt-repository-loader",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    install_requires=["pyperclip"],
    entry_points={
        "console_scripts": [
            "gpt-repository-loader=gpt_repository_loader:main",
        ],
    },
)

