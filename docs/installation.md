# Installation guide
First make sure you have a working installation of Python. Installing [Miniconda](https://docs.conda.io/en/latest/miniconda.html) is recommended but any Python installation will do. With a working Python installation, you can install OpenTerrace using either conda or pip:

## Option 1: Install using ``conda``

```bash
conda config --add channels conda-forge 
conda config --set channel_priority strict 
conda install openterrace
```

## Option 2: Install using ``pip``

```bash
pip install openterrace
```

# Install in editable mode

If you plan to extend or modify OpenTerrace, you should install it in editable mode. First, using [git](https://git-scm.com) to clone the OpenTerrace GitHub repository
```bash
git clone https://github.com/OpenTerrace/openterrace-python.git
```
Next, navigate to the "openterrace-python" folder and install in editable mode:
```bash
pip install -e .
```