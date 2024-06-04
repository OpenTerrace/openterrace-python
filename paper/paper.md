---
title: 'OpenTerrace: A fast, flexible and extendable Python framework for thermal energy storage packed bed simulations'
tags:
  - Python
  - Heat transfer
  - Energy storage
  - Packed bed
  - Phase change materials
authors:
  - name: Jakob Hærvig
    orcid: 0000-0001-8710-1610
    affiliation: 1
affiliations:
 - name: Aalborg University, Denmark
   index: 1
date: 11 December 2023
bibliography: paper.bib
---

![](https://raw.githubusercontent.com/OpenTerrace/openterrace-python/main/docs/_figures/logo-openterrace.pdf)

# Summary
`OpenTerrace` is a simulation framework for the prediction of transient temperature responses in thermal energy storage systems. Being able to store energy for extended periods of time is important for modern societies where increasing amounts of energy stem from renewable sources with time-varying production. Many storage technologies exist, each with their own set of disadvantages and advantages. Storing energy in the form of thermal energy is a promising solution because it is cheap and can be scaled up easily. While the total energy content of thermal energy storage systems can be estimated easily, the transient response requires solving partial differential equations in space and time. Using `OpenTerrace` the transient response of a wide range of thermal energy storage systems can be simulated easily. The storage system contains a storage tank filled with a carrier fluid and an optional bed phase. `OpenTerrace` comes with a wide range of predefined substances to be used as either fluid or bed material. Also, `OpenTerrace` ships with a set of primitive, predefined shapes that act as either storage tank or bed material. Besides that a set of predefined boundary conditions and source terms cover many different thermal energy storage applications.

`OpenTerrace` is built to be:

- Fast by making use of modern compilers and optimised tri-diagonal matrix solvers.

- Flexible for easy integration in system models and optimisation loops.

- Extendable by allowing new modules for new materials such as non-spherical rocks or exotic Phase Change Materials (PCM) to easily be plugged into the OpenTerrace framework.

More information about how to get started, along with a user guide, can be found in the [OpenTerrace documentation](https://openterrace.github.io/openterrace-python/). Users may send [pull requests](https://github.com/OpenTerrace/openterrace-python) to have their contributions with new functionality added to the official [OpenTerrace GitHub repository](https://github.com/OpenTerrace/openterrace-python). A set of tutorials is also provided within the framework to highlight its current functionality and to ease the learning curve for new users. Also, various unit tests are provided to verify different parts of the code in some well-defined benchmark cases.

# Statement of need
Research on thermal energy storage systems commonly relies on in-house developed code, which makes the results presented in research papers less transparent and not reproducible. Various models of varying complexity have been proposed in the literature. For a packed bed storage system, @schumann proposed a model that neglects heat conduction in the fluid, between the bed material, and inside the bed material. Later research by @littman included conduction in the fluid and between bed particles, which was shown to be important for low Reynolds number flows. Depending on the Biot number for the bed material, temperature gradients inside the particles may also be important, as shown by @handley. This is especially important when the bed material consists of Phase Change Material (PCM).

`OpenTerrace` is an open-source simulation framework, which aims to provide researchers and decision makers in industry with a common, transparent, open-source framework for simulating thermal energy storage packed bed systems. It includes the possibility to easily include or exclude the above-mentioned effects. It assumes 1D heat transfer in both the fluid and bed phases. Also, 1D heat transfer is assumed inside the bed material. 

The core part of the computations relies on calls to low-level languages using packages such as NumPy [@harris], SciPy [@virtanen] and Numba [@lam] for speed while maintaining the flexibility and user-friendliness of Python. Plotting and animation capabilities rely on Matplotlib [@hunter] and are provided with the framework to allow easy access to visualisations.

# Features and functionality
`OpenTerrace` solves for a fluid phase, which is descretised in `N` nodes. Within each fluid volume element, the bed material is assumed to have the same temperature distribution. The bed material is discretised in `M` nodes, which results in a total of `N x M` equations to be solved at each time step, as \autoref{fig:schematic} shows.

![Right-side figure shows a cylindrical storage tank with four nodes. The bed material in each volume element is assumed to have similar temperature distribution. Left-side figure shows discretisation of the bed material, which in this case is assumed to be a hollow sphere.\label{fig:schematic}](https://raw.githubusercontent.com/OpenTerrace/openterrace-python/main/docs/_figures/schematic.pdf)

Each phase is described by a non-linear, partial differential equation. The phases are coupled using source terms to account for various physical mechanisms such as heat loss and convective heat transfer between the phases. The framework is flexible in such a way that new types of source terms, new domain shape functions, new fluid and bed substances (including phase-changing substances) with both temperature dependent- and independent properties, and new numerical discretisation schemes can be added easily.

# Target Audience
`OpenTerrace` serves different purposes. First and foremost it is a research tool to be used by researchers and industry for design decisions. Also, it has now proven useful in an educational context in which engineering students become familiar with thermal storage systems, test out new ideas or extend the functionality of OpenTerrace.

# Acknowledgements
This research has received funding from EU Horizon project SERENE under grant agreement no. 130930.

# References
