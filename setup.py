# -*- coding: utf-8 -*-
"""Setuptool config file."""


from os.path import dirname
from os.path import join
from pathlib import Path

from setuptools import find_packages
from setuptools import setup


this_directory = Path(__file__).parent

setup(
    url="",
    author="Ilnur Gumerov",
    maintainer="Ilnur Gumerov",
    name="onekey-python",
    version="0.0.1",
    scripts=[],
    package_data={},
    long_description_content_type="text/markdown",
    include_package_data=True,
    packages=find_packages(),
    long_description=(this_directory / "README.md").read_text(encoding="utf8"),
    install_requires=list(
        open(join(dirname(__file__), "requirements.txt"), "r", encoding="utf8").readlines()  # pylint: disable=R1732
    ),
    extras_require={
        "tools": [
            "twine",
            "black",
            "flake8",
            "pylint",
            "mypy",
            "bump2version",
            "pre-commit",
            "pydocstyle",
            "pycodestyle",
            "python-lsp-server",
            "pylsp-mypy",
            "pyls-isort",
            "mccabe",
            "darglint",
            "flake8-broken-line",
            "flake8-bugbear",
            "flake8-builtins",
            "flake8-comprehensions",
            "flake8-docstrings",
            "flake8-docstrings-complete",
            "flake8-eradicate",
            "flake8-isort",
            "flake8-mutable",
            "flake8-rst-docstrings",
            "flake8-bandit",
            "bandit",
            "vulture",
        ],
        "test": [
            "pytest",
            "pytest-runner",
            "scalene",
            "memory_profiler",
        ],
        "docs": [
            "mkdocs",
            "mkdocstrings",
            "mkdocs-material",
            "mkdocstrings-python-legacy",
        ],
        "disttools": ["pyinstaller"],
    },
    entry_points={
        "console_scripts": [
            "onekey-start=app.main:main",
        ]
    },
    tests_require=["pytest"],
)
