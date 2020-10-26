from setuptools import setup

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='helix-swarm',
    version='0.1.0',
    description='Python client for Perforce Helix Swarm (review board)',
    long_description_content_type='text/markdown',
    long_description=README,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    license='MIT',
    packages=['helixswarm'],
    package_data={
        '': ['py.typed', '*.pyi'],
    },
    author='Petr Belskiy',
    author_email='petr.belskiy@gmail.com',
    keywords=['helix', 'swarm', 'swarm review', 'perforce helix swarm'],
    url='https://github.com/pbelskiy/helix-swarm',
    download_url='https://pypi.org/project/helix-swarm'
)

install_requires = [
    'requests'
]

if __name__ == '__main__':
    setup(install_requires=install_requires,
          python_requires='>=3.5',
          **setup_args)
