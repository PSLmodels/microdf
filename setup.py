from setuptools import setup

setup(name='microdf',
      version='0.1',
      description='Survey microdata as DataFrames.',
      url='http://github.com/maxghenis/microdf',
      author='Max Ghenis',
      author_email='mghenis@gmail.com',
      license='MIT',
      packages=['microdf'],
      install_requires=[
          'numpy',
          'pandas',
          'matplotlib',
          'seaborn',
          # 'labellines'  # Causing an error, but works without.
      ],
      extras_require=[
          'taxcalc',
      ],
      zip_safe=False)
