# User installation
First, make sure to have a working installation of Python. We recommand using [Miniconda](https://docs.conda.io/en/latest/miniconda.html). With a working Python installation, you can install OpenTerrace using either pip or conda:

## Install using ``pip``

```bash
pip install openterrace
```

## Install using ``conda``

```bash
conda config --add channels conda-forge
```
```bash
conda config --set channel_priority strict
```
```bash
conda install -c conda-forge openterrace
```

Next, head to [Getting started](user-guide/get-started.md) to set up your first simulation.