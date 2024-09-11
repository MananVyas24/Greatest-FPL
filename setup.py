from setuptools import setup, find_packages

setup(
    name="fpl_scoring",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests",
        "beautifulsoup4",
        "pandas",
        "gspread",
        "oauth2client",
    ],
    author="Manan Vyas",
    author_email="test",
    description="A library for FPL scoring and sheet updates",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MananVyas24/Greatest-FPL.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)