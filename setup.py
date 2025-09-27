import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="sigma-nex",
    version="0.4.0",
    author="Sebastian",
    author_email="rootedlab6@gmail.com",
    description="Agente cognitivo autonomo per la sopravvivenza offline-first in scenari estremi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SebastianMartinNS/SYGMA-NEX",
    project_urls={
        "Documentazione": "https://github.com/SebastianMartinNS/SYGMA-NEX/wiki",
        "Issue Tracker": "https://github.com/SebastianMartinNS/SYGMA-NEX/issues",
    },
    license="CC BY-NC 4.0",
    packages=find_packages(exclude=["tests", "data"]),
    include_package_data=True,
    install_requires=[
        "click",
        "pyyaml",
        "torch",
        "transformers",
        "faiss-cpu",
        "cryptography",
    ],
    entry_points={
        "console_scripts": [
            "sigma=sigma_nex.cli:main",
            "sigma-install-config=scripts.install_global_config:install_global_config",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
    ],
    python_requires=">=3.10",
    extras_require={"ollama": []},  # nota: ollama deve essere installato manualmente
)
