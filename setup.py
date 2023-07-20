from setuptools import setup, find_packages
    
setup(install_requires=[
          'clang',
          'libclang',
          'typer',
          'flask',
          'pyflakes',
          'pyyaml',
          'tqdm',
          'requests'
      ],
      name = 'roblox-pyc',
      description='A Python, Lunar, C, C++ to Roblox Lua compiler',
      url="https://github.com/AsynchronousAI/roblox.pyc",
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      include_package_data=True,
      packages=find_packages(),
      author='roblox-pyc team',
      author_email="roblox.pyc@gmail.com",
      license="GNU AFFERO GENERAL PUBLIC LICENSE",
  )