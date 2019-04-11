from setuptools import setup

setup(name='taxcalc_helpers',
      version='0.1',
      description='Helpers for Tax-Calculator',
      url='http://github.com/maxghenis/taxcalc-helpers',
      author='Max Ghenis',
      author_email='mghenis@gmail.com',
      license='MIT',
      packages=['taxcalc_helpers'],
      install_requires=[
          'numpy',
          'pandas',
          'taxcalc',
          'matplotlib'
      ],
      zip_safe=False)
