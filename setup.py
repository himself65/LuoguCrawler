from setuptools import setup, find_packages

setup(
    name='LowguBrowser',
    version='0.0.1',
    keywords='luogu reptiles',
    description='Simple reptiles to find visits to Luogu.org',
    license='MIT',
    url='https://www.himself65.com/',
    author='Himself65',
    author_email='himself6565@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=['BeautifulStoneSoup>=4.6.0'],
)