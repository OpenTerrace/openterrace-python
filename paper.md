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
date: 01 July 2023
bibliography: paper.bib
---

# Summary

Being able to store energy for extended periods is important for a modern societies where increasing amounts of energy comes from renewable sources with time-varying production. Many storage technologies exist but storing energy in the form of thermal energy is a promising, cheap and efficient solution. 

A fluid is heated up when there is a surplus of electricity and pumped through a storage tank. The storage tank is either empty or filled with a bedding material (known as a packed bed). The bedding material could range from regular, readily available stones to more exotic capsules of phase-change material encapsulated in a plastic shell. In either case the hot fluid transfers energy to the bed material, which then stores the energy in form of sensible and/or latent heat. The process is simply reversed to extract energy from the bed material.

# Statement of need

`OpenTerrace` is a simulation framework for thermal storage packed bed simulations. Prediction temperature profiles in both fluid and bed phases is not straight forward numerically due to the complexity of the physics involved in the way the fluid and bed phases are coupled. The problem is governed by a set of coupled, non-linear, partial differential equations (convection-diffusion). `OpenTerrace` solves the equation set in a numerically efficient manner by calling low-level languages for speed while still maintaining the flexibility and user-friendliness of Python. Users may extend its capabilities by adding new substances (including phase-changing substances) to be used for the fluid or bed phase. Both the storage tank and the bed material may be of different shape and size. The void fraction of the bed material may may vary spatially in the storage tank to account for storage tanks where bed material only occupies the lower 3/4 of the tank.

`OpenTerrace` was designed to be used by both researchers doing research projects, industry making design decisions and engineering students with interests in energy storage who wanted to test out new ideas.

# Mathematics

Single dollars ($) are required for inline mathematics e.g. $f(x) = e^{\pi/x}$

Double dollars make self-standing equations:

$$\Theta(x) = \left\{\begin{array}{l}
0\textrm{ if } x < 0\cr
1\textrm{ else}
\end{array}\right.$$

You can also use plain \LaTeX for equations
\begin{equation}\label{eq:fourier}
\hat f(\omega) = \int_{-\infty}^{\infty} f(x) e^{i\omega x} dx
\end{equation}
and refer to \autoref{eq:fourier} from text.

# Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

If you want to cite a software repository URL (e.g. something on GitHub without a preferred
citation) then you can do it with the example BibTeX entry below for @fidgit.

For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)"

# Figures

Figures can be included like this:
![Caption for example figure.\label{fig:example}](figure.png)
and referenced from text using \autoref{fig:example}.

Figure sizes can be customized by adding an optional second parameter:
![Caption for example figure.](figure.png){ width=20% }

# Acknowledgements

Funding from 
We acknowledge contributions from Brigitta Sipocz, Syrtis Major, and Semyeong
Oh, and support from Kathryn Johnston during the genesis of this project.

# References