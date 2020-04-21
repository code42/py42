from codecs import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

about = {}
with open(path.join(here, "src", "py42", "__version__.py"), encoding="utf8") as fh:
    exec(fh.read(), about)

with open(path.join(here, "README.md"), "r", "utf-8") as f:
    readme = f.read()

setup(
    name="py42",
    version=about["__version__"],
    description="The Official Code42 Python API Client",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages("src"),
    package_dir={"": "src"},
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4",
    install_requires=["requests>=2.3"],
    license="MIT",
    url="https://github.com/code42/py42",
    project_urls={
        "Issue Tracker": "https://github.com/code42/py42/issues",
        "Documentation": "https://py42docs.code42.com/",
        "Source Code": "https://github.com/code42/py42",
    },
    include_package_data=True,
    zip_safe=False,
    extras_require={
        "dev": [
            "pre-commit",
            "pytest==4.6.5",
            "pytest-cov==2.8.1",
            "pytest-mock==2.0.0",
            "recommonmark",
            "sphinx",
            "sphinx_rtd_theme",
            "tox==3.14.3",
        ]
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)
