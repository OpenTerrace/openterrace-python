# Getting started
With OpenTerrace [installed](../installation.md), you can start setting up your simulation. The following shows a complete example of an OpenTerrace simulation setup.

## Global parameters:
First, we import openterrace and define global parameter such as end time, time step size and number of discretisations for the fluid and bed phases:
```python linenums="1"
import openterrace
ot = openterrace.GlobalParameters(t_end=3600*6, dt=0.025, n_fluid=50, n_bed=5)
```
## Setting up the fluid phase
Next, we select a fluid phase for our simulation. We can either use of the [predefined substances](../fluid_substances/air), e.g.:
```python linenums="3"
ot.fluid.select_substance(substance='air')
```
Next, we choose a [domain shape](../domains/cylinder_1d) for our fluid:
```python linenums="4"
ot.fluid.select_domain_shape(domain='cylinder_1d', D=0.5, H=2)
```
Next, we may choose to fill our domain with some specified porosity (e.g. when a bed material is added). If omitted the fluid phase fully occupies the domain:
```python linenums="5"
ot.fluid.select_porosity(phi=0.4)
```
Next, we choose discretisation schemes for the [diffusion](../diffusion_schemes/central_difference_1d) and [convective](../convection_schemes/upwind_1d) terms:
```python linenums="6"
ot.fluid.select_schemes(diff='central_difference_1d', conv='upwind_1d')
```
Next, we select intial conditions for our simulation:
```python linenums="7"
ot.fluid.select_initial_conditions(T=273.15+50, mdot=0.1)
```
Next, we select boundary conditions. Here we choose a direchlet type for one boundary with a fixed value of 873.15 K and a neumann type for the other boundary:
```python linenums="8"
ot.fluid.select_bc(bc_type='dirichlet', parameter='T', position=(slice(None, None, None), 0), value=273.15+600)
ot.fluid.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), -1))
```

## Setting up the bed phase
Next, we set up the bed phase in a similar fashion. Let's define a custom substance with constant properties:
```python linenums="10"
ot.fluid.select_substance_on_the_fly(rho=5150, cp=1130, k=1.9)
```
We choose a domain shape for the bed phase. Let's assume the bed material consists of spheres with radius of 1 cm:
```python linenums="11"
ot.bed.select_domain_shape(domain='sphere_1d', R=0.01)
```
Let's discretise our spheres using central difference:
```python linenums="12"
ot.bed.select_schemes(diff='central_difference_1d')
```
Let's initialise our bed material with a temperature of 323.15 K:
```python linenums="13"
ot.bed.select_initial_conditions(T=273.15+50)
```
Finally, we select boundary conditions for our bed material. Here we use neumann type boundary conditions (note the first line define the centre of the sphere and the second line define the outer boundary. Also, the coupling between the phases is defined next - in this case a convective coupling).
```python linenums="14"
ot.bed.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), 0))
ot.bed.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), -1))
```

## Phase interactions and post-processing
Fianlly, we define the coupling between the phases and run the simulation. Here we choose convection with a heat transfer coefficient of 20 W/(m^2 K):
```python linenums="16"
ot.select_coupling(h_coeff='constant', h_value=20)
```
Finally, we define how to visualise the results. Here we save results every 6000 timestep (dt=0.025 s) e.g. every 150 s.
```python linenums="17"
ot.animate(save_int=6000, animate_data_flag=True)
```
Finally, we execute the simulation, which will generate animations of the results:
```python linenums="18"
ot.run_simulation()
```