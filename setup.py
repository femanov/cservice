from setuptools import setup, find_packages

setup(
    name='cservice',
    version='0.9',
    author='Fedor Emanov',
    description='helper-module to make creation of control-systems daemons easier',
    license='gpl-3.0',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.0',
    install_requires=['pid', 'python-daemon-3K'],
)
