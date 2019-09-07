from setuptools import setup

setup(name='mefipy',
      version='0.1',
      description='A Python library for doing fun Metafilter things',
      url='http://github.com/foxfirefey/mefipy',
      author='foxfirefey',
      author_email='foxfirefey@gmail.com',
      license='MIT',
      packages=['mefipy'],
      install_requires=[
          'requests',
          'beautifulsoup4',
          'lxml',
      ],
      zip_safe=False)
