import os

from setuptools import setup, find_packages

VERSION = "0.0.4"
DESCRIPTION = "A Python library for streaming video over RTSP"


def long_description(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def requirements(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read().splitlines()


setup(
    name="zephyr-rtsp",
    version=VERSION,
    author="Bintang Pradana Erlangga Putra",
    author_email="<work.bpradana@gmail.com>",
    description=DESCRIPTION,
    long_description=long_description("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/bpradana/zephyr",
    packages=find_packages(),
    install_requires=requirements("requirements.txt"),
    keywords=["python", "rtsp", "streaming", "video"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    license="MIT",
)
