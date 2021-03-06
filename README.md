<h1 align="center">TuiChat</h1>

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/made%20with-Python-1f425f.svg?logo=Python" alt="Built with Python"></a>
  <a href="https://www.gnu.org/licenses/gpl-3.0/"><img src="https://img.shields.io/badge/license-GPLv3-1f425f.svg" alt="License - GNU GPLv3"></a>
  <a href="https://github.com/Kukree/tuichat/contributors/"><img src="https://img.shields.io/github/contributors/Kukree/tuichat.svg?color=1f425f" alt="Contributors"></a>
  <a href="https://github.com/Kukree/tuichat/releases"><img src="https://img.shields.io/github/release/Kukree/tuichat.svg?color=1f425f" alt="Release"></a>
  <img src="https://img.shields.io/github/repo-size/Kukree/tuichat.svg?color=1f425f" alt="Repo size">
  <br>
  <a href="https://github.com/Kukree/tuichat/issues"><img src="https://img.shields.io/github/issues-raw/Kukree/tuichat.svg?color=1f425f" alt="Open issues"></a>
  <a href="https://github.com/Kukree/tuichat/issues?q=is%3Aissue+is%3Aclosed"><img src="https://img.shields.io/github/issues-closed-raw/Kukree/tuichat.svg?color=1f425f" alt="Closed issues"></a>
  <a href="https://github.com/Kukree/tuichat/releases"><img src="https://img.shields.io/github/downloads/Kukree/tuichat/total.svg?color=1f425f" alt="Downloads"></a>
  <a href="https://www.codacy.com/app/Kukree/tuichat?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Kukree/tuichat&amp;utm_campaign=Badge_Grade"><img src="https://api.codacy.com/project/badge/Grade/533f950bb2a44c408198b24e66938d17" alt="Codacy Badge"></a>
</p>
<h3 align="center">A simple messaging program</h3>

---
## Table of Contents
- [Code of Conduct](documentation/CODE_OF_CONDUCT.md)

- **Installing**
  - [Installing (№1) compiled files](#installing-1-compiled-files)
  - [Installing (№2) pip](#installing-2-pip)
  - [Installing (№3) from sources](#installing-3-from-sources)
  - [Installing (№4) compilation guide](#installing-4-compilation-guide)

- **User's manual**
  - [User's manual (host)](#users-manual-host-or-server-holder)
  - [User's manual (client)](#users-manual-client)

- **Configuration**
  - [Configuration file description](#configuration-file-description)

- **Other info**
  - [Contributing](#contributing)
  - [Authors](#authors)
  - [Tools](#built-with)
  - [Versioning](#versioning)
  - [License](#license)

## Getting Started

> These instructions will get you a copy of the project up and running on your local machine for development. See deployment for notes on how to deploy the project on a live system.

### Installing (№1) compiled files

> Go to [releases](https://github.com/Kukree/tuichat/releases)

> Download archive with files and unzip it to any directory

### Installing (№2) pip

> Run this command in your shell:

```Bash
pip install tuichat
```

### Installing (№3) from sources

> Setup Git and type in git bash:

```Bash
git clone https://github.com/Kukree/tuichat
```

> Install [**Python 3**](https://python.org) if not installed or compile program files with your program to compile **(Pyinstaller, wheel, etc)**, the following lines are a program compilation guide

### Installing (№4) compilation guide

> Go to program directory

> Run the following commands one at a time in your shell:

```Bash
pip install pyinstaller

pyinstaller --onedir --onefile server.py

pyinstaller --onedir --onefile client.py
```

### User's manual (host, or server holder)

#### Configure
> Enter settings into **config.json** file and save it

> **config.json**

![Configuring server](https://imgur.com/wlny9ET.gif)

> **Note**: If you have problems with configuring, look at [configuration file description](#configuration-file-description)

> **Note 2**: If you don't want to use **config.json** you can delete it and configure program at startup

#### Running
> Run **server.exe** (on info table you will see information about your server, running port, limit of connections, external IP address, TUI graphics, logging and others)

> Give your **external IP address** to clients and **connection port**, written in server info table

### User's manual (client)

> Run **client.exe**

> Enter **IP address** of server and press **ENTER**

> Enter **connection port** of server and press **ENTER**

> Enjoy :)

![Client connecting](https://imgur.com/OtCQgVH.gif)

---

## Configuration file description

- `max_connections` - Variable used for set a limit of connections to server

- `port` - Port to connect to your server, users will type it in client

- `enable_log` (True/false) - Enable or disable saving logs of messages/connections or disconnections/other things, happened on server

- `enable_ui` (True/false) - Enable or disable special UI symbols, like: logo, lines for highlighting system messages, borders around license block

## Contributing

> To get started...

### Step 1

- **Option 1**
  - 🍴 Fork this repo!

- **Option 2**
  - 👯 Clone this repo to your local machine using `https://github.com/Kukree/tuichat.git`

### Step 2

- **HACK AWAY!** 🔨🔨🔨

### Step 3

- 🔃 Create a new pull request using <a href="https://github.com/joanaz/HireDot2/compare/" target="_blank">`https://github.com/Kukree/tuichat/compare/`</a>.

---

## Built With

- [Python](https://python.org) - Programming language

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/Kukree/tuichat/tags).

## Authors

- **Evgeniy Kuleshov** - *Initial work* - [Greenfield](https://github.com/Kukree)

See also the list of [contributors](https://github.com/Kukree/tuichat/contributors) who participated in this project.

## License

This project is licensed under the GNU GPLv3 - see the [LICENSE](documentation/LICENSE) file for details
