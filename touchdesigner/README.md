# Rotational Seeds viewer

The isolated component `/project1/RotationalSeeds` was installed and tested in
TouchDesigner during the recorded validation. The then-active
`Porous-Lantern.1.toe` project and its folder were preserved; no `.toe` was saved.

For another session, drag `RotationalSeeds.tox` into a network. The component
contains the three recipes, sampling code, controls, materials and its initial
locked point geometry. It does not need the source JSON files to run.
Choose the **Explore** custom page and pulse **Open viewer**.

- **Open Borromean**: m3/M6/q1/8; certified Hausdorff dimension below17/8.
- **Fine Borromean**: m6/M6/q1/8; certified Hausdorff dimension below23/12 and
  topological dimension1.
- **Dense Borromean**: m1/M6/q1/8; certified Hausdorff dimension below3.

All three have exact C3 symmetry and the stated all-scale geometric properties
in their mathematical definitions. The viewer uses **200,000 deterministic
finite point samples**. It is a research preview, not a solid or printable
mesh, a topology certificate, or an infinite-resolution rendering. The live
Magnification control enlarges this finite sample.

Candidate changes regenerate the active geometry. Turn, Tilt, Magnification,
Point size and Slow orbit update the view. After changing **Finite samples**,
pulse **Regenerate samples**. The allowed range is50,000–300,000 points, with
only one candidate's point geometry stored at a time. Sampling arrays are
released after the Script SOP is locked. The seed is20261120.

**Save preview PNG** exports the current1280×1024 TOP to **Preview folder**.
After moving the component to another machine, set that folder to a local
destination. Rendering and candidate selection remain self-contained.

## Rebuild from source

The installer reads the three selected survey JSONs from `../survey` and
embeds them in the component. Run in the TouchDesigner textport or Python MCP:

```python
from pathlib import Path
folder = Path(r"C:/path/to/fractal_discovery_2026/touchdesigner")
namespace = dict(globals(), ROTATIONAL_TD_DIR=folder.as_posix(), __name__="rotational_installer")
exec(compile((folder/"install_viewer.py").read_text(encoding="utf-8"), "install_viewer.py", "exec"), namespace)
receipt = namespace["install"]()
```

Only `/project1/RotationalSeeds` is created or updated. The installer exports
`RotationalSeeds.tox` beside itself; it does not save the surrounding project.

## Observed validation

`validation.json` records200,000 points and distinct nonempty TOP pixel hashes
for all three candidates. Recursive operator errors and warnings were empty,
and the final Script SOP callback had no stderr. The corresponding native
PNG files are included.

`import_validation.json` records a separate import of the exported `.tox`:
200,000 locked points, all three embedded recipes,1280×1024 render resolution,
and no operator errors or warnings. The temporary import was removed. Internal
camera, material, callback, panel and operator references were checked and are
relative, so they do not depend on the original component path.

The `.tox` export is approximately 3 MB. No historical artwork or saved project
was overwritten. At the final publication check, a different project was open
and the local MCP endpoint did not answer. That session was left untouched;
the portable component and the successful recorded import check are the
delivered artifacts, rather than a claim about the currently open project.
