import setuptools
import tuichat

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tuichat",
    version=tuichat.__version__,
    author="Evgeny Kuleshov",
    author_email="kulevgen32@gmail.com",
    description="A simple messaging program and API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kukree/tuichat",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'tqdm',
        'importlib.resources'
    ],
    entry_points={
      'console_scripts': [
          'tuiserver = tuichat.__main__:tuiserver',
          'tuiclient = tuichat.__main__:tuiclient'
      ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Topic :: Communications :: Chat",
    ],
)
