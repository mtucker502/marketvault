from setuptools import setup, find_packages

setup(
    name='marketvault',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/mtucker502/marketvault',
    license='MIT License',
    author='Michael Tucker',
    author_email='github@netzolt.com',
    description='A fast local cache of market data',
    entry_points={
        'console_scripts': 'marketvault = marketvault.cli:cli',
        'marketvault.plugins': 'provider_coinbase = marketvault.providers.coinbase',
    },
    install_requires=[
        "pydantic==1.8.1",
        "PyYAML==5.4.1",
        "typing-extensions==3.7.4.3",
        "multiprocessing-logging==0.3.1",
    ],
    extras_require={
        "dev": ["black", "flake8"]
    }
)
