from setuptools import find_packages, setup

setup(
    name='py42',
    version='0.1.2',
    description="Official Code42 API Client",
    packages=find_packages(),
    python_requires='>=2.7, <3',
    install_requires=['requests>=2.3'],
    license='MIT',
)
