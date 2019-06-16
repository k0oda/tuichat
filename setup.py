import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tuichat",
    version="0.5.1",
    author="Evgeny Kuleshov",
    author_email="kulevgen32@gmail.com",
    description="A simple messaging program and API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kukree/PYChat",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Topic :: Communications :: Chat",
    ],
)
