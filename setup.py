import setuptools


with open("README.md", "r") as fh:
    description = fh.read()

setuptools.setup(
    name="pyscript",
    version="0.0.1",
    author="Jamal Al",
    author_email="geenjay51@gmail.com",
    description="JS like simple language LEXER, PARSER and INTERPRETER",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/jay51/pyscript",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
