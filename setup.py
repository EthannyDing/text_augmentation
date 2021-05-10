from setuptools import find_packages, setup

setup(
    name="text_augmentation",
    version="1.0.0",
    author="Ethan Ding",
    author_email="ethanding1994@gmail.com",
    packages=find_packages(where="."),
    include_package_data=True,
    keywords=["NLP", "data augmentation", "machine learning"]
)
