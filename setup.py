from setuptools import setup, find_packages
from sugarrush import __version__

setup(
  name = 'sugarrush',
  packages = find_packages(),
  include_package_data=True,
  version = __version__,
  license='',
  description = 'Sugar analysis',
  author = 'William Finnigan',
  author_email = 'wjafinnigan@gmail.com',
  url = '',
  download_url = '',
  keywords = ['sugar'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'],
)