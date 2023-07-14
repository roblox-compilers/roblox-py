---
description: For personal usage so I can remember what commands to use.
---

# Technical Guide

## Local build

* `python3 -m build`
* `pip install dist/roblox_pyc-{version}-py3-none-any.whl --force-reinstall`

## Config

* open setup.cfg
* change version

## Upload (git releases covers this)

* `twine upload dist/*`
