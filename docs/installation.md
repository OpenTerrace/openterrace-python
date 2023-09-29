# Installation guide
First make sure you have a working installation of Python. If you have never worked with Python before, we recommend installing [Miniconda](https://docs.conda.io/en/latest/miniconda.html) alongside the [Visual Studio Code](https://code.visualstudio.com/) text editor. After selecting Miniconda as the Python interpreter in VS Code, you may now install OpenTerrace using pip:

## Install using ``pip``

```bash
pip install openterrace
```

## Install in editable mode

1. If you plan to extend or modify OpenTerrace, you should install it in editable mode. First, using [git](https://git-scm.com) to clone the OpenTerrace GitHub repository
```bash
git clone https://github.com/OpenTerrace/openterrace-python.git
```

2. Next, I recommend using Linux or WSL (if in Windows). installing it inside a virtual environment. Install Miniconda by:

```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
```
Then, initialise your conda environment:
```bash
~/miniconda3/bin/conda init bash
```

Now, reopen your terminal and create a virtual environment called ``ot``:

```bash
conda create -n ot
```

Then activate it:
```bash
conda activate ot
```

Next, navigate to the "openterrace-python" folder and install in editable mode:
```bash
pip install --editable .
```