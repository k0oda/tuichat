import os
import setuptools
import tuichat

with open("README.md", "r") as fh:
    long_description = fh.read()


class CleanCommand(setuptools.Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info ./tuichat/__pycache__ ./tuichat/*/__pycache__ ./tuichat/*/*/__pycache__')


setuptools.setup(
    name="tuichat",
    version=tuichat.__version__,
    author="Evgeny Kuleshov",
    author_email="kulevgen32@gmail.com",
    description="A simple messaging program and API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kukree/tuichat",
    download_url="httpsL//github.com/kukree/tuichat/tarball/master",
    packages=setuptools.find_packages(),
    include_package_data=True,
    cmdclass={
      'clean': CleanCommand,
    },
    install_requires=[
        'tqdm',
        'importlib.resources',
        'pyqt5'
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
