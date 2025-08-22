#!/usr/bin/env python3
"""
Setup script for Generative AI Co-pilot for Embedded Software Design
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ai-embedded-copilot",
    version="0.1.0",
    author="TATA Project Team",
    author_email="team@tata-project.com",
    description="Generative AI Co-pilot for Embedded Software Design in Smart Vehicles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tata-project/ai-embedded-copilot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.4.0",
            "pre-commit>=3.3.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.2.0",
            "mkdocs>=1.5.0",
            "mkdocs-material>=9.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-copilot=ai_copilot.cli:main",
            "embedded-ai=ai_copilot.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "ai_copilot": ["data/*.json", "templates/*.txt", "models/*.pt"],
        "vehicle_context": ["protocols/*.json", "standards/*.yaml"],
    },
)
