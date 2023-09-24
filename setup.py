from setuptools import setup, find_packages

with open('src/find_imdb/requirements.txt') as f:
    REQUIREMENTS = f.readlines()

setup(
    name='find_imdb',
    version='0.1',
    license='MIT',
    author="famgz",
    author_email='famgz@proton.me',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'find_imdb = find_imdb.__main__:main'
        ]
    },
    url='https://github.com/famgz/find_imdb',
    install_requires=REQUIREMENTS
)
