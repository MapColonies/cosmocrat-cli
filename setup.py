from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="cosmocrat-cli",
    author="MapColonies",
    author_email="mapcolonies@gmail.com",
    description="osm tools wrapper cli",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MapColonies/cosmocrat-cli",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "osmeterium==0.0.3",
        "pytest",
        "mapcoloniesjsonlogger==1.0.0",
        "validators",
    ],
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["cosmocrat=cosmocrat.start:main"]},
)
