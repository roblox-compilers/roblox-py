from setuptools import setup

# One up version in setup.cfg
with open("setup.cfg", "r") as f:
    oldcode = f.read()
    version = "1.16.16" # for testing purposes
    f.write(oldcode.replace("version = 1.16.15", "version = {}".format(version)))
    
setup(install_requires=[
          'clang',
          'libclang',
          'typer',
          'flask',
          'pyflakes',
          'pyyaml'
      ],
      name = 'roblox-pyc',
      description='A Python, Lunar, C, C++ to Roblox Lua compiler',
      url="https://github.com/AsynchronousAI/roblox.pyc",
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      include_package_data=True,
    )