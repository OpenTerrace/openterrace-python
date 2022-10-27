# Installation
First, make sure to have a working installation of Python. 

## Install using PyPi
OpenTerrace is available at the PyPI repository. Do yourself the favour to install it inside a virtual environment to isolate the installation from your system-wide Python installation. 

=== "Windows"

    ``` sh
    python3 -m venv $HOME/openterrace
    $HOME\openterrace\Scripts\activate.bat
    ```

=== "macOS/Linux"

    ``` sh
    python3 -m venv $HOME/openterrace
    source $HOME/openterrace/bin/activate
    ```

Next, use pip to install it inside the virtual environment:

```python
python3 -m pip install openterrace
```