#!/usr/bin/env python3
"""
FixPipeline - Professional CircleCI APK Auto-Fixer
Setup script for pip installation
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

setup(
    name="fixpipeline",
    version="1.0.0",
    author="QA Team",
    author_email="qa@company.com",
    description="Professional tool to automatically convert CircleCI APK downloads from .zip to .apk",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/subhadip-unn/FixPipeline",
    py_modules=["fixpipeline"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pystray>=0.19.4",
        "pillow>=9.0.0",
        "plyer>=2.1.0",
        "watchdog>=2.1.0",
        "psutil>=5.9.0",
    ],
    entry_points={
        "console_scripts": [
            "fixpipeline=fixpipeline:main",
        ],
    },
    keywords="circleci, apk, android, qa, testing, automation, fixpipeline",
    project_urls={
        "Bug Reports": "https://github.com/subhadip-unn/FixPipeline/issues",
        "Source": "https://github.com/subhadip-unn/FixPipeline",
    },
)
