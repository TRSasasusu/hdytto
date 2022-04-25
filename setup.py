# coding: utf-8

import setuptools


with open('README.md', 'r') as f:
    long_description = f.read()

requires = []


setuptools.setup(
    name='hdytto',
    version='0.2.1',
    description='Add not pythonic syntax into your python.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/TRSasasusu/hdytto',
    author='kaito kishi',
    author_email='trsasasusu@gmail.com',
    license='MIT',
    keywords='shell commands alias',
    packages=setuptools.find_packages(),
    install_requires=requires,
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires=">=3.8",
)
