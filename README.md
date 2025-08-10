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

**License**

MIT
