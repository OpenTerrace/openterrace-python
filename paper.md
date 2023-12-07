---
title: 'OpenTerrace: A fast, flexible and extendable Python framework for thermal storage packed bed simulations'
tags:
  - Python
  - Heat transfer
  - Energy storage
  - Packed bed
  - Phase change materials
authors:
  - name: Jakob Hærvig
    orcid: 0000-0001-8710-1610
    equal-contrib: true
affiliations:
 - name: Aalborg University, Denmark
date: 04 October 2023
bibliography: paper.bib
---

# Summary

Being able to store energy for extended periods of time is important for modern societies where increasing amounts of energy comes from renewable sources with time-varying production. Many storage technologies exist, each with their own set of disadvantages and advantages. Storing energy in the form of thermal energy is a promising, cheap and energy efficient solution, which can easily be scaled up.

A fluid is heated up and pumped through a storage tank. The storage tank contains either just a fluid or is filled with a bedding material (known as a packed bed). The bedding material could range from regular, readily available stones to more exotic capsules containing phase-change material encapsulated in a plastic shell. In either case the hot fluid transfers energy to the bed material, which then stores the energy in form of sensible and/or latent heat. The process is simply reversed to extract energy from the bed material and transfer it to the fluid.

![](docs/_figures/logo-banner-paths-grey.svg)

# Statement of need
`OpenTerrace` is an open-source simulation framework providing easy access to complex simulations. The core part of the computations are made by calling low-level languages using packages such as NumPy [@harris], SciPy [@virtanen] and  Numba [@lam] for speed while maintaining the flexibility and user-friendliness of Python. Plotting and animation capabilities based on Matplotlib [@hunter] are provided with the framework to allow easy access to visualisations.

`OpenTerrace` solves for a fluid phase, which is descretised in `N` nodes. For each node, the bed material may be discretised in `M` nodes. The framework allows an arbritrary number of phases to be defined and coupled in different ways. Each phase is described by a non-linear, partial differential equation. These are coupled using source terms to account for various effects such as convection and radiation. The framework is flexible in such a way that new types of source terms, new domain shape functions, new fluid and bed substances (including phase-changing substances) and new numerical discretisation schemes can easily be added. A set of tutorials is also provided with the framework to highlight its current functionality and ease the learning curve for new users. Also various unit tests are provided to verify different parts of the code and its correctness for some well-defined benchmark cases.

![](docs/_figures/schematic.svg)

`OpenTerrace` serves different purposes. First, it was designed to be used by both researchers doing research projects and industry making design decisions. Also, it has now proven useful for engineering students working on semester projects where the learning outcome includes both thermal energy storage knowledge and coding experience with Python.

# Acknowledgements

This research has received funding from EU Horizon project SERENE under
grant agreement no. 130930.

# References

