import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as r:
    required = r.read().splitlines()

setuptools.setup(
    name="ALaCarte-word-embedding",
    version="1.0.0",
    author="Shirin Dehghani",
    author_email="shirin.dehghani1996@gmail.com",
    description="This is unoffcial implementation of ALC word embedding.",
    long_description=long_description,
    packages=setuptools.find_packages(),
    install_requires=required,
    python_requires='>=3.10.0',
    include_package_data=True
)
