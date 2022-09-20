# Installation

First, make sure to have a working installation of Python. We recommend downloading and installing [Miniconda](https://docs.conda.io/en/latest/miniconda.html). 

OpenTerrace is yet to be released. Once released it will be available by both conda-forge and PyPi:

## Install using conda-forge
With Miniconda installed run the following commands one by one:
```bash
conda config --add channels conda-forge
conda config --set channel_priority strict
conda install openterrace
```

## Install using PyPi
Using pip, OpenTerrace can be installed by:
```bash
pip install openterrace
```