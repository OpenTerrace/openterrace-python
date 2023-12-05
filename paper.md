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

A fluid is heated up and pumped through a storage tank. The storage tank is either empty or filled with a bedding material (known as a packed bed). The bedding material could range from regular, readily available stones to more exotic capsules containing phase-change material encapsulated in a plastic shell. In either case the hot fluid transfers energy to the bed material, which then stores the energy in form of sensible and/or latent heat. The process is simply reversed to extract energy from the bed material and transfer it to the fluid.

![Caption for example figure.\label{fig:example}](docs/_figures/logo-banner-paths-grey.svg)

# Statement of need
Predicting transient temperature profiles in both fluid and bed phases is not straight forward numerically due to the complexity of the physics involved. The problem is governed by a set of coupled, non-linear, partial differential equations (convection-diffusion). The framework allows new shape functions, new substances (including phase-changing substances), new types of source terms and new numerical schemes to easily be added, which makes it a versatile tool to test out new ideas. 

`OpenTerrace` is an open-source simulation framework providing easy access to complex simulations. The core part of the computations are made by calling low-level languages using packages such as NumPy [@harris], SciPy [@virtanen] and  Numba [@lam] for speed while maintaining the flexibility and user-friendliness of Python. Matplotlib [@hunter] is used for static plots and animations.



`OpenTerrace` comes with a range of tutorials that highlights its functionality as well as unittests that verifies code correctness for some well-defined benchmark cases.

`OpenTerrace` serves different purposes. First, it was designed to be used by both researchers doing research projects and industry making design decisions. Also, it has now proven useful for engineering students working on semester projects. Here the framework allows students to gain insight into energy storage while practising Python programming.

# Code structure
The following explains outlines the main structure of `OpenTerrace`. New functionality will be added over time.

# Acknowledgements

This research has received funding from EU Horizon project SERENE under
grant agreement no. 130930.

# References