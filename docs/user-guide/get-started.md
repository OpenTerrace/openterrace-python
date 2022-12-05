# Getting started
With OpenTerrace [installed](../installation.md), you can start setting up your simulation. The following shows a complete example of an OpenTerrace simulation setup.

# Define global parameters
```python linenums="1"
import openterrace
ot = openterrace.Simulate(t_end=3600*6, dt=0.025, n_fluid=50, n_bed=5)
```
Here, we import openterrace and define global parameters that control our simulation. They include:
- ``t_end`` (required): End time of the simulation in seconds
- ``dt`` (required): Time step size in seconds
- ``n_fluid`` (optional): Number of discretisations for the fluid phase (omit if only solving the bed phase)
- ``n_bed`` (optional): Number of discretisations for the bed phase (omit if only solving the fluid phase)

Note, either ``n_fluid`` or ``n_bed`` should be specified. If either is omitted that phase wont be simulated.

# Setup the fluid phase

## 1. Select a fluid
```python linenums="3"
ot.fluid.select_substance(substance='air')
```
- ``substance`` (required): Name of substance for the phase we are defining

We select a substance for our simulation. We can either use of the [predefined substances](../fluid_substances/air) such as ``'air'`` or define one on the fly with temperature-independent properties, e.g.:
```python linenums="4"
ot.fluid.select_substance_on_the_fly(rho=1.2, cp=1000, k=0.06)
```
- ``rho`` (required): Density in kg/m^3
- ``cp`` (required): Specific heat capacity in J/(kg*K)
- ``k`` (required): Thermal conductivity in W/(m*K)

## 2. Select a domain shape
```python linenums="5"
ot.fluid.select_domain_shape(domain='cylinder_1d', D=0.5, H=2)
```
- ``domain`` (required): Domain used for the phase

We choose a domain shape using on of the primivite shapes that come built into OpenTerrace. See [this list](../domains/cylinder_1d) for avialable shapes. Note, each domain will have additional parameters required, e.g. a sphere requires a radius to be defined. You will be prompted to add these if you are missing some.

## 3. Select a porosity (``optional``)
```python linenums="6"
ot.fluid.select_porosity(phi=0.4)
```
- ``phi`` (required): Porosity m^3/m^3 (e.g. set to 0.4 and the fluid only occupies 40% of the volume)

The domain may be only partially filled with fluid as a bed phase occupies some space. This command may be omitted in which case the fluid occupies the whole domain.

## 4. Select discretisation schemes
```python linenums="7"
ot.fluid.select_schemes(diff='central_difference_1d', conv='upwind_1d')
```
- ``diff`` (required): Discretisation scheme for the diffusion term
- ``conv`` (required): Discretisation scheme for the convective term

We choose how to discretise our diffusion and convective terms in our [governing equations](..theory/governing). A list of avialable schemes is avialable here [diffusion schemes](../diffusion_schemes/central_difference_1d) and [convective schemes](../convection_schemes/upwind_1d).

## 5. Select intial conditions
```python linenums="8"
ot.fluid.select_initial_conditions(T=273.15+50, mdot=0.1)
```
- ``T`` (required): Temperature in K
- ``mdot`` (optional): mass flow rate in kg/s

We choose initial conditions for our simulation in terms of temperature and mass flow rate.

## 6. Select boundary conditions
```python linenums="9"
ot.fluid.select_bc(bc_type='dirichlet', parameter='T', position=(slice(None, None, None), 0), value=273.15+600)
ot.fluid.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), -1))
```
- ``bc_type`` (required): Name of the boundary condition type
- ``parameter`` (required): Parameter for which you are specifying boundary condition
- ``position`` (required): Can be either ``(slice(None, None, None), 0)`` for lower bc (e.g. 1d cylinder) or centre boundary (e.g. 1d sphere), or ``(slice(None, None, None), -1)`` for upper bc (e.g. 1d cylinder) or surface boundary (e.g. 1d sphere).
- ``value`` (required): Specifies the value for ``dirichlet`` or ``dirichlet_timevarying`` type bcs. 

# Setup the bed phase
The bed phase is setup in a similar fashion to the fluid phase. An example is given below:

```python linenums="11"
ot.bed.select_substance_on_the_fly(rho=5150, cp=1130, k=1.9)
ot.bed.select_domain_shape(domain='sphere_1d', R=0.01)
ot.bed.select_schemes(diff='central_difference_1d')
ot.bed.select_initial_conditions(T=273.15+50)
ot.bed.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), 0))
ot.bed.select_bc(bc_type='neumann', parameter='T', position=(slice(None, None, None), -1))
```

Note we use neumann type bcs for both boundaries. The coupling between the phases is a source term, which will be added using the ``coupling`` keyword next.

# Define phase interactions and post-processing
```python linenums="17"
ot.select_coupling(h_coeff='constant', h_value=20)
```
- ``h_coeff`` (required): Correlation for the heat transfer coefficient (note currently only ``constant`` is available)
- ``h_value`` (required): Heat transfer coefficient in W/(m^2*K)


```python linenums="18"
ot.output_animation(save_int=6000, file_name='mySimulations')
```
- ``save_int`` (required): Save interval (number of time steps between two successive write outs)
- ``file_name`` (optional): Specfies a filename for the animation

Finally, we define how to visualise the results. Here, we save results every 6000 timestep (dt=0.025 s) e.g. every 150 s.

```python linenums="19"
ot.run_simulation()
```
Finally, we execute the simulation and wait for the results to be generated.
