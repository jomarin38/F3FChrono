import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(
    name='F3FChrono',
    version='0.1',
    scripts=[] ,
    author="",
    author_email="",
    description="F3F Chronometer and race managment app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jomarin38/F3FChrono",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GPL v3",
        "Operating System :: OS Independent",
     ],
    install_requires=[
        'pandas', 'requests', 'pymysql', 'Django'
    ]

 )