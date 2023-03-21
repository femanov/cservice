from setuptools import setup, find_packages

setup(
    name='cservice',
    version='0.10',
    author='Fedor Emanov',
    author_email='femanov@gmail.com',
    description='helper-module to make creation of control-systems daemons easier',
    license='GPL-3.0',
    url='https://github.com/femanov/cservice',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.0',
    install_requires=['pid', 'python-daemon'],
)
