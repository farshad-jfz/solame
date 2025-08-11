# solame
Solame is a simple Python solar-cell simulator for planar devices which targets teaching the physics of solar cells. 

**Features**

- Optics: Beer–Lambert absorption → generation profile G(x)
- Electrical: ideal-diode J–V with photogeneration
- Outputs: J–V curve, Voc, Jsc, FF, efficiency
- Plots: J–V, generation vs depth

**Limitations**
  
- No interference effects (use TMM in a future version).
- No full drift–diffusion (planned via Sesame).
- Parameters are approximate; tune for your study.

**Contribution**

Issues and PRs are welcome. Focus areas: TMM integration, Sesame coupling, parameter validation, tests, docs.

**Usage Example**

```

import matplotlib.pyplot as plt

from solame import Layer, Device, solve, plot_jv, plot_generation

# Define layers: ETL, absorber, HTL with typical parameters
etl = Layer(name="TiO2", thickness=50e-9, Nd=1e19, Eg=3.2, chi=4.0, epsr=9)
absorber = Layer(name="MAPbI3", thickness=500e-9, Na=1e15, Nd=1e15, Eg=1.55, chi=3.9, epsr=25)
htl = Layer(name="Spiro-OMeTAD", thickness=200e-9, Na=1e19, Eg=3.0, chi=2.2, epsr=3)

# Build device
device = Device([etl, absorber, htl], T=300)

# Run simulation
solve(device)

# Print key performance metrics
print(f"Short-circuit current density: {device.results['jsc']*1e3/1e4:.2f} mA/cm^2")
print(f"Open-circuit voltage: {device.results['voc']:.2f} V")
print(f"Fill factor: {device.results['ff']*100:.1f} %")
print(f"Efficiency: {device.results['efficiency']*100:.1f} %")

# Plot results
fig1, ax1 = plot_jv(device, units="mA/cm^2")
ax1.set_title("J–V Curve")
fig2, ax2 = plot_generation(device)
ax2.set_title("Generation Profile")
plt.show()
```

**License**

MIT
