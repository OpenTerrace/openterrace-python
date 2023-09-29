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
6. Install pip inside the ``ot`` environment
```bash
conda install pip
```

7. Verify that the right pip version is picked up:
```bash
which pip
```
which should give you something like ``/home/[username]/miniconda3/envs/ot/bin/pip``


8. Finally, install OpenTerrace inside our virtual environment by navigating to the "openterrace-python" folder and install in editable mode by:
```bash
pip install --editable .
```

Now you are ready to run tutorials and modify the OpenTerrace like as you like.