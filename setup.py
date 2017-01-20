from setuptools import setup

# Based on
# https://python-packaging.readthedocs.io/en/latest/minimal.html

def readme():
    with open('README.md','r') as fr:
        return fr.read()


setup(name='docker_machinator',
        version='0.1',
        description='A tool for managing docker machines from multiple'
            'workstations',
        long_description=readme(),
        entry_points={
            'console_scripts': [
                'dmachinator = docker_machinator.dmachinator:main',
            ],
        },
        classifiers=[
            'Development Status :: 4 - Beta',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.5',
            'Topic :: Security',
        ],
        keywords='docker machine dmachinator secure on-disk',
        url='https://github.com/realcr/docker_machinator',
        author='real',
        author_email='real@freedomlayer.org',
        license='MIT',
        packages=['docker_machinator'],
        install_requires=[
            'sstash',
        ],
        setup_requires=['pytest-runner'],
        tests_require=['pytest'],
        include_package_data=True,
        zip_safe=False)
