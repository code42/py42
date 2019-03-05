from setuptools import setup, find_packages

setup(
    name='py42',
    version='0.1.0',
    description="Official Code42 API Client",
    packages=find_packages(),
    python_requires='>=2.7, <3',
    install_requires=['requests>=2.3'],
    license='MIT',
)