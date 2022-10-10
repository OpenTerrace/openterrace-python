# Getting started

When OpenTerrace is [installed](../installation.md), you can start setting up your simulation.

## Example of complete simulation
The following shows a complete example of an OpenTerrace simulation setup. 

First, we create an instance of the OpenTerrace class:
```python linenums="1"
ot = OpenTerrace(t_end=1800, dt=0.1, n_fluid=10, n_bed=5)
```

Next, we set up the fluid phase:
```python linenums="2"
ot.fluid.select_substance(substance='water')
ot.fluid.select_domain(domain='1d_cylinder', D=1, H=5)
ot.fluid.select_scheme(conv='upwind_1d') #diff='central_difference_1d')
ot.fluid.initialise(T=20+273.15, mdot=1)
ot.fluid.define_bc(bc_type='dirichlet', parameter='T', position=(0,0), value=80+273.15)
ot.fluid.define_bc(bc_type='neumann', parameter='T', position=(0,1))
ot.fluid.update_properties()
```

Then, we set up the bed phase in a similar manner:
```python linenums="9"
ot.bed.select_substance(substance='magnetite')
ot.bed.select_domain(domain='1d_sphere', D=0.05, n=7)
ot.bed.select_scheme(diff='central_difference_1d')
ot.bed.initialise(T=50+273.15)
ot.bed.define_bc(bc_type='neumann', parameter='T', position=(0,0))
ot.bed.define_bc(bc_type='neumann', parameter='T', position=(0,1))
ot.bed.update_properties()
```

Fianlly, we execute the simulation:
```python linenums="16"
ot.run_simulation()
```
## Additional details