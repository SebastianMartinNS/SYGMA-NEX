from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name='sigma-nex',
    version='0.3.1',
    author='Sebastian',
    author_email='rootedlab6@gmail.com',
    description='Agente cognitivo autonomo per la sopravvivenza offline-first in scenari estremi',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tuo-username/sigma-nex',
    project_urls={
        'Documentazione': 'https://github.com/tuo-username/sigma-nex/wiki',
        'Issue Tracker': 'https://github.com/tuo-username/sigma-nex/issues',
    },
    license='MIT',
    packages=find_packages(exclude=['tests', 'data']),
    include_package_data=True,
    install_requires=[
        'click',
        'pyyaml',
        'torch',
        'transformers',
        'faiss-cpu',
        'cryptography'
    ],
    entry_points={
        'console_scripts': [
            'sigma=sigma_nex.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
    ],
    python_requires='>=3.10',
    extras_require={
        'ollama': []  # nota: ollama deve essere installato manualmente
    },
)
