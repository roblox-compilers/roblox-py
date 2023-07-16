---
description: For personal usage so I can remember what commands to use.
---

# Technical Guide

## Build

* `python3 -m build`
* `pip install dist/roblox_pyc-{version}-py3-none-any.whl --force-reinstall`

## Config

* open setup.cfg
* change version

## Upload

GitHub actions does this whenever a commit is passed on `setup.cfg.`

* `twine upload dist/*`
