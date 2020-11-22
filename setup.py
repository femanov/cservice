from setuptools import setup, find_packages

setup(
    name='cservice',
    version='0.1',
    author='Fedor Emanov',
    description='helper-module to make creation of control-systems daemons easier',
    license='',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.0',
    requires=['python-daemon'],
)
