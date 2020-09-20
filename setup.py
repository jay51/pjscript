import setuptools


with open("README.md", "r") as fh:
    description = fh.read()

setuptools.setup(
    name="pjscript",
    version="0.0.4",
    author="Jamal Al",
    author_email="geenjay51@gmail.com",
    description="JS like simple language LEXER, PARSER and INTERPRETER",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/jay51/pjscript",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

# to upload to pypi
# * make sure to change version number
# 1. python setup.py sdist bdist_wheel
# 2. twine upload --skip-existing dist/*
# 3. input username: __token__
# 4. input password: <your token>
