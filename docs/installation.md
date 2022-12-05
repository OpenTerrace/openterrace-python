# Installation guide
First make sure you have a working installation of Python. If you have never worked with Python before, we recommend installing [Miniconda](https://docs.conda.io/en/latest/miniconda.html) alongside the [Visual Studio Code](https://code.visualstudio.com/) text editor. After selecting Miniconda as the Python interpreter in VS Code, you may now install OpenTerrace using pip:

## Install using ``pip``

```bash
pip install openterrace
```

## Install in editable mode

If you plan to extend or modify OpenTerrace, you should install it in editable mode. First, using [git](https://git-scm.com) to clone the OpenTerrace GitHub repository
```bash
git clone https://github.com/OpenTerrace/openterrace-python.git
```
Next, navigate to the "openterrace-python" folder and install in editable mode:
```bash
pip install -e .
```