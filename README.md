# cvp

[![PyPI](https://img.shields.io/pypi/v/cvp?style=flat-square)](https://pypi.org/project/cvp/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cvp?style=flat-square)

Computer Vision Player

![Screenshot](./docs/images/screenshot.jpg)

## Features

* Graph based visual programming
* ONVIF Client
* WsDiscovery
* FFmpeg media player
* Layout management
* Subprocess management
* Window management
* Font browser
* [Planned] Stitching
* [Planned] Labeling
* [Planned] Modeling
* [Planned] Database
* [Planned] CEF

## Developing

```shell
## Create a local Python virtual environment.
./python

## Black formatting
./black.sh

## PEP8 linting
./flake8.sh

## Sort import order
./isort.sh

## Type checking
./mypy.sh

## Unit testing
./pytest.sh
```

## Installation

### from pip

```shell
pip install cvp
```

### from source

```shell
git clone https://github.com/osom8979/cvp "$HOME/.local/share/cvp"
cd "$HOME/.local/share/cvp"
./run
```

## License

See the [LICENSE](./LICENSE) file for details. In summary,
**cvp** is licensed under the **MIT license**.
