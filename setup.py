from setuptools import setup, find_packages

setup(
    name="smv",
    version="0.1",
    packages=find_packages(),
    install_requires=['click', 'pyyaml', 'pandas', 'requests'],
    package_data={
        'static': ['smv/assets/*']
    }
)