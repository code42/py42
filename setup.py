from codecs import open
from os import path

from setuptools import find_packages
from setuptools import setup

here = path.abspath(path.dirname(__file__))

about = {}
with open(path.join(here, "src", "py42", "__version__.py"), encoding="utf8") as fh:
    exec(fh.read(), about)

with open(path.join(here, "README.md"), "r", "utf-8") as f:
    readme = f.read()

setup(
    name="py42",
    version=about["__version__"],
    url="https://github.com/code42/py42",
    project_urls={
        "Issue Tracker": "https://github.com/code42/py42/issues",
        "Documentation": "https://py42docs.code42.com/",
        "Source Code": "https://github.com/code42/py42",
    },
    description="The Official Code42 Python API Client",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.6, <4",
    install_requires=["requests>=2.4.2"],
    extras_require={
        "dev": [
            "flake8==3.9.2",
            "pytest==6.2.4",
            "pytest-cov==2.12.1",
            "pytest-mock==3.6.1",
            "tox==3.24.0",
        ],
        "docs": [
            "sphinx==4.4.0",
            "myst-parser==0.17.2",
            "sphinx_rtd_theme==1.0.0",
            "docutils == 0.16",
        ],
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)
