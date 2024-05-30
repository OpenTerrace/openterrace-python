# Installation guide
First make sure you have a working installation of Python. If you have never worked with Python before, it's recommended to install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) alongside with the [Visual Studio Code](https://code.visualstudio.com/) text editor. There are two different ways of installing OpenTerrace depending on how you plan to use it.

## Install OpenTerrace using ``pip`` (for regular users)

```bash
pip install openterrace
```

Pip should resolve all dependencies automatically. For the user interested, a full list of dependencies can be found [here](https://github.com/OpenTerrace/openterrace-python/blob/main/pyproject.toml). 

## Install OpenTerrace in editable mode (for developers)

##### Step 1
If you plan on extending or modifying OpenTerrace, you should install it in editable mode, which makes it easier for you to try out new functionality. First, use any git client such as [GitHub Desktop](https://desktop.github.com/) to clone the OpenTerrace repository. If you already have Conda installed, you may jump to [step 4](#step-4).

##### Step 2
Next, I recommend using Linux or WSL (if on Windows). Inside a linux terminal do:
```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
```

##### Step 3
Then, initialise your conda environment:
```bash
~/miniconda3/bin/conda init bash
```

##### Step 4
Now, open a terminal and create a virtual environment called ``ot``:
```bash
conda create -n ot pip
```

##### Step 5
Activate the virtual environment:
```bash
conda activate ot
```

##### Step 6
Verify that the right pip version is picked up:
```bash
which pip
```
which should give you something like ``/home/[username]/miniconda3/envs/ot/bin/pip``


##### Step 7
Finally, install OpenTerrace inside our virtual environment by navigating to the "openterrace-python" folder and install in editable mode by:
```bash
pip install --editable .
```

##### Step 8
Verify that the ``ot`` virtual environment is picked up as the interpreter in VS Code.

##### Step 9
Now you are ready to run tutorials and modify and extend OpenTerrace as you like.