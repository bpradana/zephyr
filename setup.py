from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "A Python library for streaming video over RTSP."
LONG_DESCRIPTION = "A Python library for streaming video over RTSP."

setup(
    name="zephyr-rtsp",
    version=VERSION,
    author="Bintang Pradana Erlangga Putra",
    author_email="<work.bpradana@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["opencv-python", "numpy", "tenacity"],
    keywords=["python", "rtsp", "streaming", "video"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
)
