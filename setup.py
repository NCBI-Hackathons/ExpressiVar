import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="expressivar",
    version="0.0.1",
    author="NCBI-Hackathons",
    author_email="author@example.com",
    description="Package to determine mutations from expressed genes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NCBI-Hackathons/ExpressiVar",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
