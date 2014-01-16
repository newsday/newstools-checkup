import os
from setuptools import setup
from pip.req import parse_requirements

install_reqs = parse_requirements("requirements.txt")
reqs = [str(ir.req) for ir in install_reqs]

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

setup(
    name = "newstools-checkup",
    version = "0.8.01",
    packages=['checkup'],
    include_package_data=True,
    license = "MIT",
    description = ("A tool to survey politicians and to visualize their answers"),
    long_description=README,
    url = "http://github.com/newsday/checkup",
    author = "Newsday Investigations Team",
    author_email = "adam.playford@newsday.com",
    keywords = "newstools newsday checkup surveying politicians",
    install_requires=reqs,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
