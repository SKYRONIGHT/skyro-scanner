from setuptools import setup
import os

# Read the README file
with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

# Read the requirements file
with open(os.path.join(os.path.dirname(__file__), 'requirements.txt'), 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="skyro",
    version="1.0.0",
    description="SKYRO Web Application Security Scanner - Advanced vulnerability detection tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Vikash Kumar Ray",
    py_modules=["skyro"],
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "skyro=skyro:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="security vulnerability scanner web application penetration testing",
)