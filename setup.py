from setuptools import setup

setup(name='skbinday',
      version='1.0.0',
      description='',
      url='',
      author='Ben Cromwell',
      author_email='',
      license='MIT',
      packages=['skbinday'],
      install_requires=[
          'requests',
          'bs4',
      ],
      zip_safe=False,
      entry_points={
          'console_scripts': [
              'skbinday = skbinday.command_line:main'
          ],
      }
)
