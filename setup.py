from setuptools import setup, find_packages

setup(
    name="smv",
    version="0.1",
    packages=find_packages(),
    install_requires=['click', 'pyyaml', 'pandas', 'requests', 'plotly', 'dash',
                      'dash_core_components', 'datetime>=3.8'],
    package_data={
        'static': ['smv/assets/*']
    }
)