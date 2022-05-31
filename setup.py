import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ask_siri",
    version="0.0.3",
    author="Intouch Group",
    author_email="cody.persinger@intouchsol.com",
    description="Siri voice parser using Python3 and Applescript",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://intazdoweb.intouchsol.com/IntouchProduct/Core/_git/ask_siri",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "applescript",
        "keyboard"
    ]
)