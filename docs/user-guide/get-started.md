# Getting started with Open Terrace
The complete set of parameters for your simulation is specified in a .yaml input file (see below).
The path to your input file has to be specified relative to the main file `openterrace.py` in the top of the main file. You may additionaly specify a `storagefolder`, which will store your simulation results (default is `'simulations'`).


```python
read_input_data(inputfile='simulations/my_simulation.yaml', storagefolder='simulations')
```

## The Open Terrace input file
Simulation parameters are specified in a .yaml file format. More details on the different options are specified below.

```python
# Define fluid and bed material
fluid: 'water'
solid: 'stone'
```

```python
# Define shape of bed material
shape: 'sphere'
```

```python
# Define size of tank and bed material
h_tank: 5
d_tank: 2
d_particle: 0.02
phi_particle: 0.6
```

```python
# Numerical settings
t_end: 3600
dt: 1
nx_particle: 10
ny_tank: 50
```

```python
# Define transient mass flow rate. Linear interpolation between points.

# First column is time (s)
# Second column is massflow rate (kg/s)
massflow_vs_time:
[
[0,  1],
[900,  1],
[1800,  3],
[3600, 4],
]

# In this example the mass flow rate is 1 kg/s for 15 min. From 15 min to 30 min the mass flow rate ramps up to 3 kg/s. From 30 min to 60 min the mass flow rate ramps up to 4 kg/s.
```

```python
# Define transient tank inlet tamperature. Linear interpolation between points.

# First column is time (s)
# Second column is temperature (K)
inlettemp_vs_time:
[
[0,  573.15],
[1800, 573.15],
[3600, 673.15],
]

# In this example the tamk inlet temperature is 573.15 K for 30 min. From 30 min to 60 min the temperature ramps up to 673.15 K.
```