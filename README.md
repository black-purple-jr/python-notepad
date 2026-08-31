# Notepad App

## Overview

This is a simple GUI (Graphical User Interface) made with Python and PySide6 that is identical to Windows 10 Notepad. I published a version in the releases section. [Here is the download link](https://github.com/black-purple-jr/python-notepad/releases/download/v1.0.0/Notepad.exe), It may be heavy, maybe I could remake it later with C++ and Qt, but I'm not doing it for the moment, because I don't know neither C++ or how to use Qt.

## Features

* Saving a new file to your local machine.
* Opening an existing file in the editor.
* Opening a new window while keeping your first window.
* Toggling word wrap.
* Toggling the status bar.
* Adjusting the screen size.
* Switching fonts.
* Keyboard shortcuts.

## Technology Used

![Static Badge](https://img.shields.io/badge/Python-blue?logo=python&logoColor=%233776AB&labelColor=%231F1F1F&color=%233776AB)

## Packages

* `PySide6`: PySide6 is the official Python module from the [Qt for Python project](https://wiki.qt.io/Qt_for_Python), which provides access to the complete Qt 6.0+ framework.

## Quick Start

### Prerequisites

* Git
* Python 3.14.3+

### Installation

#### 1. Clone the repo locally

```bash
git clone https://github.com/black-purple-jr/python-notepad
```

#### 2. Create a virtual environement

```bash
python -m venv .venv
```

#### 3. Activate the virtual environement you created

##### Linux / MacOS

```bash
./.venv/bin/activate
```

##### Windows

```bash
./.venv/scripts/activate
```

#### 4. Install the necessary package

```bash
pip install PySide6
```

#### 5. Run the main file

```bash
python main.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) for details.

## Author

* Abdellah DAKIR ALLAH - a.k.a [black-purple-jr](https://github.com/black-purple-jr) on Github and some other platforms.