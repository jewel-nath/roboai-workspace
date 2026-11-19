# Inertials: what to write and where the numbers come from

Part of [ros2-robot-description](../SKILL.md). Every link that moves in a simulator needs an
`<inertial>`. RViz ignores it; Gazebo, MuJoCo, MoveIt's dynamics and any model-based controller do
not.

## What the tag means

```xml
<inertial>
  <origin xyz="0.012 0 0.031" rpy="0 0 0"/>   <!-- centre of mass, in the link frame -->
  <mass value="0.42"/>                         <!-- kg -->
  <inertia ixx="4.1e-4" ixy="-2.0e-6" ixz="1.1e-5"
           iyy="3.8e-4" iyz="0" izz="1.9e-4"/> <!-- kg m^2, about the centre of mass -->
</inertial>
```

- `origin` places the centre of mass (COM) in the link frame. Its `rpy` rotates the frame in which
  the tensor is written; leave it at zero and write the tensor in the link's own axes unless a
  primitive formula is easier in a rotated frame (the wheel in
  [description-package.md](description-package.md) does this).
- The six numbers are the inertia tensor about the COM. `ixy`, `ixz` and `iyz` are the tensor's
  off-diagonal entries, so `ixy = -∫ x·y dm`.
- Units are SI: kg, m, kg·m². CAD tools often report g, mm and g·mm².

## Is it physically possible?

Check every link before simulating:

- `mass > 0`.
- The tensor is symmetric and positive definite: its three principal moments (eigenvalues) are
  all greater than zero.
- Triangle inequality on the principal moments: each one is at most the sum of the other two.
  A box or cylinder formula always passes; hand-typed numbers often fail.
- Plausible size: the equivalent box of the inertia should be about the size of the part.
  Inertias far too large for the mass are common in published URDFs; MuJoCo's docs call this out
  and its viewer can draw the equivalent inertia boxes.
- Avoid placeholder masses and inertias such as `1e-6` on real links: they make physics solvers
  badly conditioned. A link that only marks a frame should have no `<inertial>` and a fixed joint.

A short check with NumPy, given the six values:

```python
import numpy as np

def check_inertia(ixx, iyy, izz, ixy=0.0, ixz=0.0, iyz=0.0):
    tensor = np.array([[ixx, ixy, ixz], [ixy, iyy, iyz], [ixz, iyz, izz]])
    p = np.sort(np.linalg.eigvalsh(tensor))
    assert p[0] > 0, f'not positive definite: {p}'
    assert p[2] <= p[0] + p[1] + 1e-12, f'triangle inequality fails: {p}'
    return p
```

## Primitive shapes

Use the macros in [description-package.md](description-package.md) for links that are close to a
box, cylinder or sphere of uniform density: battery packs, wheels, simple brackets. Use the real
measured mass, not volume times a guessed density, and place the COM where the mass really is.

## From CAD mass properties

1. **One body per link.** Group every part that moves with the link (structure, motor, screws,
   electronics) and give each part its real material or mass. Fasteners and motors are often most
   of the mass.
2. **Model in the link frame.** Put the link's origin at its joint frame, axes as in the URDF,
   or add a coordinate system there. Mass properties must be reported about the COM, in axes
   parallel to the link frame.
3. **Read mass, COM and tensor** and convert the units: g to kg ×1e-3; mm to m ×1e-3;
   g·mm² to kg·m² ×1e-9; kg·mm² to kg·m² ×1e-6.
4. **Check the sign of the products.** FreeCAD (through OpenCASCADE) and trimesh return the tensor
   form that URDF wants. A tool that reports "products of inertia" as `+∫ x·y dm` needs the three
   off-diagonal values negated. If unsure, export an L-shaped test block and compare.
5. **Weigh the real part when you can.** If the scale disagrees with CAD, scale the tensor by
   `measured_mass / cad_mass` (this assumes the mass is spread the way CAD says).
6. **Rotate if the CAD axes differ** from the link axes: `I_link = R · I_cad · Rᵀ`, where `R`'s
   columns are the CAD axes written in link coordinates.

### FreeCAD (headless, `freecadcmd`)

```python
# link_inertia.py - run with: freecadcmd link_inertia.py
import FreeCAD

DOC = '/path/to/my_robot.FCStd'
BODY = 'UpperArm'          # the link's body
FRAME = 'UpperArmFrame'    # a local coordinate system at the link frame, in the same container
MASS_KG = 0.42             # weighed, or the CAD assembly's mass

doc = FreeCAD.openDocument(DOC)
shape = doc.getObject(BODY).Shape.copy()
# Express the geometry in the link frame.
shape.Placement = doc.getObject(FRAME).Placement.inverse().multiply(shape.Placement)
solid = shape.Solids[0]    # one solid per link; fuse the parts first if there are several

# FreeCAD reports mass properties for density 1 in millimetres.
k = MASS_KG / solid.Mass * 1e-6   # density scale, then mm^2 -> m^2
com = solid.CenterOfMass * 1e-3
m = solid.MatrixOfInertia         # about the COM, axes parallel to the link frame
print(f'<origin xyz="{com.x:.6f} {com.y:.6f} {com.z:.6f}" rpy="0 0 0"/>')
print(f'<mass value="{MASS_KG}"/>')
print(f'<inertia ixx="{m.A11 * k:.4e}" ixy="{m.A12 * k:.4e}" ixz="{m.A13 * k:.4e}" '
      f'iyy="{m.A22 * k:.4e}" iyz="{m.A23 * k:.4e}" izz="{m.A33 * k:.4e}"/>')
```

Scaling by `MASS_KG / solid.Mass` assumes one uniform density for the body. For mixed materials,
compute each part separately and combine them with the parallel-axis theorem, or let the CAD tool's
own mass-properties dialog do it.

### A mesh (trimesh)

For a closed (watertight) mesh exported in the link frame:

```python
import trimesh

mesh = trimesh.load('meshes/collision/upper_arm.stl', force='mesh')
mesh.apply_scale(0.001)            # STL in mm -> m; skip if already in metres
assert mesh.is_watertight, 'inertia of an open mesh is meaningless'
mesh.density = 0.42 / mesh.volume  # spread the measured mass uniformly
print('com', mesh.center_mass)
print('inertia about com\n', mesh.moment_inertia)  # axes of the mesh frame
```

## Units and frames, once more

- One wrong unit (mm for m) changes an inertia by 10⁶; a simulated robot then floats, shakes or
  explodes. `gz sdf --inertial-stats model.sdf` (Gazebo) and MuJoCo's equivalent inertia boxes show
  the totals and the shapes at a glance.
- The COM is in the link frame, not the visual mesh frame. If a mesh needs a visual `origin`, the
  inertial `origin` usually needs the same offset.
