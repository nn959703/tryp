try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

requires = ['pandas', 'xlwt', 'psycopg2']

setup(name='tryp',
      version='0.0',
      description='tryp',
      install_requires=requires,
      entry_points={
          'console_scripts': ['trypgen = tryp.tryp:main']
          }
      )
