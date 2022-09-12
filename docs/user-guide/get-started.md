# Getting started

When openterrace is installed, you can start setting up your simulation.

## Example of how to setup a simulation
First, we create an instance of the OpenTerrace class. Let's call the instance `ot` and define a simulation time of 7200 s and time step size of 0.01 s.

```python
ot = OpenTerrace(t_end=7200, dt=0.01)
```

Our OpenTerrace class contains a function to define our fluid substance. Let's use air for our simulation:
```python
ot.define_fluid_phase(substance='air')
```    

Likewise, let's define our bed phase. Here we use swedish diabase stone:
```python
ot.define_bed_phase(substance='swedish_diabase')
``` 

Next, we select one of the fluid domain types. Let's simulate flow in a cylinder with a diameter of 0.3 m and height 5 m and let's dicretise it using 200 nodes:
```python
ot.select_fluid_domain(domain='1d_cylinder', D=0.3, H=5, ny=200)
```

Likewise, let's define the bed type. Let's discretise our diabase stones into 10 nodes and assume them to be spherical with a diameter of 1 cm:
```python
ot.select_bed_domain(domain='1d_sphere', D=0.01, n=200)
```    