from setuptools import setup

requirements = [
    'importlib-metadata; python_version == "3.10"',
    "pyhumps",
    "scikit-learn>=1.1.1",
]

requirements_dev = [
    "black",
    "flake8",
    "isort",
    "jupyter",
    "pre-commit",
    "pytest",
    "pytest-cov",
    "requests",
]

setup(
    name="someproject",
    version="0.2.0",
    description="someproject to help you",
    url="https://github.com/TheErdosInstitute/swe-for-de",
    author="The Erdos Institute",
    packages=["someproject"],
    package_dir={"": "src"},
    install_requires=requirements,
    extras_require={
        "dev": requirements_dev,
    },
)
