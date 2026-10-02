from setuptools import find_packages, setup


setup(
    name="voe-benchmark",
    version="0.1.0",
    description="A deterministic benchmark for evidence-native company memory",
    package_dir={"": "src"},
    packages=find_packages("src"),
    python_requires=">=3.11",
    entry_points={"console_scripts": ["emb=emb.cli:main"]},
)
