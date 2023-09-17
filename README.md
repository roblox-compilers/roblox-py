# Introduction

> **NOTICE:**
> This is the indev build
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-5-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

<div align="center">

<figure><img src=".gitbook/assets/Screenshot 2023-07-10 at 12.06.03 AM.png" alt="" width="375"><figcaption></figcaption></figure>

## Sponsors
<!-- sponsors --><!-- sponsors -->
<sub>0 sadly</sub>

## Contributors 
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/AsynchronousAI"><img src="https://avatars.githubusercontent.com/u/72946059?v=4?s=100" width="100px;" alt="aqzp"/><br /><sub><b>aqzp</b></sub></a><br /><a href="https://github.com/AsynchronousAI/roblox-pyc/commits?author=AsynchronousAI" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/tututuana"><img src="https://avatars.githubusercontent.com/u/51187395?v=4?s=100" width="100px;" alt="tututuana"/><br /><sub><b>tututuana</b></sub></a><br /><a href="https://github.com/AsynchronousAI/roblox-pyc/commits?author=tututuana" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/BazirGames"><img src="https://avatars.githubusercontent.com/u/49544193?v=4?s=100" width="100px;" alt="BazirGames"/><br /><sub><b>BazirGames</b></sub></a><br /><a href="https://github.com/AsynchronousAI/roblox-pyc/issues?q=author%3ABazirGames" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://lawmixerscpf.tk/group"><img src="https://avatars.githubusercontent.com/u/53837083?v=4?s=100" width="100px;" alt="LawMixer"/><br /><sub><b>LawMixer</b></sub></a><br /><a href="https://github.com/AsynchronousAI/roblox-pyc/issues?q=author%3ALawMixer" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/cataclysmic-dev"><img src="https://avatars.githubusercontent.com/u/141081747?v=4?s=100" width="100px;" alt="cataclysmic-dev"/><br /><sub><b>cataclysmic-dev</b></sub></a><br /><a href="https://github.com/AsynchronousAI/roblox-pyc/commits?author=cataclysmic-dev" title="Code">🔨</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
<!-- markdownlint-disable -->

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
</div>


## roblox-pyc

[**Docs**](https://robloxpyc.gitbook.io/roblox-pyc) **|** [**Devforum**](https://devforum.roblox.com/t/roblox-py-python-luau/2457105?u=dev98799) **|** [**Github**](https://github.com/AsynchronousAI/roblox.pyc) **|** [**Tests/Examples**](https://github.com/AsynchronousAI/roblox.py/tree/main/test)

***

Python, C, C++ Compiler for Roblox.

> This has NO RELATION with .pyc files, roblox-py, or roblox-ts

> C/C++ is still in progress.

> Python is fully implemented, all code should work because it supports the dev build of Python 3.13.

***

### Building
```bash
cmake -DCOBALT_INCLUDES=/path/to/cobalt/headers .
make
```
***
### API
```js
var rpyc = import("roblox-pyc"); // #include-ing roblox-pyc/init.cobalt might turn on interface mode and cause issues.
var ast = rpyc->ParseCPP("#include <stdio.h> \n int main() { printf('Hi') return 0; }");
print(rpyc->Generate(ast))
/*
Output:
_G.rpyc.include("stdio.h")

function main()
    printf("Hi")
    return 0
end
*/

```