import os

from setuptools import setup, find_packages

VERSION = "0.0.2"
DESCRIPTION = "A Python library for streaming video over RTSP"


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="zephyr-rtsp",
    version=VERSION,
    author="Bintang Pradana Erlangga Putra",
    author_email="<work.bpradana@gmail.com>",
    description=DESCRIPTION,
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/bpradana/zephyr",
    packages=find_packages(),
    install_requires=["opencv-python", "numpy", "tenacity"],
    keywords=["python", "rtsp", "streaming", "video"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    license="MIT",
)
