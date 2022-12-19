from setuptools import find_packages, setup

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [line.strip() for line in open("requirements.txt").readlines()]
requirements = requirements[1:]

requirements_dev = [line.strip() for line in open("requirements-dev.txt").readlines()]

setup(
    name="digitalearth",
    version="0.1.8",
    description="visualization package",
    author="Mostafa Farrag",
    author_email="moah.farag@gmail.come",
    url="https://github.com/MAfarrag/digitalearth",
    keywords=["matplotlib", "maps", "visualization"],
    repository = "https://github.com/MAfarrag/Digital-Earth",
    documentation = "https://Hapi-hm.readthedocs.io/",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/markdown",
    license="GNU General Public License v3",
    zip_safe=False,
    packages=find_packages(include=['digitalearth', 'digitalearth.*']),
    test_suite="tests",
    tests_require=requirements_dev,
    install_requires=requirements,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        "Natural Language :: English",
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Visualization",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
    ],
)
