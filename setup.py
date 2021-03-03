from setuptools import setup

setup(
    name="microdf",
    version="0.3.0",
    description="Survey microdata as DataFrames.",
    url="http://github.com/PSLmodels/microdf",
    author="Max Ghenis",
    author_email="max@ubicenter.org",
    license="MIT",
    packages=["microdf"],
    install_requires=[
        "matplotlib",
        "matplotlib-label-lines",
        "numpy",
        "pandas",
        "seaborn",
    ],
    extras_require={"taxcalc": ["taxcalc"]},
    zip_safe=False,
)
