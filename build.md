---
description: For personal usage mainly.
---

# Build Guide

## Local build

* `python3 -m build`
* `pip install dist/roblox.py-{version}-py3-none-any.whl --force-reinstall`

## Config

* open setup.cfg
* change version

## Upload (git releases covers this)

* `twine upload dist/*`
