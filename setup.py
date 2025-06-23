#!/usr/bin/env python3
"""
Setup script pour GESTIA
========================

Configuration pour l'installation du package GESTIA.
"""

from setuptools import setup, find_packages
import os

# Lire le contenu du README
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Lire les dépendances
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="gestia",
    version="1.0.0",
    author="Assistant IA",
    author_email="assistant@example.com",
    description="Système de Gestion d'Appareils avec Interface Graphique",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/example/gestia",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "gestia=main:main",
            "gestia-gui=gestia.ui.gui:main",
            "gestia-console=gestia.ui.console:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
) 