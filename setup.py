from setuptools import setup

setup(install_requires=[
          'clang',
          'libclang',
          'typer',
          'flask',
          'pyflakes',
          'pyyaml'
      ],
      name = 'roblox-pyc',
      description='A Python, C, C++ to Roblox Lua compiler',
      url="https://github.com/AsynchronousAI/roblox-pyc",
      long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    
    )