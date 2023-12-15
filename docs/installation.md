# Installation guide
First make sure you have a working installation of Python. If you have never worked with Python before, we recommend installing [Miniconda](https://docs.conda.io/en/latest/miniconda.html) alongside the [Visual Studio Code](https://code.visualstudio.com/) text editor. After selecting Miniconda as the Python interpreter in VS Code, you may now install OpenTerrace using pip:

## Install using ``pip``

```bash
pip install openterrace
```

## Install in editable mode

1. If you plan on extending or modifying OpenTerrace, you should install it in editable mode. First, use any git client such as [GitHub Desktop](https://desktop.github.com/) to clone the OpenTerrace repository

2. Next, I recommend using Linux or WSL (if on Windows). Inside a linux terminal do:

```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
```

3. Then, initialise your conda environment:
```bash
~/miniconda3/bin/conda init bash
```

4. Now, reopen your terminal and create a virtual environment called ``ot``:

```bash
conda create -n ot
```

5. Then activate it:
```bash
conda activate ot
```

6. Make sure to use compatible Python version:
```bash
conda install python=3.11
```

7. Install pip inside the ``ot`` environment
```bash
conda install pip
```

8. Verify that the right pip version is picked up:
```bash
which pip
```
which should give you something like ``/home/[username]/miniconda3/envs/ot/bin/pip``


9. Finally, install OpenTerrace inside our virtual environment by navigating to the "openterrace-python" folder and install in editable mode by:
```bash
pip install --editable .
```

10. Verify that the ``ot`` virtual environment is picked up in VS Code.

![Select ot environment](_figures/conda_ot.jpg)

Now you are ready to run tutorials and modify the OpenTerrace like as you like.