from setuptools import setup, find_packages

setup(
    name="lltf-wrapper",
    version="1.0.0",
    author="Evan Bray",
    description="Python wrapper for NKT Photonics Laser Line Tunable Filter (LLTF) DLL",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/evanbray1/LLTF-wrapper",
    packages=find_packages(),
    package_data={
        "lltf_wrapper": ["xml_files/*.xml"],
    },
    install_requires=[
        "numpy",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    python_requires=">=3.8",
)