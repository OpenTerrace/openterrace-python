[![Logo](_figures/logo-banner.png)](#)

OpenTerrace is a pure Python framework for thermal energy storage packed bed simulations. It is built from the ground up to be flexible and extendable on modern Python 3.x with speed in mind. It utilises Nvidia CUDA cores to harness the power of modern GPUs and has automatic fallback to CPU cores.

OpenTerrace uses awesome open-source software such as
[Numba](https://numba.pydata.org), [NumPy](https://numpy.org/) and [SciPy](https://scipy.org/):grey_exclamation:

### [Read the docs](https://openterrace.github.io/openterrace-python/)

## Why OpenTerrace?
- **FAST**  
By making use of modern compilers and optimised tri-diagonal matrix solvers, OpenTerrace approaches the speed of compiled C or FORTRAN code with the added convenience of easy-to-read Python language.

- **FLEXIBLE**  
OpenTerrace is built from the ground up to be flexible for easy integration in system models or optimisation loops.

- **EXTENDABLE**  
Modules for new materials such as non-spherical rocks or exotic Phase Change Materials (PCM) can easily be plugged into the OpenTerrace framework.

## Want to contribute?
Contributions are welcome :pray: Feel free to send pull requests or get in touch with me to discuss how to collaborate. More details in the [docs](https://openterrace.github.io/openterrace-python/).

## Code contributors
* Jakob Hærvig, Associate Professor, AAU Energy, Aalborg University, Denmark