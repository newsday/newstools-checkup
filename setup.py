from setuptools import setup

setup(
    name = "newstools-checkup",
    version = "0.8.01",
    author = "Newsday Investigations Team",
    author_email = "adam.playford@newsday.com",
    description = ("A tool to survey politicians and to visualize their answers"),
    license = "MIT",
    keywords = "newstools newsday checkup surveying politicians",
    url = "http://github.com/newsday/checkup",
    packages=['checkup'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
    ],
)
