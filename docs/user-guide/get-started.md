# Getting started
With OpenTerrace [installed](../installation.md), you can start setting up your simulation.

## Example of complete simulation
The following shows a complete example of an OpenTerrace simulation setup.

First, we import openterrace and create global parameter:
```python linenums="1"
import openterrace
ot = openterrace.GlobalParameters(t_end=3600*10, dt=0.1, n_fluid=50, n_bed=10)
```

Next, we set up the fluid phase:
```python linenums="3"
ot.fluid.define_substance_on_the_fly(substance='air')
ot.fluid.select_domain(domain='1d_cylinder', D=1, H=5)
ot.fluid.add_porosity(phi=0.4)
ot.fluid.select_schemes(diff='central_difference_1d', conv='upwind_1d')
ot.fluid.initialise(T=273.15+20, mdot=0.1)
ot.fluid.define_bc(bc_type='dirichlet', parameter='T', position=(slice(None, None, None), 0), value=273.15+50)
ot.fluid.define_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), -1))
```

Then, we set up the bed phase in a similar fashion:
```python linenums="10"
ot.bed.select_substance(substance='magnetite)
ot.bed.select_domain(domain='1d_sphere', R=0.005)
ot.bed.select_schemes(diff='central_difference_1d')
ot.bed.initialise(T=273.15+20)
ot.bed.define_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), 0))
ot.bed.define_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), -1))
```

Fianlly, we define the coupling between the phases and run the simulation:
```python linenums="16"
ot.define_coupling(h_coeff='constant', h_value=5)
ot.run_simulation()
```