# Removed Code — Changes after eb4d57a (reverted)

This file contains all code changes made between commit `eb4d57a` (Mar 18, 2026 — "Add intelligent vertical surface selection in Step 3") and `6d7d9db` (Apr 4, 2026 — HEAD at time of revert).

## Commits Removed (chronological order)

183f5de Merge pull request #1 from JakeWhiteArchitecture/claude/sunform-sun-hours-analysis-N62F0
f0b813b Merge pull request #2 from JakeWhiteArchitecture/claude/sunform-sun-hours-analysis-N62F0
8da7f94 Merge pull request #3 from JakeWhiteArchitecture/claude/sunform-sun-hours-analysis-N62F0
51aad95 Fix logo image paths to use relative URLs for production
564cbbd Merge pull request #4 from JakeWhiteArchitecture/claude/fix-image-path-production-4BKSA
e5994bf Remove shade emitters step and add orientation check modal
8f5e771 Add beta testing feedback wizard for sun position verification
0c60497 Merge pull request #5 from JakeWhiteArchitecture/claude/fix-image-path-production-4BKSA
eda56d2 Move beta feedback button inside the results step section
7a8de51 Allow sun analysis on all mesh layers, not just the topmost surface
d9c1192 Merge pull request #6 from JakeWhiteArchitecture/claude/fix-image-path-production-4BKSA
06e0dfa Fix results step not opening after analysis completes
3cca945 Merge pull request #7 from JakeWhiteArchitecture/claude/fix-image-path-production-4BKSA
9e60f9e Add interval notch markers to color legend key
7c58ea4 Scale legend bar to actual max sun hours across all seasons
3310211 Snap heatmap colors to whole-hour boundaries and add 0.25m grid option
c241e64 Add clickable SunCalc.org link to beta feedback modal
ba8c4ea Update bug report email to sunform@jakewhitearchitecture.com
1359880 Remove jsPDF and Flask from third-party credits list
0d57503 Add mobile slide-out sidebar and scale logo for phone screens
08c7b02 Change beta feedback tolerance from fixed 2° to 1% threshold
21e7475 Add three-tier tolerance: <1% good, 1-2% acceptable, >2% difference
a4a613d Fix email showing UTC instead of local time, handle near-horizon altitude %
3d8cd8a Show UTC offset instead of 'local' in beta feedback email
c8cadb1 Move Site Location to its own wizard step, grey out Run Analysis until area selected
27afe07 Fix GLB normals (single-sided upward) and PDF blank page (centre on heatmap)
baf8cc6 Revert heatmap viewport to DoubleSide, only fix normals in GLB export
f595b06 Fix blank PDF: ortho camera frustum should be symmetric around zero
6430484 Move north arrow down to avoid overlap with coffee button; remove first disclaimer checkbox
2fd7faf Merge pull request #8 from JakeWhiteArchitecture/claude/fix-image-path-production-4BKSA
22c2b51 Replace manual mesh selection with automatic voxel-based sun hours analysis
0187c10 Add orientation step with 2D screenshot preview
9cc7662 Fix missing surfaces: compute world-space centroid and relax normal filter
1f5a9cc Fix normal flipping: use empty-neighbour directions instead of scene centroid
7443875 Fix zero-hour edge cells: remove dot product ray validity check
078871f Fix missing pitched roof surfaces and prefer upward normals at edges
8a027a9 Prioritise topmost upward-facing layer in voxels with overlapping geometry
426844d Add Pyodide + IfcOpenShell for improved geometry processing
6ba99d1 Add manifold check and void removal for IfcOpenShell mesh
c78465d Orient all face normals outward after IfcOpenShell processing
ae5fec7 Fix checkerboard normals: orient per-triangle normals using empty-neighbour reference direction in voxel pipeline (winding-independent)
3be7263 Fix coordinate system mismatch and improve normal orientation
e451052 Fix normal orientation for pitched and vertical surfaces
f312ad7 Add vertex welding and duplicate face removal for continuous mesh
44a9832 Switch IfcOpenShell to per-element meshes instead of merged mesh
7ad0059 Implement dual-geometry architecture: web-ifc for analysis, IfcOpenShell for display
e9a9c31 Add geometry debug console with match statistics and magenta unmatched triangles
c9d90ed Add per-element mesh healing checks with failure notes in debug console
c1ec70b Fix debug console showing in both voxel-only and dual-geometry modes
f54b9f8 Show IfcOpenShell failure reason in debug console when in voxel-only mode
e0c3e1c Capture full Python traceback when IfcOpenShell fails
14d8025 Fix IfcOpenShell iterator: remove unsupported multiprocessing param in wasm
9d75d41 Move IfcOpenShell/Pyodide into a Web Worker to avoid blocking the main thread
0a37481 Wire up ifcos-worker.js: replace inline Pyodide with Web Worker messaging
479aec0 Simplify IfcOpenShell to merge + cull: single outer shell mesh
45a3ee4 Add code.md: complete codebase dump with mesh issue summary
93c1156 Fix ifcos-worker: conservative face culling — only remove exactly-paired interior faces, keep 3+ junction faces
382b5a2 Fix voxel pipeline: restore vertical wall and sloped roof surfaces by fixing normal filter thresholds and upward bias
e150bb8 Fix voxel display: discard off-normal triangles within each voxel cell
2c597ab Fix voxel display: cluster triangles by normal, render only dominant face
52f7eca Fix voxel display: group clipped triangles by dominant facing direction, render only dominant face per cell
a5438a4 Voxel display: coplanar clustering + boundary extraction + ear-clip triangulation — dissolve internal edges, expose genuine mesh holes
550f397 Revert "Voxel display: coplanar clustering + boundary extraction + ear-clip triangulation — dissolve internal edges, expose genuine mesh holes"
5b70ad8 Fix boundary loop winding: directed edge adjacency in traceBoundaryLoops, preserve triangle winding in extractBoundaryEdges
5e4b806 Revert "Fix boundary loop winding: directed edge adjacency in traceBoundaryLoops, preserve triangle winding in extractBoundaryEdges"
20d7e14 Revert: remove coplanar clustering and ear-clip helpers, restore original voxel display loop
fd200d0 Revert to 382b5a2: restore original voxel display loop before clustering changes
d7da9a4 Update code.md: refresh embedded index.html and git history after voxel display reverts
3fcb61b Fix layer selection: apply topmost-layer filter only for upward cells, keep all triangles for wall cells
ecb1928 Filter display triangles using refDir dot product — discard perpendicular slab fragments per cell
6d7d9db Revert "Filter display triangles using refDir dot product — discard perpendicular slab fragments per cell"

## Full Diff (eb4d57a..HEAD)

```diff
diff --git a/app.py b/app.py
index fa10628..4048d02 100644
--- a/app.py
+++ b/app.py
@@ -18,6 +18,11 @@ def logo():
     return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "sunform-logo.png")
 
 
+@app.route("/ifcos-worker.js")
+def ifcos_worker():
+    return send_from_directory(ROOT, "ifcos-worker.js", mimetype="application/javascript")
+
+
 @app.route("/")
 def index():
     resp = make_response(render_template("index.html"))
diff --git a/code.md b/code.md
new file mode 100644
index 0000000..58fc86a
--- /dev/null
+++ b/code.md
@@ -0,0 +1,6849 @@
+# SunForm — Complete Codebase & Mesh Issue Summary
+
+## Table of Contents
+
+1. [Summary of Broken Mesh Issues & IfcOpenShell Attempts](#summary-of-broken-mesh-issues--ifcopenshell-attempts)
+2. [Source Files](#source-files)
+   - [app.py](#apppy) — Flask server
+   - [ifcos-worker.js](#ifcos-workerjs) — IfcOpenShell Web Worker
+   - [sunform_engine.py](#sunform_enginepy) — Python analysis engine
+   - [requirements.txt](#requirementstxt)
+   - [tests/test_sun_engine.py](#teststest_sun_enginepy) — Unit tests
+   - [index.html](#indexhtml) — Main frontend application (5,320 lines)
+3. [Git Commit History (Mesh/IFC-related)](#git-commit-history)
+
+---
+
+## Summary of Broken Mesh Issues & IfcOpenShell Attempts
+
+### The Problem
+
+IFC files contain geometry defined as individual building elements (walls, slabs, roofs, etc.), each modelled independently. When these elements are parsed by **web-ifc** (the client-side IFC parser), they produce individual meshes that:
+
+1. **Have coincident faces at element boundaries** — where a wall meets a slab, both elements contribute a face at the junction, resulting in duplicate interior faces
+2. **Have inconsistent winding order** — different elements may have normals pointing inward vs outward, creating a "checkerboard" normal pattern
+3. **Contain interior voids** — window/door openings and internal cavities create small closed mesh components inside larger ones
+4. **Have non-manifold edges** — some edges are shared by 3+ faces, or only 1 face (boundary edges), making topological analysis unreliable
+5. **Produce degenerate triangles** — zero-area triangles where vertices collapse to the same point
+
+These issues cause problems for:
+- **Heatmap painting**: triangles in the display mesh can't be reliably mapped to analysis voxel cells
+- **Shadow ray casting**: interior faces cause false shadow hits
+- **Normal orientation**: inconsistent normals cause surfaces to appear lit/shaded incorrectly
+- **Visual quality**: magenta "unmatched" triangles appear in the debug console
+
+### What We Tried (Chronological)
+
+#### Attempt 1: Initial IfcOpenShell Integration (commit `426844d`)
+**What**: Added Pyodide + IfcOpenShell running in-browser via WASM to replace/supplement web-ifc geometry processing.
+**Why**: IfcOpenShell provides more robust geometry extraction than web-ifc, particularly for complex IFC schemas.
+**Result**: Got basic geometry extraction working but encountered issues with the merged mesh having broken normals and interior faces.
+
+#### Attempt 2: Manifold Check & Void Removal (commit `6ba99d1`)
+**What**: Implemented full mesh topology analysis:
+- Built edge-face adjacency maps
+- Detected non-manifold edges (shared by != 2 faces) and boundary edges (shared by 1 face)
+- Found connected components via flood-fill face traversal
+- Detected interior void components by ray-casting from component centroid
+- Removed void components (small manifold meshes fully inside larger ones)
+
+**Result**: Successfully identified and removed some void components, but the mesh still had issues with normal orientation and coincident faces between elements.
+
+#### Attempt 3: Orient All Normals Outward (commit `c78465d`)
+**What**: Implemented outward normal orientation using:
+- Ray-cast parity test: shoot ray from face centroid along face normal, count mesh crossings — odd count means normal points inward
+- BFS winding propagation: for manifold components, determine one seed face's correct orientation via ray-cast, then propagate consistent winding to all connected faces through shared edges
+
+**Result**: Worked for simple cases but produced "checkerboard" patterns on complex models where the manifold assumption didn't hold.
+
+#### Attempt 4: Fix Checkerboard Normals (commit `ae5fec7`)
+**What**: Changed normal orientation strategy to use **empty-neighbour reference directions** in the voxel pipeline instead of relying on mesh topology:
+- For each voxel cell, check which of the 6 face-neighbours are empty (not occupied by geometry)
+- Sum the empty directions to get a topological "outward" reference vector
+- Orient each triangle's normal to agree with this reference (independent of mesh winding)
+- Added small upward bias for cells with equal empty above/below
+
+**Result**: Fixed the checkerboard issue. This approach is winding-independent and works regardless of mesh topology quality.
+
+#### Attempt 5: Fix Coordinate System Mismatch (commit `3be7263`)
+**What**: IfcOpenShell uses Z-up coordinates while Three.js uses Y-up. Applied coordinate transform (X stays, Y→Z, Z→-Y) when creating Three.js meshes from IfcOpenShell data.
+**Result**: Fixed geometry appearing rotated/mirrored.
+
+#### Attempt 6: Fix Normal Orientation for Pitched/Vertical Surfaces (commit `e451052`)
+**What**: The empty-neighbour approach with upward bias was incorrectly orienting pitched roof surfaces and vertical walls. Refined the bias strength and direction computation.
+**Result**: Improved but still had edge cases.
+
+#### Attempt 7: Vertex Welding & Duplicate Face Removal (commit `f312ad7`)
+**What**: Implemented vertex welding and face deduplication to make the concatenated IfcOpenShell mesh continuous at element seams:
+- Quantised vertex positions to a 1mm tolerance grid
+- Merged coincident vertices to canonical positions
+- Removed degenerate faces (collapsed vertices)
+- Removed duplicate faces (same 3 vertex indices, regardless of winding)
+
+**Result**: Reduced face count and made the mesh more continuous, but didn't solve the core issue of interior faces between adjacent elements.
+
+#### Attempt 8: Per-Element Meshes (commit `44a9832`)
+**What**: Instead of one merged mesh, kept IfcOpenShell meshes as individual per-element meshes (matching web-ifc's approach).
+**Why**: Thought per-element meshes might avoid the interior face problem.
+**Result**: Per-element meshes had the same interior face issue AND lost the benefit of vertex welding at element boundaries. Reverted.
+
+#### Attempt 9: Dual-Geometry Architecture (commit `7ad0059`)
+**What**: Fundamental architecture change — use **two parallel geometry pipelines**:
+- **web-ifc meshes** (`allMeshes[]`): Used for all analysis (voxel pipeline, ray casting, BVH shadow queries). These are robust and well-tested.
+- **IfcOpenShell meshes** (`analysisMeshes[]`): Used only for display — painted with the analysis results by looking up voxel cell sun hours for each triangle centroid.
+
+**Why**: Decoupled analysis correctness from display quality. Even if IfcOpenShell mesh has issues, analysis results are unaffected.
+**Result**: Analysis became robust. Display quality depends on how well IfcOpenShell triangles map to voxel cells.
+
+#### Attempt 10: Debug Console & Diagnostics (commits `e9a9c31`, `c9d90ed`)
+**What**: Added a geometry debug console showing:
+- Geometry source counts (web-ifc vs IfcOpenShell mesh/triangle counts)
+- Bounding box comparisons between the two pipelines
+- Triangle-to-voxel mapping statistics (exact matches, neighbour matches, misses)
+- Mesh healing notes per element
+- Magenta highlighting for unmatched triangles
+
+**Result**: Made mesh issues visible and diagnosable. Auto-shows when >5% triangles miss or IfcOpenShell errors occur.
+
+#### Attempt 11: Web Worker (commits `9d75d41`, `0a37481`)
+**What**: Moved IfcOpenShell/Pyodide processing into a dedicated Web Worker (`ifcos-worker.js`) to avoid blocking the main thread during the ~10-30 second WASM initialization.
+**Result**: UI stays responsive during IfcOpenShell loading. Worker communicates via postMessage protocol.
+
+#### Attempt 12: Simplified Merge + Cull (commit `479aec0` — current approach)
+**What**: Simplified the IfcOpenShell processing to a clean 4-step pipeline:
+1. **Collect**: Iterate all IFC elements, collect all vertices and face indices with offsets
+2. **Deduplicate vertices**: Snap vertex positions to a 0.1mm grid, merge coincident vertices from different elements
+3. **Cull interior faces**: For each face, compute a sorted vertex-index key. Faces that appear more than once (same 3 vertices = shared interior face between two elements) are ALL removed. Only faces appearing exactly once (outer shell) are kept.
+4. **Pack**: Convert to binary Float32Array/Uint32Array buffers and transfer back to main thread
+
+**Result**: This is the current working approach. The interior face culling works well — shared faces between adjacent elements (e.g. wall-slab junction) appear twice with opposite winding, so sorting their vertex indices produces the same key, and both copies are removed. This leaves only the outer shell. Stats typically show 20-40% of faces removed as interior.
+
+### Current Architecture (as of latest commit)
+
+```
+IFC File
+  ├── web-ifc (client-side) ──→ allMeshes[] ──→ BVH ──→ Shadow Ray Casting ──→ Sun Hours per Voxel Cell
+  │                                                                                      │
+  └── IfcOpenShell (Web Worker) ──→ analysisMeshes[] ──→ Paint triangles with voxel hours ──→ Heatmap Display
+                                          │
+                                    (falls back to web-ifc if IfcOpenShell fails)
+```
+
+### Remaining Known Issues
+
+1. **IfcOpenShell WASM wheel dependency**: The WASM wheel is loaded from `ifcopenshell.github.io` — if this CDN is down or the wheel version becomes incompatible, IfcOpenShell fails silently and falls back to voxel-only display mode.
+
+2. **Triangle-to-voxel mapping misses**: Some IfcOpenShell triangles don't map to any voxel cell (shown as magenta in debug). This happens when:
+   - The IfcOpenShell mesh has slightly different geometry than web-ifc (coordinate precision differences)
+   - Triangle centroids fall in gaps between voxel cells at element boundaries
+
+3. **Non-manifold mesh**: The outer shell after interior face culling is not guaranteed to be manifold. Some edges may still have 1 or 3+ faces. This doesn't affect analysis (which uses web-ifc meshes) but can cause visual artifacts in the heatmap overlay.
+
+4. **Large model performance**: The vertex deduplication and face culling steps run in Python (via Pyodide WASM) which is ~10-50x slower than native. For models with 500K+ faces, this can take 30+ seconds.
+
+---
+
+## Source Files
+
+
+### app.py
+
+```python
+"""
+SunForm — Sun Hours Analysis Tool
+
+Minimal Flask server — just serves the frontend.
+All analysis runs client-side in the browser.
+"""
+
+import os
+
+from flask import Flask, make_response, render_template, send_from_directory
+
+ROOT = os.path.dirname(os.path.abspath(__file__))
+app = Flask(__name__, template_folder=ROOT)
+
+
+@app.route("/sunform-logo.png")
+def logo():
+    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "sunform-logo.png")
+
+
+@app.route("/ifcos-worker.js")
+def ifcos_worker():
+    return send_from_directory(ROOT, "ifcos-worker.js", mimetype="application/javascript")
+
+
+@app.route("/")
+def index():
+    resp = make_response(render_template("index.html"))
+    resp.headers["Cache-Control"] = (
+        "no-store, no-cache, must-revalidate, max-age=0"
+    )
+    resp.headers["Pragma"] = "no-cache"
+    resp.headers["Expires"] = "0"
+    return resp
+
+
+if __name__ == "__main__":
+    app.run(host="0.0.0.0", port=8080, debug=True)
+```
+
+---
+
+### ifcos-worker.js
+
+```javascript
+/*
+ * Web Worker for Pyodide + IfcOpenShell geometry processing.
+ *
+ * Merges all IFC element geometry into a single mesh and culls
+ * duplicate/interior faces (shared between adjacent elements).
+ *
+ * Protocol (postMessage):
+ *   Main → Worker:
+ *     { type: 'init' }                          — start loading Pyodide + IfcOpenShell
+ *     { type: 'process', buffer: ArrayBuffer }   — merge geometry from IFC file
+ *
+ *   Worker → Main:
+ *     { type: 'status',  msg: string }
+ *     { type: 'ready' }
+ *     { type: 'result',  vBuf: ArrayBuffer, fBuf: ArrayBuffer, nv: N, nf: N, stats: {...} }
+ *     { type: 'error',   error: string }
+ */
+
+importScripts('https://cdn.jsdelivr.net/pyodide/v0.26.2/full/pyodide.js');
+
+let pyodide = null;
+
+async function init() {
+    if (pyodide) return;
+
+    postMessage({ type: 'status', msg: 'Loading Python runtime...' });
+
+    pyodide = await loadPyodide({
+        indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.26.2/full/'
+    });
+
+    postMessage({ type: 'status', msg: 'Installing IfcOpenShell...' });
+    await pyodide.loadPackage('micropip');
+    await pyodide.runPythonAsync(`
+import micropip
+await micropip.install("https://ifcopenshell.github.io/wasm-wheels/ifcopenshell-0.8.2+d50e806-cp312-cp312-emscripten_3_1_58_wasm32.whl")
+import ifcopenshell
+import ifcopenshell.geom
+print("IfcOpenShell", ifcopenshell.version, "loaded successfully")
+`);
+
+    postMessage({ type: 'ready' });
+}
+
+async function processIFC(buffer) {
+    await init();
+
+    postMessage({ type: 'status', msg: 'Extracting geometry with IfcOpenShell...' });
+
+    const uint8 = new Uint8Array(buffer);
+    pyodide.globals.set('ifc_bytes', uint8);
+
+    await pyodide.runPythonAsync(`
+import traceback as _tb
+try:
+    import ifcopenshell
+    import ifcopenshell.geom
+    import struct
+    import math
+
+    ifc_data = bytes(ifc_bytes.to_py())
+    tmp_path = '/tmp/model.ifc'
+    with open(tmp_path, 'wb') as f:
+        f.write(ifc_data)
+
+    model = ifcopenshell.open(tmp_path)
+    elem_count = len(model.by_type('IfcProduct'))
+    print(f"IFC schema: {model.schema}, elements: {elem_count}")
+
+    settings = ifcopenshell.geom.settings()
+    settings.set(settings.USE_WORLD_COORDS, True)
+
+    iterator = ifcopenshell.geom.iterator(settings, model)
+
+    # ── Step 1: Collect all verts and faces from all elements ──
+    all_verts = []   # flat list of floats (x,y,z,x,y,z,...)
+    all_faces = []   # flat list of ints (i0,i1,i2,...)
+    vert_offset = 0
+    elem_processed = 0
+
+    if iterator.initialize():
+        while True:
+            shape = iterator.get()
+            geom = shape.geometry
+            verts = geom.verts
+            faces = geom.faces
+            n_verts = len(verts) // 3
+            n_faces = len(faces) // 3
+
+            if n_verts > 0 and n_faces > 0:
+                all_verts.extend(verts)
+                # Offset face indices by current vertex count
+                all_faces.extend(f + vert_offset for f in faces)
+                vert_offset += n_verts
+                elem_processed += 1
+
+            if not iterator.next():
+                break
+
+    total_verts = vert_offset
+    total_faces_before = len(all_faces) // 3
+    print(f"Collected {elem_processed} elements: {total_verts} verts, {total_faces_before} faces")
+
+    # ── Step 2: Deduplicate vertices (snap to grid) ──
+    # Round vertex positions to merge coincident vertices from different elements
+    SNAP = 1e-4  # 0.1mm tolerance
+    inv_snap = 1.0 / SNAP
+    vertex_map = {}   # (rx, ry, rz) -> new_index
+    old_to_new = [0] * total_verts
+    new_verts = []
+    new_idx = 0
+
+    for i in range(total_verts):
+        x = all_verts[i*3]
+        y = all_verts[i*3+1]
+        z = all_verts[i*3+2]
+        key = (round(x * inv_snap), round(y * inv_snap), round(z * inv_snap))
+        if key in vertex_map:
+            old_to_new[i] = vertex_map[key]
+        else:
+            vertex_map[key] = new_idx
+            old_to_new[i] = new_idx
+            new_verts.extend([x, y, z])
+            new_idx += 1
+
+    print(f"Vertex dedup: {total_verts} -> {new_idx}")
+
+    # Remap face indices
+    remapped_faces = [old_to_new[fi] for fi in all_faces]
+
+    # ── Step 3: Cull duplicate faces (interior faces shared between elements) ──
+    # A face shared by two elements appears twice with opposite winding.
+    # We detect faces with the same sorted vertex indices and remove ALL copies
+    # (both sides of interior face).
+    face_count = {}  # sorted tuple -> list of face indices
+    for f in range(total_faces_before):
+        i0 = remapped_faces[f*3]
+        i1 = remapped_faces[f*3+1]
+        i2 = remapped_faces[f*3+2]
+        # Skip degenerate faces
+        if i0 == i1 or i1 == i2 or i0 == i2:
+            continue
+        key = tuple(sorted([i0, i1, i2]))
+        if key not in face_count:
+            face_count[key] = []
+        face_count[key].append(f)
+
+    # Keep only faces that appear exactly once (outer shell)
+    final_faces = []
+    interior_removed = 0
+    for key, indices in face_count.items():
+        if len(indices) == 1:
+            f = indices[0]
+            final_faces.extend([remapped_faces[f*3], remapped_faces[f*3+1], remapped_faces[f*3+2]])
+        else:
+            interior_removed += len(indices)
+
+    total_faces_after = len(final_faces) // 3
+    print(f"Face cull: {total_faces_before} -> {total_faces_after} (removed {interior_removed} interior faces)")
+
+    # ── Step 4: Pack into binary buffers ──
+    _vb = struct.pack(f'{len(new_verts)}f', *new_verts)
+    _fb = struct.pack(f'{len(final_faces)}I', *final_faces)
+    _nv = new_idx
+    _nf = total_faces_after
+    _stats = {
+        'elements': elem_processed,
+        'verts_before': total_verts,
+        'verts_after': new_idx,
+        'faces_before': total_faces_before,
+        'faces_after': total_faces_after,
+        'interior_removed': interior_removed,
+    }
+    _error = None
+
+except Exception as e:
+    _vb = b''
+    _fb = b''
+    _nv = 0
+    _nf = 0
+    _stats = {}
+    _error = _tb.format_exc()
+    print("IfcOpenShell error:", _error)
+`);
+
+    const error = pyodide.globals.get('_error');
+    if (error) {
+        postMessage({ type: 'error', error: String(error) });
+        return;
+    }
+
+    const nv = pyodide.globals.get('_nv');
+    const nf = pyodide.globals.get('_nf');
+
+    // Pull stats
+    const pyStats = pyodide.globals.get('_stats');
+    const stats = pyStats.toJs();
+    pyStats.destroy();
+
+    // Pull binary buffers
+    const vbPy = pyodide.globals.get('_vb');
+    const fbPy = pyodide.globals.get('_fb');
+    const vbRaw = vbPy.toJs();
+    const fbRaw = fbPy.toJs();
+    vbPy.destroy();
+    fbPy.destroy();
+
+    // Create aligned ArrayBuffers
+    const vBuf = new ArrayBuffer(vbRaw.length);
+    new Uint8Array(vBuf).set(vbRaw);
+    const fBuf = new ArrayBuffer(fbRaw.length);
+    new Uint8Array(fBuf).set(fbRaw);
+
+    // Clean up Python globals
+    pyodide.runPython('del _vb, _fb, _nv, _nf, _stats, _error');
+
+    postMessage(
+        { type: 'result', vBuf, fBuf, nv, nf, stats: Object.fromEntries(stats) },
+        [vBuf, fBuf]
+    );
+}
+
+onmessage = async (e) => {
+    try {
+        if (e.data.type === 'init') {
+            await init();
+        } else if (e.data.type === 'process') {
+            await processIFC(e.data.buffer);
+        }
+    } catch (err) {
+        postMessage({ type: 'error', error: String(err) });
+    }
+};
+```
+
+---
+
+### sunform_engine.py
+
+```python
+"""
+SunForm — Pure-Python analysis engine.
+
+Mirrors the client-side JavaScript sun position calculator and ray-triangle
+intersection logic so they can be tested deterministically with pytest.
+"""
+
+import math
+from typing import List, Tuple, Optional
+
+Vec3 = Tuple[float, float, float]
+Triangle = Tuple[Vec3, Vec3, Vec3]
+
+
+# ── Sun Position (Spencer 1971) ──────────────────────────────────────────
+
+def get_day_of_year(year: int, month: int, day: int) -> int:
+    """Day-of-year (1-indexed)."""
+    from datetime import date
+    return (date(year, month, day) - date(year, 1, 1)).days + 1
+
+
+def get_sun_positions(
+    latitude: float, longitude: float,
+    year: int, month: int, day: int,
+    time_step: float = 1.0,
+) -> List[dict]:
+    """Return list of {'azimuth': deg, 'altitude': deg, 'hour': h} dicts."""
+    doy = get_day_of_year(year, month, day)
+    lat_rad = math.radians(latitude)
+
+    B = (doy - 1) * 2 * math.pi / 365
+    decl = (0.006918
+            - 0.399912 * math.cos(B) + 0.070257 * math.sin(B)
+            - 0.006758 * math.cos(2*B) + 0.000907 * math.sin(2*B)
+            - 0.002697 * math.cos(3*B) + 0.00148 * math.sin(3*B))
+
+    eot = 229.18 * (0.000075
+                     + 0.001868 * math.cos(B) - 0.032077 * math.sin(B)
+                     - 0.014615 * math.cos(2*B) - 0.04089 * math.sin(2*B))
+
+    positions = []
+    hour = 0.0
+    while hour < 24.0:
+        solar_time = hour + (eot + 4 * longitude) / 60
+        hour_angle = math.radians((solar_time - 12) * 15)
+
+        sin_alt = (math.sin(lat_rad) * math.sin(decl)
+                   + math.cos(lat_rad) * math.cos(decl) * math.cos(hour_angle))
+        altitude = math.asin(max(-1.0, min(1.0, sin_alt)))
+
+        if altitude > 0:
+            cos_az = ((math.sin(decl) - math.sin(lat_rad) * sin_alt)
+                      / (math.cos(lat_rad) * math.cos(altitude)))
+            azimuth = math.acos(max(-1.0, min(1.0, cos_az)))
+            if hour_angle > 0:
+                azimuth = 2 * math.pi - azimuth
+
+            positions.append({
+                'azimuth': math.degrees(azimuth),
+                'altitude': math.degrees(altitude),
+                'hour': hour,
+            })
+
+        hour += time_step
+
+    return positions
+
+
+def sun_direction(azimuth_deg: float, altitude_deg: float) -> Vec3:
+    """Convert azimuth/altitude to a Three.js direction vector (X, Y, Z).
+
+    Azimuth convention: 0°=North, 90°=East, 180°=South, 270°=West (CW from North).
+    """
+    az = math.radians(azimuth_deg)
+    alt = math.radians(altitude_deg)
+    ifc_x = math.sin(az) * math.cos(alt)
+    ifc_y = math.cos(az) * math.cos(alt)
+    ifc_z = math.sin(alt)
+    # Three.js: X=east, Y=up, Z=-north
+    length = math.sqrt(ifc_x**2 + ifc_z**2 + ifc_y**2)
+    return (ifc_x / length, ifc_z / length, -ifc_y / length)
+
+
+# ── Ray-Triangle Intersection (Möller-Trumbore) ─────────────────────────
+
+def ray_triangle_intersect(
+    origin: Vec3, direction: Vec3, tri: Triangle, eps: float = 1e-10
+) -> Optional[float]:
+    """Return hit distance t, or None if miss."""
+    (ax, ay, az), (bx, by, bz), (cx, cy, cz) = tri
+    dx, dy, dz = direction
+
+    e1x, e1y, e1z = bx-ax, by-ay, bz-az
+    e2x, e2y, e2z = cx-ax, cy-ay, cz-az
+    px = dy*e2z - dz*e2y
+    py = dz*e2x - dx*e2z
+    pz = dx*e2y - dy*e2x
+    det = e1x*px + e1y*py + e1z*pz
+    if abs(det) < eps:
+        return None
+    inv_det = 1.0 / det
+    tx, ty, tz = origin[0]-ax, origin[1]-ay, origin[2]-az
+    u = (tx*px + ty*py + tz*pz) * inv_det
+    if u < 0 or u > 1:
+        return None
+    qx = ty*e1z - tz*e1y
+    qy = tz*e1x - tx*e1z
+    qz = tx*e1y - ty*e1x
+    v = (dx*qx + dy*qy + dz*qz) * inv_det
+    if v < 0 or u + v > 1:
+        return None
+    t = (e2x*qx + e2y*qy + e2z*qz) * inv_det
+    if t > 1e-4:
+        return t
+    return None
+
+
+def ray_hits_any_triangle(
+    origin: Vec3, direction: Vec3, triangles: List[Triangle]
+) -> bool:
+    """Return True if the ray hits any triangle in the list."""
+    for tri in triangles:
+        if ray_triangle_intersect(origin, direction, tri) is not None:
+            return True
+    return False
+
+
+# ── Simple Grid Analysis ─────────────────────────────────────────────────
+
+def compute_sun_hours_flat_grid(
+    ground_y: float,
+    grid_min_x: float, grid_min_z: float,
+    grid_max_x: float, grid_max_z: float,
+    grid_size: float,
+    shadow_triangles: List[Triangle],
+    sun_positions: List[dict],
+    time_step: float,
+) -> dict:
+    """
+    Simplified flat-grid analysis for testing.
+    Returns dict mapping (col, row) -> sun_hours.
+    """
+    results = {}
+    col_start = int(math.floor(grid_min_x / grid_size))
+    col_end = int(math.ceil(grid_max_x / grid_size))
+    row_start = int(math.floor(grid_min_z / grid_size))
+    row_end = int(math.ceil(grid_max_z / grid_size))
+
+    sun_dirs = [sun_direction(sp['azimuth'], sp['altitude']) for sp in sun_positions]
+
+    for col in range(col_start, col_end):
+        for row in range(row_start, row_end):
+            cx = (col + 0.5) * grid_size
+            cz = (row + 0.5) * grid_size
+            origin = (cx, ground_y + 0.01, cz)  # 10mm above ground
+            hours = 0.0
+            for sd in sun_dirs:
+                if not ray_hits_any_triangle(origin, sd, shadow_triangles):
+                    hours += time_step
+            results[(col, row)] = hours
+
+    return results
+
+
+def compute_sun_hours_array_style(
+    cells: List[Vec3],
+    shadow_triangles: List[Triangle],
+    sun_positions: List[dict],
+    time_step: float,
+    batch_size: int = 2000,
+) -> List[float]:
+    """
+    Mirrors the exact JS loop structure in runTerrainAnalysis():
+    - Shared array initialized once to zeros
+    - Outer loop: sun positions
+    - Inner loop: cells in batches
+    - Accumulation via array[j] += time_step
+
+    This catches bugs the dict-style function cannot: accidental resets
+    inside the sun loop, batch-boundary resets, overwrite vs accumulate.
+    """
+    n = len(cells)
+    cell_sun_hours = [0.0] * n  # mirrors Float32Array init
+
+    sun_dirs = [sun_direction(sp['azimuth'], sp['altitude']) for sp in sun_positions]
+
+    for sun_idx in range(len(sun_dirs)):
+        dx, dy, dz = sun_dirs[sun_idx]
+
+        for i in range(0, n, batch_size):
+            end = min(i + batch_size, n)
+
+            for j in range(i, end):
+                ox, oy, oz = cells[j]
+                if not ray_hits_any_triangle(
+                    (ox, oy + 0.01, oz), (dx, dy, dz), shadow_triangles
+                ):
+                    cell_sun_hours[j] += time_step
+
+    return cell_sun_hours
+```
+
+---
+
+### requirements.txt
+
+```
+flask>=3.0
+```
+
+---
+
+### tests/test_sun_engine.py
+
+```python
+"""
+Deterministic unit tests for the SunForm analysis engine.
+
+All tests use known geometry, known sun positions, and known expected answers.
+No external API calls, no randomness.
+
+Run with: python -m pytest tests/ -v   (from project root)
+    or:   python3 tests/test_sun_engine.py   (standalone)
+"""
+
+import math
+import sys
+import os
+import pytest
+
+# Ensure the project root is on sys.path so `sunform_engine` can be imported
+# regardless of whether we run via pytest from root or python3 from tests/
+sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
+
+from sunform_engine import (
+    get_sun_positions,
+    sun_direction,
+    ray_triangle_intersect,
+    ray_hits_any_triangle,
+    compute_sun_hours_flat_grid,
+    compute_sun_hours_array_style,
+)
+
+
+# ── Helpers: programmatic test geometry ──────────────────────────────────
+
+def make_box_triangles(cx, cy, cz, sx, sy, sz):
+    """Create 12 triangles forming an axis-aligned box centred at (cx,cy,cz)
+    with half-extents (sx,sy,sz)."""
+    x0, x1 = cx - sx, cx + sx
+    y0, y1 = cy - sy, cy + sy
+    z0, z1 = cz - sz, cz + sz
+
+    # 8 corners
+    v = [
+        (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),  # back face
+        (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1),  # front face
+    ]
+
+    # 6 faces x 2 triangles = 12
+    faces = [
+        # back
+        (v[0], v[1], v[2]), (v[0], v[2], v[3]),
+        # front
+        (v[4], v[6], v[5]), (v[4], v[7], v[6]),
+        # left
+        (v[0], v[3], v[7]), (v[0], v[7], v[4]),
+        # right
+        (v[1], v[5], v[6]), (v[1], v[6], v[2]),
+        # bottom
+        (v[0], v[4], v[5]), (v[0], v[5], v[1]),
+        # top
+        (v[3], v[2], v[6]), (v[3], v[6], v[7]),
+    ]
+    return faces
+
+
+def make_wall_triangles(x, z0, z1, y0, y1, thickness=0.1):
+    """Create a thin wall along X=x from z0..z1, y0..y1."""
+    return make_box_triangles(x, (y0+y1)/2, (z0+z1)/2,
+                              thickness/2, (y1-y0)/2, (z1-z0)/2)
+
+
+# ── Geometry fixture validation (runs first — prerequisite for all) ──────
+
+class TestGeometryFixtures:
+    """Validate that test geometry helpers produce genuinely opaque objects.
+    These must pass before any shadow/accumulation test is meaningful."""
+
+    def test_box_is_opaque_to_axis_aligned_rays(self):
+        """Rays through the centre of a box must hit. Rays that miss must miss."""
+        box = make_box_triangles(0, 5, 0, 2, 5, 2)  # 4x10x4 box at origin
+
+        # Ray from below pointing up through centre — must hit bottom face
+        assert ray_hits_any_triangle((0, -1, 0), (0, 1, 0), box), \
+            "Ray through box centre should hit — box may have gaps"
+
+        # Ray from left pointing right through centre — must hit left face
+        assert ray_hits_any_triangle((-5, 5, 0), (1, 0, 0), box), \
+            "Ray through box side should hit"
+
+        # Ray from front pointing back through centre — must hit front face
+        assert ray_hits_any_triangle((0, 5, 5), (0, 0, -1), box), \
+            "Ray through box front should hit"
+
+        # Ray that clearly misses — must NOT hit
+        assert not ray_hits_any_triangle((10, 10, 10), (0, 1, 0), box), \
+            "Ray missing box should not hit"
+        # Ray parallel to a face but offset — should miss
+        assert not ray_hits_any_triangle((0, -1, 0), (1, 0, 0), box), \
+            "Ray parallel to box below it should not hit"
+
+    def test_box_blocks_diagonal_rays(self):
+        """Diagonal rays that pass through the box must hit."""
+        box = make_box_triangles(0, 5, 0, 3, 5, 3)
+        # Diagonal from far away toward box centre
+        dx, dy, dz = 0 - (-20), 5 - 20, 0 - (-20)
+        length = math.sqrt(dx*dx + dy*dy + dz*dz)
+        d = (dx/length, dy/length, dz/length)
+        assert ray_hits_any_triangle((-20, 20, -20), d, box), \
+            "Diagonal ray toward box centre should hit"
+
+    def test_box_all_6_faces_opaque(self):
+        """Verify rays hit from all 6 axis directions — no face has wrong winding."""
+        box = make_box_triangles(0, 0, 0, 1, 1, 1)  # 2x2x2 cube at origin
+        # +X, -X, +Y, -Y, +Z, -Z
+        directions = [
+            ((-5, 0, 0), (1, 0, 0)),   # from -X toward +X
+            ((5, 0, 0), (-1, 0, 0)),   # from +X toward -X
+            ((0, -5, 0), (0, 1, 0)),   # from -Y toward +Y
+            ((0, 5, 0), (0, -1, 0)),   # from +Y toward -Y
+            ((0, 0, -5), (0, 0, 1)),   # from -Z toward +Z
+            ((0, 0, 5), (0, 0, -1)),   # from +Z toward -Z
+        ]
+        for origin, direction in directions:
+            assert ray_hits_any_triangle(origin, direction, box), \
+                f"Ray from {origin} dir {direction} should hit box — face may have wrong winding"
+
+
+# ── Test A: Unobstructed flat plane ──────────────────────────────────────
+
+class TestUnobstructed:
+    """Flat 10m x 10m ground, no buildings. Every cell should receive sun."""
+
+    def test_all_cells_receive_sun(self):
+        sun_pos = get_sun_positions(51.5, -0.1, 2024, 3, 21, time_step=1.0)
+        assert len(sun_pos) > 0, "Must have sun positions above horizon"
+
+        results = compute_sun_hours_flat_grid(
+            ground_y=0.0,
+            grid_min_x=0, grid_min_z=0,
+            grid_max_x=10, grid_max_z=10,
+            grid_size=1.0,
+            shadow_triangles=[],  # NO obstacles
+            sun_positions=sun_pos,
+            time_step=1.0,
+        )
+
+        for key, hours in results.items():
+            assert hours > 0, f"Cell {key} should receive sunlight but got {hours}h"
+            assert hours == len(sun_pos) * 1.0, \
+                f"Cell {key} should get {len(sun_pos)}h but got {hours}h"
+
+
+# ── Test B: Single box, sun at 45° due south ────────────────────────────
+
+class TestSingleBoxShadow:
+    """10m cube at origin, sun from due south at 45° altitude.
+    Shadow should extend exactly 10m in the -Z direction from the box."""
+
+    def test_shadow_extends_north(self):
+        # 10m cube centred at (0, 5, 0) — half-extent 5m each axis
+        box = make_box_triangles(0, 5, 0, 5, 5, 5)
+
+        # Single sun position: azimuth 180° (due south), altitude 45°
+        sun_pos = [{'azimuth': 180.0, 'altitude': 45.0, 'hour': 12}]
+
+        # Sun direction is (0, 0.707, 0.707) — comes from +Z side.
+        # Shadow extends in -Z. At 45°, shadow length = building height = 10m.
+        # Box north face at z=-5, so shadow covers z from -5 to -15.
+
+        results = compute_sun_hours_flat_grid(
+            ground_y=0.0,
+            grid_min_x=-20, grid_min_z=-25,
+            grid_max_x=20, grid_max_z=20,
+            grid_size=1.0,
+            shadow_triangles=box,
+            sun_positions=sun_pos,
+            time_step=1.0,
+        )
+
+        # 1) Cells under the box footprint (x: -5..5, z: -5..5) must be shaded
+        for col in range(-5, 5):
+            for row in range(-5, 5):
+                assert results[(col, row)] == 0.0, \
+                    f"Cell ({col},{row}) under box should be in shadow, got {results[(col,row)]}h"
+
+        # 2) Cells in the shadow zone (x: -4..4, z: -14..-6) must be shaded
+        #    Using x range -4..4 (centres -3.5..3.5) to stay well within box width
+        shadow_cells_checked = 0
+        for col in range(-4, 4):
+            for row in range(-14, -5):  # centres at z=-13.5 to z=-4.5
+                assert results[(col, row)] == 0.0, \
+                    f"Cell ({col},{row}) in shadow zone (z={row+0.5}) should be shaded"
+                shadow_cells_checked += 1
+        assert shadow_cells_checked > 0
+
+        # 3) Cells BEYOND the 10m shadow (z < -16, with margin) must be LIT
+        for col in range(-3, 3):
+            for row in range(-24, -17):  # centres at z=-23.5 to z=-16.5
+                assert results[(col, row)] == 1.0, \
+                    f"Cell ({col},{row}) beyond shadow (z={row+0.5}) should be lit"
+
+        # 4) Cells on the sun side (south / +Z) should be lit
+        for col in range(-3, 3):
+            for row in range(10, 15):
+                assert results[(col, row)] == 1.0, \
+                    f"Cell ({col},{row}) south of box should be lit"
+
+
+# ── Test C: Complete enclosure ───────────────────────────────────────────
+
+class TestEnclosure:
+    """Deep courtyard — 50m walls on all sides. Centre cells get near-zero."""
+
+    def test_courtyard_shaded(self):
+        # 4 walls forming a 20m x 20m courtyard, 50m tall
+        # Walls at x/z = ±10, height 0..50
+        walls = []
+        walls += make_box_triangles(0, 25, -10, 10, 25, 0.5)  # north wall (z=-10)
+        walls += make_box_triangles(0, 25, 10, 10, 25, 0.5)   # south wall (z=+10)
+        walls += make_box_triangles(-10, 25, 0, 0.5, 25, 10)  # west wall
+        walls += make_box_triangles(10, 25, 0, 0.5, 25, 10)   # east wall
+
+        # Winter sun — low angle (max altitude ~15° at London solstice)
+        sun_pos = get_sun_positions(51.5, -0.1, 2024, 12, 21, time_step=1.0)
+        assert len(sun_pos) > 0
+
+        results = compute_sun_hours_flat_grid(
+            ground_y=0.0,
+            grid_min_x=-5, grid_min_z=-5,
+            grid_max_x=5, grid_max_z=5,
+            grid_size=2.0,
+            shadow_triangles=walls,
+            sun_positions=sun_pos,
+            time_step=1.0,
+        )
+
+        max_possible = len(sun_pos) * 1.0
+
+        # Centre cell must be fully shaded — 50m walls with ~15° max sun angle
+        # means shadow length ≈ 50/tan(15°) ≈ 186m, far exceeding courtyard width
+        centre_hours = results.get((0, 0), 0)
+        assert centre_hours == 0.0, \
+            f"Centre of 50m-deep courtyard in winter should get 0h, got {centre_hours}h"
+
+        # ALL cells inside the courtyard must be fully shaded
+        for key, hours in results.items():
+            assert hours == 0.0, \
+                f"Cell {key} in deep courtyard should get 0h, got {hours}h"
+
+
+# ── Test D: Sun below horizon filtered ───────────────────────────────────
+
+class TestBelowHorizon:
+    """Sun positions with negative altitude should be skipped entirely."""
+
+    def test_negative_altitude_skipped(self):
+        # At the North Pole in December, sun never rises
+        sun_pos = get_sun_positions(89.0, 0.0, 2024, 12, 21, time_step=1.0)
+        assert len(sun_pos) == 0, \
+            f"North pole in December should have no sun above horizon, got {len(sun_pos)}"
+
+
+# ── Test E: Sun directly overhead ────────────────────────────────────────
+
+class TestDirectlyOverhead:
+    """Sun at altitude ~90° — shadow has near-zero length, only footprint is shaded."""
+
+    def test_overhead_sun_no_shadow_extension(self):
+        # 2m x 2m box, 5m tall, centred at x=5, z=5
+        # Footprint: x in [4, 6], z in [4, 6]
+        box = make_box_triangles(5, 2.5, 5, 1, 2.5, 1)
+
+        sun_pos = [{'azimuth': 180.0, 'altitude': 89.9, 'hour': 12}]
+
+        results = compute_sun_hours_flat_grid(
+            ground_y=0.0,
+            grid_min_x=0, grid_min_z=0,
+            grid_max_x=10, grid_max_z=10,
+            grid_size=1.0,
+            shadow_triangles=box,
+            sun_positions=sun_pos,
+            time_step=1.0,
+        )
+
+        # At 89.9°, shadow length = 5/tan(89.9°) ≈ 0.009m — negligible.
+        # Only footprint cells should be shaded. Footprint covers x=[4,6], z=[4,6].
+        # Grid cells (col, row) with centres at (col+0.5, row+0.5):
+        # Footprint cells: col=4 (cx=4.5), col=5 (cx=5.5), row=4 (cz=4.5), row=5 (cz=5.5)
+        footprint_cells = {(4, 4), (4, 5), (5, 4), (5, 5)}
+
+        # All cells far from footprint must be lit (check a comprehensive set)
+        for col in range(0, 10):
+            for row in range(0, 10):
+                if (col, row) not in footprint_cells:
+                    assert results[(col, row)] == 1.0, \
+                        f"Cell ({col},{row}) outside footprint should be lit, got {results[(col,row)]}h"
+
+        # Footprint cells must be shaded
+        for cell in footprint_cells:
+            assert results[cell] == 0.0, \
+                f"Footprint cell {cell} should be shaded, got {results[cell]}h"
+
+
+# ── Test F: Known shadow length at specific angle ────────────────────────
+
+class TestKnownShadowLength:
+    """5m tall box, sun at 30° altitude from due south.
+    Shadow length = 5 / tan(30°) ≈ 8.66m in the -Z direction."""
+
+    def test_shadow_length(self):
+        # 2m x 2m box, 5m tall at origin (x: -1..1, y: 0..5, z: -1..1)
+        box = make_box_triangles(0, 2.5, 0, 1, 2.5, 1)
+
+        sun_pos = [{'azimuth': 180.0, 'altitude': 30.0, 'hour': 12}]
+        expected_shadow_len = 5.0 / math.tan(math.radians(30.0))  # ≈ 8.66m
+
+        # Shadow extends in -Z from z=-1 (north face), so tip at z = -1 - 8.66 = -9.66
+        results = compute_sun_hours_flat_grid(
+            ground_y=0.0,
+            grid_min_x=-10, grid_min_z=-15,
+            grid_max_x=10, grid_max_z=15,
+            grid_size=1.0,
+            shadow_triangles=box,
+            sun_positions=sun_pos,
+            time_step=1.0,
+        )
+
+        # 1) Cell under the box must be shaded
+        assert results[(0, 0)] == 0.0, "Cell under box should be shaded"
+
+        # 2) Cell in the middle of the shadow zone (z ≈ -5) must be shaded
+        #    Centre of cell (0, -5) is at z=-4.5 — well within shadow
+        assert results[(0, -5)] == 0.0, \
+            f"Cell (0,-5) at z=-4.5 should be in shadow (shadow tip at z≈-9.66)"
+
+        # 3) Cell just inside the shadow tip (z ≈ -9, centre at -8.5) must be shaded
+        #    Shadow tip is at ≈-9.66, cell centre at -8.5 is within
+        assert results[(0, -9)] == 0.0, \
+            f"Cell (0,-9) at z=-8.5 should be in shadow (tip at z≈-9.66)"
+
+        # 4) Cell clearly BEYOND shadow tip (z ≈ -12, centre at -11.5) must be lit
+        #    Shadow tip at ≈-9.66, cell centre at -11.5 is 1.84m beyond
+        assert results[(0, -12)] == 1.0, \
+            f"Cell (0,-12) at z=-11.5 should be beyond shadow (tip at z≈-9.66)"
+
+        # 5) Cells on the sun side (+Z, south) must be lit
+        assert results[(0, 5)] == 1.0, "Cell south of box should be lit"
+
+        # 6) Cells laterally outside the box (x > 1) at shadow Z should be lit
+        assert results[(3, -5)] == 1.0, \
+            f"Cell (3,-5) laterally outside box shadow should be lit"
+
+
+# ── Ray-triangle intersection unit tests ─────────────────────────────────
+
+class TestRayTriangle:
+    """Direct tests of the Möller-Trumbore implementation."""
+
+    def test_hit_horizontal_triangle(self):
+        tri = ((0, 0, 0), (10, 0, 0), (5, 0, 10))
+        origin = (5, 5, 3)
+        direction = (0, -1, 0)  # straight down
+        t = ray_triangle_intersect(origin, direction, tri)
+        assert t is not None
+        assert abs(t - 5.0) < 0.01
+
+    def test_miss_parallel_ray(self):
+        tri = ((0, 0, 0), (10, 0, 0), (5, 0, 10))
+        origin = (5, 5, 3)
+        direction = (1, 0, 0)  # parallel to triangle plane
+        t = ray_triangle_intersect(origin, direction, tri)
+        assert t is None
+
+    def test_miss_behind_ray(self):
+        tri = ((0, 0, 0), (10, 0, 0), (5, 0, 10))
+        origin = (5, -5, 3)
+        direction = (0, -1, 0)  # pointing away
+        t = ray_triangle_intersect(origin, direction, tri)
+        assert t is None
+
+    def test_miss_outside_triangle(self):
+        tri = ((0, 0, 0), (1, 0, 0), (0, 0, 1))
+        origin = (5, 5, 5)  # far outside triangle
+        direction = (0, -1, 0)
+        t = ray_triangle_intersect(origin, direction, tri)
+        assert t is None
+
+    def test_grazing_ray_at_1_degree(self):
+        """Ray at 1° altitude — nearly parallel to ground. Must still detect hits."""
+        # Large vertical wall at z=5, spanning x=-10..10, y=0..20
+        wall = make_box_triangles(0, 10, 5, 10, 10, 0.3)
+        d = sun_direction(180.0, 1.0)  # 1° altitude, from south (geographic convention)
+
+        # Origin at z=0 — ray should hit the wall at z≈4.7
+        assert ray_hits_any_triangle((0, 0.01, 0), d, wall), \
+            "Grazing ray at 1° should hit tall wall"
+
+    def test_grazing_ray_at_2_degrees_misses_short_wall(self):
+        """Ray at 2° over a 0.5m wall at 15m distance should clear it.
+        Wall height at 15m: 15 * tan(2°) ≈ 0.52m — just clears 0.5m wall."""
+        # Short wall (0.5m tall) at z=15
+        short_wall = make_box_triangles(0, 0.25, 15, 3, 0.25, 0.3)
+        d = sun_direction(180.0, 2.0)
+        # Origin at ground level, the ray at 2° reaches height 15*tan(2°)=0.52m at z=15
+        # Wall top is at y=0.5, ray at y≈0.52 — should just clear it
+        # This is a numerical edge case; we check the ray system handles it
+        result = ray_hits_any_triangle((0, 0.01, 0), d, short_wall)
+        # We don't assert a specific outcome here (it's at the numerical edge)
+        # but the function must not crash or produce NaN
+        assert isinstance(result, bool), "Grazing ray must return bool, not crash"
+
+
+# ── Sun position sanity tests ────────────────────────────────────────────
+
+class TestSunPositions:
+    """Tests for the Spencer 1971 solar position calculator against known values."""
+
+    def test_london_march_equinox(self):
+        positions = get_sun_positions(51.5, -0.1, 2024, 3, 21, time_step=1.0)
+        assert 11 <= len(positions) <= 13, \
+            f"London on equinox should have ~12 daylight hours, got {len(positions)}"
+
+    def test_london_equinox_noon_azimuth_altitude(self):
+        """At solar noon on equinox, London should see sun due south at ~38-39° altitude."""
+        positions = get_sun_positions(51.5, -0.1, 2024, 3, 21, time_step=1.0)
+        noon_pos = [p for p in positions if 11.5 <= p['hour'] <= 12.5]
+        assert len(noon_pos) >= 1, "Should have a position near solar noon"
+
+        p = noon_pos[0]
+        # Azimuth should be near 180° (due south in geographic convention), within ±5°
+        assert 172 <= p['azimuth'] <= 188, \
+            f"Noon azimuth should be ~180° (south), got {p['azimuth']:.1f}°"
+        # Altitude should be ~38.7° (90° - 51.5° + small correction)
+        assert 35 <= p['altitude'] <= 42, \
+            f"Noon altitude should be ~38.7°, got {p['altitude']:.1f}°"
+
+    def test_london_equinox_morning_rises_in_east(self):
+        """Morning sun should have azimuth < 180° (eastern half in geographic convention)."""
+        positions = get_sun_positions(51.5, -0.1, 2024, 3, 21, time_step=1.0)
+        morning = [p for p in positions if p['hour'] < 12]
+        assert len(morning) >= 3, "Should have multiple morning hours"
+        for p in morning:
+            assert p['azimuth'] < 180, \
+                f"Morning sun at hour {p['hour']} should have azimuth < 180° (east), got {p['azimuth']:.1f}°"
+
+    def test_london_equinox_afternoon_sets_in_west(self):
+        """Afternoon sun should have azimuth > 180° (western half in geographic convention)."""
+        positions = get_sun_positions(51.5, -0.1, 2024, 3, 21, time_step=1.0)
+        afternoon = [p for p in positions if p['hour'] > 13]
+        assert len(afternoon) >= 3, "Should have multiple afternoon hours"
+        for p in afternoon:
+            assert p['azimuth'] > 180, \
+                f"Afternoon sun at hour {p['hour']} should have azimuth > 180° (west), got {p['azimuth']:.1f}°"
+
+    def test_all_altitudes_positive(self):
+        positions = get_sun_positions(51.5, -0.1, 2024, 6, 21, time_step=0.5)
+        for p in positions:
+            assert p['altitude'] > 0, f"Returned position has non-positive altitude: {p}"
+
+    def test_summer_more_hours_than_winter(self):
+        summer = get_sun_positions(51.5, -0.1, 2024, 6, 21, time_step=1.0)
+        winter = get_sun_positions(51.5, -0.1, 2024, 12, 21, time_step=1.0)
+        assert len(summer) > len(winter) + 4, \
+            f"Summer ({len(summer)}) should have much more daylight than winter ({len(winter)})"
+
+    def test_equator_roughly_12_hours(self):
+        positions = get_sun_positions(0.0, 0.0, 2024, 3, 21, time_step=1.0)
+        assert 11 <= len(positions) <= 13, \
+            f"Equator on equinox should have ~12h daylight, got {len(positions)}"
+
+    def test_sun_direction_south_at_noon(self):
+        """Sun due south (azimuth 180° in geographic convention) at 45° altitude."""
+        dx, dy, dz = sun_direction(180.0, 45.0)
+        # Y = sin(alt) = 0.707
+        assert abs(dy - 0.7071) < 0.01, f"Y component should be ~0.707, got {dy}"
+        # X should be ~0 (due south, no east/west component)
+        assert abs(dx) < 0.01, f"X component should be ~0 for due south, got {dx}"
+        # Z should be positive (sun from +Z = south in Three.js coords)
+        assert dz > 0.5, f"Z component should be positive for south sun, got {dz}"
+
+    def test_sun_direction_east_west_symmetry(self):
+        """Azimuth 90° (east) and 270° (west) should mirror in X (geographic convention)."""
+        dx_e, dy_e, dz_e = sun_direction(90.0, 45.0)
+        dx_w, dy_w, dz_w = sun_direction(270.0, 45.0)
+        assert abs(dx_e + dx_w) < 0.01, "East/west X components should be opposite"
+        assert abs(dy_e - dy_w) < 0.01, "East/west Y components should be equal"
+        assert abs(dz_e - dz_w) < 0.01, "East/west Z components should be equal"
+
+
+# ── Accumulation tests (mirrors JS loop structure) ───────────────────────
+
+class TestAccumulation:
+    """Tests targeting the shared-array, sun-outer, cell-inner accumulation
+    pattern used in the JavaScript implementation."""
+
+    def _make_open_cells(self, n):
+        """Return n cell positions on a flat plane with no obstacles."""
+        return [(float(i), 0.0, 0.0) for i in range(n)]
+
+    def _make_sun_positions(self, n):
+        """Return n sun positions with genuinely different directions."""
+        # Vary azimuth (120°–240°) and altitude (25°–65°) so each produces
+        # a different shadow direction — catches caching / repeat bugs.
+        azimuths = [120, 150, 180, 210, 240]  # Geographic convention (0°=North CW)
+        altitudes = [25, 35, 45, 55, 65]
+        return [
+            {'azimuth': azimuths[i % 5], 'altitude': altitudes[i % 5], 'hour': 8 + i}
+            for i in range(n)
+        ]
+
+    def test_g_multi_position_accumulation(self):
+        """1 cell, 3 sun positions, no obstacles → hours = 3 * timeStep."""
+        cells = [(0.0, 0.0, 0.0)]
+        sun_pos = self._make_sun_positions(3)
+        result = compute_sun_hours_array_style(cells, [], sun_pos, time_step=1.0)
+        assert result[0] == 3.0, \
+            f"Expected 3.0h from 3 sun positions, got {result[0]}h — accumulator may be overwriting"
+
+    def test_h_partial_shadow_across_day(self):
+        """1 cell, 5 sun positions. Pre-verify which rays hit the wall,
+        then assert the exact expected hour count."""
+        cells = [(0.0, 0.0, 0.0)]
+        wall = make_box_triangles(0, 5, 3, 5, 5, 0.5)  # wall at z=3
+        origin = (0.0, 0.01, 0.0)  # 10mm above ground (matches engine offset)
+
+        sun_pos = [
+            {'azimuth': 180.0, 'altitude': 10.0, 'hour': 8},
+            {'azimuth': 180.0, 'altitude': 15.0, 'hour': 9},
+            {'azimuth': 180.0, 'altitude': 70.0, 'hour': 10},
+            {'azimuth': 180.0, 'altitude': 80.0, 'hour': 11},
+            {'azimuth': 180.0, 'altitude': 85.0, 'hour': 12},
+        ]
+
+        # Pre-verify: independently check which rays are blocked
+        blocked_count = 0
+        for sp in sun_pos:
+            d = sun_direction(sp['azimuth'], sp['altitude'])
+            if ray_hits_any_triangle(origin, d, wall):
+                blocked_count += 1
+        lit_count = len(sun_pos) - blocked_count
+
+        assert blocked_count > 0, \
+            "Test geometry must block at least one ray — fixture is broken"
+        assert lit_count > 0, \
+            "Test geometry must let at least one ray through — fixture is broken"
+
+        # Now run the accumulation and assert the EXACT expected result
+        result = compute_sun_hours_array_style(cells, wall, sun_pos, time_step=1.0)
+        assert result[0] == float(lit_count), \
+            f"Expected exactly {lit_count}h ({blocked_count} blocked, {lit_count} lit), " \
+            f"got {result[0]}h — accumulation error"
+
+    def test_i_array_style_matches_dict_style(self):
+        """Both accumulation strategies produce identical results for same input."""
+        box = make_box_triangles(5, 2.5, 5, 1, 2.5, 1)
+        sun_pos = get_sun_positions(51.5, -0.1, 2024, 3, 21, time_step=1.0)
+
+        # Dict-style (cell-outer)
+        grid_results = compute_sun_hours_flat_grid(
+            ground_y=0.0,
+            grid_min_x=0, grid_min_z=0,
+            grid_max_x=10, grid_max_z=10,
+            grid_size=2.0,
+            shadow_triangles=box,
+            sun_positions=sun_pos,
+            time_step=1.0,
+        )
+
+        # Array-style (sun-outer, cell-inner) — same cells
+        cells = []
+        cell_keys = []
+        for col in range(0, 5):  # 10/2 = 5 columns
+            for row in range(0, 5):
+                cx = (col + 0.5) * 2.0
+                cz = (row + 0.5) * 2.0
+                cells.append((cx, 0.0, cz))
+                cell_keys.append((col, row))
+
+        array_results = compute_sun_hours_array_style(cells, box, sun_pos, time_step=1.0)
+
+        for idx, key in enumerate(cell_keys):
+            dict_val = grid_results.get(key, 0.0)
+            arr_val = array_results[idx]
+            assert abs(dict_val - arr_val) < 0.01, \
+                f"Cell {key}: dict={dict_val}, array={arr_val} — accumulation strategies diverge"
+
+    def test_j_batching_doesnt_reset(self):
+        """10 cells, batch_size=3 (4 batches), 2 sun positions → every cell = 2h."""
+        cells = self._make_open_cells(10)
+        sun_pos = self._make_sun_positions(2)
+
+        result = compute_sun_hours_array_style(
+            cells, [], sun_pos, time_step=1.0, batch_size=3
+        )
+
+        for j in range(10):
+            assert result[j] == 2.0, \
+                f"Cell {j} got {result[j]}h instead of 2.0h — batch boundary may reset accumulator"
+
+    def test_k_single_sun_position_gives_exactly_timestep(self):
+        """1 sun position, no obstacles → every cell = exactly timeStep."""
+        cells = self._make_open_cells(5)
+        sun_pos = self._make_sun_positions(1)
+
+        result = compute_sun_hours_array_style(cells, [], sun_pos, time_step=0.5)
+
+        for j in range(5):
+            assert result[j] == 0.5, \
+                f"Cell {j} got {result[j]}h instead of 0.5h — single position not counted correctly"
+
+    def test_l_zero_sun_positions_gives_zero(self):
+        """Empty sun_positions → every cell = 0.0."""
+        cells = self._make_open_cells(5)
+        result = compute_sun_hours_array_style(cells, [], [], time_step=1.0)
+
+        for j in range(5):
+            assert result[j] == 0.0, \
+                f"Cell {j} got {result[j]}h with no sun positions — uninitialised value leak"
+
+
+    def test_l2_time_step_scales_proportionally(self):
+        """Same sun positions at time_step=0.5 and time_step=2.0 must produce
+        proportionally scaled results. Catches hardcoded time_step values."""
+        cells = self._make_open_cells(3)
+        sun_pos = self._make_sun_positions(4)
+
+        result_half = compute_sun_hours_array_style(cells, [], sun_pos, time_step=0.5)
+        result_two = compute_sun_hours_array_style(cells, [], sun_pos, time_step=2.0)
+
+        for j in range(3):
+            assert result_half[j] == 4 * 0.5, \
+                f"Cell {j} at time_step=0.5: expected 2.0h, got {result_half[j]}h"
+            assert result_two[j] == 4 * 2.0, \
+                f"Cell {j} at time_step=2.0: expected 8.0h, got {result_two[j]}h"
+            # Ratio must be exactly 4:1
+            assert abs(result_two[j] / result_half[j] - 4.0) < 0.001, \
+                f"Cell {j}: time_step ratio should be 4:1, got {result_two[j]/result_half[j]}"
+
+    def test_m_morning_data_survives_afternoon_pass(self):
+        """THE CORE TEST: proves earlier sun positions are not obliterated.
+
+        Two walls on opposite sides of two cells. Sun position 1 casts shadow
+        on cell A but not cell B. Sun position 2 casts shadow on cell B but
+        not cell A. After both positions, both cells must have exactly timeStep
+        — proving the afternoon pass didn't overwrite the morning data."""
+        # Cell A at (-5, 0, 0), Cell B at (+5, 0, 0)
+        cells = [(-5.0, 0.0, 0.0), (5.0, 0.0, 0.0)]
+
+        # Wall east of cell A at x=−3, blocks rays coming from the east
+        wall_east = make_box_triangles(-3, 5, 0, 0.5, 5, 5)
+        # Wall west of cell B at x=+3, blocks rays coming from the west
+        wall_west = make_box_triangles(3, 5, 0, 0.5, 5, 5)
+        obstacles = wall_east + wall_west
+
+        # Sun position 1: from the east (azimuth 90° in geographic convention)
+        # Sun position 2: from the west (azimuth 270° in geographic convention)
+        sun_pos = [
+            {'azimuth': 90.0, 'altitude': 30.0, 'hour': 8},    # from east
+            {'azimuth': 270.0, 'altitude': 30.0, 'hour': 16},  # from west
+        ]
+
+        # Pre-verify: independently confirm the shadow pattern
+        origin_a = (-5.0, 0.01, 0.0)
+        origin_b = (5.0, 0.01, 0.0)
+        dir1 = sun_direction(90.0, 30.0)
+        dir2 = sun_direction(270.0, 30.0)
+
+        # Cell A should be blocked by east wall from east sun, lit from west sun
+        a_blocked_by_1 = ray_hits_any_triangle(origin_a, dir1, obstacles)
+        a_blocked_by_2 = ray_hits_any_triangle(origin_a, dir2, obstacles)
+        # Cell B should be lit from east sun, blocked by west wall from west sun
+        b_blocked_by_1 = ray_hits_any_triangle(origin_b, dir1, obstacles)
+        b_blocked_by_2 = ray_hits_any_triangle(origin_b, dir2, obstacles)
+
+        assert a_blocked_by_1 and not a_blocked_by_2, \
+            f"Cell A shadow pattern wrong: blocked_by_east={a_blocked_by_1}, blocked_by_west={a_blocked_by_2}"
+        assert not b_blocked_by_1 and b_blocked_by_2, \
+            f"Cell B shadow pattern wrong: blocked_by_east={b_blocked_by_1}, blocked_by_west={b_blocked_by_2}"
+
+        # Run accumulation
+        result = compute_sun_hours_array_style(cells, obstacles, sun_pos, time_step=1.0)
+
+        # Both cells should have exactly 1h — each lit by one position
+        assert result[0] == 1.0, \
+            f"Cell A got {result[0]}h, expected 1.0h — morning data was obliterated by afternoon"
+        assert result[1] == 1.0, \
+            f"Cell B got {result[1]}h, expected 1.0h — afternoon data overwrote morning result"
+
+    def test_n_three_different_directions_accumulate_with_obstacle(self):
+        """3 genuinely different sun directions. Obstacle blocks exactly 1.
+        Pre-verified, then asserted exactly."""
+        cells = [(0.0, 0.0, 0.0)]
+        # Tall thin wall to the south
+        wall = make_box_triangles(0, 10, 5, 3, 10, 0.3)
+        origin = (0.0, 0.01, 0.0)
+
+        sun_pos = [
+            {'azimuth': 180.0, 'altitude': 20.0, 'hour': 9},    # south, low
+            {'azimuth': 90.0, 'altitude': 45.0, 'hour': 12},     # east, mid
+            {'azimuth': 270.0, 'altitude': 45.0, 'hour': 15},   # west, mid
+        ]
+
+        # Pre-verify each direction independently
+        blocked = []
+        for sp in sun_pos:
+            d = sun_direction(sp['azimuth'], sp['altitude'])
+            blocked.append(ray_hits_any_triangle(origin, d, wall))
+
+        assert sum(blocked) >= 1, \
+            f"Wall must block at least one direction, got blocked={blocked}"
+        expected_hours = sum(1.0 for b in blocked if not b)
+
+        result = compute_sun_hours_array_style(cells, wall, sun_pos, time_step=1.0)
+        assert result[0] == expected_hours, \
+            f"Expected {expected_hours}h (blocked={blocked}), got {result[0]}h"
+
+
+if __name__ == '__main__':
+    pytest.main([__file__, '-v'])
+```
+
+---
+
+### index.html
+
+```html
+```html
+<!DOCTYPE html>
+<html lang="en">
+<head>
+    <meta charset="UTF-8">
+    <meta name="viewport" content="width=device-width, initial-scale=1.0">
+    <title>SunForm — Sun Hours Analysis</title>
+    <style>
+        * { margin: 0; padding: 0; box-sizing: border-box; }
+
+        body {
+            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
+            background: #1a1a2e;
+            color: #e0e0e0;
+            display: flex;
+            height: 100vh;
+            overflow: hidden;
+        }
+
+        /* ─── LEFT PANEL ─── */
+        .panel {
+            width: 380px;
+            min-width: 380px;
+            background: #16213e;
+            display: flex;
+            flex-direction: column;
+            border-right: 1px solid #0f3460;
+        }
+
+        .panel-scroll {
+            flex: 1;
+            overflow-y: auto;
+            padding: 6px 20px 20px 20px;
+        }
+
+        .panel h1 {
+            font-size: 20px;
+            color: #D4880F;
+            margin-bottom: 4px;
+        }
+
+        .panel .subtitle {
+            font-size: 12px;
+            color: #888;
+            margin-bottom: 4px;
+        }
+
+        /* ─── ACCORDION STEPS ─── */
+        .step {
+            margin-bottom: 4px;
+            border: 1px solid #0f3460;
+            border-radius: 6px;
+            overflow: hidden;
+            transition: opacity 0.2s;
+        }
+
+        .step.upcoming {
+            opacity: 0.4;
+            pointer-events: none;
+        }
+
+        .step-header {
+            display: flex;
+            align-items: center;
+            padding: 10px 14px;
+            background: #1a1a2e;
+            cursor: pointer;
+            user-select: none;
+            gap: 10px;
+        }
+
+        .step-header:hover {
+            background: #1e2444;
+        }
+
+        .step-number {
+            width: 24px;
+            height: 24px;
+            border-radius: 50%;
+            background: #0f3460;
+            color: #888;
+            display: flex;
+            align-items: center;
+            justify-content: center;
+            font-size: 12px;
+            font-weight: 700;
+            flex-shrink: 0;
+        }
+
+        .step.active .step-number {
+            background: #D4880F;
+            color: #fff;
+        }
+
+        .step.completed .step-number {
+            background: #00CFC8;
+            color: #fff;
+        }
+
+        .step-title {
+            font-size: 13px;
+            font-weight: 600;
+            text-transform: uppercase;
+            letter-spacing: 0.5px;
+            color: #aaa;
+            flex: 1;
+        }
+
+        .step.active .step-title { color: #e0e0e0; }
+        .step.completed .step-title { color: #aaa; }
+
+        .step-summary {
+            font-size: 11px;
+            color: #00CFC8;
+            display: none;
+        }
+
+        .step.completed .step-summary { display: inline; }
+
+        .step-body {
+            display: none;
+            padding: 12px 14px 16px;
+            border-top: 1px solid #0f3460;
+        }
+
+        .step.active .step-body { display: block; }
+
+        .step-check {
+            color: #00CFC8;
+            font-size: 16px;
+            display: none;
+        }
+
+        .step.completed .step-check { display: inline; }
+
+        /* ─── FORM FIELDS ─── */
+        .field {
+            margin-bottom: 10px;
+        }
+
+        .field label {
+            display: block;
+            font-size: 12px;
+            color: #aaa;
+            margin-bottom: 3px;
+        }
+
+        .field input, .field select {
+            width: 100%;
+            padding: 6px 10px;
+            background: #1a1a2e;
+            border: 1px solid #0f3460;
+            color: #e0e0e0;
+            border-radius: 4px;
+            font-size: 13px;
+        }
+
+        .field input:focus, .field select:focus {
+            outline: none;
+            border-color: #D4880F;
+        }
+
+        .field .unit {
+            font-size: 11px;
+            color: #666;
+        }
+
+        .field-row {
+            display: flex;
+            gap: 10px;
+        }
+
+        .field-row .field { flex: 1; }
+
+        /* ─── FILE UPLOAD ─── */
+        .upload-zone {
+            border: 2px dashed #0f3460;
+            border-radius: 8px;
+            padding: 20px;
+            text-align: center;
+            cursor: pointer;
+            transition: border-color 0.2s, background 0.2s;
+            margin-bottom: 10px;
+        }
+
+        .upload-zone:hover, .upload-zone.dragover {
+            border-color: #D4880F;
+            background: rgba(212, 136, 15, 0.05);
+        }
+
+        .upload-zone.loaded {
+            border-color: #00CFC8;
+            background: rgba(0, 207, 200, 0.05);
+        }
+
+        .upload-zone .upload-icon { font-size: 28px; margin-bottom: 6px; }
+        .upload-zone .upload-text { font-size: 13px; color: #aaa; }
+        .upload-zone .upload-filename {
+            font-size: 12px;
+            color: #00CFC8;
+            margin-top: 4px;
+            font-weight: 600;
+        }
+
+        /* ─── RESULTS PANEL ─── */
+        .results-panel {
+            background: #1a1a2e;
+            border-radius: 6px;
+            padding: 12px;
+            margin-top: 10px;
+            display: none;
+        }
+
+        .results-panel.visible { display: block; }
+
+        .results-title {
+            font-size: 14px;
+            font-weight: 700;
+            margin-bottom: 6px;
+            color: #e0e0e0;
+        }
+
+        .results-detail {
+            font-size: 12px;
+            color: #aaa;
+            line-height: 1.6;
+        }
+
+        /* ─── BUTTONS ─── */
+        .btn {
+            display: block;
+            width: 100%;
+            padding: 10px;
+            border: none;
+            border-radius: 4px;
+            font-size: 14px;
+            font-weight: 600;
+            cursor: pointer;
+            margin-top: 10px;
+            transition: background 0.2s;
+        }
+
+        .btn:disabled { opacity: 0.4; cursor: not-allowed; }
+
+        .btn-primary { background: #D4880F; color: white; }
+        .btn-primary:hover:not(:disabled) { background: #B8720A; }
+
+        .btn-secondary { background: #0f3460; color: #e0e0e0; }
+        .btn-secondary:hover:not(:disabled) { background: #1a4a80; }
+
+        .btn-run { background: #D4880F; color: white; font-size: 15px; padding: 12px; }
+        .btn-run:hover:not(:disabled) { background: #E5A50A; }
+
+        /* ─── 3D VIEWPORT ─── */
+        .viewport {
+            flex: 1;
+            min-width: 0;
+            position: relative;
+            overflow: hidden;
+            background: #0a0a1a;
+        }
+
+        .viewport canvas {
+            display: block;
+            position: relative;
+            z-index: 1;
+        }
+
+        .viewport-info {
+            position: absolute;
+            top: 10px;
+            right: 10px;
+            font-size: 11px;
+            color: #00CFC8;
+            z-index: 5;
+        }
+
+        /* ─── FLY MODE CROSSHAIR ─── */
+        .fly-crosshair {
+            display: none;
+            position: absolute;
+            top: 50%;
+            left: 50%;
+            transform: translate(-50%, -50%);
+            z-index: 10;
+            color: rgba(255, 255, 255, 0.7);
+            font-size: 24px;
+            font-weight: 300;
+            pointer-events: none;
+            line-height: 1;
+        }
+
+        /* ─── DEBUG CONSOLE ─── */
+        .debug-console {
+            display: none;
+            position: absolute;
+            bottom: 10px;
+            left: 10px;
+            z-index: 30;
+            background: rgba(0,0,0,0.88);
+            color: #ccc;
+            font-family: 'Courier New', monospace;
+            font-size: 11px;
+            border-radius: 6px;
+            max-width: 520px;
+            max-height: 460px;
+            overflow-y: auto;
+            padding: 0;
+            border: 1px solid #444;
+        }
+        .debug-console.visible { display: block; }
+        .debug-header {
+            display: flex;
+            justify-content: space-between;
+            align-items: center;
+            padding: 4px 8px;
+            background: rgba(255,255,255,0.08);
+            border-bottom: 1px solid #444;
+            cursor: pointer;
+            user-select: none;
+        }
+        .debug-header span { font-weight: 700; color: #E5A50A; }
+        .debug-body { padding: 6px 8px; }
+        .debug-body table { width: 100%; border-collapse: collapse; }
+        .debug-body td { padding: 1px 4px; }
+        .debug-body td:first-child { color: #888; white-space: nowrap; }
+        .debug-body td:last-child { color: #eee; text-align: right; }
+        .debug-section { margin-top: 6px; padding-top: 4px; border-top: 1px solid #333; }
+        .debug-section-title { color: #E5A50A; font-weight: 700; margin-bottom: 2px; }
+        .debug-ok { color: #4CAF50; }
+        .debug-warn { color: #FFC107; }
+        .debug-err { color: #ff6b6b; }
+        .debug-toggle-btn {
+            position: absolute;
+            bottom: 10px;
+            left: 10px;
+            z-index: 31;
+            background: rgba(0,0,0,0.7);
+            color: #E5A50A;
+            border: 1px solid #555;
+            border-radius: 4px;
+            padding: 3px 8px;
+            font-size: 10px;
+            cursor: pointer;
+            font-family: monospace;
+        }
+        .debug-toggle-btn:hover { background: rgba(255,255,255,0.15); }
+
+        /* ─── NORTH ARROW OVERLAY ─── */
+        .north-arrow {
+            display: none;
+            position: absolute;
+            top: 90px;
+            right: 20px;
+            z-index: 10;
+            text-align: center;
+            color: #D4880F;
+            font-size: 12px;
+            font-weight: 700;
+        }
+
+        .north-arrow svg {
+            width: 50px;
+            height: 50px;
+        }
+
+        /* ─── ORIENTATION PREVIEW OVERLAY ─── */
+        .orient-preview-container {
+            display: none;
+            position: absolute;
+            top: 0; left: 0; right: 0; bottom: 0;
+            z-index: 8;
+            background: rgba(11, 19, 43, 0.92);
+            justify-content: center;
+            align-items: center;
+            overflow: hidden;
+        }
+        .orient-preview-container.visible {
+            display: flex;
+        }
+        #orient-preview {
+            max-width: 85%;
+            max-height: 85%;
+            transition: transform 0.3s ease;
+            image-rendering: auto;
+        }
+
+        /* ─── BOUNDING BOX MODE INDICATOR ─── */
+        .bbox-overlay {
+            display: none;
+            position: absolute;
+            top: 10px;
+            left: 10px;
+            z-index: 5;
+            background: rgba(22, 33, 62, 0.95);
+            padding: 10px 14px;
+            border-radius: 6px;
+            font-size: 12px;
+            line-height: 1.6;
+            border: 1px solid #D4880F;
+            min-width: 200px;
+        }
+
+        .bbox-overlay.visible { display: block; }
+        .bbox-overlay .bbox-title { color: #D4880F; font-weight: 600; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
+        .bbox-overlay .bbox-hint { color: #aaa; font-size: 12px; }
+        .bbox-overlay .bbox-coords { color: #00CFC8; font-size: 12px; margin-top: 4px; font-family: monospace; }
+
+        .viewport.drawing-bbox { cursor: crosshair; }
+
+        /* ─── STATUS OVERLAY ─── */
+        .status-overlay {
+            position: absolute;
+            bottom: 20px;
+            right: 20px;
+            background: rgba(22, 33, 62, 0.9);
+            padding: 10px 14px;
+            border-radius: 6px;
+            font-size: 12px;
+            line-height: 1.4;
+            border: 1px solid #0f3460;
+            color: #aaa;
+            z-index: 10;
+            text-align: center;
+            max-width: 260px;
+        }
+
+        /* ─── COLOUR LEGEND (viewport overlay) ─── */
+        .colour-legend {
+            display: none;
+            position: absolute;
+            right: 20px;
+            bottom: 60px;
+            z-index: 10;
+            width: 36px;
+            text-align: center;
+        }
+
+        .colour-legend.visible { display: flex; flex-direction: column; align-items: center; }
+
+        .colour-legend .legend-label {
+            font-size: 10px;
+            color: #ccc;
+            margin: 2px 0;
+        }
+
+        .colour-legend .legend-bar-v {
+            width: 18px;
+            height: 180px;
+            border-radius: 3px;
+            border: 1px solid #333;
+            background: linear-gradient(to top,
+                rgb(38, 0, 64),
+                rgb(204, 26, 26),
+                rgb(255, 128, 0),
+                rgb(255, 217, 0),
+                rgb(255, 255, 51),
+                rgb(255, 255, 204)
+            );
+            position: relative;
+        }
+        .legend-notch {
+            position: absolute;
+            right: -1px;
+            height: 1px;
+            background: rgba(255, 255, 255, 0.6);
+            pointer-events: none;
+        }
+        .legend-notch.hour {
+            width: 8px;
+            height: 1.5px;
+            background: rgba(255, 255, 255, 0.85);
+        }
+        .legend-notch.sub-hour {
+            width: 4px;
+            height: 1px;
+            background: rgba(255, 255, 255, 0.45);
+        }
+
+        /* ─── RAY PROBE PANEL ─── */
+        .ray-probe-panel {
+            display: none;
+            position: absolute;
+            left: 20px;
+            top: auto;
+            bottom: 60px;
+            z-index: 12;
+            background: rgba(10, 10, 30, 0.92);
+            border: 1px solid #0f3460;
+            border-radius: 6px;
+            padding: 10px 14px;
+            min-width: 260px;
+            max-width: 340px;
+            max-height: 320px;
+            backdrop-filter: blur(6px);
+            font-size: 11px;
+            color: #ccc;
+        }
+        .ray-probe-panel.visible { display: block; }
+        .ray-probe-panel .probe-title {
+            font-size: 12px;
+            font-weight: 600;
+            color: #e0e0e0;
+            margin-bottom: 6px;
+            display: flex;
+            justify-content: space-between;
+            align-items: center;
+            cursor: grab;
+            user-select: none;
+        }
+        .ray-probe-panel .probe-title:active {
+            cursor: grabbing;
+        }
+        .ray-probe-panel .probe-clear-btn {
+            background: #D4880F;
+            color: #fff;
+            border: none;
+            border-radius: 3px;
+            padding: 2px 10px;
+            font-size: 10px;
+            font-weight: 600;
+            cursor: pointer;
+        }
+        .ray-probe-panel .probe-summary {
+            margin-bottom: 6px;
+            color: #aaa;
+            font-size: 10px;
+        }
+        .ray-probe-panel .probe-table {
+            max-height: 220px;
+            overflow-y: auto;
+        }
+        .ray-probe-panel .probe-table table {
+            width: 100%;
+            border-collapse: collapse;
+        }
+        .ray-probe-panel .probe-table th {
+            text-align: left;
+            padding: 2px 6px;
+            border-bottom: 1px solid #0f3460;
+            color: #888;
+            font-weight: 600;
+            font-size: 10px;
+            position: sticky;
+            top: 0;
+            background: rgba(10, 10, 30, 0.98);
+        }
+        .ray-probe-panel .probe-table td {
+            padding: 2px 6px;
+            font-size: 10px;
+            border-bottom: 1px solid rgba(15, 52, 96, 0.4);
+        }
+        .ray-probe-panel .probe-table tr.ray-hit td { color: #FFD700; }
+        .ray-probe-panel .probe-table tr.ray-blocked td { color: #FF6666; }
+
+
+        /* ─── PROGRESS BAR ─── */
+        .progress-bar {
+            display: none;
+            height: 3px;
+            background: #0f3460;
+            border-radius: 2px;
+            margin-top: 8px;
+            overflow: hidden;
+        }
+
+        .progress-bar.visible { display: block; }
+
+        .progress-bar .progress-fill {
+            height: 100%;
+            background: #D4880F;
+            border-radius: 2px;
+            transition: width 0.3s;
+            animation: progress-pulse 1.5s ease-in-out infinite;
+        }
+
+        @keyframes progress-pulse {
+            0%, 100% { opacity: 1; }
+            50% { opacity: 0.5; }
+        }
+
+        /* ─── DISCLAIMER ─── */
+        .disclaimer {
+            font-size: 10px;
+            color: #555;
+            margin-top: 12px;
+            line-height: 1.5;
+            padding-top: 8px;
+            border-top: 1px solid #0f3460;
+        }
+
+        .hint { font-size: 12px; color: #aaa; margin-bottom: 8px; line-height: 1.5; }
+
+        /* ─── LOCATION MAP ─── */
+        .location-map {
+            width: 100%;
+            height: 180px;
+            border-radius: 4px;
+            border: 1px solid #0f3460;
+            margin-bottom: 8px;
+        }
+        .location-search {
+            width: 100%;
+            padding: 6px 10px;
+            background: #1a1a2e;
+            border: 1px solid #0f3460;
+            color: #e0e0e0;
+            border-radius: 4px;
+            font-size: 12px;
+            margin-bottom: 6px;
+        }
+        .location-search:focus { outline: none; border-color: #D4880F; }
+
+        /* ─── SEASON TOGGLES ─── */
+        .season-toggles {
+            display: flex;
+            gap: 6px;
+            margin-bottom: 8px;
+        }
+        .season-toggle {
+            flex: 1;
+            padding: 6px 4px;
+            border: 1px solid #0f3460;
+            border-radius: 4px;
+            background: #1a1a2e;
+            color: #888;
+            font-size: 11px;
+            font-weight: 600;
+            cursor: pointer;
+            text-align: center;
+            transition: all 0.15s;
+        }
+        .season-toggle.active {
+            border-color: #D4880F;
+            color: #e0e0e0;
+            background: rgba(212, 136, 15, 0.15);
+        }
+
+        /* ─── SEASON SWITCHER (viewport overlay) ─── */
+        .season-switcher {
+            display: none;
+            position: absolute;
+            top: 10px;
+            left: 50%;
+            transform: translateX(-50%);
+            z-index: 10;
+            background: rgba(22, 33, 62, 0.95);
+            border-radius: 6px;
+            border: 1px solid #0f3460;
+            padding: 4px;
+            gap: 4px;
+        }
+        .season-switcher.visible { display: flex; }
+        .season-sw-btn {
+            padding: 5px 12px;
+            border: none;
+            border-radius: 3px;
+            background: transparent;
+            color: #888;
+            font-size: 11px;
+            font-weight: 600;
+            cursor: pointer;
+            transition: all 0.15s;
+        }
+        .season-sw-btn.active {
+            background: #D4880F;
+            color: #fff;
+        }
+
+        /* ─── BUG REPORT ─── */
+        .bug-report {
+            font-size: 10px;
+            color: #666;
+            margin-top: 6px;
+            text-align: center;
+        }
+        .bug-report a {
+            color: #888;
+            text-decoration: none;
+        }
+        .bug-report a:hover { color: #D4880F; text-decoration: underline; }
+
+        /* ─── DISCLAIMER MODAL ─── */
+        .modal-overlay {
+            position: fixed;
+            top: 0; left: 0; right: 0; bottom: 0;
+            background: rgba(0, 0, 0, 0.85);
+            z-index: 9999;
+            display: flex;
+            align-items: center;
+            justify-content: center;
+        }
+        .modal-overlay.hidden { display: none; }
+        .modal-box {
+            background: #16213e;
+            border: 1px solid #D4880F;
+            border-radius: 10px;
+            max-width: 620px;
+            width: 90%;
+            max-height: 85vh;
+            overflow-y: auto;
+            padding: 28px 32px;
+            color: #e0e0e0;
+        }
+        .modal-box h2 {
+            font-size: 18px;
+            color: #E5A50A;
+            margin-bottom: 4px;
+        }
+        .modal-box .modal-subtitle {
+            font-size: 12px;
+            color: #888;
+            margin-bottom: 16px;
+        }
+        .modal-box h3 {
+            font-size: 13px;
+            color: #D4880F;
+            margin: 14px 0 4px;
+            text-transform: uppercase;
+            letter-spacing: 0.5px;
+        }
+        .modal-box p, .modal-box li {
+            font-size: 12px;
+            line-height: 1.6;
+            color: #ccc;
+        }
+        .modal-box ul { padding-left: 18px; margin: 4px 0; }
+        .modal-box .beta-badge {
+            display: inline-block;
+            background: #D4880F;
+            color: #000;
+            font-size: 10px;
+            font-weight: 700;
+            padding: 2px 8px;
+            border-radius: 3px;
+            text-transform: uppercase;
+            letter-spacing: 1px;
+            margin-left: 8px;
+            vertical-align: middle;
+        }
+        .modal-box .checkbox-row {
+            display: flex;
+            align-items: flex-start;
+            gap: 8px;
+            margin: 10px 0;
+            font-size: 12px;
+            color: #ccc;
+            cursor: pointer;
+        }
+        .modal-box .checkbox-row input[type="checkbox"] {
+            margin-top: 2px;
+            accent-color: #D4880F;
+        }
+        .modal-box .btn-accept {
+            display: block;
+            width: 100%;
+            padding: 12px;
+            border: none;
+            border-radius: 4px;
+            font-size: 14px;
+            font-weight: 600;
+            cursor: pointer;
+            margin-top: 16px;
+            background: #D4880F;
+            color: #fff;
+            transition: background 0.2s;
+        }
+        .modal-box .btn-accept:disabled {
+            opacity: 0.3;
+            cursor: not-allowed;
+        }
+        .modal-box .btn-accept:hover:not(:disabled) {
+            background: #E5A50A;
+        }
+        .modal-box .role-gate {
+            margin-bottom: 14px;
+        }
+        .modal-box .role-gate label {
+            display: block;
+            font-size: 12px;
+            color: #aaa;
+            margin-bottom: 4px;
+        }
+        .modal-box .role-gate select {
+            width: 100%;
+            padding: 8px 10px;
+            background: #1a1a2e;
+            border: 1px solid #0f3460;
+            color: #e0e0e0;
+            border-radius: 4px;
+            font-size: 13px;
+        }
+        .modal-box .role-gate select:focus {
+            outline: none;
+            border-color: #D4880F;
+        }
+        .modal-box .role-message {
+            font-size: 11px;
+            line-height: 1.5;
+            margin-top: 8px;
+            padding: 8px 10px;
+            border-radius: 4px;
+        }
+        .modal-box .role-message.allowed {
+            color: #00CFC8;
+            background: rgba(0, 207, 200, 0.08);
+            border: 1px solid rgba(0, 207, 200, 0.2);
+        }
+        .modal-box .role-message.blocked {
+            color: #D4880F;
+            background: rgba(212, 136, 15, 0.08);
+            border: 1px solid rgba(212, 136, 15, 0.2);
+        }
+
+        /* ─── DOWNLOAD CONFIRMATION MODAL ─── */
+        .download-confirm-overlay {
+            position: fixed;
+            top: 0; left: 0; right: 0; bottom: 0;
+            background: rgba(0, 0, 0, 0.75);
+            z-index: 9998;
+            display: none;
+            align-items: center;
+            justify-content: center;
+        }
+        .download-confirm-overlay.visible { display: flex; }
+        .download-confirm-box {
+            background: #16213e;
+            border: 1px solid #D4880F;
+            border-radius: 10px;
+            max-width: 480px;
+            width: 90%;
+            padding: 24px 28px;
+            color: #e0e0e0;
+        }
+        .download-confirm-box h3 {
+            font-size: 15px;
+            color: #E5A50A;
+            margin-bottom: 12px;
+        }
+        .download-confirm-box p {
+            font-size: 12px;
+            line-height: 1.6;
+            color: #ccc;
+            margin-bottom: 10px;
+        }
+        .download-confirm-box .checkbox-row {
+            display: flex;
+            align-items: flex-start;
+            gap: 8px;
+            margin: 10px 0;
+            font-size: 12px;
+            color: #ccc;
+            cursor: pointer;
+        }
+        .download-confirm-box .checkbox-row input[type="checkbox"] {
+            margin-top: 2px;
+            accent-color: #D4880F;
+        }
+        .download-confirm-box .btn-row {
+            display: flex;
+            gap: 8px;
+            margin-top: 14px;
+        }
+        .download-confirm-box .btn-row button {
+            flex: 1;
+            padding: 10px;
+            border: none;
+            border-radius: 4px;
+            font-size: 13px;
+            font-weight: 600;
+            cursor: pointer;
+        }
+        .download-confirm-box .btn-cancel {
+            background: #0f3460;
+            color: #e0e0e0;
+        }
+        .download-confirm-box .btn-proceed {
+            background: #D4880F;
+            color: #fff;
+        }
+        .download-confirm-box .btn-proceed:disabled {
+            opacity: 0.3;
+            cursor: not-allowed;
+        }
+
+        /* ─── LOGO ─── */
+        .logo-img {
+            display: block;
+            width: 100%;
+            max-height: 260px;
+            object-fit: contain;
+            margin: -20px auto -50px auto;
+        }
+        .modal-logo {
+            display: block;
+            max-width: 400px;
+            height: auto;
+            margin: -20px auto -40px auto;
+        }
+        /* ─── COFFEE BUTTON ─── */
+        .coffee-wrap {
+            position: absolute;
+            top: 32px;
+            right: 20px;
+            z-index: 10;
+            text-align: center;
+        }
+        .coffee-btn {
+            display: inline-block;
+            background: rgba(212,136,15,0.85);
+            color: #fff;
+            font-size: 11px;
+            font-weight: 600;
+            padding: 6px 14px;
+            border-radius: 4px;
+            text-decoration: none;
+            letter-spacing: 0.3px;
+            backdrop-filter: blur(4px);
+        }
+
+        /* ─── HAMBURGER MENU BUTTON ─── */
+        .hamburger-btn {
+            display: none;
+            position: fixed;
+            top: 12px;
+            left: 12px;
+            z-index: 1001;
+            width: 40px;
+            height: 40px;
+            align-items: center;
+            justify-content: center;
+            background: #16213e;
+            border: 1px solid #0f3460;
+            border-radius: 6px;
+            cursor: pointer;
+            flex-direction: column;
+            gap: 5px;
+            padding: 8px;
+        }
+        .hamburger-btn span {
+            display: block;
+            width: 22px;
+            height: 2px;
+            background: #D4880F;
+            border-radius: 1px;
+            transition: transform 0.3s ease, opacity 0.3s ease;
+        }
+        .hamburger-btn.active span:nth-child(1) {
+            transform: rotate(45deg) translate(5px, 5px);
+        }
+        .hamburger-btn.active span:nth-child(2) {
+            opacity: 0;
+        }
+        .hamburger-btn.active span:nth-child(3) {
+            transform: rotate(-45deg) translate(5px, -5px);
+        }
+
+        /* ─── RESPONSIVE ─── */
+        @media (max-width: 900px) {
+            .panel {
+                width: 300px;
+                min-width: 300px;
+            }
+            .panel-scroll {
+                padding: 6px 12px 16px 12px;
+            }
+        }
+
+        @media (max-width: 700px) {
+            .panel {
+                width: 260px;
+                min-width: 260px;
+            }
+            .viewport-info {
+                font-size: 9px;
+                right: 6px;
+            }
+            .coffee-wrap {
+                right: 6px;
+                top: 28px;
+            }
+            .coffee-btn {
+                font-size: 10px;
+                padding: 4px 10px;
+            }
+            .season-switcher {
+                font-size: 10px;
+            }
+            .colour-legend {
+                right: 8px;
+                bottom: 40px;
+            }
+        }
+
+        @media (max-width: 550px) {
+            body {
+                flex-direction: row;
+            }
+            .panel {
+                position: fixed;
+                top: 0;
+                left: 0;
+                bottom: 0;
+                width: 85vw;
+                max-width: 340px;
+                min-width: unset;
+                max-height: none;
+                border-right: 1px solid #0f3460;
+                border-bottom: none;
+                z-index: 1000;
+                transform: translateX(-100%);
+                transition: transform 0.3s ease;
+            }
+            .panel.open {
+                transform: translateX(0);
+            }
+            .panel-backdrop {
+                display: none;
+                position: fixed;
+                top: 0; left: 0; right: 0; bottom: 0;
+                background: rgba(0,0,0,0.5);
+                z-index: 999;
+            }
+            .panel-backdrop.visible {
+                display: block;
+            }
+            .viewport {
+                flex: 1;
+                min-height: 0;
+                width: 100%;
+            }
+            .viewport-info {
+                font-size: 8px;
+                right: 4px;
+                top: 6px;
+            }
+            .coffee-wrap {
+                right: 4px;
+                top: 22px;
+            }
+            .season-switcher {
+                top: 6px;
+            }
+            .hamburger-btn {
+                display: flex;
+            }
+            .logo-img {
+                width: 80%;
+                max-height: 160px;
+                margin: -10px auto -30px auto;
+            }
+            .modal-logo {
+                max-width: 220px;
+                margin: -10px auto -20px auto;
+            }
+        }
+
+    </style>
+</head>
+<body>
+    <!-- ─── DISCLAIMER MODAL ─── -->
+    <div class="modal-overlay" id="disclaimer-modal">
+        <div class="modal-box">
+            <img src="sunform-logo.png" alt="SunForm" class="modal-logo">
+            <h2>SunForm &mdash; Terms of Use</h2>
+
+            <div id="disclaimer-terms">
+                <p>SunForm is currently in active beta development. You are using unfinished software. Outputs may be incomplete, inaccurate, or incorrect &mdash; this is expected at this stage and is part of why your testing matters.</p>
+
+                <p>All outputs are indicative only. They have not been validated against any building regulation, standard, or code of practice &mdash; including BRE 209, BS EN 17037, or the Building Regulations 2010. Do not use them for any formal purpose.</p>
+
+                <p>As a beta tester you are asked to use SunForm critically. If something looks wrong, it may well be. Please report anything unexpected so the tool can be improved.</p>
+
+                <p>SunForm is provided free of charge and entirely at your own risk. To the fullest extent permitted by law, Jake White Architecture accepts no liability for any loss or damage arising from use of or reliance upon its outputs.</p>
+
+                <p>The tool and its source code remain the intellectual property of Jake White Architecture.</p>
+
+                <p style="margin-top:14px; font-weight:600; color:#ccc; font-size:12px;">Third-Party Software Credits</p>
+                <p style="font-size:11px; color:#999; margin-top:4px;">SunForm incorporates the following open-source libraries. These are independent projects maintained by their respective authors; Jake White Architecture does not claim ownership of, nor accept liability for, any third-party component.</p>
+                <ul style="font-size:11px; color:#999; margin:6px 0 0 16px; padding:0; line-height:1.7;">
+                    <li><strong style="color:#bbb;">Three.js</strong> (r128) &mdash; 3D rendering &mdash; MIT License &mdash; &copy; Three.js Authors</li>
+                    <li><strong style="color:#bbb;">web-ifc</strong> (0.0.57) &mdash; IFC file parsing &mdash; Mozilla Public License 2.0 &mdash; &copy; IFC.js Contributors</li>
+                    <li><strong style="color:#bbb;">Leaflet</strong> (1.9.4) &mdash; Interactive maps &mdash; BSD-2-Clause License &mdash; &copy; Volodymyr Agafonkin</li>
+                </ul>
+                <p style="font-size:11px; color:#999; margin-top:8px;">Sun position calculations use the Spencer (1971) algorithm; shadow ray&ndash;triangle intersection uses the M&ouml;ller&ndash;Trumbore algorithm. Both are implemented from published academic sources and carry no third-party licence obligations.</p>
+
+                <p style="margin-top:14px; font-size:11px; color:#888;">SunForm is provided by Jake White Architecture. For professional Architectural Technology services, visit <a href="https://www.jakewhitearchitecture.com" target="_blank" style="color:#00CFC8;">jakewhitearchitecture.com</a></p>
+            </div>
+
+            <hr style="border-color:#0f3460; margin:16px 0 12px;">
+
+            <div style="font-size:12px; color:#aaa; margin-bottom:8px;">Confirmations:</div>
+            <div id="disclaimer-checkboxes">
+                <label class="checkbox-row">
+                    <input type="checkbox" id="disclaimer-check1" onchange="updateDisclaimerAccept()">
+                    <span>I confirm that I am competent to interpret solar analysis outputs and would be able to identify inconsistencies or errors in the results.</span>
+                </label>
+                <label class="checkbox-row">
+                    <input type="checkbox" id="disclaimer-check2" onchange="updateDisclaimerAccept()">
+                    <span>I understand that SunForm is not a substitute for professional daylighting consultancy and I will not present its outputs to others as verified analysis.</span>
+                </label>
+            </div>
+
+            <button class="btn-accept" id="disclaimer-accept-btn" disabled onclick="acceptDisclaimer()">Accept &amp; Continue</button>
+        </div>
+    </div>
+
+
+    <!-- ─── BETA FEEDBACK WIZARD MODAL ─── -->
+    <div class="modal-overlay hidden" id="beta-feedback-modal">
+        <div class="modal-box" style="max-width:520px;">
+            <!-- Step 1: Instructions + generated challenge -->
+            <div id="bf-step-1">
+                <h2 style="margin-bottom:12px;">Beta Testing Feedback</h2>
+                <p style="margin-bottom:6px;"><a id="bf-suncalc-link" href="#" target="_blank" rel="noopener" style="color:#00CFC8; text-decoration:underline; font-weight:bold;">Check this result on SunCalc.org &rarr;</a></p>
+                <p style="margin-bottom:14px; color:#aaa; font-size:12px;">Open the link, then compare the Azimuth and Altitude values shown on SunCalc with SunForm's values below.</p>
+
+                <div style="background:#0a1628; border:1px solid #0f3460; border-radius:6px; padding:12px 16px; margin-bottom:14px; font-size:13px;">
+                    <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
+                        <span style="color:#888;">Latitude:</span>
+                        <span id="bf-lat" style="color:#00CFC8; font-family:monospace;"></span>
+                    </div>
+                    <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
+                        <span style="color:#888;">Longitude:</span>
+                        <span id="bf-lng" style="color:#00CFC8; font-family:monospace;"></span>
+                    </div>
+                    <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
+                        <span style="color:#888;">Date:</span>
+                        <span id="bf-date" style="color:#00CFC8; font-family:monospace;"></span>
+                    </div>
+                    <div style="display:flex; justify-content:space-between;">
+                        <span style="color:#888;">Time (local clock):</span>
+                        <span id="bf-time" style="color:#00CFC8; font-family:monospace;"></span>
+                    </div>
+                </div>
+
+                <p style="margin-bottom:10px; font-size:12px;">Enter the values from your chosen calculator:</p>
+                <div style="display:flex; gap:12px; margin-bottom:14px;">
+                    <div style="flex:1;">
+                        <label style="font-size:11px; color:#888; display:block; margin-bottom:3px;">Azimuth (°)</label>
+                        <input type="number" id="bf-user-azimuth" step="0.01" placeholder="e.g. 165.3" style="width:100%; padding:6px 8px; background:#0a1628; border:1px solid #0f3460; color:#e0e0e0; border-radius:4px; font-size:13px;">
+                    </div>
+                    <div style="flex:1;">
+                        <label style="font-size:11px; color:#888; display:block; margin-bottom:3px;">Altitude (°)</label>
+                        <input type="number" id="bf-user-altitude" step="0.01" placeholder="e.g. 42.7" style="width:100%; padding:6px 8px; background:#0a1628; border:1px solid #0f3460; color:#e0e0e0; border-radius:4px; font-size:13px;">
+                    </div>
+                </div>
+
+                <div style="display:flex; gap:10px;">
+                    <button class="btn btn-secondary" onclick="closeBetaFeedback()" style="flex:1;">Cancel</button>
+                    <button class="btn btn-primary" onclick="checkBetaFeedback()" style="flex:1;">Check</button>
+                </div>
+            </div>
+
+            <!-- Step 2: Results comparison -->
+            <div id="bf-step-2" style="display:none;">
+                <h2 style="margin-bottom:12px;">Results Comparison</h2>
+
+                <div style="background:#0a1628; border:1px solid #0f3460; border-radius:6px; padding:12px 16px; margin-bottom:6px; font-size:13px;">
+                    <div style="font-size:11px; color:#888; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px;">Your Input (external calculator)</div>
+                    <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
+                        <span style="color:#888;">Azimuth:</span>
+                        <span id="bf-user-az-result" style="color:#e0e0e0; font-family:monospace;"></span>
+                    </div>
+                    <div style="display:flex; justify-content:space-between;">
+                        <span style="color:#888;">Altitude:</span>
+                        <span id="bf-user-alt-result" style="color:#e0e0e0; font-family:monospace;"></span>
+                    </div>
+                </div>
+
+                <div style="background:#0a1628; border:1px solid #0f3460; border-radius:6px; padding:12px 16px; margin-bottom:6px; font-size:13px;">
+                    <div style="font-size:11px; color:#888; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px;">SunForm Calculated</div>
+                    <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
+                        <span style="color:#888;">Azimuth:</span>
+                        <span id="bf-calc-az-result" style="color:#00CFC8; font-family:monospace;"></span>
+                    </div>
+                    <div style="display:flex; justify-content:space-between;">
+                        <span style="color:#888;">Altitude:</span>
+                        <span id="bf-calc-alt-result" style="color:#00CFC8; font-family:monospace;"></span>
+                    </div>
+                </div>
+
+                <div style="background:#0a1628; border:1px solid #0f3460; border-radius:6px; padding:12px 16px; margin-bottom:14px; font-size:13px;">
+                    <div style="font-size:11px; color:#888; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px;">Difference</div>
+                    <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
+                        <span style="color:#888;">Azimuth:</span>
+                        <span id="bf-diff-az" style="font-family:monospace;"></span>
+                    </div>
+                    <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
+                        <span style="color:#888;">Altitude:</span>
+                        <span id="bf-diff-alt" style="font-family:monospace;"></span>
+                    </div>
+                    <div id="bf-verdict" style="text-align:center; font-size:13px; font-weight:bold; padding:6px; border-radius:4px;"></div>
+                </div>
+
+                <div style="display:flex; gap:10px;">
+                    <button class="btn btn-secondary" onclick="closeBetaFeedback()" style="flex:1;">Close</button>
+                    <button class="btn btn-primary" onclick="sendBetaFeedback()" style="flex:1;">Send Feedback</button>
+                </div>
+            </div>
+        </div>
+    </div>
+
+    <!-- ─── MOBILE HAMBURGER & BACKDROP ─── -->
+    <button class="hamburger-btn" id="hamburger-btn" onclick="toggleMobilePanel()">
+        <span></span><span></span><span></span>
+    </button>
+    <div class="panel-backdrop" id="panel-backdrop" onclick="closeMobilePanel()"></div>
+
+    <div class="panel" id="main-panel">
+      <div class="panel-scroll">
+        <img src="sunform-logo.png" alt="SunForm" class="logo-img">
+        <p class="subtitle" style="text-align:center;">A free sun hours web tool (Beta)</p>
+
+        <!-- STEP 1: IMPORT -->
+        <div class="step active" id="step-1" onclick="openStep(1)">
+            <div class="step-header">
+                <div class="step-number">1</div>
+                <div class="step-title">Import</div>
+                <span class="step-check">&#10003;</span>
+                <span class="step-summary" id="step1-summary"></span>
+            </div>
+            <div class="step-body">
+                <div class="upload-zone" id="upload-zone" onclick="event.stopPropagation(); document.getElementById('ifc-file').click();">
+                    <div class="upload-icon">&#9729;</div>
+                    <div class="upload-text" id="upload-text">
+                        Drop IFC file here or click to browse
+                    </div>
+                    <div class="upload-filename" id="upload-filename" style="display:none;"></div>
+                </div>
+                <input type="file" id="ifc-file" accept=".ifc" style="display:none;" onchange="handleFileUpload(this);">
+                <div class="progress-bar" id="upload-progress">
+                    <div class="progress-fill" style="width: 100%;"></div>
+                </div>
+                <div id="ifcos-status" style="display:none; font-size:10px; color:#aaa; margin-top:6px; padding:2px 4px;"></div>
+            </div>
+        </div>
+
+        <!-- STEP 2: SET ORIENTATION -->
+        <div class="step upcoming" id="step-2" onclick="openStep(2)">
+            <div class="step-header">
+                <div class="step-number">2</div>
+                <div class="step-title">Set Orientation</div>
+                <span class="step-check">&#10003;</span>
+                <span class="step-summary" id="step2-summary"></span>
+            </div>
+            <div class="step-body">
+                <div style="font-size:11px; color:#aaa; margin-bottom:8px;">Rotate the plan so that <b>North is up</b>. Use the arrows or type degrees.</div>
+                <div style="display:flex; align-items:center; gap:6px; margin-bottom:10px;">
+                    <button class="btn btn-secondary" onclick="event.stopPropagation(); applyManualRotation(1);" style="margin-top:0; padding:4px 12px; font-size:16px;">&#x2190;</button>
+                    <input type="number" id="north-rotation" value="5" step="5" min="1" max="180" style="width:60px; text-align:center;">
+                    <button class="btn btn-secondary" onclick="event.stopPropagation(); applyManualRotation(-1);" style="margin-top:0; padding:4px 12px; font-size:16px;">&#x2192;</button>
+                    <span class="unit" style="margin-left:2px;">&deg;</span>
+                </div>
+                <div style="display:flex; gap:8px;">
+                    <button class="btn btn-primary" onclick="event.stopPropagation(); confirmOrientation();" style="flex:1;">Confirm Orientation</button>
+                    <button class="btn btn-secondary" onclick="event.stopPropagation(); resetOrientation();" style="flex:0;">Reset</button>
+                </div>
+            </div>
+        </div>
+
+        <!-- STEP 3: SITE LOCATION -->
+        <div class="step upcoming" id="step-3" onclick="openStep(3)">
+            <div class="step-header">
+                <div class="step-number">3</div>
+                <div class="step-title">Site Location</div>
+                <span class="step-check">&#10003;</span>
+                <span class="step-summary" id="step3-summary"></span>
+            </div>
+            <div class="step-body">
+                <input type="text" class="location-search" id="location-search" placeholder="Search place name or postcode..." autocomplete="off">
+                <div class="location-map" id="location-map"></div>
+                <div class="field-row">
+                    <div class="field">
+                        <label>Latitude</label>
+                        <input type="number" id="latitude" value="51.5074" min="-90" max="90" step="0.0001">
+                    </div>
+                    <div class="field">
+                        <label>Longitude</label>
+                        <input type="number" id="longitude" value="-0.1278" min="-180" max="180" step="0.0001">
+                    </div>
+                </div>
+                <button class="btn btn-primary" onclick="event.stopPropagation(); confirmSiteLocation();" style="margin-top:10px;">Confirm Location</button>
+            </div>
+        </div>
+
+        <!-- STEP 4: DEFINE ANALYSIS AREA -->
+        <div class="step upcoming" id="step-4" onclick="openStep(4)">
+            <div class="step-header">
+                <div class="step-number">4</div>
+                <div class="step-title">Define Analysis Area</div>
+                <span class="step-check">&#10003;</span>
+                <span class="step-summary" id="step4-summary"></span>
+            </div>
+            <div class="step-body">
+                <div style="display:flex; gap:8px; margin-bottom:10px;">
+                    <button class="btn btn-secondary" id="use-entire-btn" onclick="event.stopPropagation(); useEntireScene();" style="flex:1; margin-top:0;">Analyse Entire Scene</button>
+                    <button class="btn btn-secondary" id="bbox-btn" onclick="event.stopPropagation(); toggleBboxMode();" style="flex:1; margin-top:0;">Draw Bounding Box</button>
+                </div>
+                <div class="field-row" id="bbox-fields" style="display:none;">
+                    <div class="field">
+                        <label>Min X <span class="unit">m</span></label>
+                        <input type="number" id="bbox_min_x" value="" step="0.5" placeholder="auto">
+                    </div>
+                    <div class="field">
+                        <label>Min Y <span class="unit">m</span></label>
+                        <input type="number" id="bbox_min_y" value="" step="0.5" placeholder="auto">
+                    </div>
+                </div>
+                <div class="field-row" id="bbox-fields2" style="display:none;">
+                    <div class="field">
+                        <label>Max X <span class="unit">m</span></label>
+                        <input type="number" id="bbox_max_x" value="" step="0.5" placeholder="auto">
+                    </div>
+                    <div class="field">
+                        <label>Max Y <span class="unit">m</span></label>
+                        <input type="number" id="bbox_max_y" value="" step="0.5" placeholder="auto">
+                    </div>
+                </div>
+                <hr style="border-color:#0f3460; margin:12px 0;">
+                <div class="field-row">
+                    <div class="field">
+                        <label>Grid Resolution <span class="unit">m</span></label>
+                        <select id="grid_resolution">
+                            <option value="0.25">0.25 m</option>
+                            <option value="0.5">0.5 m</option>
+                            <option value="1" selected>1 m</option>
+                            <option value="2">2 m</option>
+                        </select>
+                    </div>
+                </div>
+                <div style="font-size:11px; color:#666; margin-bottom:8px;">Smaller grid = more detail but slower analysis.</div>
+                <hr style="border-color:#0f3460; margin:12px 0;">
+                <label style="font-size:12px; color:#aaa; margin-bottom:3px; display:block;">Seasons to Analyse</label>
+                <div class="season-toggles">
+                    <div class="season-toggle" id="season-winter" onclick="toggleSeason('winter')">Winter</div>
+                    <div class="season-toggle active" id="season-spring" onclick="toggleSeason('spring')">Spring/Autumn</div>
+                    <div class="season-toggle" id="season-summer" onclick="toggleSeason('summer')">Summer</div>
+                </div>
+                <div style="font-size:11px; color:#666; margin-bottom:8px;">Select one or more seasons. At least one must be active.</div>
+                <div class="field-row">
+                    <div class="field">
+                        <label>Time Step <span class="unit">hours</span></label>
+                        <select id="time_step">
+                            <option value="0.0833">5 min</option>
+                            <option value="0.25">15 min</option>
+                            <option value="0.5">30 min</option>
+                            <option value="1" selected>1 hour</option>
+                        </select>
+                    </div>
+                </div>
+                <div id="run-btn-hint" style="font-size:11px; color:#666; margin-bottom:6px;">Select analysis area method above to enable.</div>
+                <button class="btn btn-run" id="run-btn" onclick="event.stopPropagation(); runAnalysis();" disabled style="opacity:0.4; cursor:not-allowed;">Run Analysis</button>
+            </div>
+        </div>
+
+        <!-- STEP 5: RESULTS -->
+        <div class="step upcoming" id="step-5" onclick="openStep(5)">
+            <div class="step-header">
+                <div class="step-number">5</div>
+                <div class="step-title">Results</div>
+                <span class="step-check">&#10003;</span>
+                <span class="step-summary" id="step5-summary"></span>
+            </div>
+            <div class="step-body">
+                <div class="results-panel visible" id="results-panel">
+                    <div class="results-title" id="results-title">Sun Hours Summary</div>
+                    <div class="results-detail" id="results-detail"></div>
+                </div>
+                <div style="display:flex; gap:8px; margin-top:10px;">
+                    <button class="btn btn-primary" id="glb-btn" onclick="event.stopPropagation(); showDownloadConfirm('glb');" style="flex:1;">Download GLB</button>
+                    <button class="btn btn-secondary" id="pdf-btn" onclick="event.stopPropagation(); showDownloadConfirm('pdf');" style="flex:1;">Download PDF</button>
+                </div>
+                <button class="btn btn-secondary" onclick="event.stopPropagation(); resetWorkflow();" style="margin-top:8px;">New Analysis</button>
+                <div class="bug-report">
+                    Results look wrong? <a id="bug-report-link" href="#">Report an issue</a>
+                </div>
+                <button class="btn btn-secondary" onclick="event.stopPropagation(); openBetaFeedback();" style="margin-top:10px; width:100%; font-size:11px; padding:6px 14px;">Provide Beta Testing Feedback</button>
+            </div>
+        </div>
+
+        <div class="disclaimer">
+            SunForm is beta software. There is no warranty. The Software provided under the author is incomplete and may contain errors or inaccuracies and therefore cannot be relied upon for design decision making.
+        </div>
+
+      </div>
+    </div>
+
+    <!-- ─── DOWNLOAD CONFIRMATION MODAL ─── -->
+    <div class="download-confirm-overlay" id="download-confirm-overlay">
+        <div class="download-confirm-box">
+            <h3>Confirm Download</h3>
+            <p>SunForm is beta software. There is no warranty. The Software provided under the author is incomplete and may contain errors or inaccuracies and therefore cannot be relied upon for design decision making.</p>
+            <label class="checkbox-row">
+                <input type="checkbox" id="download-confirm-check" onchange="updateDownloadConfirm()">
+                <span>I understand this is a beta output for testing only and I will not use it for any formal purpose.</span>
+            </label>
+            <div class="btn-row">
+                <button class="btn-cancel" onclick="hideDownloadConfirm()">Cancel</button>
+                <button class="btn-proceed" id="download-confirm-btn" disabled onclick="proceedDownload()">Download</button>
+            </div>
+        </div>
+    </div>
+
+    <div class="viewport" id="viewport">
+        <div class="fly-crosshair" id="fly-crosshair">+</div>
+        <div class="viewport-info" id="viewport-info">Orbit: drag | Zoom: scroll | Pan: right-drag &nbsp;|&nbsp; F: fly mode &nbsp; O: orbit mode</div>
+        <div class="coffee-wrap">
+            <a class="coffee-btn" href="https://buymeacoffee.com/jakewhite" target="_blank" rel="noopener noreferrer">
+                ☕ Buy me a coffee
+            </a>
+        </div>
+        <div class="north-arrow" id="north-arrow">
+            <div id="north-arrow-rotator" style="display:inline-block;">
+                <div>N</div>
+                <svg viewBox="0 0 50 50">
+                    <polygon points="25,5 30,20 25,15 20,20" fill="#E5A50A"/>
+                    <polygon points="25,45 20,30 25,35 30,30" fill="#666"/>
+                </svg>
+            </div>
+        </div>
+        <div class="orient-preview-container" id="orient-preview-container">
+            <img id="orient-preview" src="" alt="Plan view">
+        </div>
+        <div class="bbox-overlay" id="bbox-overlay">
+            <div class="bbox-title">Bounding Box Tool</div>
+            <div class="bbox-hint" id="bbox-hint">Click first corner on the ground plane</div>
+            <div class="bbox-coords" id="bbox-coords"></div>
+        </div>
+        <div class="colour-legend" id="colour-legend">
+            <div class="legend-label" id="legend-top-label">6h+</div>
+            <div class="legend-bar-v" id="legend-bar">
+            </div>
+            <div class="legend-label">0h</div>
+        </div>
+        <div class="season-switcher" id="season-switcher">
+            <button class="season-sw-btn" id="sw-winter" onclick="switchVisibleSeason('winter')">Winter</button>
+            <button class="season-sw-btn" id="sw-spring" onclick="switchVisibleSeason('spring')">Spring/Autumn</button>
+            <button class="season-sw-btn" id="sw-summer" onclick="switchVisibleSeason('summer')">Summer</button>
+        </div>
+        <div class="status-overlay" id="status-overlay" style="display:none;"></div>
+        <button class="debug-toggle-btn" id="debug-toggle" onclick="toggleDebugConsole()">Debug</button>
+        <div class="debug-console" id="debug-console">
+            <div class="debug-header" onclick="toggleDebugConsole()">
+                <span>Geometry Debug Console</span>
+                <span style="color:#888;">x</span>
+            </div>
+            <div class="debug-body" id="debug-body">
+                <em style="color:#666;">Run analysis to see diagnostics...</em>
+            </div>
+        </div>
+        <div class="ray-probe-panel" id="ray-probe-panel">
+            <div class="probe-title">
+                <span>Sun Ray Probe</span>
+                <button class="probe-clear-btn" onclick="clearRayProbe()">Clear</button>
+            </div>
+            <div class="probe-summary" id="probe-summary"></div>
+            <div class="probe-table" id="probe-table"></div>
+        </div>
+    </div>
+
+    <!-- Leaflet.js for location picker -->
+    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
+    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
+
+    <!-- Three.js r128 -->
+    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
+    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
+    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/exporters/GLTFExporter.js"></script>
+    <!-- web-ifc for client-side IFC parsing -->
+    <script src="https://cdn.jsdelivr.net/npm/web-ifc@0.0.57/web-ifc-api-iife.js"></script>
+    <!-- jsPDF for client-side PDF export -->
+    <script src="https://cdn.jsdelivr.net/npm/jspdf@2.5.2/dist/jspdf.umd.min.js"></script>
+    <!-- IfcOpenShell runs inside ifcos-worker.js (Web Worker) — no main-thread Pyodide needed -->
+
+    <script>
+        // ─── GLOBAL STATE ───
+        let scene, camera, renderer, controls;
+        let perspCamera, orthoCamera;
+        let buildingGroup = null;
+        let allMeshes = [];         // individual THREE.Mesh objects from IFC
+        let allMeshMeta = [];       // { mesh, expressID, ifcType, name } per mesh
+        let shadowBVH = null;       // BVH of all scene geometry for shadow casting
+        let heatmapGroup = null;
+        let bboxHelper = null;
+        let groundPlane = null;
+        let ifcApi = null;
+        let ifcLoaded = false;
+        let lastAnalysisResults = null;
+        let currentStep = 1;
+        let useEntireBounds = true;
+        let modelRotationGroup = null;
+        let northRotationDeg = 0;
+        let ifcosWorker = null;      // Web Worker for Pyodide + IfcOpenShell
+        let ifcosWorkerReady = false;
+        let analysisMeshes = [];    // IfcOpenShell-processed meshes for voxel/BVH (falls back to allMeshes)
+        let meshHealingNotes = [];  // Debug notes about mesh issues found during IfcOpenShell processing
+        let lastIFCArrayBuffer = null;  // Raw IFC bytes for IfcOpenShell processing
+
+        // Season analysis state
+        const SEASON_DATES = {
+            winter: '2024-12-21',
+            spring: '2024-03-21',
+            summer: '2024-06-21',
+        };
+        const SEASON_LABELS = {
+            winter: 'Winter',
+            spring: 'Spring/Autumn',
+            summer: 'Summer',
+        };
+        let activeSeasons = { winter: false, spring: true, summer: false };
+        let seasonResults = {};         // { winter: {results}, spring: {results}, ... }
+        let seasonHeatmaps = {};        // { winter: THREE.Group, ... }
+        let visibleSeason = 'spring';   // currently displayed season
+
+        // Ray probe state
+        let rayProbeGroup = null;       // THREE.Group holding probe ray lines + marker
+        let rayProbeActive = false;     // whether a probe is currently displayed
+
+        // Fly mode state
+        let flyMode = false;
+        const flyKeys = { w: false, a: false, s: false, d: false, q: false, e: false };
+        const FLY_SPEED = 0.5;
+        let flyYaw = 0;
+        let flyPitch = 0;
+        let flyYawTarget = 0;
+        let flyPitchTarget = 0;
+        const FLY_LOOK_SMOOTHING = 0.15;
+
+        // Leaflet map state
+        let locationMap = null;
+        let locationMarker = null;
+
+        // ─── THREE.JS SETUP ───
+        function initThree() {
+            const container = document.getElementById('viewport');
+            const w = container.clientWidth;
+            const h = container.clientHeight;
+
+            scene = new THREE.Scene();
+            scene.background = new THREE.Color(0x0a0a1a);
+
+            perspCamera = new THREE.PerspectiveCamera(45, w / h, 0.1, 10000);
+            perspCamera.position.set(50, 40, 50);
+
+            orthoCamera = new THREE.OrthographicCamera(-50, 50, 50, -50, 0.1, 10000);
+            orthoCamera.position.set(0, 500, 0);
+            orthoCamera.lookAt(0, 0, 0);
+
+            camera = perspCamera;
+
+            renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
+            renderer.setSize(w, h);
+            renderer.setPixelRatio(window.devicePixelRatio);
+            container.appendChild(renderer.domElement);
+
+            controls = new THREE.OrbitControls(camera, renderer.domElement);
+            controls.enableDamping = true;
+            controls.dampingFactor = 0.05;
+            controls.target.set(0, 5, 0);
+            controls.update();
+
+            const ambient = new THREE.AmbientLight(0x404040, 0.6);
+            scene.add(ambient);
+
+            const dir1 = new THREE.DirectionalLight(0xffffff, 0.8);
+            dir1.position.set(50, 80, 30);
+            scene.add(dir1);
+
+            const dir2 = new THREE.DirectionalLight(0x8888ff, 0.3);
+            dir2.position.set(-30, 20, -50);
+            scene.add(dir2);
+
+            const grid = new THREE.GridHelper(200, 200, 0x222244, 0x111133);
+            grid.visible = false;
+            scene.add(grid);
+
+            const planeGeo = new THREE.PlaneGeometry(2000, 2000);
+            const planeMat = new THREE.MeshBasicMaterial({ visible: false, side: THREE.DoubleSide });
+            groundPlane = new THREE.Mesh(planeGeo, planeMat);
+            groundPlane.rotation.x = -Math.PI / 2;
+            groundPlane.position.y = 0;
+            scene.add(groundPlane);
+
+            document.querySelector('.panel').addEventListener('mousedown', (e) => {
+                e.stopPropagation();
+            });
+
+            window.addEventListener('resize', () => {
+                const w = container.clientWidth;
+                const h = container.clientHeight;
+                perspCamera.aspect = w / h;
+                perspCamera.updateProjectionMatrix();
+                updateOrthoCamera();
+                renderer.setSize(w, h);
+            });
+
+            animate();
+        }
+
+        function animate() {
+            requestAnimationFrame(animate);
+            updateFlyMovement();
+            if (!flyMode) controls.update();
+            renderer.render(scene, camera);
+        }
+
+        function updateOrthoCamera() {
+            if (!buildingGroup) return;
+            const bb = new THREE.Box3().setFromObject(buildingGroup);
+            const cx = (bb.min.x + bb.max.x) / 2;
+            const cz = (bb.min.z + bb.max.z) / 2;
+            const sx = (bb.max.x - bb.min.x) / 2 + 10;
+            const sz = (bb.max.z - bb.min.z) / 2 + 10;
+            const s = Math.max(sx, sz);
+            const container = document.getElementById('viewport');
+            const aspect = container.clientWidth / container.clientHeight;
+            orthoCamera.left = -s * aspect;
+            orthoCamera.right = s * aspect;
+            orthoCamera.top = s;
+            orthoCamera.bottom = -s;
+            orthoCamera.position.set(cx, 500, cz);
+            orthoCamera.lookAt(cx, 0, cz);
+            orthoCamera.updateProjectionMatrix();
+        }
+
+        function switchToOrtho() {
+            updateOrthoCamera();
+            camera = orthoCamera;
+            controls.object = camera;
+            controls.enableRotate = false;
+            controls.update();
+        }
+
+        function switchToPersp() {
+            camera = perspCamera;
+            controls.object = camera;
+            controls.enableRotate = true;
+            controls.update();
+        }
+
+        // ─── INIT WEB-IFC ───
+        async function initWebIfc() {
+            try {
+                ifcApi = new WebIFC.IfcAPI();
+                await ifcApi.Init();
+                console.log('web-ifc initialised');
+            } catch (err) {
+                console.error('web-ifc init failed:', err);
+                ifcApi = null;
+            }
+        }
+
+        // ─── ACCORDION WORKFLOW ───
+        function openStep(n) {
+            const step = document.getElementById('step-' + n);
+            if (step.classList.contains('upcoming')) return;
+            for (let i = 1; i <= 5; i++) {
+                const s = document.getElementById('step-' + i);
+                if (i === n) {
+                    s.classList.add('active');
+                    s.classList.remove('upcoming');
+                } else if (s.classList.contains('completed')) {
+                    s.classList.remove('active');
+                } else if (i > n) {
+                    if (!s.classList.contains('completed')) {
+                        s.classList.add('upcoming');
+                    }
+                    s.classList.remove('active');
+                } else {
+                    s.classList.remove('active');
+                }
+            }
+            currentStep = n;
+
+            switchToPersp();
+            if (n !== 5) clearRayProbe();
+
+            // Step 2: show orientation preview, lock controls
+            if (n === 2) {
+                showOrientationPreview();
+            } else {
+                hideOrientationPreview();
+            }
+
+            // Mesh visibility: gray out on step 4, show results on step 5
+            if (n === 4 && Object.keys(seasonHeatmaps).length > 0) {
+                showCalculationMeshes();
+                grayOutResults();
+            } else if (n === 5) {
+                hideCalculationMeshes();
+                restoreResults();
+            } else {
+                showCalculationMeshes();
+                if (Object.keys(seasonHeatmaps).length > 0) {
+                    restoreResults();
+                }
+            }
+
+            // Lazy-init Leaflet map when step 3 (Site Location) first opens
+            if (n === 3 && !mapInitialized) {
+                mapInitialized = true;
+                setTimeout(() => {
+                    initLocationMap();
+                    locationMap.invalidateSize();
+                }, 100);
+            }
+        }
+
+        function completeStep(n, summary) {
+            const step = document.getElementById('step-' + n);
+            step.classList.add('completed');
+            step.classList.remove('active');
+            const sumEl = document.getElementById('step' + n + '-summary');
+            if (sumEl) sumEl.textContent = summary;
+            // Advance to next
+            const next = n + 1;
+            if (next <= 5) {
+                const ns = document.getElementById('step-' + next);
+                ns.classList.remove('upcoming');
+                openStep(next);
+            }
+        }
+
+        function resetWorkflow() {
+            // Restore mesh visibility before cleanup
+            showCalculationMeshes();
+            clearRayProbe();
+            // Reset all state
+            if (buildingGroup) {
+                scene.remove(buildingGroup);
+                buildingGroup = null;
+            }
+            if (modelRotationGroup) {
+                scene.remove(modelRotationGroup);
+                modelRotationGroup = null;
+            }
+            if (heatmapGroup) {
+                scene.remove(heatmapGroup);
+                heatmapGroup = null;
+            }
+            // Remove all season heatmaps
+            for (const [key, group] of Object.entries(seasonHeatmaps)) {
+                scene.remove(group);
+                group.traverse(c => {
+                    if (c.geometry) c.geometry.dispose();
+                    if (c.material) c.material.dispose();
+                });
+            }
+            seasonHeatmaps = {};
+            seasonResults = {};
+            cachedCellData = null;
+            cachedGridSize = null;
+            cachedCellMap = null;
+            cachedSliverIndices = null;
+            visibleSeason = 'spring';
+            document.getElementById('season-switcher').classList.remove('visible');
+            removeBboxHelper();
+            allMeshes = [];
+            allMeshMeta = [];
+            analysisMeshes = [];
+            lastIFCArrayBuffer = null;
+            shadowBVH = null;
+            ifcLoaded = false;
+            lastAnalysisResults = null;
+            useEntireBounds = true;
+            northRotationDeg = 0;
+            hideOrientationPreview();
+            document.getElementById('orient-preview').style.transform = 'rotate(0deg)';
+            document.getElementById('north-arrow-rotator').style.transform = 'rotate(0deg)';
+            document.getElementById('colour-legend').classList.remove('visible');
+            document.getElementById('upload-text').textContent = 'Drop IFC file here or click to browse';
+            document.getElementById('upload-filename').style.display = 'none';
+            document.getElementById('upload-zone').classList.remove('loaded');
+            const ifcosStatusEl = document.getElementById('ifcos-status');
+            if (ifcosStatusEl) { ifcosStatusEl.style.display = 'none'; ifcosStatusEl.style.color = '#aaa'; }
+            document.getElementById('bbox-fields').style.display = 'none';
+            document.getElementById('bbox-fields2').style.display = 'none';
+
+            // Reset run button to disabled state
+            const runBtn = document.getElementById('run-btn');
+            runBtn.disabled = true;
+            runBtn.style.opacity = '0.4';
+            runBtn.style.cursor = 'not-allowed';
+            const runHint = document.getElementById('run-btn-hint');
+            if (runHint) runHint.style.display = '';
+
+            for (let i = 1; i <= 5; i++) {
+                const s = document.getElementById('step-' + i);
+                s.classList.remove('completed', 'active', 'upcoming');
+                if (i === 1) s.classList.add('active');
+                else s.classList.add('upcoming');
+                const sum = document.getElementById('step' + i + '-summary');
+                if (sum) sum.textContent = '';
+            }
+            currentStep = 1;
+            switchToPersp();
+        }
+
+        // ─── IFC UPLOAD (client-side parsing — per-mesh) ───
+        const uploadZone = document.getElementById('upload-zone');
+
+        uploadZone.addEventListener('dragover', (e) => {
+            e.preventDefault();
+            e.stopPropagation();
+            uploadZone.classList.add('dragover');
+        });
+
+        uploadZone.addEventListener('dragleave', () => {
+            uploadZone.classList.remove('dragover');
+        });
+
+        uploadZone.addEventListener('drop', (e) => {
+            e.preventDefault();
+            e.stopPropagation();
+            uploadZone.classList.remove('dragover');
+            const files = e.dataTransfer.files;
+            if (files.length > 0 && files[0].name.toLowerCase().endsWith('.ifc')) {
+                parseIFCClientSide(files[0]);
+            }
+        });
+
+        function handleFileUpload(input) {
+            if (input.files.length > 0) {
+                parseIFCClientSide(input.files[0]);
+            }
+        }
+
+        async function parseIFCClientSide(file) {
+            if (!ifcApi) {
+                document.getElementById('upload-text').textContent =
+                    'web-ifc not ready. Please wait and try again.';
+                return;
+            }
+
+            const progressBar = document.getElementById('upload-progress');
+            progressBar.classList.add('visible');
+            document.getElementById('upload-text').textContent = 'Parsing IFC (client-side)...';
+            showStatus('Parsing IFC file in browser...');
+
+            try {
+                const arrayBuffer = await file.arrayBuffer();
+                lastIFCArrayBuffer = arrayBuffer;  // Save for IfcOpenShell processing
+                const data = new Uint8Array(arrayBuffer);
+                const modelID = ifcApi.OpenModel(data);
+
+                // Collect per-mesh geometry
+                if (buildingGroup) {
+                    scene.remove(buildingGroup);
+                    buildingGroup.traverse(c => {
+                        if (c.geometry) c.geometry.dispose();
+                        if (c.material) c.material.dispose();
+                    });
+                }
+                if (modelRotationGroup) {
+                    scene.remove(modelRotationGroup);
+                }
+
+                buildingGroup = new THREE.Group();
+                buildingGroup.name = 'buildings';
+                modelRotationGroup = new THREE.Group();
+                modelRotationGroup.name = 'rotation_group';
+                modelRotationGroup.add(buildingGroup);
+                scene.add(modelRotationGroup);
+
+                allMeshes = [];
+                allMeshMeta = [];
+
+                // Gather IFC type info for express IDs
+                const ifcTypes = {};
+                try {
+                    // Try to get IfcSite and IfcSlab entities for ground suggestions
+                    const IFCSITE = 4097777520;
+                    const IFCSLAB = 1529196076;
+                    const IFCBUILDINGSTOREY = 3124254112;
+                    [IFCSITE, IFCSLAB].forEach(typeId => {
+                        try {
+                            const ids = ifcApi.GetLineIDsWithType(modelID, typeId);
+                            for (let i = 0; i < ids.size(); i++) {
+                                ifcTypes[ids.get(i)] = typeId === IFCSITE ? 'IfcSite' : 'IfcSlab';
+                            }
+                        } catch(e) {}
+                    });
+                } catch(e) {}
+
+                let meshIndex = 0;
+                ifcApi.StreamAllMeshes(modelID, (mesh) => {
+                    const expressID = mesh.expressID;
+                    const placedGeometries = mesh.geometries;
+
+                    const meshVertices = [];
+                    const meshIndices = [];
+                    let vertexOffset = 0;
+
+                    for (let i = 0; i < placedGeometries.size(); i++) {
+                        const placedGeom = placedGeometries.get(i);
+                        const geomData = ifcApi.GetGeometry(modelID, placedGeom.geometryExpressID);
+
+                        const vertPtr = geomData.GetVertexData();
+                        const vertSize = geomData.GetVertexDataSize();
+                        const idxPtr = geomData.GetIndexData();
+                        const idxSize = geomData.GetIndexDataSize();
+
+                        const verts = new Float32Array(ifcApi.GetVertexArray(vertPtr, vertSize));
+                        const indices = new Uint32Array(ifcApi.GetIndexArray(idxPtr, idxSize));
+                        geomData.delete();
+
+                        if (verts.length === 0 || indices.length === 0) continue;
+
+                        const flatMatrix = placedGeom.flatTransformation;
+                        const m = new THREE.Matrix4();
+                        m.set(
+                            flatMatrix[0], flatMatrix[4], flatMatrix[8],  flatMatrix[12],
+                            flatMatrix[1], flatMatrix[5], flatMatrix[9],  flatMatrix[13],
+                            flatMatrix[2], flatMatrix[6], flatMatrix[10], flatMatrix[14],
+                            flatMatrix[3], flatMatrix[7], flatMatrix[11], flatMatrix[15]
+                        );
+
+                        const numVerts = verts.length / 6;
+                        for (let v = 0; v < numVerts; v++) {
+                            const pos = new THREE.Vector3(
+                                verts[v * 6], verts[v * 6 + 1], verts[v * 6 + 2]
+                            );
+                            pos.applyMatrix4(m);
+                            meshVertices.push(pos.x, pos.y, pos.z);
+                        }
+
+                        for (let idx = 0; idx < indices.length; idx++) {
+                            meshIndices.push(indices[idx] + vertexOffset);
+                        }
+                        vertexOffset += numVerts;
+                    }
+
+                    if (meshVertices.length === 0) return;
+
+                    const geo = new THREE.BufferGeometry();
+                    const positions = new Float32Array(meshVertices);
+                    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
+                    geo.setIndex(new THREE.BufferAttribute(new Uint32Array(meshIndices), 1));
+                    geo.computeVertexNormals();
+
+                    const mat = new THREE.MeshPhongMaterial({
+                        color: 0xdddddd,
+                        flatShading: true,
+                        side: THREE.DoubleSide,
+                    });
+
+                    const thMesh = new THREE.Mesh(geo, mat);
+                    thMesh.name = 'mesh_' + meshIndex;
+                    thMesh.userData.expressID = expressID;
+                    thMesh.userData.ifcType = ifcTypes[expressID] || '';
+                    buildingGroup.add(thMesh);
+
+                    allMeshes.push(thMesh);
+                    allMeshMeta.push({
+                        mesh: thMesh,
+                        expressID: expressID,
+                        ifcType: ifcTypes[expressID] || '',
+                        name: 'mesh_' + meshIndex + (ifcTypes[expressID] ? ' (' + ifcTypes[expressID] + ')' : ''),
+                    });
+                    meshIndex++;
+                });
+
+                ifcApi.CloseModel(modelID);
+
+                if (allMeshes.length === 0) {
+                    throw new Error('No geometry found in IFC file');
+                }
+
+                ifcLoaded = true;
+
+                // Fit camera
+                const bb = new THREE.Box3().setFromObject(buildingGroup);
+                const cx = (bb.min.x + bb.max.x) / 2;
+                const cy = (bb.min.y + bb.max.y) / 2;
+                const cz = (bb.min.z + bb.max.z) / 2;
+                const size = Math.max(bb.max.x - bb.min.x, bb.max.y - bb.min.y, bb.max.z - bb.min.z);
+                const dist = size * 1.5;
+                perspCamera.position.set(cx + dist, cy + dist * 0.7, cz + dist);
+                controls.target.set(cx, cy, cz);
+                controls.update();
+
+                uploadZone.classList.add('loaded');
+                document.getElementById('upload-text').textContent = 'IFC loaded';
+                document.getElementById('upload-filename').textContent = file.name + ' (' + allMeshes.length + ' meshes)';
+                document.getElementById('upload-filename').style.display = 'block';
+                progressBar.classList.remove('visible');
+                hideStatus();
+
+                completeStep(1, file.name);
+
+                // Capture top-down screenshot for orientation step
+                setTimeout(() => captureOrientationPreview(), 200);
+
+                // Start IfcOpenShell processing in background
+                processWithIfcOpenShell(arrayBuffer);
+
+            } catch (err) {
+                console.error('IFC parse error:', err);
+                progressBar.classList.remove('visible');
+                document.getElementById('upload-text').textContent = 'Parse error: ' + err.message;
+                uploadZone.classList.remove('loaded');
+                hideStatus();
+            }
+        }
+
+        // ─── IFCOPENSHELL VIA WEB WORKER ───
+        function initIfcosWorker() {
+            if (ifcosWorker) return;
+            ifcosWorker = new Worker('/ifcos-worker.js');
+            ifcosWorker.postMessage({ type: 'init' });
+            ifcosWorker.onmessage = (e) => {
+                const d = e.data;
+                if (d.type === 'status') {
+                    showStatus(d.msg);
+                    const statusEl = document.getElementById('ifcos-status');
+                    if (statusEl) { statusEl.textContent = d.msg; statusEl.style.display = 'block'; }
+                } else if (d.type === 'ready') {
+                    ifcosWorkerReady = true;
+                    console.log('IfcOpenShell worker ready');
+                }
+            };
+            ifcosWorker.onerror = (err) => {
+                console.error('IfcOpenShell worker error:', err);
+            };
+        }
+
+        async function processWithIfcOpenShell(arrayBuffer) {
+            const statusEl = document.getElementById('ifcos-status');
+            try {
+                if (statusEl) {
+                    statusEl.textContent = 'Loading IfcOpenShell (Web Worker)...';
+                    statusEl.style.display = 'block';
+                }
+
+                // Ensure worker is created
+                if (!ifcosWorker) initIfcosWorker();
+
+                // Send IFC data to worker and wait for result
+                const workerResult = await new Promise((resolve, reject) => {
+                    const handler = (e) => {
+                        const d = e.data;
+                        if (d.type === 'status') {
+                            showStatus(d.msg);
+                            if (statusEl) statusEl.textContent = d.msg;
+                        } else if (d.type === 'ready') {
+                            ifcosWorkerReady = true;
+                            // Worker just finished init, don't resolve yet — wait for result
+                        } else if (d.type === 'result') {
+                            ifcosWorker.onmessage = null;
+                            resolve(d);
+                        } else if (d.type === 'error') {
+                            ifcosWorker.onmessage = null;
+                            reject(new Error(d.error));
+                        }
+                    };
+                    ifcosWorker.onmessage = handler;
+                    // Transfer the buffer to avoid copying
+                    const copy = arrayBuffer.slice(0);
+                    ifcosWorker.postMessage({ type: 'process', buffer: copy }, [copy]);
+                });
+
+                const { vBuf, fBuf, nv, nf, stats } = workerResult;
+
+                console.log(`IfcOpenShell merge+cull:`, stats);
+
+                if (nf === 0) {
+                    console.warn('IfcOpenShell returned no geometry, falling back to web-ifc meshes');
+                    analysisMeshes = [];
+                    if (statusEl) statusEl.textContent = 'IfcOpenShell: no geometry (using web-ifc)';
+                    hideStatus();
+                    return;
+                }
+
+                // Create single merged Three.js mesh (outer shell)
+                if (statusEl) statusEl.textContent = 'Creating merged shell mesh...';
+                await new Promise(r => setTimeout(r, 0));
+
+                analysisMeshes = [];
+                meshHealingNotes = [];
+
+                const verts = new Float32Array(vBuf);
+                const faceIdx = new Uint32Array(fBuf);
+
+                // Convert IFC coordinates (Z-up) to Three.js coordinates (Y-up)
+                for (let i = 0; i < nv; i++) {
+                    const ix = i * 3;
+                    const ifcX = verts[ix], ifcY = verts[ix + 1], ifcZ = verts[ix + 2];
+                    verts[ix]     = ifcX;
+                    verts[ix + 1] = ifcZ;
+                    verts[ix + 2] = -ifcY;
+                }
+
+                const geo = new THREE.BufferGeometry();
+                geo.setAttribute('position', new THREE.BufferAttribute(verts, 3));
+                geo.setIndex(new THREE.BufferAttribute(faceIdx, 1));
+                geo.computeVertexNormals();
+
+                const mat = new THREE.MeshPhongMaterial({
+                    color: 0xdddddd,
+                    flatShading: true,
+                    side: THREE.DoubleSide,
+                    visible: false,
+                });
+
+                const mesh = new THREE.Mesh(geo, mat);
+                mesh.name = 'ifcos_merged_shell';
+                if (modelRotationGroup) {
+                    modelRotationGroup.add(mesh);
+                }
+
+                analysisMeshes.push(mesh);
+
+                if (stats.interior_removed > 0) {
+                    meshHealingNotes.push({ type: 'info', elem: -1,
+                        msg: `Merged ${stats.elements} elements, removed ${stats.interior_removed} interior faces, ` +
+                             `verts ${stats.verts_before} → ${stats.verts_after}, faces ${stats.faces_before} → ${stats.faces_after}` });
+                }
+
+                console.log(`IfcOpenShell: merged shell — ${nv} verts, ${nf} faces (removed ${stats.interior_removed} interior)`);
+
+                if (statusEl) {
+                    statusEl.textContent = `IfcOpenShell: ${nf} faces (${stats.interior_removed} interior removed)`;
+                    statusEl.style.color = '#4CAF50';
+                }
+                hideStatus();
+
+            } catch (err) {
+                console.error('IfcOpenShell processing error:', err);
+                analysisMeshes = [];  // Fall back to web-ifc meshes
+                meshHealingNotes.push({ type: 'error', elem: -1, msg: 'IfcOpenShell FAILED: ' + (err.message || String(err)).substring(0, 200) });
+                if (statusEl) {
+                    statusEl.textContent = 'IfcOpenShell failed: ' + (err.message || String(err)).substring(0, 80);
+                    statusEl.style.color = '#ff6b6b';
+                }
+                hideStatus();
+            }
+        }
+
+        // Get the meshes to use for analysis (prefer IfcOpenShell, fall back to web-ifc)
+        // Analysis always uses web-ifc meshes (robust for voxel pipeline).
+        // IfcOpenShell meshes are used for display only (painted with analysis results).
+        function getAnalysisMeshes() {
+            return allMeshes;
+        }
+
+        // ─── DEBUG CONSOLE ───
+
+        function toggleDebugConsole() {
+            const el = document.getElementById('debug-console');
+            el.classList.toggle('visible');
+        }
+
+        function computeBBox(meshes) {
+            const min = [Infinity, Infinity, Infinity];
+            const max = [-Infinity, -Infinity, -Infinity];
+            let totalTris = 0;
+            for (const mesh of meshes) {
+                mesh.updateWorldMatrix(true, false);
+                const wm = mesh.matrixWorld;
+                const pos = mesh.geometry.attributes.position.array;
+                const idx = mesh.geometry.index ? mesh.geometry.index.array : null;
+                const nv = pos.length / 3;
+                totalTris += idx ? idx.length / 3 : nv / 3;
+                const v = new THREE.Vector3();
+                for (let i = 0; i < nv; i++) {
+                    v.set(pos[i*3], pos[i*3+1], pos[i*3+2]).applyMatrix4(wm);
+                    if (v.x < min[0]) min[0] = v.x; if (v.x > max[0]) max[0] = v.x;
+                    if (v.y < min[1]) min[1] = v.y; if (v.y > max[1]) max[1] = v.y;
+                    if (v.z < min[2]) min[2] = v.z; if (v.z > max[2]) max[2] = v.z;
+                }
+            }
+            return { min, max, tris: totalTris };
+        }
+
+        function updateDebugConsole(debugData) {
+            const body = document.getElementById('debug-body');
+            if (!body) return;
+
+            const d = debugData;
+            const pct = (v, total) => total > 0 ? (v / total * 100).toFixed(1) + '%' : '0%';
+            const fmt = v => typeof v === 'number' ? v.toLocaleString() : v;
+            const fmtV = (arr) => arr.map(v => v.toFixed(2)).join(', ');
+
+            let html = '';
+
+            // Render mode
+            const mode = d.mode || 'dual-geometry';
+            const modeCls = mode === 'dual-geometry' ? 'debug-ok' : 'debug-warn';
+            html += `<div style="margin-bottom:4px;">Mode: <span class="${modeCls}">${mode}</span></div>`;
+
+            if (mode === 'voxel-only') {
+                html += `<div class="debug-warn" style="margin-bottom:6px;">IfcOpenShell not loaded — using voxel-clipped triangles for display.<br>`;
+                html += `IfcOpenShell Worker: ${ifcosWorker ? (ifcosWorkerReady ? 'ready' : 'loading') : 'not started'}<br>`;
+                // Check for IfcOpenShell error
+                const ifcosErr = meshHealingNotes.find(n => n.msg && n.msg.startsWith('IfcOpenShell FAILED'));
+                if (ifcosErr) {
+                    html += `<span class="debug-err">${ifcosErr.msg}</span><br>`;
+                }
+                const ifcosStatus = document.getElementById('ifcos-status');
+                if (ifcosStatus && ifcosStatus.textContent) {
+                    html += `Status: ${ifcosStatus.textContent}`;
+                }
+                html += `</div>`;
+            }
+
+            // Geometry sources
+            html += '<div class="debug-section-title">Geometry Sources</div>';
+            html += '<table>';
+            html += `<tr><td>web-ifc meshes</td><td>${fmt(d.webifcMeshCount)} (${fmt(d.webifcTris)} tris)</td></tr>`;
+            html += `<tr><td>IfcOpenShell meshes</td><td>${fmt(d.ifcosMeshCount)} (${fmt(d.ifcosTris)} tris)</td></tr>`;
+            html += '</table>';
+
+            // Bounding boxes
+            if (d.webifcBBox && d.ifcosBBox) {
+                html += '<div class="debug-section"><div class="debug-section-title">Bounding Boxes (world space)</div>';
+                html += '<table>';
+                html += `<tr><td>web-ifc min</td><td>${fmtV(d.webifcBBox.min)}</td></tr>`;
+                html += `<tr><td>web-ifc max</td><td>${fmtV(d.webifcBBox.max)}</td></tr>`;
+                html += `<tr><td>IfcOS min</td><td>${fmtV(d.ifcosBBox.min)}</td></tr>`;
+                html += `<tr><td>IfcOS max</td><td>${fmtV(d.ifcosBBox.max)}</td></tr>`;
+
+                // Offset between centres
+                const wcx = (d.webifcBBox.min[0] + d.webifcBBox.max[0]) / 2;
+                const wcy = (d.webifcBBox.min[1] + d.webifcBBox.max[1]) / 2;
+                const wcz = (d.webifcBBox.min[2] + d.webifcBBox.max[2]) / 2;
+                const icx = (d.ifcosBBox.min[0] + d.ifcosBBox.max[0]) / 2;
+                const icy = (d.ifcosBBox.min[1] + d.ifcosBBox.max[1]) / 2;
+                const icz = (d.ifcosBBox.min[2] + d.ifcosBBox.max[2]) / 2;
+                const offX = icx - wcx, offY = icy - wcy, offZ = icz - wcz;
+                const dist = Math.sqrt(offX*offX + offY*offY + offZ*offZ);
+                const cls = dist > 1 ? 'debug-err' : dist > 0.1 ? 'debug-warn' : 'debug-ok';
+                html += `<tr><td>Centre offset</td><td class="${cls}">${offX.toFixed(3)}, ${offY.toFixed(3)}, ${offZ.toFixed(3)} (${dist.toFixed(3)}m)</td></tr>`;
+                html += '</table></div>';
+            }
+
+            // Voxel grid info
+            html += '<div class="debug-section"><div class="debug-section-title">Voxel Grid</div>';
+            html += '<table>';
+            html += `<tr><td>Grid size</td><td>${d.gridSize.toFixed(3)}m</td></tr>`;
+            html += `<tr><td>Voxel cells</td><td>${fmt(d.voxelCellCount)}</td></tr>`;
+            html += '</table></div>';
+
+            // Match statistics
+            html += '<div class="debug-section"><div class="debug-section-title">Triangle → Voxel Mapping</div>';
+            html += '<table>';
+            html += `<tr><td>Total triangles</td><td>${fmt(d.totalDisplayTris)}</td></tr>`;
+            const exactCls = d.exactMatches / d.totalDisplayTris > 0.7 ? 'debug-ok' : 'debug-warn';
+            html += `<tr><td>Exact voxel match</td><td class="${exactCls}">${fmt(d.exactMatches)} (${pct(d.exactMatches, d.totalDisplayTris)})</td></tr>`;
+            html += `<tr><td>Neighbour match</td><td>${fmt(d.neighbourMatches)} (${pct(d.neighbourMatches, d.totalDisplayTris)})</td></tr>`;
+            const missCls = d.misses / d.totalDisplayTris > 0.1 ? 'debug-err' : d.misses > 0 ? 'debug-warn' : 'debug-ok';
+            html += `<tr><td>No match (magenta)</td><td class="${missCls}">${fmt(d.misses)} (${pct(d.misses, d.totalDisplayTris)})</td></tr>`;
+            html += `<tr><td>Degenerate (skipped)</td><td>${fmt(d.degenerate)}</td></tr>`;
+            html += '</table></div>';
+
+            // Hours distribution
+            if (d.hoursDistribution) {
+                html += '<div class="debug-section"><div class="debug-section-title">Hours Distribution (mapped tris)</div>';
+                html += '<table>';
+                for (const [range, count] of d.hoursDistribution) {
+                    html += `<tr><td>${range}</td><td>${fmt(count)}</td></tr>`;
+                }
+                html += '</table></div>';
+            }
+
+            // Mesh healing notes
+            if (meshHealingNotes.length > 0) {
+                // Summary stats
+                const errors = meshHealingNotes.filter(n => n.type === 'error');
+                const warns = meshHealingNotes.filter(n => n.type === 'warn');
+                const titleCls = errors.length > 0 ? 'debug-err' : 'debug-warn';
+
+                html += `<div class="debug-section"><div class="debug-section-title ${titleCls}">Mesh Healing (${meshHealingNotes.length} issues)</div>`;
+                html += '<table>';
+
+                // Count unique issue types
+                const issueCounts = {};
+                for (const note of meshHealingNotes) {
+                    const cat = note.msg.split(':')[0].split('(')[0].trim();
+                    issueCounts[cat] = (issueCounts[cat] || 0) + 1;
+                }
+                for (const [cat, count] of Object.entries(issueCounts)) {
+                    html += `<tr><td>${cat}</td><td>${count} elements</td></tr>`;
+                }
+                html += '</table>';
+
+                // Show first 20 detailed notes
+                const showNotes = meshHealingNotes.slice(0, 20);
+                html += '<div style="margin-top:4px; font-size:10px; max-height:250px; overflow-y:auto;">';
+                for (const note of showNotes) {
+                    const cls = note.type === 'error' ? 'debug-err' : 'debug-warn';
+                    const prefix = note.elem >= 0 ? `elem[${note.elem}]: ` : '';
+                    const msgHtml = note.msg.replace(/\n/g, '<br>');
+                    html += `<div class="${cls}" style="margin-bottom:3px; white-space:pre-wrap;">${prefix}${msgHtml}</div>`;
+                }
+                if (meshHealingNotes.length > 20) {
+                    html += `<div style="color:#666;">...and ${meshHealingNotes.length - 20} more</div>`;
+                }
+                html += '</div></div>';
+            } else if (analysisMeshes.length > 0) {
+                html += '<div class="debug-section"><div class="debug-section-title debug-ok">Mesh Healing</div>';
+                html += '<div style="color:#4CAF50;">All elements passed health checks</div></div>';
+            }
+
+            body.innerHTML = html;
+
+            // Auto-show if there are problems
+            if (d.misses / d.totalDisplayTris > 0.05 || meshHealingNotes.some(n => n.type === 'error')) {
+                document.getElementById('debug-console').classList.add('visible');
+            }
+        }
+
+        // ─── VERTEX WELDING & DUPLICATE FACE REMOVAL ───
+
+        // Merge vertices within a tolerance and remove duplicate/degenerate faces.
+        // This makes the concatenated IfcOpenShell mesh continuous at element seams.
+        function weldMesh(positions, indices, tolerance) {
+            tolerance = tolerance || 0.001;  // 1mm default
+            const invTol = 1.0 / tolerance;
+            const vertexCount = positions.length / 3;
+            const faceCount = indices.length / 3;
+
+            // Quantise vertex positions to grid cells of size=tolerance
+            // Map quantised key → canonical vertex index
+            const keyToCanon = new Map();
+            const oldToCanon = new Uint32Array(vertexCount);
+            let canonCount = 0;
+            const canonPositions = [];  // flat x,y,z
+
+            for (let v = 0; v < vertexCount; v++) {
+                const x = positions[v * 3];
+                const y = positions[v * 3 + 1];
+                const z = positions[v * 3 + 2];
+
+                const qx = Math.round(x * invTol);
+                const qy = Math.round(y * invTol);
+                const qz = Math.round(z * invTol);
+                const key = qx + ',' + qy + ',' + qz;
+
+                if (keyToCanon.has(key)) {
+                    oldToCanon[v] = keyToCanon.get(key);
+                } else {
+                    const ci = canonCount++;
+                    keyToCanon.set(key, ci);
+                    oldToCanon[v] = ci;
+                    canonPositions.push(x, y, z);
+                }
+            }
+
+            // Remap face indices and remove degenerate + duplicate faces
+            const faceSet = new Set();
+            const newIndices = [];
+            let degenerateCount = 0;
+            let duplicateCount = 0;
+
+            for (let f = 0; f < faceCount; f++) {
+                let a = oldToCanon[indices[f * 3]];
+                let b = oldToCanon[indices[f * 3 + 1]];
+                let c = oldToCanon[indices[f * 3 + 2]];
+
+                // Skip degenerate faces (two or more vertices collapsed to same point)
+                if (a === b || b === c || a === c) {
+                    degenerateCount++;
+                    continue;
+                }
+
+                // Canonical face key: sorted vertex indices
+                const sorted = [a, b, c].sort((x, y) => x - y);
+                const faceKey = sorted[0] + ',' + sorted[1] + ',' + sorted[2];
+
+                if (faceSet.has(faceKey)) {
+                    duplicateCount++;
+                    continue;
+                }
+                faceSet.add(faceKey);
+
+                newIndices.push(a, b, c);
+            }
+
+            const mergedVerts = vertexCount - canonCount;
+            const removedFaces = degenerateCount + duplicateCount;
+            console.log(`Vertex welding: ${vertexCount}→${canonCount} verts (${mergedVerts} merged), ` +
+                `${faceCount}→${newIndices.length / 3} faces (${degenerateCount} degenerate, ${duplicateCount} duplicate removed)`);
+
+            return {
+                positions: new Float32Array(canonPositions),
+                indices: new Uint32Array(newIndices),
+                mergedVerts,
+                degenerateCount,
+                duplicateCount,
+            };
+        }
+
+        // ─── MANIFOLD CHECK & VOID REMOVAL ───
+
+        // Make an edge key with sorted vertex indices (order-independent)
+        function edgeKey(a, b) {
+            return a < b ? a + ',' + b : b + ',' + a;
+        }
+
+        // Check manifoldness and find connected components
+        // Returns { isManifold, components: [{faces: [faceIdx,...], manifold: bool}], edgeMap }
+        function analyseMesh(positions, indices) {
+            const faceCount = indices.length / 3;
+
+            // Build edge → face list map
+            const edgeFaces = new Map();
+            for (let f = 0; f < faceCount; f++) {
+                const i0 = indices[f * 3], i1 = indices[f * 3 + 1], i2 = indices[f * 3 + 2];
+                const edges = [edgeKey(i0, i1), edgeKey(i1, i2), edgeKey(i2, i0)];
+                for (const ek of edges) {
+                    if (!edgeFaces.has(ek)) edgeFaces.set(ek, []);
+                    edgeFaces.get(ek).push(f);
+                }
+            }
+
+            // Overall manifold check: every edge has exactly 2 faces
+            let isManifold = true;
+            let nonManifoldEdges = 0;
+            let boundaryEdges = 0;
+            for (const [ek, faces] of edgeFaces) {
+                if (faces.length !== 2) {
+                    isManifold = false;
+                    if (faces.length === 1) boundaryEdges++;
+                    else nonManifoldEdges++;
+                }
+            }
+
+            console.log(`Mesh analysis: ${faceCount} faces, ${edgeFaces.size} edges, manifold=${isManifold}, boundary=${boundaryEdges}, non-manifold=${nonManifoldEdges}`);
+
+            // Find connected components via face adjacency (shared edges)
+            const faceAdj = new Array(faceCount);
+            for (let f = 0; f < faceCount; f++) faceAdj[f] = [];
+
+            for (const [ek, faces] of edgeFaces) {
+                for (let i = 0; i < faces.length; i++) {
+                    for (let j = i + 1; j < faces.length; j++) {
+                        faceAdj[faces[i]].push(faces[j]);
+                        faceAdj[faces[j]].push(faces[i]);
+                    }
+                }
+            }
+
+            const visited = new Uint8Array(faceCount);
+            const components = [];
+
+            for (let f = 0; f < faceCount; f++) {
+                if (visited[f]) continue;
+                const component = [];
+                const stack = [f];
+                visited[f] = 1;
+                while (stack.length > 0) {
+                    const cur = stack.pop();
+                    component.push(cur);
+                    for (const adj of faceAdj[cur]) {
+                        if (!visited[adj]) {
+                            visited[adj] = 1;
+                            stack.push(adj);
+                        }
+                    }
+                }
+                components.push(component);
+            }
+
+            // Check manifoldness per component
+            const componentInfos = components.map(comp => {
+                const faceSet = new Set(comp);
+                let compManifold = true;
+                let compBoundary = 0;
+                for (const f of comp) {
+                    const i0 = indices[f * 3], i1 = indices[f * 3 + 1], i2 = indices[f * 3 + 2];
+                    const edges = [edgeKey(i0, i1), edgeKey(i1, i2), edgeKey(i2, i0)];
+                    for (const ek of edges) {
+                        const ef = edgeFaces.get(ek);
+                        const inComp = ef.filter(ff => faceSet.has(ff));
+                        if (inComp.length !== 2) {
+                            compManifold = false;
+                            if (inComp.length === 1) compBoundary++;
+                        }
+                    }
+                }
+                return { faces: comp, manifold: compManifold, boundaryEdges: compBoundary };
+            });
+
+            console.log(`Found ${components.length} connected components`);
+            return { isManifold, components: componentInfos, edgeFaces };
+        }
+
+        // Determine if a point is inside a manifold mesh using ray casting (parity test)
+        // Shoots a ray in +X direction and counts intersections with the given triangles
+        function isPointInsideMesh(px, py, pz, positions, faceIndices) {
+            let crossings = 0;
+            const numFaces = faceIndices.length / 3;
+            for (let f = 0; f < numFaces; f++) {
+                const i0 = faceIndices[f * 3] * 3;
+                const i1 = faceIndices[f * 3 + 1] * 3;
+                const i2 = faceIndices[f * 3 + 2] * 3;
+
+                const ax = positions[i0] - px, ay = positions[i0 + 1] - py, az = positions[i0 + 2] - pz;
+                const bx = positions[i1] - px, by = positions[i1 + 1] - py, bz = positions[i1 + 2] - pz;
+                const cx = positions[i2] - px, cy = positions[i2 + 1] - py, cz = positions[i2 + 2] - pz;
+
+                // Möller-Trumbore for ray direction (1,0,0)
+                const ebx = bx - ax, eby = by - ay, ebz = bz - az;
+                const ecx = cx - ax, ecy = cy - ay, ecz = cz - az;
+
+                // h = cross(dir, ec) where dir = (1,0,0)
+                const hx = 0, hy = -ecz, hz = ecy;
+                const det = ebx * hx + eby * hy + ebz * hz;
+                if (Math.abs(det) < 1e-12) continue;
+
+                const invDet = 1.0 / det;
+                // s = origin - a = (-ax, -ay, -az) relative, but origin is (0,0,0) after shift
+                const sx = -ax, sy = -ay, sz = -az;
+                const u = invDet * (sx * hx + sy * hy + sz * hz);
+                if (u < 0 || u > 1) continue;
+
+                // q = cross(s, eb)
+                const qx = sy * ebz - sz * eby;
+                const qy = sz * ebx - sx * ebz;
+                const qz = sx * eby - sy * ebx;
+                const v = invDet * (1 * qx + 0 * qy + 0 * qz);  // dot(dir, q)
+                if (v < 0 || u + v > 1) continue;
+
+                const t = invDet * (ecx * qx + ecy * qy + ecz * qz);
+                if (t > 1e-6) crossings++;
+            }
+            return (crossings % 2) === 1;
+        }
+
+        // Remove void components: find manifold closed components that are fully inside
+        // another component, and remove them from the mesh
+        function removeVoids(positions, indices) {
+            const analysis = analyseMesh(positions, indices);
+            const comps = analysis.components;
+
+            if (comps.length <= 1) {
+                console.log('Single component — no voids to remove');
+                return { positions, indices, voidsRemoved: 0, analysis };
+            }
+
+            // Sort components by face count descending (largest = likely outer shell)
+            const sorted = comps.map((c, i) => ({ ...c, idx: i }))
+                .sort((a, b) => b.faces.length - a.faces.length);
+
+            // For each manifold closed component (except the largest), check if its
+            // centroid is inside any larger component. If so, mark it as a void.
+            const voidFlags = new Uint8Array(comps.length);
+            let voidsRemoved = 0;
+
+            for (let si = 1; si < sorted.length; si++) {
+                const comp = sorted[si];
+                // Only consider manifold closed components as potential voids
+                if (!comp.manifold) continue;
+
+                // Compute centroid of this component
+                let cx = 0, cy = 0, cz = 0, nv = 0;
+                const seenVerts = new Set();
+                for (const f of comp.faces) {
+                    for (let k = 0; k < 3; k++) {
+                        const vi = indices[f * 3 + k];
+                        if (!seenVerts.has(vi)) {
+                            seenVerts.add(vi);
+                            cx += positions[vi * 3];
+                            cy += positions[vi * 3 + 1];
+                            cz += positions[vi * 3 + 2];
+                            nv++;
+                        }
+                    }
+                }
+                cx /= nv; cy /= nv; cz /= nv;
+
+                // Check if centroid is inside any larger component
+                for (let sj = 0; sj < si; sj++) {
+                    const outer = sorted[sj];
+                    if (voidFlags[outer.idx]) continue;  // Skip if already a void
+                    if (!outer.manifold) continue;  // Can only test inside manifold meshes
+
+                    // Build face index array for the outer component
+                    const outerIndices = new Uint32Array(outer.faces.length * 3);
+                    for (let fi = 0; fi < outer.faces.length; fi++) {
+                        const f = outer.faces[fi];
+                        outerIndices[fi * 3] = indices[f * 3];
+                        outerIndices[fi * 3 + 1] = indices[f * 3 + 1];
+                        outerIndices[fi * 3 + 2] = indices[f * 3 + 2];
+                    }
+
+                    if (isPointInsideMesh(cx, cy, cz, positions, outerIndices)) {
+                        voidFlags[comp.idx] = 1;
+                        voidsRemoved++;
+                        console.log(`Void detected: component ${comp.idx} (${comp.faces.length} faces) inside component ${outer.idx}`);
+                        break;
+                    }
+                }
+            }
+
+            if (voidsRemoved === 0) {
+                console.log('No voids detected');
+                return { positions, indices, voidsRemoved: 0, analysis };
+            }
+
+            // Rebuild mesh without void components
+            const keepFaces = [];
+            for (let ci = 0; ci < comps.length; ci++) {
+                if (!voidFlags[ci]) {
+                    keepFaces.push(...comps[ci].faces);
+                }
+            }
+
+            // Remap vertices (only keep referenced ones)
+            const vertexMap = new Map();
+            let newVertIdx = 0;
+            const newIndices = [];
+            for (const f of keepFaces) {
+                for (let k = 0; k < 3; k++) {
+                    const oldV = indices[f * 3 + k];
+                    if (!vertexMap.has(oldV)) {
+                        vertexMap.set(oldV, newVertIdx++);
+                    }
+                    newIndices.push(vertexMap.get(oldV));
+                }
+            }
+
+            const newPositions = new Float32Array(newVertIdx * 3);
+            for (const [oldV, newV] of vertexMap) {
+                newPositions[newV * 3] = positions[oldV * 3];
+                newPositions[newV * 3 + 1] = positions[oldV * 3 + 1];
+                newPositions[newV * 3 + 2] = positions[oldV * 3 + 2];
+            }
+
+            const removedFaces = indices.length / 3 - newIndices.length / 3;
+            console.log(`Removed ${voidsRemoved} void components (${removedFaces} faces)`);
+
+            return {
+                positions: newPositions,
+                indices: new Uint32Array(newIndices),
+                voidsRemoved,
+                analysis
+            };
+        }
+
+
+        // ─── ORIENT NORMALS OUTWARD ───
+
+        // Compute face normal (unnormalized) for face f
+        function faceNormal(positions, indices, f) {
+            const i0 = indices[f * 3] * 3, i1 = indices[f * 3 + 1] * 3, i2 = indices[f * 3 + 2] * 3;
+            const ax = positions[i1] - positions[i0], ay = positions[i1 + 1] - positions[i0 + 1], az = positions[i1 + 2] - positions[i0 + 2];
+            const bx = positions[i2] - positions[i0], by = positions[i2 + 1] - positions[i0 + 1], bz = positions[i2 + 2] - positions[i0 + 2];
+            return { x: ay * bz - az * by, y: az * bx - ax * bz, z: ax * by - ay * bx };
+        }
+
+        // Face centroid
+        function faceCentroid(positions, indices, f) {
+            const i0 = indices[f * 3] * 3, i1 = indices[f * 3 + 1] * 3, i2 = indices[f * 3 + 2] * 3;
+            return {
+                x: (positions[i0] + positions[i1] + positions[i2]) / 3,
+                y: (positions[i0 + 1] + positions[i1 + 1] + positions[i2 + 1]) / 3,
+                z: (positions[i0 + 2] + positions[i1 + 2] + positions[i2 + 2]) / 3
+            };
+        }
+
+        // Get the directed half-edge (v0→v1) for a face's edge
+        // Returns which order the two vertices appear when traversing face f's winding
+        function faceEdgeDirection(indices, f, va, vb) {
+            const i0 = indices[f * 3], i1 = indices[f * 3 + 1], i2 = indices[f * 3 + 2];
+            // Check if edge va→vb appears in the face's winding order
+            if ((i0 === va && i1 === vb) || (i1 === va && i2 === vb) || (i2 === va && i0 === vb)) {
+                return 1;  // same direction as winding
+            }
+            return -1;  // opposite direction
+        }
+
+        // Orient all face normals outward.
+        // Strategy:
+        //   1. Build edge→face adjacency and connected components
+        //   2. For manifold components: BFS winding propagation from a seed face
+        //      - Seed face orientation determined by ray-cast parity test
+        //      - Neighbours sharing an edge must have OPPOSITE half-edge directions
+        //        (i.e., if face A has edge v0→v1, face B must have v1→v0 for consistent winding)
+        //   3. For non-manifold components: per-face ray-cast parity test
+        function orientNormalsOutward(positions, indices) {
+            const faceCount = indices.length / 3;
+            if (faceCount === 0) return 0;
+
+            // Build edge → face map with directed edge info
+            const edgeFaces = new Map();  // edgeKey → [{face, va, vb}, ...]
+            for (let f = 0; f < faceCount; f++) {
+                const i0 = indices[f * 3], i1 = indices[f * 3 + 1], i2 = indices[f * 3 + 2];
+                const pairs = [[i0, i1], [i1, i2], [i2, i0]];
+                for (const [va, vb] of pairs) {
+                    const ek = edgeKey(va, vb);
+                    if (!edgeFaces.has(ek)) edgeFaces.set(ek, []);
+                    edgeFaces.get(ek).push({ face: f, va, vb });
+                }
+            }
+
+            // Build face adjacency
+            const faceAdj = new Array(faceCount);
+            for (let f = 0; f < faceCount; f++) faceAdj[f] = [];
+            for (const [ek, entries] of edgeFaces) {
+                if (entries.length === 2) {
+                    // Manifold edge — record adjacency with directed edge info
+                    const a = entries[0], b = entries[1];
+                    faceAdj[a.face].push({ neighbor: b.face, aVa: a.va, aVb: a.vb, bVa: b.va, bVb: b.vb });
+                    faceAdj[b.face].push({ neighbor: a.face, aVa: b.va, aVb: b.vb, bVa: a.va, bVb: a.vb });
+                }
+                // Non-manifold edges (1 or 3+ faces) are skipped for winding propagation
+            }
+
+            // Find connected components
+            const compId = new Int32Array(faceCount).fill(-1);
+            const components = [];
+            for (let f = 0; f < faceCount; f++) {
+                if (compId[f] >= 0) continue;
+                const cid = components.length;
+                const comp = [];
+                const stack = [f];
+                compId[f] = cid;
+                while (stack.length > 0) {
+                    const cur = stack.pop();
+                    comp.push(cur);
+                    for (const adj of faceAdj[cur]) {
+                        if (compId[adj.neighbor] < 0) {
+                            compId[adj.neighbor] = cid;
+                            stack.push(adj.neighbor);
+                        }
+                    }
+                }
+                components.push(comp);
+            }
+
+            let totalFlipped = 0;
+
+            // Process each component
+            for (const comp of components) {
+                if (comp.length === 0) continue;
+
+                // BFS winding propagation
+                // First, determine correct orientation of seed face using ray-cast
+                const seedFace = comp[0];
+                const seedNorm = faceNormal(positions, indices, seedFace);
+                const len = Math.sqrt(seedNorm.x * seedNorm.x + seedNorm.y * seedNorm.y + seedNorm.z * seedNorm.z);
+                if (len < 1e-12) continue;
+                const nx = seedNorm.x / len, ny = seedNorm.y / len, nz = seedNorm.z / len;
+
+                const cent = faceCentroid(positions, indices, seedFace);
+
+                // Ray-cast from centroid along the face normal direction
+                // Count crossings with ALL mesh faces (not just this component)
+                // Odd crossings → normal points inward → seed should be flipped
+                let crossings = 0;
+                for (let tf = 0; tf < faceCount; tf++) {
+                    if (tf === seedFace) continue;
+                    const ti0 = indices[tf * 3] * 3, ti1 = indices[tf * 3 + 1] * 3, ti2 = indices[tf * 3 + 2] * 3;
+
+                    const ax = positions[ti0] - cent.x, ay = positions[ti0 + 1] - cent.y, az = positions[ti0 + 2] - cent.z;
+                    const bx = positions[ti1] - cent.x, by = positions[ti1 + 1] - cent.y, bz = positions[ti1 + 2] - cent.z;
+                    const cx = positions[ti2] - cent.x, cy = positions[ti2 + 1] - cent.y, cz = positions[ti2 + 2] - cent.z;
+
+                    // Möller-Trumbore for ray direction (nx, ny, nz)
+                    const ebx = bx - ax, eby = by - ay, ebz = bz - az;
+                    const ecx = cx - ax, ecy = cy - ay, ecz = cz - az;
+
+                    const hx = ny * ecz - nz * ecy, hy = nz * ecx - nx * ecz, hz = nx * ecy - ny * ecx;
+                    const det = ebx * hx + eby * hy + ebz * hz;
+                    if (Math.abs(det) < 1e-12) continue;
+
+                    const invDet = 1.0 / det;
+                    const sx = -ax, sy = -ay, sz = -az;
+                    const u = invDet * (sx * hx + sy * hy + sz * hz);
+                    if (u < 0 || u > 1) continue;
+
+                    const qx = sy * ebz - sz * eby, qy = sz * ebx - sx * ebz, qz = sx * eby - sy * ebx;
+                    const v = invDet * (nx * qx + ny * qy + nz * qz);
+                    if (v < 0 || u + v > 1) continue;
+
+                    const t = invDet * (ecx * qx + ecy * qy + ecz * qz);
+                    if (t > 1e-4) crossings++;
+                }
+
+                // If odd crossings, the seed normal points inward — need to flip seed
+                const seedNeedsFlip = (crossings % 2) === 1;
+
+                // BFS to propagate consistent winding from seed
+                const flipFlag = new Uint8Array(faceCount);  // 1 = this face needs flipping
+                const visited = new Uint8Array(faceCount);
+                visited[seedFace] = 1;
+                if (seedNeedsFlip) flipFlag[seedFace] = 1;
+
+                const queue = [seedFace];
+                let qi = 0;
+                while (qi < queue.length) {
+                    const cur = queue[qi++];
+                    const curFlipped = flipFlag[cur];
+
+                    for (const adj of faceAdj[cur]) {
+                        if (visited[adj.neighbor]) continue;
+                        visited[adj.neighbor] = 1;
+
+                        // For consistent outward normals, two faces sharing a manifold edge
+                        // must traverse the shared edge in OPPOSITE directions.
+                        // If face A has half-edge va→vb, face B should have vb→va.
+                        // Check: do both faces traverse the shared edge in the same direction?
+                        const sameDirection = (adj.aVa === adj.bVa && adj.aVb === adj.bVb);
+                        // sameDirection means they have the SAME half-edge order for this edge
+                        // which means their normals point in OPPOSITE directions (inconsistent)
+                        // So: neighbor needs flip if:
+                        //   - same direction + cur NOT flipped → neighbor must flip (to become consistent then flip outward)
+                        //   - opposite direction + cur flipped → neighbor must flip
+                        // Simplified: neighborFlip = curFlipped XOR !sameDirection
+                        // Wait, let me think more carefully:
+                        //   Consistent winding: shared edge traversed in opposite directions
+                        //   sameDirection = true → currently INCONSISTENT → neighbor needs flip relative to cur
+                        //   sameDirection = false → currently CONSISTENT → neighbor same as cur
+                        const neighborFlip = sameDirection ? !curFlipped : curFlipped;
+                        flipFlag[adj.neighbor] = neighborFlip ? 1 : 0;
+
+                        queue.push(adj.neighbor);
+                    }
+                }
+
+                // Also handle faces not reached by BFS (non-manifold boundaries within component)
+                // These get individual ray-cast tests
+                for (const f of comp) {
+                    if (visited[f]) continue;
+
+                    const fn = faceNormal(positions, indices, f);
+                    const fnLen = Math.sqrt(fn.x * fn.x + fn.y * fn.y + fn.z * fn.z);
+                    if (fnLen < 1e-12) continue;
+                    const fnx = fn.x / fnLen, fny = fn.y / fnLen, fnz = fn.z / fnLen;
+                    const fc = faceCentroid(positions, indices, f);
+
+                    let fc_crossings = 0;
+                    for (let tf = 0; tf < faceCount; tf++) {
+                        if (tf === f) continue;
+                        const ti0 = indices[tf * 3] * 3, ti1 = indices[tf * 3 + 1] * 3, ti2 = indices[tf * 3 + 2] * 3;
+
+                        const ax = positions[ti0] - fc.x, ay = positions[ti0 + 1] - fc.y, az = positions[ti0 + 2] - fc.z;
+                        const bx = positions[ti1] - fc.x, by = positions[ti1 + 1] - fc.y, bz = positions[ti1 + 2] - fc.z;
+                        const cx = positions[ti2] - fc.x, cy = positions[ti2 + 1] - fc.y, cz = positions[ti2 + 2] - fc.z;
+
+                        const ebx = bx - ax, eby = by - ay, ebz = bz - az;
+                        const ecx = cx - ax, ecy = cy - ay, ecz = cz - az;
+                        const hx = fny * ecz - fnz * ecy, hy = fnz * ecx - fnx * ecz, hz = fnx * ecy - fny * ecx;
+                        const det = ebx * hx + eby * hy + ebz * hz;
+                        if (Math.abs(det) < 1e-12) continue;
+                        const invDet = 1.0 / det;
+                        const sx = -ax, sy = -ay, sz = -az;
+                        const u = invDet * (sx * hx + sy * hy + sz * hz);
+                        if (u < 0 || u > 1) continue;
+                        const qx = sy * ebz - sz * eby, qy = sz * ebx - sx * ebz, qz = sx * eby - sy * ebx;
+                        const v = invDet * (fnx * qx + fny * qy + fnz * qz);
+                        if (v < 0 || u + v > 1) continue;
+                        const t = invDet * (ecx * qx + ecy * qy + ecz * qz);
+                        if (t > 1e-4) fc_crossings++;
+                    }
+
+                    if ((fc_crossings % 2) === 1) flipFlag[f] = 1;
+                }
+
+                // Apply flips
+                let compFlipped = 0;
+                for (const f of comp) {
+                    if (flipFlag[f]) {
+                        // Swap indices[f*3+1] and indices[f*3+2] to reverse winding
+                        const tmp = indices[f * 3 + 1];
+                        indices[f * 3 + 1] = indices[f * 3 + 2];
+                        indices[f * 3 + 2] = tmp;
+                        compFlipped++;
+                    }
+                }
+                totalFlipped += compFlipped;
+            }
+
+            console.log(`Normal orientation: flipped ${totalFlipped}/${faceCount} faces across ${components.length} components`);
+            return totalFlipped;
+        }
+
+
+        document.getElementById('viewport').addEventListener('click', (event) => {
+            if (event.target !== renderer.domElement) return;
+            if (bboxMode) {
+                handleBboxClick(event);
+                return;
+            }
+            if (currentStep === 5 && Object.keys(seasonHeatmaps).length > 0) {
+                handleRayProbeClick(event);
+                return;
+            }
+        });
+
+        // ─── BUILD SHADOW BVH (all scene geometry) ───
+        function buildShadowBVH() {
+            showStatus('Building BVH for shadow casters...');
+            const allVerts = [];
+            const allIdx = [];
+            let offset = 0;
+            const meshes = getAnalysisMeshes();
+            for (const mesh of meshes) {
+                const geo = mesh.geometry;
+                const pos = geo.attributes.position.array;
+                const idx = geo.index ? geo.index.array : null;
+                mesh.updateWorldMatrix(true, false);
+                const wm = mesh.matrixWorld;
+                const numVerts = pos.length / 3;
+                for (let v = 0; v < numVerts; v++) {
+                    const p = new THREE.Vector3(pos[v*3], pos[v*3+1], pos[v*3+2]);
+                    p.applyMatrix4(wm);
+                    allVerts.push(p.x, p.y, p.z);
+                }
+                if (idx) {
+                    for (let i = 0; i < idx.length; i++) allIdx.push(idx[i] + offset);
+                } else {
+                    for (let i = 0; i < numVerts; i++) allIdx.push(i + offset);
+                }
+                offset += numVerts;
+            }
+            if (allVerts.length > 0) {
+                shadowBVH = new BVH(new Float32Array(allVerts), new Uint32Array(allIdx));
+                console.log('Shadow BVH built:', (allIdx.length / 3) + ' triangles');
+            } else {
+                shadowBVH = null;
+            }
+            hideStatus();
+        }
+
+        // ─── STEP 2: SET ORIENTATION (2D Screenshot Preview) ───
+        function captureOrientationPreview() {
+            if (!buildingGroup) return;
+            // Save current camera
+            const savedCamera = camera;
+            const savedRotateEnabled = controls.enableRotate;
+            const savedPanEnabled = controls.enablePan;
+
+            // Set up ortho camera centred on building
+            updateOrthoCamera();
+            camera = orthoCamera;
+
+            // Render to canvas and capture
+            renderer.render(scene, orthoCamera);
+            const dataURL = renderer.domElement.toDataURL('image/png');
+
+            // Restore perspective camera
+            camera = savedCamera;
+            controls.object = camera;
+            controls.enableRotate = savedRotateEnabled;
+            controls.enablePan = savedPanEnabled;
+            controls.update();
+
+            // Set the preview image
+            document.getElementById('orient-preview').src = dataURL;
+        }
+
+        function showOrientationPreview() {
+            document.getElementById('orient-preview-container').classList.add('visible');
+            document.getElementById('north-arrow').style.display = 'block';
+            // Lock 3D controls during orientation
+            controls.enableRotate = false;
+            controls.enablePan = false;
+        }
+
+        function hideOrientationPreview() {
+            document.getElementById('orient-preview-container').classList.remove('visible');
+            document.getElementById('north-arrow').style.display = 'none';
+            // Restore controls
+            controls.enableRotate = true;
+            controls.enablePan = true;
+        }
+
+        function confirmOrientation() {
+            // Apply the chosen rotation to the model group
+            if (modelRotationGroup) {
+                modelRotationGroup.rotation.y = northRotationDeg * Math.PI / 180;
+            }
+            hideOrientationPreview();
+            const summary = northRotationDeg === 0
+                ? 'North: confirmed'
+                : 'North: rotated ' + (northRotationDeg > 0 ? '+' : '') + northRotationDeg + '\u00b0';
+            completeStep(2, summary);
+        }
+
+        function applyManualRotation(sign) {
+            const degrees = parseFloat(document.getElementById('north-rotation').value) || 5;
+            northRotationDeg += sign * Math.abs(degrees);
+            // Wrap to -180..180
+            while (northRotationDeg > 180) northRotationDeg -= 360;
+            while (northRotationDeg <= -180) northRotationDeg += 360;
+            northRotationDeg = Math.round(northRotationDeg * 10) / 10;
+
+            // Rotate the 2D preview image via CSS
+            document.getElementById('orient-preview').style.transform = 'rotate(' + northRotationDeg + 'deg)';
+            // Rotate north arrow inversely
+            document.getElementById('north-arrow-rotator').style.transform = 'rotate(' + (-northRotationDeg) + 'deg)';
+        }
+
+        function resetOrientation() {
+            northRotationDeg = 0;
+            document.getElementById('orient-preview').style.transform = 'rotate(0deg)';
+            document.getElementById('north-arrow-rotator').style.transform = 'rotate(0deg)';
+        }
+
+        // ─── STEP 3: SITE LOCATION ───
+        function confirmSiteLocation() {
+            const lat = parseFloat(document.getElementById('latitude').value) || 51.5074;
+            const lng = parseFloat(document.getElementById('longitude').value) || -0.1278;
+            completeStep(3, lat.toFixed(2) + ', ' + lng.toFixed(2));
+        }
+
+        // ─── STEP 4: ANALYSIS AREA ───
+        function enableRunButton() {
+            const btn = document.getElementById('run-btn');
+            btn.disabled = false;
+            btn.style.opacity = '';
+            btn.style.cursor = '';
+            const hint = document.getElementById('run-btn-hint');
+            if (hint) hint.style.display = 'none';
+        }
+
+        function useEntireScene() {
+            useEntireBounds = true;
+            document.getElementById('use-entire-btn').style.background = '#D4880F';
+            document.getElementById('use-entire-btn').style.color = '#fff';
+            document.getElementById('bbox-btn').style.background = '';
+            document.getElementById('bbox-btn').style.color = '';
+            document.getElementById('bbox-fields').style.display = 'none';
+            document.getElementById('bbox-fields2').style.display = 'none';
+            removeBboxHelper();
+            enableRunButton();
+        }
+
+        // ─── BVH (Bounding Volume Hierarchy) for fast ray casting ───
+        class BVH {
+            constructor(positions, index) {
+                const triCount = index.length / 3;
+                const tris = new Array(triCount);
+                for (let i = 0; i < triCount; i++) {
+                    const i0 = index[i * 3] * 3, i1 = index[i * 3 + 1] * 3, i2 = index[i * 3 + 2] * 3;
+                    const ax = positions[i0], ay = positions[i0+1], az = positions[i0+2];
+                    const bx = positions[i1], by = positions[i1+1], bz = positions[i1+2];
+                    const cx = positions[i2], cy = positions[i2+1], cz = positions[i2+2];
+                    tris[i] = {
+                        ax, ay, az, bx, by, bz, cx, cy, cz,
+                        centX: (ax + bx + cx) / 3,
+                        centY: (ay + by + cy) / 3,
+                        centZ: (az + bz + cz) / 3,
+                    };
+                }
+                this.root = this._build(tris, 0, tris.length);
+            }
+
+            _build(tris, start, end) {
+                let mnx = Infinity, mny = Infinity, mnz = Infinity;
+                let mxx = -Infinity, mxy = -Infinity, mxz = -Infinity;
+                for (let i = start; i < end; i++) {
+                    const t = tris[i];
+                    mnx = Math.min(mnx, t.ax, t.bx, t.cx);
+                    mny = Math.min(mny, t.ay, t.by, t.cy);
+                    mnz = Math.min(mnz, t.az, t.bz, t.cz);
+                    mxx = Math.max(mxx, t.ax, t.bx, t.cx);
+                    mxy = Math.max(mxy, t.ay, t.by, t.cy);
+                    mxz = Math.max(mxz, t.az, t.bz, t.cz);
+                }
+                const node = { minX: mnx, minY: mny, minZ: mnz, maxX: mxx, maxY: mxy, maxZ: mxz };
+                const count = end - start;
+
+                if (count <= 8) {
+                    const buf = new Float64Array(count * 9);
+                    for (let i = start; i < end; i++) {
+                        const t = tris[i], o = (i - start) * 9;
+                        buf[o] = t.ax; buf[o+1] = t.ay; buf[o+2] = t.az;
+                        buf[o+3] = t.bx; buf[o+4] = t.by; buf[o+5] = t.bz;
+                        buf[o+6] = t.cx; buf[o+7] = t.cy; buf[o+8] = t.cz;
+                    }
+                    node.tris = buf;
+                    node.triCount = count;
+                    return node;
+                }
+
+                const dx = mxx - mnx, dy = mxy - mny, dz = mxz - mnz;
+                const axis = dx >= dy && dx >= dz ? 'centX' : dy >= dz ? 'centY' : 'centZ';
+                const mid = (start + end) >> 1;
+                const slice = tris.slice(start, end);
+                slice.sort((a, b) => a[axis] - b[axis]);
+                for (let i = 0; i < slice.length; i++) tris[start + i] = slice[i];
+
+                node.left = this._build(tris, start, mid);
+                node.right = this._build(tris, mid, end);
+                return node;
+            }
+
+            intersectsAny(ox, oy, oz, dx, dy, dz) {
+                const invDx = 1 / dx, invDy = 1 / dy, invDz = 1 / dz;
+                return this._query(this.root, ox, oy, oz, dx, dy, dz, invDx, invDy, invDz);
+            }
+
+            _query(node, ox, oy, oz, dx, dy, dz, invDx, invDy, invDz) {
+                let tmin, tmax, tymin, tymax, tzmin, tzmax;
+                if (invDx >= 0) {
+                    tmin = (node.minX - ox) * invDx;
+                    tmax = (node.maxX - ox) * invDx;
+                } else {
+                    tmin = (node.maxX - ox) * invDx;
+                    tmax = (node.minX - ox) * invDx;
+                }
+                if (invDy >= 0) {
+                    tymin = (node.minY - oy) * invDy;
+                    tymax = (node.maxY - oy) * invDy;
+                } else {
+                    tymin = (node.maxY - oy) * invDy;
+                    tymax = (node.minY - oy) * invDy;
+                }
+                if (tmin > tymax || tymin > tmax) return false;
+                if (tymin > tmin) tmin = tymin;
+                if (tymax < tmax) tmax = tymax;
+                if (invDz >= 0) {
+                    tzmin = (node.minZ - oz) * invDz;
+                    tzmax = (node.maxZ - oz) * invDz;
+                } else {
+                    tzmin = (node.maxZ - oz) * invDz;
+                    tzmax = (node.minZ - oz) * invDz;
+                }
+                if (tmin > tzmax || tzmin > tmax) return false;
+                if (tzmin > tmin) tmin = tzmin;
+                if (tzmax < tmax) tmax = tzmax;
+                if (tmax < 0) return false;
+
+                if (node.tris) {
+                    const buf = node.tris;
+                    for (let i = 0; i < node.triCount; i++) {
+                        const o = i * 9;
+                        const e1x = buf[o+3] - buf[o], e1y = buf[o+4] - buf[o+1], e1z = buf[o+5] - buf[o+2];
+                        const e2x = buf[o+6] - buf[o], e2y = buf[o+7] - buf[o+1], e2z = buf[o+8] - buf[o+2];
+                        const px = dy * e2z - dz * e2y, py = dz * e2x - dx * e2z, pz = dx * e2y - dy * e2x;
+                        const det = e1x * px + e1y * py + e1z * pz;
+                        if (det > -1e-10 && det < 1e-10) continue;
+                        const invDet = 1 / det;
+                        const tx = ox - buf[o], ty = oy - buf[o+1], tz = oz - buf[o+2];
+                        const u = (tx * px + ty * py + tz * pz) * invDet;
+                        if (u < 0 || u > 1) continue;
+                        const qx = ty * e1z - tz * e1y, qy = tz * e1x - tx * e1z, qz = tx * e1y - ty * e1x;
+                        const v = (dx * qx + dy * qy + dz * qz) * invDet;
+                        if (v < 0 || u + v > 1) continue;
+                        const t = (e2x * qx + e2y * qy + e2z * qz) * invDet;
+                        if (t > 1e-4) return true;
+                    }
+                    return false;
+                }
+
+                return this._query(node.left, ox, oy, oz, dx, dy, dz, invDx, invDy, invDz)
+                    || this._query(node.right, ox, oy, oz, dx, dy, dz, invDx, invDy, invDz);
+            }
+        }
+
+        // ─── SUN POSITION CALCULATOR (pure JS — Spencer 1971) ───
+        function getSunPositions(latitude, longitude, dateStr, timeStep) {
+            const date = new Date(dateStr + 'T12:00:00');
+            const dayOfYear = getDayOfYear(date);
+            const latRad = latitude * Math.PI / 180;
+
+            const B = (dayOfYear - 1) * 2 * Math.PI / 365;
+            const declination = 0.006918 - 0.399912 * Math.cos(B) + 0.070257 * Math.sin(B)
+                - 0.006758 * Math.cos(2 * B) + 0.000907 * Math.sin(2 * B)
+                - 0.002697 * Math.cos(3 * B) + 0.00148 * Math.sin(3 * B);
+
+            const eot = 229.18 * (0.000075 + 0.001868 * Math.cos(B) - 0.032077 * Math.sin(B)
+                - 0.014615 * Math.cos(2 * B) - 0.04089 * Math.sin(2 * B));
+
+            const positions = [];
+
+            for (let hour = 0; hour < 24; hour += timeStep) {
+                const solarTime = hour + (eot + 4 * longitude) / 60;
+                const hourAngle = (solarTime - 12) * 15 * Math.PI / 180;
+
+                const sinAlt = Math.sin(latRad) * Math.sin(declination)
+                    + Math.cos(latRad) * Math.cos(declination) * Math.cos(hourAngle);
+                const altitude = Math.asin(Math.max(-1, Math.min(1, sinAlt)));
+
+                if (altitude * 180 / Math.PI <= -0.833) continue;
+
+                const cosAz = (Math.sin(declination) - Math.sin(latRad) * sinAlt)
+                    / (Math.cos(latRad) * Math.cos(altitude));
+                let azimuth = Math.acos(Math.max(-1, Math.min(1, cosAz)));
+                if (hourAngle > 0) azimuth = 2 * Math.PI - azimuth;
+
+                positions.push({
+                    azimuth: azimuth * 180 / Math.PI,
+                    altitude: altitude * 180 / Math.PI,
+                    hour: hour,
+                });
+            }
+
+            return positions;
+        }
+
+        function getDayOfYear(date) {
+            const start = new Date(date.getFullYear(), 0, 0);
+            const diff = date - start;
+            return Math.floor(diff / (1000 * 60 * 60 * 24));
+        }
+
+        function sunDirection(azimuthDeg, altitudeDeg) {
+            // Azimuth: 0°=North, 90°=East, 180°=South, 270°=West (CW from North)
+            const az = azimuthDeg * Math.PI / 180;
+            const alt = altitudeDeg * Math.PI / 180;
+            const ifcX = Math.sin(az) * Math.cos(alt);
+            const ifcY = Math.cos(az) * Math.cos(alt);
+            const ifcZ = Math.sin(alt);
+            return new THREE.Vector3(ifcX, ifcZ, -ifcY).normalize();
+        }
+
+        // ─── SUTHERLAND-HODGMAN POLYGON CLIPPING ───
+        function clipPolygonToPlane(vertices, axis, value, keepAbove) {
+            if (vertices.length === 0) return [];
+            const result = [];
+            const n = vertices.length;
+            for (let i = 0; i < n; i++) {
+                const curr = vertices[i];
+                const next = vertices[(i + 1) % n];
+                const currInside = keepAbove ? curr[axis] >= value - 1e-10 : curr[axis] <= value + 1e-10;
+                const nextInside = keepAbove ? next[axis] >= value - 1e-10 : next[axis] <= value + 1e-10;
+                if (currInside) {
+                    result.push(curr);
+                    if (!nextInside) {
+                        const t = (value - curr[axis]) / (next[axis] - curr[axis]);
+                        result.push([
+                            curr[0] + t * (next[0] - curr[0]),
+                            curr[1] + t * (next[1] - curr[1]),
+                            curr[2] + t * (next[2] - curr[2]),
+                        ]);
+                    }
+                } else if (nextInside) {
+                    const t = (value - curr[axis]) / (next[axis] - curr[axis]);
+                    result.push([
+                        curr[0] + t * (next[0] - curr[0]),
+                        curr[1] + t * (next[1] - curr[1]),
+                        curr[2] + t * (next[2] - curr[2]),
+                    ]);
+                }
+            }
+            return result;
+        }
+
+        function clipTriangleToVoxel(tri, minX, minY, minZ, maxX, maxY, maxZ) {
+            let poly = [tri[0], tri[1], tri[2]];
+            poly = clipPolygonToPlane(poly, 0, minX, true);
+            if (poly.length < 3) return [];
+            poly = clipPolygonToPlane(poly, 0, maxX, false);
+            if (poly.length < 3) return [];
+            poly = clipPolygonToPlane(poly, 1, minY, true);
+            if (poly.length < 3) return [];
+            poly = clipPolygonToPlane(poly, 1, maxY, false);
+            if (poly.length < 3) return [];
+            poly = clipPolygonToPlane(poly, 2, minZ, true);
+            if (poly.length < 3) return [];
+            poly = clipPolygonToPlane(poly, 2, maxZ, false);
+            return poly;
+        }
+
+        function triangulatePolygon(vertices) {
+            if (vertices.length < 3) return [];
+            const tris = [];
+            for (let i = 1; i < vertices.length - 1; i++) {
+                tris.push([vertices[0], vertices[i], vertices[i + 1]]);
+            }
+            return tris;
+        }
+
+        // ─── VOXEL-BASED ANALYSIS PIPELINE ───
+        let cachedCellData = null;
+        let cachedGridSize = null;
+        let cachedCellMap = null;
+        let cachedSliverIndices = null;
+
+        async function prepareVoxelCells() {
+            const gridSize = parseFloat(document.getElementById('grid_resolution').value) || 1.0;
+
+            // Apply bbox filter if set
+            let bboxFilter = null;
+            if (!useEntireBounds) {
+                const bx1 = parseFloat(document.getElementById('bbox_min_x').value);
+                const by1 = parseFloat(document.getElementById('bbox_min_y').value);
+                const bx2 = parseFloat(document.getElementById('bbox_max_x').value);
+                const by2 = parseFloat(document.getElementById('bbox_max_y').value);
+                if (!isNaN(bx1) && !isNaN(by1) && !isNaN(bx2) && !isNaN(by2)) {
+                    bboxFilter = { minX: Math.min(bx1, bx2), maxX: Math.max(bx1, bx2),
+                                   minY: Math.min(by1, by2), maxY: Math.max(by1, by2) };
+                }
+            }
+
+            // Step 1: Voxelise all IFC geometry
+            showStatus('Voxelising geometry...');
+            await new Promise(r => setTimeout(r, 0));
+
+            const voxelGrid = new Map();
+            const allWorldTris = [];
+            let sceneMinY = Infinity;
+
+            const meshes = getAnalysisMeshes();
+            for (const mesh of meshes) {
+                mesh.updateWorldMatrix(true, false);
+                const wm = mesh.matrixWorld;
+                const geo = mesh.geometry;
+                const pos = geo.attributes.position.array;
+                const idx = geo.index ? geo.index.array : null;
+                const faceCount = idx ? idx.length / 3 : pos.length / 9;
+
+                for (let f = 0; f < faceCount; f++) {
+                    const i0 = idx ? idx[f*3]*3 : f*9;
+                    const i1 = idx ? idx[f*3+1]*3 : f*9+3;
+                    const i2 = idx ? idx[f*3+2]*3 : f*9+6;
+
+                    const a = new THREE.Vector3(pos[i0], pos[i0+1], pos[i0+2]).applyMatrix4(wm);
+                    const b = new THREE.Vector3(pos[i1], pos[i1+1], pos[i1+2]).applyMatrix4(wm);
+                    const c = new THREE.Vector3(pos[i2], pos[i2+1], pos[i2+2]).applyMatrix4(wm);
+
+                    const tri = [[a.x, a.y, a.z], [b.x, b.y, b.z], [c.x, c.y, c.z]];
+                    const triIdx = allWorldTris.length;
+                    allWorldTris.push(tri);
+
+                    sceneMinY = Math.min(sceneMinY, a.y, b.y, c.y);
+
+                    const tMinX = Math.min(a.x, b.x, c.x), tMaxX = Math.max(a.x, b.x, c.x);
+                    const tMinY = Math.min(a.y, b.y, c.y), tMaxY = Math.max(a.y, b.y, c.y);
+                    const tMinZ = Math.min(a.z, b.z, c.z), tMaxZ = Math.max(a.z, b.z, c.z);
+
+                    const ixMin = Math.floor(tMinX / gridSize);
+                    const ixMax = Math.floor(tMaxX / gridSize);
+                    const iyMin = Math.floor(tMinY / gridSize);
+                    const iyMax = Math.floor(tMaxY / gridSize);
+                    const izMin = Math.floor(tMinZ / gridSize);
+                    const izMax = Math.floor(tMaxZ / gridSize);
+
+                    for (let ix = ixMin; ix <= ixMax; ix++) {
+                        for (let iy = iyMin; iy <= iyMax; iy++) {
+                            for (let iz = izMin; iz <= izMax; iz++) {
+                                const key = ix + ',' + iy + ',' + iz;
+                                if (!voxelGrid.has(key)) {
+                                    voxelGrid.set(key, { triIndices: [], ix, iy, iz });
+                                }
+                                voxelGrid.get(key).triIndices.push(triIdx);
+                            }
+                        }
+                    }
+                }
+            }
+
+            showStatus(`Voxelised: ${voxelGrid.size} cells from ${allWorldTris.length} triangles`);
+            await new Promise(r => setTimeout(r, 0));
+
+            // Step 2: Clip geometry per voxel and remove phantom voxels
+            // (AABB registration creates phantom voxels where the triangle's bounding
+            //  box overlaps but the triangle itself doesn't — these must be removed
+            //  before outer shell extraction to avoid making real cells look interior)
+            showStatus('Clipping geometry per voxel...');
+            await new Promise(r => setTimeout(r, 0));
+
+            const clippedVoxels = new Map(); // key → { ix, iy, iz, tris, area, centroid, normal }
+            let clipCount = 0;
+            const voxelKeys = Array.from(voxelGrid.keys());
+
+            for (let vi = 0; vi < voxelKeys.length; vi++) {
+                const key = voxelKeys[vi];
+                const cell = voxelGrid.get(key);
+                const { ix, iy, iz, triIndices } = cell;
+
+                // Skip cells below ground
+                const cellCentroidY = (iy + 0.5) * gridSize;
+                if (cellCentroidY < sceneMinY) continue;
+
+                const vMinX = ix * gridSize, vMinY = iy * gridSize, vMinZ = iz * gridSize;
+                const vMaxX = vMinX + gridSize, vMaxY = vMinY + gridSize, vMaxZ = vMinZ + gridSize;
+
+                // Bbox spatial filter (X-Z plane)
+                if (bboxFilter) {
+                    const vcx = (vMinX + vMaxX) / 2;
+                    const vcz = (vMinZ + vMaxZ) / 2;
+                    const ifcX = vcx, ifcY = -vcz;
+                    if (ifcX < bboxFilter.minX || ifcX > bboxFilter.maxX ||
+                        ifcY < bboxFilter.minY || ifcY > bboxFilter.maxY) continue;
+                }
+
+                // Clip all registered triangles to this voxel
+                let totalArea = 0;
+                let sumCx = 0, sumCy = 0, sumCz = 0;
+                let sumNx = 0, sumNy = 0, sumNz = 0;
+                const clippedTris = [];
+
+                for (const ti of triIndices) {
+                    const tri = allWorldTris[ti];
+                    const clippedPoly = clipTriangleToVoxel(tri, vMinX, vMinY, vMinZ, vMaxX, vMaxY, vMaxZ);
+                    if (clippedPoly.length < 3) continue;
+
+                    const subTris = triangulatePolygon(clippedPoly);
+                    for (const ct of subTris) {
+                        const [a, b, c] = ct;
+                        const e1x = b[0]-a[0], e1y = b[1]-a[1], e1z = b[2]-a[2];
+                        const e2x = c[0]-a[0], e2y = c[1]-a[1], e2z = c[2]-a[2];
+                        const nx = e1y*e2z - e1z*e2y;
+                        const ny = e1z*e2x - e1x*e2z;
+                        const nz = e1x*e2y - e1y*e2x;
+                        const len = Math.sqrt(nx*nx + ny*ny + nz*nz);
+                        if (len === 0) continue;
+
+                        const area = len * 0.5;
+                        const cx = (a[0] + b[0] + c[0]) / 3;
+                        const cy = (a[1] + b[1] + c[1]) / 3;
+                        const cz = (a[2] + b[2] + c[2]) / 3;
+
+                        totalArea += area;
+                        sumCx += cx * area;
+                        sumCy += cy * area;
+                        sumCz += cz * area;
+                        sumNx += (nx / len) * area;
+                        sumNy += (ny / len) * area;
+                        sumNz += (nz / len) * area;
+
+                        clippedTris.push(ct);
+                    }
+                }
+
+                // Skip phantom voxels (AABB overlap but no actual geometry)
+                if (clippedTris.length === 0 || totalArea === 0) continue;
+
+                // Separate clipped triangles into height layers within this voxel.
+                // When multiple layers exist (e.g. ground slab + roof in same column),
+                // keep only the topmost upward-facing layer since it receives sun.
+                const HEIGHT_TOL = gridSize * 0.15;
+                const trisByY = clippedTris.map((tri, idx) => {
+                    const [a, b, c] = tri;
+                    return { tri, y: (a[1] + b[1] + c[1]) / 3 };
+                });
+                trisByY.sort((a, b) => b.y - a.y); // highest first
+
+                const layers = [];
+                let curLayer = [trisByY[0]];
+                let curMaxY = trisByY[0].y;
+                for (let ti = 1; ti < trisByY.length; ti++) {
+                    if (trisByY[ti].y < curMaxY - HEIGHT_TOL) {
+                        layers.push(curLayer);
+                        curLayer = [trisByY[ti]];
+                        curMaxY = trisByY[ti].y;
+                    } else {
+                        curLayer.push(trisByY[ti]);
+                    }
+                }
+                layers.push(curLayer);
+
+                // Use the topmost layer
+                const topLayer = layers[0];
+                let layerArea = 0, lsCx = 0, lsCy = 0, lsCz = 0;
+                let lsNx = 0, lsNy = 0, lsNz = 0;
+                const layerTris = [];
+                for (const { tri } of topLayer) {
+                    layerTris.push(tri);
+                    const [a, b, c] = tri;
+                    const e1x = b[0]-a[0], e1y = b[1]-a[1], e1z = b[2]-a[2];
+                    const e2x = c[0]-a[0], e2y = c[1]-a[1], e2z = c[2]-a[2];
+                    const nx = e1y*e2z - e1z*e2y;
+                    const ny = e1z*e2x - e1x*e2z;
+                    const nz = e1x*e2y - e1y*e2x;
+                    const len = Math.sqrt(nx*nx + ny*ny + nz*nz);
+                    if (len === 0) continue;
+                    const a2 = len * 0.5;
+                    layerArea += a2;
+                    lsCx += ((a[0]+b[0]+c[0])/3) * a2;
+                    lsCy += ((a[1]+b[1]+c[1])/3) * a2;
+                    lsCz += ((a[2]+b[2]+c[2])/3) * a2;
+                    lsNx += (nx/len) * a2;
+                    lsNy += (ny/len) * a2;
+                    lsNz += (nz/len) * a2;
+                }
+                if (layerArea === 0) continue;
+
+                const centroid = {
+                    x: lsCx / layerArea,
+                    y: lsCy / layerArea,
+                    z: lsCz / layerArea,
+                };
+
+                let nLen = Math.sqrt(lsNx*lsNx + lsNy*lsNy + lsNz*lsNz);
+                let normal;
+                if (nLen > 0) {
+                    normal = { x: lsNx / nLen, y: lsNy / nLen, z: lsNz / nLen };
+                } else {
+                    normal = { x: 0, y: 1, z: 0 };
+                }
+
+                clippedVoxels.set(key, {
+                    ix, iy, iz, tris: layerTris, area: layerArea, centroid, normal,
+                });
+                clipCount++;
+
+                if (vi % 500 === 0 && vi > 0) {
+                    showStatus(`Clipping voxels... ${Math.round(vi / voxelKeys.length * 100)}%`);
+                    await new Promise(r => setTimeout(r, 0));
+                }
+            }
+
+            showStatus(`Clipped: ${clipCount} voxels with geometry (${voxelGrid.size - clipCount} phantom voxels removed)`);
+            await new Promise(r => setTimeout(r, 0));
+
+            // Step 3: Extract outer shell from the cleaned grid
+            // For sun analysis, orient normals upward: the sun is always above,
+            // so we always want the top-facing side of any surface.
+            showStatus('Extracting outer shell...');
+            await new Promise(r => setTimeout(r, 0));
+
+            const NEIGHBOURS = [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]];
+            const cellData = [];
+            const targetFaceArea = gridSize * gridSize;
+
+            for (const [key, cell] of clippedVoxels) {
+                const { ix, iy, iz } = cell;
+                // Check which face-neighbours are empty in the CLEANED grid
+                const emptyDirs = [];
+                for (const [dx, dy, dz] of NEIGHBOURS) {
+                    if (!clippedVoxels.has((ix+dx) + ',' + (iy+dy) + ',' + (iz+dz))) {
+                        emptyDirs.push([dx, dy, dz]);
+                    }
+                }
+                if (emptyDirs.length === 0) continue; // fully interior
+
+                // Compute reference "outward" direction from empty neighbours.
+                // This is purely topological (independent of mesh winding).
+                // Each triangle's normal is oriented to agree with this reference.
+                let refX = 0, refY = 0, refZ = 0;
+                for (const [dx, dy, dz] of emptyDirs) {
+                    refX += dx; refY += dy; refZ += dz;
+                }
+                // Add a small upward bias: for cells with equal empty above/below,
+                // prefer upward (sun is above). The bias is small enough not to
+                // override horizontal directions for walls.
+                refY += 0.05;
+                let refLen = Math.sqrt(refX*refX + refY*refY + refZ*refZ);
+                if (refLen > 0) { refX /= refLen; refY /= refLen; refZ /= refLen; }
+                else { refX = 0; refY = 1; refZ = 0; }
+
+                // Recompute normal from clipped triangles, using the reference
+                // direction to orient each triangle (winding-independent).
+                let sumNx = 0, sumNy = 0, sumNz = 0;
+
+                for (const tri of cell.tris) {
+                    const [a, b, c] = tri;
+                    const e1x = b[0]-a[0], e1y = b[1]-a[1], e1z = b[2]-a[2];
+                    const e2x = c[0]-a[0], e2y = c[1]-a[1], e2z = c[2]-a[2];
+                    let nx = e1y*e2z - e1z*e2y;
+                    let ny = e1z*e2x - e1x*e2z;
+                    let nz = e1x*e2y - e1y*e2x;
+                    const len = Math.sqrt(nx*nx + ny*ny + nz*nz);
+                    if (len === 0) continue;
+                    const area = len * 0.5;
+
+                    // Orient this triangle's normal to agree with the reference
+                    const dot = nx * refX + ny * refY + nz * refZ;
+                    if (dot < 0) { nx = -nx; ny = -ny; nz = -nz; }
+
+                    sumNx += (nx / len) * area;
+                    sumNy += (ny / len) * area;
+                    sumNz += (nz / len) * area;
+                }
+
+                let nLen = Math.sqrt(sumNx*sumNx + sumNy*sumNy + sumNz*sumNz);
+                let normal;
+                if (nLen > 0) {
+                    normal = { x: sumNx / nLen, y: sumNy / nLen, z: sumNz / nLen };
+                } else {
+                    normal = { x: 0, y: 1, z: 0 };
+                }
+
+                // Discard cells whose normal points significantly downward
+                // (underside surfaces that can't receive sunlight)
+                if (normal.y < -0.5) continue;
+                // Keep any cell with a horizontal empty neighbour — outer wall surface
+                const hasHorizontalEmpty = emptyDirs.some(([dx, dy, dz]) =>
+                    (dx !== 0 || dz !== 0) && dy === 0
+                );
+                if (normal.y < 0 && !hasHorizontalEmpty) continue;
+
+                cellData.push({
+                    key,
+                    ix, iy, iz,
+                    tris: cell.tris,
+                    area: cell.area,
+                    centroid: cell.centroid,
+                    normal,
+                });
+            }
+
+            if (cellData.length === 0) {
+                throw new Error('No analysis cells found in scene geometry');
+            }
+
+            showStatus(`Outer shell: ${cellData.length} cells`);
+            await new Promise(r => setTimeout(r, 0));
+
+            // Step 4: Small cell inheritance markers
+            const sliverThreshold = 0.1 * targetFaceArea;
+            const cellMap = new Map();
+            for (let i = 0; i < cellData.length; i++) {
+                cellMap.set(cellData[i].key, i);
+            }
+            const sliverIndices = [];
+            for (let i = 0; i < cellData.length; i++) {
+                if (cellData[i].area < sliverThreshold) {
+                    sliverIndices.push(i);
+                    cellData[i]._isSliver = true;
+                }
+            }
+            if (sliverIndices.length > 0) {
+                showStatus(`Marking ${sliverIndices.length} sliver cells for inheritance...`);
+            }
+
+            cachedCellData = cellData;
+            cachedGridSize = gridSize;
+            cachedCellMap = cellMap;
+            cachedSliverIndices = sliverIndices;
+            showStatus(`Voxel grid prepared: ${cellData.length} cells at ${gridSize}m resolution (${sliverIndices.length} slivers)`);
+            return cellData;
+        }
+
+        // Apply sliver cell inheritance after ray casting
+        function applySmallCellInheritance(cellData, cellSunHours) {
+            if (!cachedSliverIndices || cachedSliverIndices.length === 0) return;
+            const NEIGHBOURS = [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]];
+            for (const si of cachedSliverIndices) {
+                const cell = cellData[si];
+                let bestNeighbour = -1;
+                let bestArea = -1;
+                for (const [dx, dy, dz] of NEIGHBOURS) {
+                    const nk = (cell.ix+dx) + ',' + (cell.iy+dy) + ',' + (cell.iz+dz);
+                    const ni = cachedCellMap.get(nk);
+                    if (ni === undefined || cellData[ni]._isSliver) continue;
+                    if (cellData[ni].area > bestArea) {
+                        bestArea = cellData[ni].area;
+                        bestNeighbour = ni;
+                    }
+                }
+                if (bestNeighbour >= 0) {
+                    cellSunHours[si] = cellSunHours[bestNeighbour];
+                }
+            }
+        }
+
+        // ─── RAY CAST SUN HOURS (uses cached cell data) ───
+        async function runTerrainAnalysis(latitude, longitude, timeStep, dateStr, cellData) {
+            if (!shadowBVH) {
+                throw new Error('Shadow BVH not built');
+            }
+
+            const sunPositions = getSunPositions(latitude, longitude, dateStr, timeStep);
+            if (sunPositions.length === 0) {
+                throw new Error('No sun positions above horizon for given date/location');
+            }
+
+            const gridSize = cachedGridSize;
+
+            // Ray-cast sun hours per grid cell
+            const totalRays = cellData.length * sunPositions.length;
+            showStatus(`Casting ${totalRays.toLocaleString()} rays (${cellData.length} cells x ${sunPositions.length} sun positions)...`);
+
+            const sunDirs = sunPositions.map(sp => {
+                const v = sunDirection(sp.azimuth, sp.altitude);
+                return [v.x, v.y, v.z];
+            });
+
+            const cellSunHours = new Float32Array(cellData.length);
+            let raysProcessed = 0;
+            const BATCH_SIZE = 2000;
+
+            for (let sunIdx = 0; sunIdx < sunDirs.length; sunIdx++) {
+                const [dx, dy, dz] = sunDirs[sunIdx];
+
+                for (let i = 0; i < cellData.length; i += BATCH_SIZE) {
+                    const end = Math.min(i + BATCH_SIZE, cellData.length);
+
+                    for (let j = i; j < end; j++) {
+                        const cd = cellData[j];
+                        // Skip sliver cells — they inherit values later
+                        if (cd._isSliver) continue;
+
+                        const ox = cd.centroid.x + cd.normal.x * 0.05;
+                        const oy = cd.centroid.y + cd.normal.y * 0.05;
+                        const oz = cd.centroid.z + cd.normal.z * 0.05;
+
+                        if (!shadowBVH.intersectsAny(ox, oy, oz, dx, dy, dz)) {
+                            cellSunHours[j] += timeStep;
+                        }
+                    }
+
+                    raysProcessed += (end - i);
+                    if (raysProcessed % (BATCH_SIZE * 4) === 0) {
+                        const pct = Math.round(raysProcessed / totalRays * 100);
+                        showStatus(`Ray casting... ${pct}%`);
+                        await new Promise(r => setTimeout(r, 0));
+                    }
+                }
+            }
+
+            // Apply small cell inheritance (sliver cells get neighbour values)
+            applySmallCellInheritance(cellData, cellSunHours);
+
+            // Compute summary statistics
+            let totalArea = 0;
+            let minHours = Infinity, maxHours = -Infinity;
+            let sumHoursWeighted = 0;
+            for (let i = 0; i < cellData.length; i++) {
+                const a = cellData[i].area;
+                const h = cellSunHours[i];
+                totalArea += a;
+                sumHoursWeighted += h * a;
+                if (h < minHours) minHours = h;
+                if (h > maxHours) maxHours = h;
+            }
+            const avgHours = totalArea > 0 ? sumHoursWeighted / totalArea : 0;
+
+            return {
+                cellData,
+                cellSunHours,
+                gridSize,
+                sunPositions,
+                summary: {
+                    area_total: totalArea.toFixed(1),
+                    cells_total: cellData.length,
+                    min_hours: Math.round(minHours * 10) / 10,
+                    max_hours: Math.round(maxHours * 10) / 10,
+                    avg_hours: Math.round(avgHours * 10) / 10,
+                },
+            };
+        }
+
+        // ─── LEGEND NOTCH BUILDER ───
+        function buildLegendNotches(timeStep) {
+            const bar = document.getElementById('legend-bar');
+            const topLabel = document.getElementById('legend-top-label');
+            // Clear existing notches
+            bar.querySelectorAll('.legend-notch').forEach(n => n.remove());
+
+            const maxH = legendMaxHours;
+
+            // Rebuild the CSS gradient to match the current colour ramp
+            const stops = HEAT_COLOUR_STOPS.map(([s, r, g, b]) => {
+                const pct = (s * 100).toFixed(1);
+                return `rgb(${Math.round(r*255)},${Math.round(g*255)},${Math.round(b*255)}) ${pct}%`;
+            });
+            bar.style.background = `linear-gradient(to top, ${stops.join(', ')})`;
+
+            // Always add hour notches
+            for (let h = 1; h < maxH; h++) {
+                const pct = (h / maxH) * 100;
+                const notch = document.createElement('div');
+                notch.className = 'legend-notch hour';
+                notch.style.bottom = pct + '%';
+                notch.title = h + 'h';
+                bar.appendChild(notch);
+            }
+
+            // Add sub-hour notches if timeStep < 1
+            if (timeStep < 1) {
+                for (let t = timeStep; t < maxH; t += timeStep) {
+                    // Skip full hours (already drawn)
+                    if (Math.abs(t - Math.round(t)) < 0.001) continue;
+                    const pct = (t / maxH) * 100;
+                    const notch = document.createElement('div');
+                    notch.className = 'legend-notch sub-hour';
+                    notch.style.bottom = pct + '%';
+                    const mins = Math.round((t % 1) * 60);
+                    notch.title = Math.floor(t) + 'h ' + mins + 'm';
+                    bar.appendChild(notch);
+                }
+            }
+
+            topLabel.textContent = maxH + 'h';
+        }
+
+        // ─── HEAT MAP COLOUR GRADIENT ───
+        // Normalised colour stops (0..1) – scaled to legendMaxHours at paint time
+        const HEAT_COLOUR_STOPS = [
+            [0.00, 0.15, 0.0, 0.25],
+            [0.17, 0.8, 0.1, 0.1],
+            [0.33, 1.0, 0.5, 0.0],
+            [0.50, 1.0, 0.85, 0.0],
+            [0.67, 1.0, 1.0, 0.2],
+            [1.00, 1.0, 1.0, 0.8],
+        ];
+        let legendMaxHours = 6; // updated after analysis
+
+        function lerpColour(hours) {
+            const t = legendMaxHours > 0 ? hours / legendMaxHours : 0;
+            const clamped = Math.max(0, Math.min(1, t));
+            const stops = HEAT_COLOUR_STOPS;
+            if (clamped <= stops[0][0]) return [stops[0][1], stops[0][2], stops[0][3]];
+            if (clamped >= stops[stops.length-1][0]) {
+                const c = stops[stops.length-1];
+                return [c[1], c[2], c[3]];
+            }
+            for (let i = 0; i < stops.length - 1; i++) {
+                const [s0, r0, g0, b0] = stops[i];
+                const [s1, r1, g1, b1] = stops[i + 1];
+                if (clamped >= s0 && clamped <= s1) {
+                    const f = (clamped - s0) / (s1 - s0);
+                    return [r0 + f * (r1 - r0), g0 + f * (g1 - g0), b0 + f * (b1 - b0)];
+                }
+            }
+            const c = stops[stops.length-1];
+            return [c[1], c[2], c[3]];
+        }
+
+        // ─── CREATE HEATMAP GROUP (20mm OFFSET) ───
+        function createHeatmapGroup(results) {
+            const group = new THREE.Group();
+            group.name = 'heatmap_' + (results.season || 'default');
+            if (!results.cellData || results.cellData.length === 0) return group;
+
+            const gridSize = cachedGridSize || 1.0;
+
+            // Build voxel lookup: key → sun hours
+            const voxelHours = new Map();
+            for (let i = 0; i < results.cellData.length; i++) {
+                voxelHours.set(results.cellData[i].key, results.cellSunHours[i]);
+            }
+
+            // Determine which meshes to paint:
+            // If IfcOpenShell meshes exist, paint those (high detail display).
+            // Otherwise, fall back to the voxel-clipped triangles.
+            const displayMeshes = analysisMeshes.length > 0 ? analysisMeshes : null;
+
+            if (displayMeshes) {
+                // ─── DUAL-GEOMETRY MODE ───
+                // Paint IfcOpenShell triangles using voxel sun hours lookup
+                const off = 0.005; // small offset to prevent z-fighting
+
+                const tilePositions = [];
+                const tileColors = [];
+
+                // Debug counters
+                let dbgExact = 0, dbgNeighbour = 0, dbgMiss = 0, dbgDegen = 0;
+                let dbgTotalTris = 0;
+                const hoursHist = [0, 0, 0, 0, 0, 0]; // 0h, 0-1h, 1-2h, 2-4h, 4-6h, 6h+
+
+                for (const mesh of displayMeshes) {
+                    mesh.updateWorldMatrix(true, false);
+                    const wm = mesh.matrixWorld;
+                    const geo = mesh.geometry;
+                    const pos = geo.attributes.position.array;
+                    const idx = geo.index ? geo.index.array : null;
+                    const faceCount = idx ? idx.length / 3 : pos.length / 9;
+
+                    for (let f = 0; f < faceCount; f++) {
+                        dbgTotalTris++;
+                        const i0 = idx ? idx[f*3]*3 : f*9;
+                        const i1 = idx ? idx[f*3+1]*3 : f*9+3;
+                        const i2 = idx ? idx[f*3+2]*3 : f*9+6;
+
+                        // Get world-space positions
+                        const a = new THREE.Vector3(pos[i0], pos[i0+1], pos[i0+2]).applyMatrix4(wm);
+                        const b = new THREE.Vector3(pos[i1], pos[i1+1], pos[i1+2]).applyMatrix4(wm);
+                        const c = new THREE.Vector3(pos[i2], pos[i2+1], pos[i2+2]).applyMatrix4(wm);
+
+                        // Check for degenerate triangle
+                        const e1x = b.x-a.x, e1y = b.y-a.y, e1z = b.z-a.z;
+                        const e2x = c.x-a.x, e2y = c.y-a.y, e2z = c.z-a.z;
+                        let nx = e1y*e2z - e1z*e2y;
+                        let ny = e1z*e2x - e1x*e2z;
+                        let nz = e1x*e2y - e1y*e2x;
+                        const nlen = Math.sqrt(nx*nx + ny*ny + nz*nz);
+                        if (nlen < 1e-10) { dbgDegen++; continue; }
+                        nx /= nlen; ny /= nlen; nz /= nlen;
+
+                        // Triangle centroid
+                        const cx = (a.x + b.x + c.x) / 3;
+                        const cy = (a.y + b.y + c.y) / 3;
+                        const cz = (a.z + b.z + c.z) / 3;
+
+                        // Look up which voxel cell this triangle centroid falls in
+                        const vix = Math.floor(cx / gridSize);
+                        const viy = Math.floor(cy / gridSize);
+                        const viz = Math.floor(cz / gridSize);
+                        const vkey = vix + ',' + viy + ',' + viz;
+
+                        let hours = voxelHours.get(vkey);
+                        let matchType = 'exact';
+
+                        // If no exact match, check the 26 neighbours (triangle may straddle boundary)
+                        if (hours === undefined) {
+                            matchType = 'neighbour';
+                            for (let dx = -1; dx <= 1 && hours === undefined; dx++) {
+                                for (let dy = -1; dy <= 1 && hours === undefined; dy++) {
+                                    for (let dz = -1; dz <= 1 && hours === undefined; dz++) {
+                                        if (dx === 0 && dy === 0 && dz === 0) continue;
+                                        const nkey = (vix+dx) + ',' + (viy+dy) + ',' + (viz+dz);
+                                        const nh = voxelHours.get(nkey);
+                                        if (nh !== undefined) hours = nh;
+                                    }
+                                }
+                            }
+                        }
+
+                        let r, g, b2;
+                        if (hours === undefined) {
+                            // No match — render in magenta so it's visible in debug
+                            dbgMiss++;
+                            r = 1.0; g = 0.0; b2 = 1.0; // magenta
+                        } else {
+                            if (matchType === 'exact') dbgExact++; else dbgNeighbour++;
+                            [r, g, b2] = lerpColour(hours);
+                            // Hours histogram
+                            if (hours === 0) hoursHist[0]++;
+                            else if (hours < 1) hoursHist[1]++;
+                            else if (hours < 2) hoursHist[2]++;
+                            else if (hours < 4) hoursHist[3]++;
+                            else if (hours < 6) hoursHist[4]++;
+                            else hoursHist[5]++;
+                        }
+
+                        tilePositions.push(
+                            a.x + nx*off, a.y + ny*off, a.z + nz*off,
+                            b.x + nx*off, b.y + ny*off, b.z + nz*off,
+                            c.x + nx*off, c.y + ny*off, c.z + nz*off
+                        );
+                        tileColors.push(r, g, b2, r, g, b2, r, g, b2);
+                    }
+                }
+
+                if (tilePositions.length > 0) {
+                    const tileGeo = new THREE.BufferGeometry();
+                    tileGeo.setAttribute('position', new THREE.Float32BufferAttribute(tilePositions, 3));
+                    tileGeo.setAttribute('color', new THREE.Float32BufferAttribute(tileColors, 3));
+                    tileGeo.computeVertexNormals();
+
+                    const tileMat = new THREE.MeshBasicMaterial({
+                        vertexColors: true,
+                        side: THREE.DoubleSide,
+                    });
+
+                    const tileMesh = new THREE.Mesh(tileGeo, tileMat);
+                    tileMesh.name = 'heatmap_mesh';
+                    group.add(tileMesh);
+                }
+
+                // Populate debug console
+                const webifcBBox = allMeshes.length > 0 ? computeBBox(allMeshes) : null;
+                const ifcosBBox = analysisMeshes.length > 0 ? computeBBox(analysisMeshes) : null;
+
+                updateDebugConsole({
+                    webifcMeshCount: allMeshes.length,
+                    webifcTris: webifcBBox ? webifcBBox.tris : 0,
+                    ifcosMeshCount: analysisMeshes.length,
+                    ifcosTris: ifcosBBox ? ifcosBBox.tris : 0,
+                    webifcBBox,
+                    ifcosBBox,
+                    gridSize,
+                    voxelCellCount: voxelHours.size,
+                    totalDisplayTris: dbgTotalTris,
+                    exactMatches: dbgExact,
+                    neighbourMatches: dbgNeighbour,
+                    misses: dbgMiss,
+                    degenerate: dbgDegen,
+                    hoursDistribution: [
+                        ['0h exactly', hoursHist[0]],
+                        ['0-1h', hoursHist[1]],
+                        ['1-2h', hoursHist[2]],
+                        ['2-4h', hoursHist[3]],
+                        ['4-6h', hoursHist[4]],
+                        ['6h+', hoursHist[5]],
+                    ],
+                    mode: 'dual-geometry',
+                });
+            } else {
+                // ─── VOXEL-ONLY MODE (fallback, no IfcOpenShell) ───
+                // Paint clipped voxel triangles directly
+                const off = 0.02;
+                const tilePositions = [];
+                const tileColors = [];
+
+                for (let i = 0; i < results.cellData.length; i++) {
+                    const cd = results.cellData[i];
+                    const hours = results.cellSunHours[i];
+                    const [r, g, b] = lerpColour(hours);
+                    const n = cd.normal;
+
+                    for (const tri of cd.tris) {
+                        for (const v of tri) {
+                            tilePositions.push(
+                                v[0] + n.x * off,
+                                v[1] + n.y * off,
+                                v[2] + n.z * off
+                            );
+                            tileColors.push(r, g, b);
+                        }
+                    }
+                }
+
+                if (tilePositions.length > 0) {
+                    const tileGeo = new THREE.BufferGeometry();
+                    tileGeo.setAttribute('position', new THREE.Float32BufferAttribute(tilePositions, 3));
+                    tileGeo.setAttribute('color', new THREE.Float32BufferAttribute(tileColors, 3));
+                    tileGeo.computeVertexNormals();
+
+                    const tileMat = new THREE.MeshBasicMaterial({
+                        vertexColors: true,
+                        side: THREE.DoubleSide,
+                    });
+
+                    const tileMesh = new THREE.Mesh(tileGeo, tileMat);
+                    tileMesh.name = 'heatmap_mesh';
+                    group.add(tileMesh);
+                }
+
+                // Debug console for voxel-only mode
+                let voxelTris = 0;
+                for (let i = 0; i < results.cellData.length; i++) {
+                    voxelTris += results.cellData[i].tris.length;
+                }
+
+                updateDebugConsole({
+                    webifcMeshCount: allMeshes.length,
+                    webifcTris: allMeshes.reduce((s, m) => {
+                        const idx = m.geometry.index;
+                        return s + (idx ? idx.count / 3 : m.geometry.attributes.position.count / 3);
+                    }, 0),
+                    ifcosMeshCount: 0,
+                    ifcosTris: 0,
+                    webifcBBox: allMeshes.length > 0 ? computeBBox(allMeshes) : null,
+                    ifcosBBox: null,
+                    gridSize,
+                    voxelCellCount: voxelHours.size,
+                    totalDisplayTris: voxelTris,
+                    exactMatches: voxelTris,
+                    neighbourMatches: 0,
+                    misses: 0,
+                    degenerate: 0,
+                    hoursDistribution: null,
+                    mode: 'voxel-only',
+                });
+            }
+
+            return group;
+        }
+
+        // ─── RUN ANALYSIS (multi-season) ───
+        async function runAnalysis() {
+            const btn = document.getElementById('run-btn');
+            if (!ifcLoaded) {
+                alert('Please import an IFC file first.');
+                return;
+            }
+
+            const seasons = getActiveSeasonKeys();
+            if (seasons.length === 0) {
+                alert('Please select at least one season.');
+                return;
+            }
+
+            btn.textContent = 'Analysing...';
+            btn.disabled = true;
+
+            // Clear previous season heatmaps
+            for (const [key, group] of Object.entries(seasonHeatmaps)) {
+                scene.remove(group);
+                group.traverse(c => {
+                    if (c.geometry) c.geometry.dispose();
+                    if (c.material) c.material.dispose();
+                });
+            }
+            seasonHeatmaps = {};
+            seasonResults = {};
+
+            try {
+                const lat = parseFloat(document.getElementById('latitude').value);
+                const lng = parseFloat(document.getElementById('longitude').value);
+                const timeStep = parseFloat(document.getElementById('time_step').value);
+
+                // Build BVH from all scene geometry
+                buildShadowBVH();
+
+                // Prepare voxel cells (voxelise + outer shell + clip + probe placement)
+                const cellData = await prepareVoxelCells();
+
+                for (let si = 0; si < seasons.length; si++) {
+                    const season = seasons[si];
+                    const dateStr = SEASON_DATES[season];
+                    showStatus(`Ray casting ${SEASON_LABELS[season]} (${si + 1}/${seasons.length})...`);
+
+                    const results = await runTerrainAnalysis(lat, lng, timeStep, dateStr, cellData);
+                    results.season = season;
+                    results.seasonLabel = SEASON_LABELS[season];
+                    seasonResults[season] = results;
+
+                    // Paint heatmap for this season
+                    const hm = createHeatmapGroup(results);
+                    seasonHeatmaps[season] = hm;
+                    scene.add(hm);
+                    hm.visible = false; // hide initially
+                }
+
+                // Compute global max hours across all seasons, round up to next whole hour
+                let globalMax = 0;
+                for (const s of seasons) {
+                    const mx = parseFloat(seasonResults[s].summary.max_hours);
+                    if (mx > globalMax) globalMax = mx;
+                }
+                legendMaxHours = Math.max(1, Math.ceil(globalMax));
+
+                // Rebuild heatmaps now that legendMaxHours is set
+                for (const s of seasons) {
+                    scene.remove(seasonHeatmaps[s]);
+                    seasonHeatmaps[s].traverse(c => {
+                        if (c.geometry) c.geometry.dispose();
+                        if (c.material) c.material.dispose();
+                    });
+                    const hm = createHeatmapGroup(seasonResults[s]);
+                    seasonHeatmaps[s] = hm;
+                    scene.add(hm);
+                    hm.visible = false;
+                }
+
+                // Show first analysed season
+                visibleSeason = seasons[0];
+                seasonHeatmaps[visibleSeason].visible = true;
+                lastAnalysisResults = seasonResults[visibleSeason];
+
+                // Show results
+                showResults(seasonResults[visibleSeason].summary, visibleSeason);
+
+                // Show season switcher if > 1 season
+                const switcher = document.getElementById('season-switcher');
+                if (seasons.length > 1) {
+                    switcher.classList.add('visible');
+                    document.querySelectorAll('.season-sw-btn').forEach(btn => {
+                        const key = btn.id.replace('sw-', '');
+                        btn.style.display = seasonResults[key] ? '' : 'none';
+                        btn.classList.toggle('active', key === visibleSeason);
+                    });
+                } else {
+                    switcher.classList.remove('visible');
+                }
+
+                // Show colour legend with notches
+                document.getElementById('colour-legend').classList.add('visible');
+                buildLegendNotches(timeStep);
+
+                const totalCells = seasonResults[visibleSeason].cellData.length;
+                showStatus(`Analysis complete \u2014 ${seasons.length} season(s), ${totalCells} grid cells`);
+                setTimeout(hideStatus, 5000);
+
+                // Build summary for step completion
+                const avgList = seasons.map(s => {
+                    const label = s === 'spring' ? 'Spr' : s === 'winter' ? 'Win' : 'Sum';
+                    return label + ' ' + seasonResults[s].summary.avg_hours + 'h';
+                });
+                // Complete step 4 which opens step 5 (results)
+                completeStep(4, '');
+                const s5sum = document.getElementById('step5-summary');
+                if (s5sum) s5sum.textContent = avgList.join(' | ');
+
+                // Hide the IFC meshes so only heatmap is visible
+                hideCalculationMeshes();
+
+                updateBugReportLink();
+
+            } catch (err) {
+                alert('Analysis failed: ' + err.message);
+                console.error(err);
+                hideStatus();
+            } finally {
+                btn.textContent = 'Run Analysis';
+                btn.disabled = false;
+            }
+        }
+
+        // ─── RESULTS DISPLAY ───
+        function showResults(summary, seasonKey) {
+            const label = seasonKey ? SEASON_LABELS[seasonKey] : 'Sun Hours Summary';
+            document.getElementById('results-title').textContent = label;
+
+            // Build per-season summary lines (hours omitted — heatmap only)
+            let html = '';
+            const keys = getActiveSeasonKeys();
+            for (const k of keys) {
+                if (!seasonResults[k]) continue;
+                const bold = k === seasonKey ? 'color:#e0e0e0; font-weight:600;' : '';
+                html += `<div style="${bold}">${SEASON_LABELS[k]}: analysis complete</div>`;
+            }
+            html += `<div style="margin-top:4px;">Total area: ${summary.area_total} m\u00b2 &nbsp;|&nbsp; Grid cells: ${summary.cells_total}</div>`;
+            document.getElementById('results-detail').innerHTML = html;
+        }
+
+        // ─── EXPORT GLB (coloured ground + grey buildings) ───
+        function downloadGLB() {
+            const btn = document.getElementById('glb-btn');
+            btn.textContent = 'Generating...';
+            btn.disabled = true;
+
+            const exportScene = new THREE.Scene();
+
+            // Add currently visible season heatmap
+            const activeHeatmap = seasonHeatmaps[visibleSeason];
+            if (activeHeatmap) {
+                const hmClone = activeHeatmap.clone();
+                // Convert vertex-color MeshBasicMaterial to MeshStandardMaterial for GLB compat
+                hmClone.traverse(c => {
+                    if (c.isMesh && c.material) {
+                        // Ensure consistent upward-facing normals by flipping
+                        // triangles whose face normal points downward (negative Y)
+                        const geo = c.geometry;
+                        const pos = geo.attributes.position.array;
+                        const col = geo.attributes.color ? geo.attributes.color.array : null;
+                        const v0 = new THREE.Vector3(), v1 = new THREE.Vector3(), v2 = new THREE.Vector3();
+                        for (let i = 0; i < pos.length; i += 9) {
+                            v0.set(pos[i], pos[i+1], pos[i+2]);
+                            v1.set(pos[i+3], pos[i+4], pos[i+5]);
+                            v2.set(pos[i+6], pos[i+7], pos[i+8]);
+                            const edge1 = new THREE.Vector3().subVectors(v1, v0);
+                            const edge2 = new THREE.Vector3().subVectors(v2, v0);
+                            const faceNormal = new THREE.Vector3().crossVectors(edge1, edge2);
+                            if (faceNormal.y < 0) {
+                                // Swap v1 and v2 to flip winding
+                                pos[i+3] = v2.x; pos[i+4] = v2.y; pos[i+5] = v2.z;
+                                pos[i+6] = v1.x; pos[i+7] = v1.y; pos[i+8] = v1.z;
+                                if (col) {
+                                    // Color array has same layout as position (3 per vertex, 9 per tri)
+                                    const r1 = col[i+3], g1 = col[i+4], b1 = col[i+5];
+                                    const r2 = col[i+6], g2 = col[i+7], b2 = col[i+8];
+                                    col[i+3] = r2; col[i+4] = g2; col[i+5] = b2;
+                                    col[i+6] = r1; col[i+7] = g1; col[i+8] = b1;
+                                }
+                            }
+                        }
+                        geo.attributes.position.needsUpdate = true;
+                        if (col) geo.attributes.color.needsUpdate = true;
+                        geo.computeVertexNormals();
+
+                        const newMat = new THREE.MeshStandardMaterial({
+                            vertexColors: c.material.vertexColors,
+                            side: THREE.FrontSide,
+                            roughness: 1.0,
+                            metalness: 0.0,
+                        });
+                        c.material.dispose();
+                        c.material = newMat;
+                    }
+                });
+                exportScene.add(hmClone);
+            }
+
+            // Add all meshes as grey context geometry
+            for (const mesh of allMeshes) {
+                mesh.updateWorldMatrix(true, false);
+                const clone = mesh.clone();
+                clone.applyMatrix4(mesh.matrixWorld);
+                clone.material = new THREE.MeshStandardMaterial({ color: 0xdddddd });
+                exportScene.add(clone);
+            }
+
+            try {
+                const exporter = new THREE.GLTFExporter();
+                exporter.parse(exportScene, (result) => {
+                    const blob = new Blob(
+                        [result],
+                        { type: 'application/octet-stream' }
+                    );
+                    const url = URL.createObjectURL(blob);
+                    const a = document.createElement('a');
+                    a.href = url;
+                    const d = new Date();
+                    a.download = `SunForm_${d.getDate()}-${d.getMonth()+1}-${d.getFullYear()}.glb`;
+                    document.body.appendChild(a);
+                    a.click();
+                    document.body.removeChild(a);
+                    URL.revokeObjectURL(url);
+                    btn.textContent = 'Download GLB';
+                    btn.disabled = false;
+                }, { binary: true });
+            } catch (err) {
+                alert('GLB export error: ' + err.message);
+                btn.textContent = 'Download GLB';
+                btn.disabled = false;
+            }
+        }
+
+        // ─── EXPORT PDF (plan view: raster heatmap + vector mesh edges) ───
+        function downloadPDF() {
+            const analysedSeasons = Object.keys(seasonResults);
+            if (analysedSeasons.length === 0) return;
+            const btn = document.getElementById('pdf-btn');
+            btn.textContent = 'Generating...';
+            btn.disabled = true;
+
+            try {
+                const { jsPDF } = window.jspdf;
+                const doc = new jsPDF({ orientation: 'landscape' });
+                const lat = document.getElementById('latitude').value;
+                const lng = document.getElementById('longitude').value;
+                const firstSummary = seasonResults[analysedSeasons[0]].summary;
+                const pageW = doc.internal.pageSize.width;
+                const pageH = doc.internal.pageSize.height;
+
+                // Save current camera state
+                const savedCamera = camera;
+                const savedRotateEnabled = controls.enableRotate;
+
+                // Set up ortho camera for true plan view
+                // Compute tight bounds around heatmap + selected ground meshes
+                const bb = new THREE.Box3();
+                // Include all season heatmaps
+                for (const group of Object.values(seasonHeatmaps)) {
+                    bb.expandByObject(group);
+                }
+                // Include all meshes for context
+                for (const mesh of allMeshes) {
+                    mesh.updateWorldMatrix(true, false);
+                    bb.expandByObject(mesh);
+                }
+                // Fallback to building group if bounds are empty
+                if (bb.isEmpty() && buildingGroup) {
+                    bb.setFromObject(buildingGroup);
+                }
+                const cx = (bb.min.x + bb.max.x) / 2;
+                const cz = (bb.min.z + bb.max.z) / 2;
+                const extX = (bb.max.x - bb.min.x) / 2 + 2;
+                const extZ = (bb.max.z - bb.min.z) / 2 + 2;
+
+                // Fit ortho camera to bounds (frustum is camera-local, position handles centering)
+                const planAspect = (pageW - 40) / (pageH - 60);
+                const orthoExtent = Math.max(extX, extZ / planAspect, extZ, extX / planAspect);
+                orthoCamera.left = -orthoExtent * planAspect;
+                orthoCamera.right = orthoExtent * planAspect;
+                orthoCamera.top = orthoExtent;
+                orthoCamera.bottom = -orthoExtent;
+                orthoCamera.position.set(cx, 500, cz);
+                orthoCamera.lookAt(cx, 0, cz);
+                orthoCamera.updateProjectionMatrix();
+
+                // Helper: project 3D point to PDF page coords
+                function projectToPDF(x, y, z) {
+                    const v = new THREE.Vector3(x, y, z);
+                    v.project(orthoCamera);
+                    // v.x, v.y are now in [-1, 1] NDC
+                    const px = 20 + ((v.x + 1) / 2) * (pageW - 40);
+                    const py = 25 + ((1 - v.y) / 2) * (pageH - 55);
+                    return { x: px, y: py };
+                }
+
+                // Collect mesh edges for vector overlay
+                const edgeLines = []; // [{x1,y1,x2,y2}, ...]
+                for (const mesh of allMeshes) {
+                    mesh.updateWorldMatrix(true, false);
+                    const wm = mesh.matrixWorld;
+                    const edges = new THREE.EdgesGeometry(mesh.geometry, 15);
+                    const pos = edges.attributes.position.array;
+                    for (let i = 0; i < pos.length; i += 6) {
+                        const p1 = new THREE.Vector3(pos[i], pos[i+1], pos[i+2]).applyMatrix4(wm);
+                        const p2 = new THREE.Vector3(pos[i+3], pos[i+4], pos[i+5]).applyMatrix4(wm);
+                        const a = projectToPDF(p1.x, p1.y, p1.z);
+                        const b = projectToPDF(p2.x, p2.y, p2.z);
+                        edgeLines.push({ x1: a.x, y1: a.y, x2: b.x, y2: b.y });
+                    }
+                    edges.dispose();
+                }
+
+                for (let si = 0; si < analysedSeasons.length; si++) {
+                    const season = analysedSeasons[si];
+                    const s = seasonResults[season].summary;
+
+                    if (si > 0) doc.addPage();
+
+                    // ── Render heatmap-only plan view as PNG ──
+                    // Hide ALL meshes, show only this season's heatmap
+                    for (const mesh of allMeshes) mesh.visible = false;
+                    for (const [k, group] of Object.entries(seasonHeatmaps)) {
+                        group.visible = (k === season);
+                    }
+                    // Set scene background to white for print
+                    const savedBg = scene.background;
+                    scene.background = new THREE.Color(0xffffff);
+
+                    renderer.render(scene, orthoCamera);
+                    const imgData = renderer.domElement.toDataURL('image/png');
+
+                    // Restore background
+                    scene.background = savedBg;
+
+                    // Place raster image (heatmap plan view)
+                    doc.addImage(imgData, 'PNG', 20, 25, pageW - 40, pageH - 55);
+
+                    // ── Draw vector edge overlay ──
+                    doc.setDrawColor(80, 80, 80);
+                    doc.setLineWidth(0.15);
+                    for (const line of edgeLines) {
+                        doc.line(line.x1, line.y1, line.x2, line.y2);
+                    }
+
+                    // ── Title bar at top ──
+                    doc.setFillColor(22, 33, 62);
+                    doc.rect(0, 0, pageW, 22, 'F');
+                    doc.setFontSize(14);
+                    doc.setTextColor(212, 136, 15);
+                    doc.text('SunForm', 10, 14);
+                    doc.setFontSize(10);
+                    doc.setTextColor(200, 200, 200);
+                    doc.text(SEASON_LABELS[season], 60, 14);
+                    doc.setFontSize(9);
+                    doc.setTextColor(150, 150, 150);
+                    doc.text(`Lat: ${lat}  Lng: ${lng}`, pageW - 10, 14, { align: 'right' });
+
+                    // ── Disclaimer footer ──
+                    doc.setFontSize(7);
+                    doc.setTextColor(120);
+                    doc.text('SunForm is beta software. There is no warranty. The Software provided under the author is incomplete and may contain errors or inaccuracies and therefore cannot be relied upon for design decision making.', 20, pageH - 5);
+                    doc.text('Generated: ' + new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' }), pageW - 20, pageH - 5, { align: 'right' });
+                }
+
+                // Restore scene state — hide all meshes (results view)
+                for (const mesh of allMeshes) {
+                    mesh.visible = false;
+                }
+                for (const [k, group] of Object.entries(seasonHeatmaps)) {
+                    group.visible = (k === visibleSeason);
+                }
+                camera = savedCamera;
+                controls.object = camera;
+                controls.enableRotate = savedRotateEnabled;
+                controls.update();
+
+                doc.save('SunForm_Report.pdf');
+
+            } catch (err) {
+                alert('PDF export error: ' + err.message);
+                console.error(err);
+            } finally {
+                btn.textContent = 'Download PDF';
+                btn.disabled = false;
+            }
+        }
+
+        // ─── BOUNDING BOX DRAWING TOOL ───
+        let bboxMode = false;
+        let bboxCorner1 = null;
+        let bboxTempHelper = null;
+
+        function toggleBboxMode() {
+            bboxMode = !bboxMode;
+            useEntireBounds = false;
+            const overlay = document.getElementById('bbox-overlay');
+            const viewport = document.getElementById('viewport');
+            const btn = document.getElementById('bbox-btn');
+
+            overlay.classList.toggle('visible', bboxMode);
+            viewport.classList.toggle('drawing-bbox', bboxMode);
+
+            document.getElementById('use-entire-btn').style.background = '';
+            document.getElementById('use-entire-btn').style.color = '';
+            document.getElementById('bbox-btn').style.background = bboxMode ? '#D4880F' : '';
+            document.getElementById('bbox-btn').style.color = bboxMode ? '#fff' : '';
+            document.getElementById('bbox-fields').style.display = 'flex';
+            document.getElementById('bbox-fields2').style.display = 'flex';
+
+            if (bboxMode) {
+                bboxCorner1 = null;
+                document.getElementById('bbox-hint').textContent = 'Click first corner on the ground plane';
+                document.getElementById('bbox-coords').textContent = '';
+                controls.enabled = false;
+            } else {
+                controls.enabled = true;
+                removeTempBbox();
+            }
+            enableRunButton();
+        }
+
+        function removeTempBbox() {
+            if (bboxTempHelper) {
+                scene.remove(bboxTempHelper);
+                bboxTempHelper.traverse(c => {
+                    if (c.geometry) c.geometry.dispose();
+                    if (c.material) c.material.dispose();
+                });
+                bboxTempHelper = null;
+            }
+        }
+
+        function drawBboxRect(x1, y1, x2, y2, color) {
+            removeTempBbox();
+            removeBboxHelper();
+            const group = new THREE.Group();
+            const points = [
+                new THREE.Vector3(x1, 0.05, -y1),
+                new THREE.Vector3(x2, 0.05, -y1),
+                new THREE.Vector3(x2, 0.05, -y2),
+                new THREE.Vector3(x1, 0.05, -y2),
+                new THREE.Vector3(x1, 0.05, -y1),
+            ];
+            group.add(new THREE.Line(
+                new THREE.BufferGeometry().setFromPoints(points),
+                new THREE.LineBasicMaterial({ color })
+            ));
+            const fillGeo = new THREE.PlaneGeometry(Math.abs(x2 - x1), Math.abs(y2 - y1));
+            const fill = new THREE.Mesh(fillGeo, new THREE.MeshBasicMaterial({
+                color, transparent: true, opacity: 0.15, side: THREE.DoubleSide
+            }));
+            fill.rotation.x = -Math.PI / 2;
+            fill.position.set((x1 + x2) / 2, 0.04, -(y1 + y2) / 2);
+            group.add(fill);
+            scene.add(group);
+            return group;
+        }
+
+        function removeBboxHelper() {
+            if (bboxHelper) {
+                scene.remove(bboxHelper);
+                bboxHelper.traverse(c => {
+                    if (c.geometry) c.geometry.dispose();
+                    if (c.material) c.material.dispose();
+                });
+                bboxHelper = null;
+            }
+        }
+
+        function getGroundIntersection(event) {
+            const container = document.getElementById('viewport');
+            const rect = container.getBoundingClientRect();
+            const mouse = new THREE.Vector2(
+                ((event.clientX - rect.left) / rect.width) * 2 - 1,
+                -((event.clientY - rect.top) / rect.height) * 2 + 1
+            );
+            const raycaster = new THREE.Raycaster();
+            raycaster.setFromCamera(mouse, camera);
+            const hits = raycaster.intersectObject(groundPlane);
+            return hits.length > 0 ? hits[0].point : null;
+        }
+
+        function handleBboxClick(event) {
+            const pt = getGroundIntersection(event);
+            if (!pt) return;
+            const ifcX = pt.x, ifcY = -pt.z;
+
+            if (!bboxCorner1) {
+                bboxCorner1 = { x: ifcX, y: ifcY };
+                document.getElementById('bbox-hint').textContent = 'Click second corner';
+                document.getElementById('bbox-coords').textContent =
+                    `Corner 1: (${ifcX.toFixed(1)}, ${ifcY.toFixed(1)})`;
+                const markerGeo = new THREE.SphereGeometry(0.3, 8, 8);
+                bboxTempHelper = new THREE.Mesh(markerGeo, new THREE.MeshBasicMaterial({ color: 0xD4880F }));
+                bboxTempHelper.position.set(pt.x, 0.2, pt.z);
+                scene.add(bboxTempHelper);
+            } else {
+                const x1 = Math.min(bboxCorner1.x, ifcX);
+                const y1 = Math.min(bboxCorner1.y, ifcY);
+                const x2 = Math.max(bboxCorner1.x, ifcX);
+                const y2 = Math.max(bboxCorner1.y, ifcY);
+                document.getElementById('bbox_min_x').value = x1.toFixed(1);
+                document.getElementById('bbox_min_y').value = y1.toFixed(1);
+                document.getElementById('bbox_max_x').value = x2.toFixed(1);
+                document.getElementById('bbox_max_y').value = y2.toFixed(1);
+                bboxHelper = drawBboxRect(x1, y1, x2, y2, 0x00CFC8);
+                // Exit bbox mode
+                bboxMode = false;
+                document.getElementById('bbox-overlay').classList.remove('visible');
+                document.getElementById('viewport').classList.remove('drawing-bbox');
+                document.getElementById('bbox-btn').style.background = '';
+                document.getElementById('bbox-btn').style.color = '';
+                controls.enabled = true;
+            }
+        }
+
+        document.getElementById('viewport').addEventListener('mousemove', (event) => {
+            if (!bboxMode || !bboxCorner1) return;
+            const pt = getGroundIntersection(event);
+            if (!pt) return;
+            const ifcX = pt.x, ifcY = -pt.z;
+            document.getElementById('bbox-coords').textContent =
+                `Corner 1: (${bboxCorner1.x.toFixed(1)}, ${bboxCorner1.y.toFixed(1)})` +
+                `  \u2192  (${ifcX.toFixed(1)}, ${ifcY.toFixed(1)})`;
+            removeTempBbox();
+            bboxTempHelper = drawBboxRect(bboxCorner1.x, bboxCorner1.y, ifcX, ifcY, 0xD4880F);
+        });
+
+        // ─── STATUS HELPERS ───
+        function showStatus(msg) {
+            const el = document.getElementById('status-overlay');
+            el.textContent = msg;
+            el.style.display = 'block';
+        }
+
+        function hideStatus() {
+            document.getElementById('status-overlay').style.display = 'none';
+        }
+
+        // ─── FLY / ORBIT MODE ───
+        function enableFlyMode() {
+            flyMode = true;
+            controls.enabled = false;
+            const euler = new THREE.Euler().setFromQuaternion(camera.quaternion, 'YXZ');
+            flyYaw = flyYawTarget = euler.y;
+            flyPitch = flyPitchTarget = euler.x;
+            renderer.domElement.requestPointerLock();
+            document.getElementById('fly-crosshair').style.display = 'block';
+            updateViewportInfo();
+        }
+
+        function enableOrbitMode() {
+            flyMode = false;
+            for (const k in flyKeys) flyKeys[k] = false;
+            if (document.pointerLockElement) document.exitPointerLock();
+            controls.enabled = true;
+            document.getElementById('fly-crosshair').style.display = 'none';
+            // Raycast along look direction to find a sensible orbit target
+            const lookDir = new THREE.Vector3(0, 0, -1).applyQuaternion(camera.quaternion);
+            const rc = new THREE.Raycaster(camera.position, lookDir);
+            const hits = rc.intersectObjects(allMeshes, false);
+            if (hits.length > 0) {
+                controls.target.copy(hits[0].point);
+            } else if (buildingGroup) {
+                // No hit — fall back to building centre
+                const bb = new THREE.Box3().setFromObject(buildingGroup);
+                bb.getCenter(controls.target);
+            }
+            controls.update();
+            updateViewportInfo();
+        }
+
+        document.addEventListener('mousemove', (e) => {
+            if (!flyMode || !document.pointerLockElement) return;
+            const sensitivity = 0.002;
+            flyYawTarget -= e.movementX * sensitivity;
+            flyPitchTarget -= e.movementY * sensitivity;
+            flyPitchTarget = Math.max(-Math.PI / 2 + 0.05, Math.min(Math.PI / 2 - 0.05, flyPitchTarget));
+        });
+
+        function updateViewportInfo() {
+            const el = document.getElementById('viewport-info');
+            if (flyMode) {
+                el.textContent = 'FLY MODE — W/S: forward/back | A/D: strafe | Q/E: up/down | Mouse: look | O: orbit mode';
+            } else {
+                el.textContent = 'ORBIT MODE — Drag: orbit | Scroll: zoom | Right-drag: pan | F: fly mode';
+            }
+        }
+
+        // Fly mode animation loop (runs inside main animate)
+        function updateFlyMovement() {
+            if (!flyMode) return;
+            // Smooth interpolation of look direction
+            flyYaw += (flyYawTarget - flyYaw) * FLY_LOOK_SMOOTHING;
+            flyPitch += (flyPitchTarget - flyPitch) * FLY_LOOK_SMOOTHING;
+            const euler = new THREE.Euler(flyPitch, flyYaw, 0, 'YXZ');
+            camera.quaternion.setFromEuler(euler);
+
+            const forward = new THREE.Vector3(0, 0, -1).applyQuaternion(camera.quaternion);
+            const right = new THREE.Vector3(1, 0, 0).applyQuaternion(camera.quaternion);
+            const up = new THREE.Vector3(0, 1, 0);
+
+            const move = new THREE.Vector3();
+            if (flyKeys.w) move.add(forward);
+            if (flyKeys.s) move.sub(forward);
+            if (flyKeys.a) move.sub(right);
+            if (flyKeys.d) move.add(right);
+            if (flyKeys.q) move.sub(up);
+            if (flyKeys.e) move.add(up);
+
+            if (move.length() > 0) {
+                move.normalize().multiplyScalar(FLY_SPEED);
+                camera.position.add(move);
+            }
+        }
+
+        // ─── KEYBOARD SHORTCUTS ───
+        document.addEventListener('keydown', (e) => {
+            if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT' || e.target.tagName === 'TEXTAREA') return;
+            const key = e.key.toLowerCase();
+
+            if (key === 'escape') {
+                if (flyMode) { enableOrbitMode(); return; }
+                if (bboxMode) toggleBboxMode();
+                return;
+            }
+
+            if (key === 'f') {
+                enableFlyMode();
+                return;
+            }
+            if (key === 'o') {
+                enableOrbitMode();
+                return;
+            }
+
+            // Left/Right arrows to cycle seasons when results are visible
+            if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
+                const seasonOrder = ['winter', 'spring', 'summer'];
+                const active = seasonOrder.filter(s => seasonResults[s]);
+                if (active.length > 1) {
+                    const idx = active.indexOf(visibleSeason);
+                    if (idx !== -1) {
+                        const next = e.key === 'ArrowRight'
+                            ? active[(idx + 1) % active.length]
+                            : active[(idx - 1 + active.length) % active.length];
+                        switchVisibleSeason(next);
+                        e.preventDefault();
+                    }
+                }
+                return;
+            }
+
+            // WASD + Q/E for fly mode
+            if (key in flyKeys) {
+                flyKeys[key] = true;
+                e.preventDefault();
+            }
+        });
+
+        document.addEventListener('keyup', (e) => {
+            const key = e.key.toLowerCase();
+            if (key in flyKeys) {
+                flyKeys[key] = false;
+            }
+        });
+
+        // ─── LOCATION PICKER (Leaflet) ───
+        function initLocationMap() {
+            locationMap = L.map('location-map', {
+                zoomControl: true,
+                attributionControl: false,
+                doubleClickZoom: false,
+            }).setView([54.0, -2.0], 6); // UK overview
+
+            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
+                maxZoom: 19,
+            }).addTo(locationMap);
+
+            locationMarker = L.marker([51.5074, -0.1278]).addTo(locationMap);
+
+            locationMap.on('click', (e) => {
+                const { lat, lng } = e.latlng;
+                locationMarker.setLatLng([lat, lng]);
+                document.getElementById('latitude').value = lat.toFixed(4);
+                document.getElementById('longitude').value = lng.toFixed(4);
+            });
+
+            // Sync: when lat/lng fields change, update map
+            ['latitude', 'longitude'].forEach(id => {
+                document.getElementById(id).addEventListener('change', () => {
+                    const lat = parseFloat(document.getElementById('latitude').value) || 51.5074;
+                    const lng = parseFloat(document.getElementById('longitude').value) || -0.1278;
+                    locationMarker.setLatLng([lat, lng]);
+                    locationMap.setView([lat, lng], Math.max(locationMap.getZoom(), 10));
+                });
+            });
+
+            // Search box (Nominatim)
+            let searchTimeout = null;
+            document.getElementById('location-search').addEventListener('input', (e) => {
+                clearTimeout(searchTimeout);
+                const query = e.target.value.trim();
+                if (query.length < 3) return;
+                searchTimeout = setTimeout(() => {
+                    fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=1`, {
+                        headers: { 'Accept': 'application/json' }
+                    })
+                    .then(r => r.json())
+                    .then(results => {
+                        if (results.length > 0) {
+                            const lat = parseFloat(results[0].lat);
+                            const lng = parseFloat(results[0].lon);
+                            document.getElementById('latitude').value = lat.toFixed(4);
+                            document.getElementById('longitude').value = lng.toFixed(4);
+                            locationMarker.setLatLng([lat, lng]);
+                            locationMap.setView([lat, lng], 14);
+                        }
+                    })
+                    .catch(() => {});
+                }, 600);
+            });
+
+            document.getElementById('location-search').addEventListener('keydown', (e) => {
+                if (e.key === 'Enter') e.preventDefault();
+            });
+        }
+
+        // ─── SEASON TOGGLES ───
+        function toggleSeason(season) {
+            // Count currently active
+            const count = Object.values(activeSeasons).filter(Boolean).length;
+            if (activeSeasons[season] && count <= 1) return; // must keep at least one
+            activeSeasons[season] = !activeSeasons[season];
+            document.getElementById('season-' + season).classList.toggle('active', activeSeasons[season]);
+        }
+
+        function getActiveSeasonKeys() {
+            return Object.keys(activeSeasons).filter(k => activeSeasons[k]);
+        }
+
+        // ─── SEASON SWITCHER ───
+        function switchVisibleSeason(season) {
+            if (!seasonResults[season]) return;
+            clearRayProbe();
+            visibleSeason = season;
+            // Hide all heatmaps, show selected
+            for (const [key, group] of Object.entries(seasonHeatmaps)) {
+                group.visible = (key === season);
+            }
+            // Update switcher buttons
+            document.querySelectorAll('.season-sw-btn').forEach(btn => btn.classList.remove('active'));
+            document.getElementById('sw-' + season).classList.add('active');
+            // Update results panel for this season
+            showResults(seasonResults[season].summary, season);
+        }
+
+        // ─── BUG REPORT ───
+        function updateBugReportLink() {
+            const lat = document.getElementById('latitude').value;
+            const lng = document.getElementById('longitude').value;
+            const seasons = getActiveSeasonKeys().join(', ');
+            const grid = document.getElementById('grid_resolution').value;
+            const ua = navigator.userAgent;
+            const ts = new Date().toISOString();
+            const body = [
+                'SunForm Bug Report',
+                '---',
+                'Latitude: ' + lat,
+                'Longitude: ' + lng,
+                'Seasons analysed: ' + seasons,
+                'Grid resolution: ' + grid + 'm',
+                'Browser: ' + ua,
+                'Timestamp: ' + ts,
+                '',
+                'Description of issue:',
+                '',
+            ].join('\n');
+            const link = document.getElementById('bug-report-link');
+            link.href = 'mailto:sunform@jakewhitearchitecture.com?subject=' +
+                encodeURIComponent('SunForm Bug Report') +
+                '&body=' + encodeURIComponent(body);
+        }
+
+        // ─── DISCLAIMER MODAL ───
+        function updateDisclaimerAccept() {
+            const c1 = document.getElementById('disclaimer-check1').checked;
+            const c2 = document.getElementById('disclaimer-check2').checked;
+            const allChecked = c1 && c2;
+            document.getElementById('disclaimer-accept-btn').disabled = !allChecked;
+        }
+
+        function acceptDisclaimer() {
+            document.getElementById('disclaimer-modal').classList.add('hidden');
+        }
+
+        // ─── MOBILE SLIDE PANEL ───
+        function toggleMobilePanel() {
+            const panel = document.getElementById('main-panel');
+            const backdrop = document.getElementById('panel-backdrop');
+            const btn = document.getElementById('hamburger-btn');
+            const isOpen = panel.classList.contains('open');
+            if (isOpen) {
+                closeMobilePanel();
+            } else {
+                panel.classList.add('open');
+                backdrop.classList.add('visible');
+                btn.classList.add('active');
+            }
+        }
+        function closeMobilePanel() {
+            document.getElementById('main-panel').classList.remove('open');
+            document.getElementById('panel-backdrop').classList.remove('visible');
+            document.getElementById('hamburger-btn').classList.remove('active');
+        }
+
+        // ─── DOWNLOAD CONFIRMATION ───
+        let pendingDownloadType = null;
+
+        function showDownloadConfirm(type) {
+            pendingDownloadType = type;
+            document.getElementById('download-confirm-check').checked = false;
+            document.getElementById('download-confirm-btn').disabled = true;
+            document.getElementById('download-confirm-overlay').classList.add('visible');
+        }
+
+        function hideDownloadConfirm() {
+            document.getElementById('download-confirm-overlay').classList.remove('visible');
+            pendingDownloadType = null;
+        }
+
+        function updateDownloadConfirm() {
+            document.getElementById('download-confirm-btn').disabled =
+                !document.getElementById('download-confirm-check').checked;
+        }
+
+        function proceedDownload() {
+            const type = pendingDownloadType;
+            hideDownloadConfirm();
+            if (type === 'glb') downloadGLB();
+            else if (type === 'pdf') downloadPDF();
+        }
+
+        // ─── MESH VISIBILITY MANAGEMENT ───
+        function hideCalculationMeshes() {
+            // Hide ALL meshes when showing results
+            for (const mesh of allMeshes) {
+                mesh.visible = false;
+            }
+        }
+
+        function showCalculationMeshes() {
+            // Show ALL meshes
+            for (const mesh of allMeshes) {
+                mesh.visible = true;
+            }
+        }
+
+        function grayOutResults() {
+            // Reduce opacity of all season heatmaps when going back to select mesh
+            for (const [key, group] of Object.entries(seasonHeatmaps)) {
+                group.traverse(c => {
+                    if (c.material && !c.material._grayedOut) {
+                        c.material = c.material.clone();
+                        c.material.opacity = 0.25;
+                        c.material.transparent = true;
+                        c.material._grayedOut = true;
+                    }
+                });
+                group.visible = true;
+            }
+        }
+
+        function restoreResults() {
+            // Restore full opacity when leaving select mesh
+            for (const [key, group] of Object.entries(seasonHeatmaps)) {
+                group.traverse(c => {
+                    if (c.material && c.material._grayedOut) {
+                        c.material.opacity = 1.0;
+                        c.material.transparent = false;
+                        c.material._grayedOut = false;
+                    }
+                });
+                group.visible = (key === visibleSeason);
+            }
+        }
+
+        // ─── RAY PROBE (click-to-interrogate heatmap) ───
+        function clearRayProbe() {
+            if (rayProbeGroup) {
+                scene.remove(rayProbeGroup);
+                rayProbeGroup.traverse(c => {
+                    if (c.geometry) c.geometry.dispose();
+                    if (c.material) c.material.dispose();
+                });
+                rayProbeGroup = null;
+            }
+            rayProbeActive = false;
+            document.getElementById('ray-probe-panel').classList.remove('visible');
+        }
+
+        // ─── PROBE PANEL DRAG ───
+        let probeDragging = false;
+        let probeDragOffX = 0;
+        let probeDragOffY = 0;
+
+        function initProbeDrag() {
+            const panel = document.getElementById('ray-probe-panel');
+            const title = panel.querySelector('.probe-title');
+
+            title.addEventListener('mousedown', (e) => {
+                // Don't drag when clicking the Clear button
+                if (e.target.closest('.probe-clear-btn')) return;
+                e.preventDefault();
+                probeDragging = true;
+                const rect = panel.getBoundingClientRect();
+                probeDragOffX = e.clientX - rect.left;
+                probeDragOffY = e.clientY - rect.top;
+            });
+
+            document.addEventListener('mousemove', (e) => {
+                if (!probeDragging) return;
+                const viewport = document.getElementById('viewport');
+                const vr = viewport.getBoundingClientRect();
+                const pw = panel.offsetWidth;
+                const ph = panel.offsetHeight;
+
+                let newLeft = e.clientX - vr.left - probeDragOffX;
+                let newTop = e.clientY - vr.top - probeDragOffY;
+
+                // Clamp to viewport bounds
+                newLeft = Math.max(0, Math.min(newLeft, vr.width - pw));
+                newTop = Math.max(0, Math.min(newTop, vr.height - ph));
+
+                panel.style.left = newLeft + 'px';
+                panel.style.top = newTop + 'px';
+                panel.style.bottom = 'auto';
+            });
+
+            document.addEventListener('mouseup', () => {
+                probeDragging = false;
+            });
+        }
+
+        function resetProbePosition() {
+            const panel = document.getElementById('ray-probe-panel');
+            panel.style.left = '20px';
+            panel.style.bottom = '60px';
+            panel.style.top = 'auto';
+        }
+
+        function handleRayProbeClick(event) {
+            // Only works when results are showing
+            if (currentStep !== 5) return;
+            if (!seasonResults[visibleSeason]) return;
+
+            const container = document.getElementById('viewport');
+            const rect = container.getBoundingClientRect();
+            const mouse = flyMode
+                ? new THREE.Vector2(0, 0)
+                : new THREE.Vector2(
+                    ((event.clientX - rect.left) / rect.width) * 2 - 1,
+                    -((event.clientY - rect.top) / rect.height) * 2 + 1
+                );
+
+            const raycaster = new THREE.Raycaster();
+            raycaster.setFromCamera(mouse, camera);
+
+            // Raycast against the active heatmap mesh
+            const heatGroup = seasonHeatmaps[visibleSeason];
+            if (!heatGroup) return;
+            const heatMeshes = [];
+            heatGroup.traverse(c => { if (c.isMesh) heatMeshes.push(c); });
+            const hits = raycaster.intersectObjects(heatMeshes, false);
+            if (hits.length === 0) return;
+
+            const hitPoint = hits[0].point;
+
+            // Find the closest cellData centroid to the hit point
+            const results = seasonResults[visibleSeason];
+            let bestIdx = -1;
+            let bestDist = Infinity;
+            for (let i = 0; i < results.cellData.length; i++) {
+                const cd = results.cellData[i];
+                const dx = cd.centroid.x - hitPoint.x;
+                const dy = cd.centroid.y - hitPoint.y;
+                const dz = cd.centroid.z - hitPoint.z;
+                const d2 = dx * dx + dy * dy + dz * dz;
+                if (d2 < bestDist) {
+                    bestDist = d2;
+                    bestIdx = i;
+                }
+            }
+            if (bestIdx === -1) return;
+
+            const cell = results.cellData[bestIdx];
+            const sunHours = results.cellSunHours[bestIdx];
+            const sunPositions = results.sunPositions;
+
+            // Clear previous probe
+            clearRayProbe();
+
+            // Build ray visualisation
+            rayProbeGroup = new THREE.Group();
+            rayProbeGroup.name = 'ray_probe';
+
+            const origin = new THREE.Vector3(
+                cell.centroid.x + cell.normal.x * 0.01,
+                cell.centroid.y + cell.normal.y * 0.01,
+                cell.centroid.z + cell.normal.z * 0.01
+            );
+
+            // Add a small sphere marker at the probe point
+            const markerGeo = new THREE.SphereGeometry(0.08, 12, 8);
+            const markerMat = new THREE.MeshBasicMaterial({ color: 0xFFFFFF });
+            const marker = new THREE.Mesh(markerGeo, markerMat);
+            marker.position.copy(origin);
+            rayProbeGroup.add(marker);
+
+            const RAY_LEN = 8; // visual length of ray lines in metres
+            const tableRows = [];
+
+            for (let si = 0; si < sunPositions.length; si++) {
+                const sp = sunPositions[si];
+                const dir = sunDirection(sp.azimuth, sp.altitude);
+
+                const ox = origin.x, oy = origin.y, oz = origin.z;
+                const blocked = shadowBVH
+                    ? shadowBVH.intersectsAny(ox, oy, oz, dir.x, dir.y, dir.z)
+                    : false;
+
+                // Draw ray line
+                const endPt = new THREE.Vector3(
+                    ox + dir.x * RAY_LEN,
+                    oy + dir.y * RAY_LEN,
+                    oz + dir.z * RAY_LEN
+                );
+
+                const lineGeo = new THREE.BufferGeometry().setFromPoints([origin, endPt]);
+                const lineMat = new THREE.LineBasicMaterial({
+                    color: blocked ? 0xFF4444 : 0xFFD700,
+                    linewidth: 1,
+                });
+                const line = new THREE.Line(lineGeo, lineMat);
+                rayProbeGroup.add(line);
+
+                // Format time as HH:MM
+                const h = Math.floor(sp.hour);
+                const m = Math.round((sp.hour - h) * 60);
+                const timeStr = String(h).padStart(2, '0') + ':' + String(m).padStart(2, '0');
+
+                tableRows.push({
+                    time: timeStr,
+                    azimuth: sp.azimuth.toFixed(1),
+                    altitude: sp.altitude.toFixed(1),
+                    blocked,
+                });
+            }
+
+            scene.add(rayProbeGroup);
+            rayProbeActive = true;
+
+            // Populate info panel
+            const hitCount = tableRows.filter(r => !r.blocked).length;
+            const panel = document.getElementById('ray-probe-panel');
+            document.getElementById('probe-summary').textContent =
+                SEASON_LABELS[visibleSeason] + ' — ' +
+                sunHours.toFixed(1) + 'h sun (' + hitCount + '/' + tableRows.length + ' rays unblocked)';
+
+            let html = '<table><tr><th>Time</th><th>Azimuth</th><th>Altitude</th><th>Status</th></tr>';
+            for (const row of tableRows) {
+                const cls = row.blocked ? 'ray-blocked' : 'ray-hit';
+                const status = row.blocked ? 'Blocked' : 'Sun';
+                html += '<tr class="' + cls + '">' +
+                    '<td>' + row.time + '</td>' +
+                    '<td>' + row.azimuth + '°</td>' +
+                    '<td>' + row.altitude + '°</td>' +
+                    '<td>' + status + '</td></tr>';
+            }
+            html += '</table>';
+            document.getElementById('probe-table').innerHTML = html;
+            resetProbePosition();
+            panel.classList.add('visible');
+        }
+
+        // ─── INIT ───
+        initThree();
+        initWebIfc();
+        initIfcosWorker();  // Start Pyodide+IfcOpenShell download in background worker
+        initProbeDrag();
+        // ─── BETA FEEDBACK WIZARD ───
+        let bfChallenge = {};  // stores the generated challenge data
+
+        function openBetaFeedback() {
+            const lat = parseFloat(document.getElementById('latitude').value) || 51.5074;
+            const lng = parseFloat(document.getElementById('longitude').value) || -0.1278;
+
+            // Pick a random date spread across the year
+            const month = Math.floor(Math.random() * 12);
+            const day = Math.floor(Math.random() * 28) + 1;
+            const year = new Date().getFullYear();
+            const dateStr = year + '-' + String(month + 1).padStart(2, '0') + '-' + String(day).padStart(2, '0');
+
+            // Get all sun positions for that date at 1-hour steps
+            const positions = getSunPositions(lat, lng, dateStr, 1);
+            if (positions.length === 0) {
+                alert('No visible sun positions found for this date and location. Please set your site coordinates first.');
+                return;
+            }
+
+            // Pick a random hour from those where the sun is up
+            const pick = positions[Math.floor(Math.random() * positions.length)];
+
+            bfChallenge = {
+                lat: lat,
+                lng: lng,
+                dateStr: dateStr,
+                hour: pick.hour,
+                localHour: null,  // set below after BST calc
+                calcAzimuth: pick.azimuth,
+                calcAltitude: pick.altitude
+            };
+
+            // Convert UTC hour to local clock time (UK: UTC in winter, UTC+1 in BST)
+            function isUKBST(dateStr) {
+                const y = parseInt(dateStr.split('-')[0]);
+                const m = parseInt(dateStr.split('-')[1]);
+                const d = parseInt(dateStr.split('-')[2]);
+                if (m < 3 || m > 10) return false;
+                if (m > 3 && m < 10) return true;
+                // March: BST starts last Sunday
+                if (m === 3) {
+                    const lastDay = new Date(y, 2, 31).getDay();
+                    const lastSun = 31 - lastDay;
+                    return d >= lastSun;
+                }
+                // October: BST ends last Sunday
+                const lastDay = new Date(y, 9, 31).getDay();
+                const lastSun = 31 - lastDay;
+                return d < lastSun;
+            }
+
+            const bstOffset = isUKBST(dateStr) ? 1 : 0;
+            const localHour = pick.hour + bstOffset;
+            bfChallenge.localHour = localHour;
+            bfChallenge.utcOffset = bstOffset;
+
+            // Build SunCalc URL: https://www.suncalc.org/#/{lat},{lon},{zoom}/{YYYY.MM.DD}/{HH:MM}/1/3
+            const suncalcDate = dateStr.replace(/-/g, '.');
+            const suncalcTime = String(localHour).padStart(2, '0') + ':00';
+            const suncalcUrl = 'https://www.suncalc.org/#/' + lat.toFixed(4) + ',' + lng.toFixed(4) + ',9/' + suncalcDate + '/' + suncalcTime + '/1/3';
+            document.getElementById('bf-suncalc-link').href = suncalcUrl;
+
+            // Populate the wizard
+            document.getElementById('bf-lat').textContent = lat.toFixed(4);
+            document.getElementById('bf-lng').textContent = lng.toFixed(4);
+            document.getElementById('bf-date').textContent = dateStr;
+            document.getElementById('bf-time').textContent = suncalcTime;
+            document.getElementById('bf-user-azimuth').value = '';
+            document.getElementById('bf-user-altitude').value = '';
+
+            // Show step 1, hide step 2
+            document.getElementById('bf-step-1').style.display = '';
+            document.getElementById('bf-step-2').style.display = 'none';
+            document.getElementById('beta-feedback-modal').classList.remove('hidden');
+        }
+
+        function closeBetaFeedback() {
+            document.getElementById('beta-feedback-modal').classList.add('hidden');
+        }
+
+        function checkBetaFeedback() {
+            const userAz = parseFloat(document.getElementById('bf-user-azimuth').value);
+            const userAlt = parseFloat(document.getElementById('bf-user-altitude').value);
+            if (isNaN(userAz) || isNaN(userAlt)) {
+                alert('Please enter both azimuth and altitude values.');
+                return;
+            }
+
+            const calcAz = bfChallenge.calcAzimuth;
+            const calcAlt = bfChallenge.calcAltitude;
+            const diffAz = Math.abs(userAz - calcAz);
+            const diffAlt = Math.abs(userAlt - calcAlt);
+            const pctAz = calcAz !== 0 ? (diffAz / Math.abs(calcAz)) * 100 : diffAz;
+            let pctAlt = calcAlt !== 0 ? (diffAlt / Math.abs(calcAlt)) * 100 : diffAlt;
+
+            // For near-horizon altitudes, use absolute difference instead of percentage
+            if (Math.abs(calcAlt) < 5) {
+                // When altitude < 5°, percentage is misleading; use degree threshold instead
+                // Treat <0.5° diff as good, <1° as acceptable
+                pctAlt = diffAlt <= 0.5 ? 0.5 : diffAlt <= 1 ? 1.5 : 3;
+            }
+
+            // Store for email
+            bfChallenge.userAzimuth = userAz;
+            bfChallenge.userAltitude = userAlt;
+            bfChallenge.diffAz = diffAz;
+            bfChallenge.diffAlt = diffAlt;
+
+            // Populate results
+            document.getElementById('bf-user-az-result').textContent = userAz.toFixed(2) + '\u00b0';
+            document.getElementById('bf-user-alt-result').textContent = userAlt.toFixed(2) + '\u00b0';
+            document.getElementById('bf-calc-az-result').textContent = calcAz.toFixed(2) + '\u00b0';
+            document.getElementById('bf-calc-alt-result').textContent = calcAlt.toFixed(2) + '\u00b0';
+
+            const diffAzEl = document.getElementById('bf-diff-az');
+            const diffAltEl = document.getElementById('bf-diff-alt');
+            diffAzEl.textContent = diffAz.toFixed(2) + '\u00b0 (' + pctAz.toFixed(1) + '%)';
+            diffAltEl.textContent = diffAlt.toFixed(2) + '\u00b0 (' + pctAlt.toFixed(1) + '%)';
+            diffAzEl.style.color = pctAz <= 1 ? '#4CAF50' : pctAz <= 2 ? '#FFA726' : '#FF5252';
+            diffAltEl.style.color = pctAlt <= 1 ? '#4CAF50' : pctAlt <= 2 ? '#FFA726' : '#FF5252';
+
+            const maxPct = Math.max(pctAz, pctAlt);
+            const verdict = document.getElementById('bf-verdict');
+            if (maxPct <= 1) {
+                verdict.textContent = 'Good match — within 1%';
+                verdict.style.background = 'rgba(76,175,80,0.15)';
+                verdict.style.color = '#4CAF50';
+            } else if (maxPct <= 2) {
+                verdict.textContent = 'Acceptable match — within 2%';
+                verdict.style.background = 'rgba(255,167,38,0.15)';
+                verdict.style.color = '#FFA726';
+            } else {
+                verdict.textContent = 'Significant difference detected';
+                verdict.style.background = 'rgba(255,82,82,0.15)';
+                verdict.style.color = '#FF5252';
+            }
+
+            // Switch to step 2
+            document.getElementById('bf-step-1').style.display = 'none';
+            document.getElementById('bf-step-2').style.display = '';
+        }
+
+        function sendBetaFeedback() {
+            const c = bfChallenge;
+            const emailMaxPct = Math.max(
+                c.diffAz / Math.abs(bfChallenge.calcAzimuth) * 100,
+                c.diffAlt / Math.abs(bfChallenge.calcAltitude) * 100
+            );
+            const matchStatus = emailMaxPct <= 1 ? 'GOOD MATCH' : emailMaxPct <= 2 ? 'ACCEPTABLE MATCH' : 'DIFFERENCE DETECTED';
+
+            const subject = encodeURIComponent('SunForm Beta Feedback — ' + matchStatus);
+            const body = encodeURIComponent(
+                'SunForm Beta Testing Feedback\n' +
+                '================================\n\n' +
+                'Site Location\n' +
+                '  Latitude:   ' + c.lat.toFixed(4) + '\n' +
+                '  Longitude:  ' + c.lng.toFixed(4) + '\n\n' +
+                'Test Parameters\n' +
+                '  Date:       ' + c.dateStr + '\n' +
+                '  Time:       ' + String(c.localHour).padStart(2, '0') + ':00 (UTC+' + c.utcOffset + ') / ' + String(c.hour).padStart(2, '0') + ':00 (UTC)\n\n' +
+                'User Input (external calculator)\n' +
+                '  Azimuth:    ' + c.userAzimuth.toFixed(2) + '\u00b0\n' +
+                '  Altitude:   ' + c.userAltitude.toFixed(2) + '\u00b0\n\n' +
+                'SunForm Calculated\n' +
+                '  Azimuth:    ' + c.calcAzimuth.toFixed(2) + '\u00b0\n' +
+                '  Altitude:   ' + c.calcAltitude.toFixed(2) + '\u00b0\n\n' +
+                'Difference\n' +
+                '  Azimuth:    ' + c.diffAz.toFixed(2) + '\u00b0\n' +
+                '  Altitude:   ' + c.diffAlt.toFixed(2) + '\u00b0\n\n' +
+                'Verdict: ' + matchStatus + '\n'
+            );
+
+            window.location.href = 'mailto:sunform@jakewhitearchitecture.com?subject=' + subject + '&body=' + body;
+        }
+
+        // Leaflet must init after DOM is ready
+        // We defer map init to when step 4 (Site Location) opens
+        let mapInitialized = false;
+    </script>
+</body>
+</html>
+```
+
+---
+
+## Git Commit History
+
+### All Commits (143 total, most recent first)
+
+```
+fd200d0 Revert to 382b5a2: restore original voxel display loop before clustering changes
+20d7e14 Revert: remove coplanar clustering and ear-clip helpers, restore original voxel display loop
+5e4b806 Revert "Fix boundary loop winding: directed edge adjacency in traceBoundaryLoops, preserve triangle winding in extractBoundaryEdges"
+5b70ad8 Fix boundary loop winding: directed edge adjacency in traceBoundaryLoops, preserve triangle winding in extractBoundaryEdges
+550f397 Revert "Voxel display: coplanar clustering + boundary extraction + ear-clip triangulation — dissolve internal edges, expose genuine mesh holes"
+a5438a4 Voxel display: coplanar clustering + boundary extraction + ear-clip triangulation — dissolve internal edges, expose genuine mesh holes
+52f7eca Fix voxel display: group clipped triangles by dominant facing direction, render only dominant face per cell
+2c597ab Fix voxel display: cluster triangles by normal, render only dominant face
+e150bb8 Fix voxel display: discard off-normal triangles within each voxel cell
+382b5a2 Fix voxel pipeline: restore vertical wall and sloped roof surfaces by fixing normal filter thresholds and upward bias
+93c1156 Fix ifcos-worker: conservative face culling — only remove exactly-paired interior faces, keep 3+ junction faces
+45a3ee4 Add code.md: complete codebase dump with mesh issue summary
+479aec0 Simplify IfcOpenShell to merge + cull: single outer shell mesh
+0a37481 Wire up ifcos-worker.js: replace inline Pyodide with Web Worker messaging
+9d75d41 Move IfcOpenShell/Pyodide into a Web Worker to avoid blocking the main thread
+14d8025 Fix IfcOpenShell iterator: remove unsupported multiprocessing param in wasm
+e0c3e1c Capture full Python traceback when IfcOpenShell fails
+f54b9f8 Show IfcOpenShell failure reason in debug console when in voxel-only mode
+c1ec70b Fix debug console showing in both voxel-only and dual-geometry modes
+c9d90ed Add per-element mesh healing checks with failure notes in debug console
+e9a9c31 Add geometry debug console with match statistics and magenta unmatched triangles
+7ad0059 Implement dual-geometry architecture: web-ifc for analysis, IfcOpenShell for display
+44a9832 Switch IfcOpenShell to per-element meshes instead of merged mesh
+f312ad7 Add vertex welding and duplicate face removal for continuous mesh
+e451052 Fix normal orientation for pitched and vertical surfaces
+3be7263 Fix coordinate system mismatch and improve normal orientation
+ae5fec7 Fix checkerboard normals: orient per-triangle normals using empty-neighbour reference direction in voxel pipeline (winding-independent)
+c78465d Orient all face normals outward after IfcOpenShell processing
+6ba99d1 Add manifold check and void removal for IfcOpenShell mesh
+426844d Add Pyodide + IfcOpenShell for improved geometry processing
+8a027a9 Prioritise topmost upward-facing layer in voxels with overlapping geometry
+078871f Fix missing pitched roof surfaces and prefer upward normals at edges
+7443875 Fix zero-hour edge cells: remove dot product ray validity check
+1f5a9cc Fix normal flipping: use empty-neighbour directions instead of scene centroid
+9cc7662 Fix missing surfaces: compute world-space centroid and relax normal filter
+0187c10 Add orientation step with 2D screenshot preview
+22c2b51 Replace manual mesh selection with automatic voxel-based sun hours analysis
+2fd7faf Merge pull request #8 from JakeWhiteArchitecture/claude/fix-image-path-production-4BKSA
+6430484 Move north arrow down to avoid overlap with coffee button; remove first disclaimer checkbox
+f595b06 Fix blank PDF: ortho camera frustum should be symmetric around zero
+baf8cc6 Revert heatmap viewport to DoubleSide, only fix normals in GLB export
+27afe07 Fix GLB normals (single-sided upward) and PDF blank page (centre on heatmap)
+c8cadb1 Move Site Location to its own wizard step, grey out Run Analysis until area selected
+3d8cd8a Show UTC offset instead of 'local' in beta feedback email
+a4a613d Fix email showing UTC instead of local time, handle near-horizon altitude %
+21e7475 Add three-tier tolerance: <1% good, 1-2% acceptable, >2% difference
+08c7b02 Change beta feedback tolerance from fixed 2° to 1% threshold
+0d57503 Add mobile slide-out sidebar and scale logo for phone screens
+1359880 Remove jsPDF and Flask from third-party credits list
+ba8c4ea Update bug report email to sunform@jakewhitearchitecture.com
+c241e64 Add clickable SunCalc.org link to beta feedback modal
+3310211 Snap heatmap colors to whole-hour boundaries and add 0.25m grid option
+7c58ea4 Scale legend bar to actual max sun hours across all seasons
+9e60f9e Add interval notch markers to color legend key
+3cca945 Merge pull request #7 from JakeWhiteArchitecture/claude/fix-image-path-production-4BKSA
+06e0dfa Fix results step not opening after analysis completes
+d9c1192 Merge pull request #6 from JakeWhiteArchitecture/claude/fix-image-path-production-4BKSA
+7a8de51 Allow sun analysis on all mesh layers, not just the topmost surface
+eda56d2 Move beta feedback button inside the results step section
+0c60497 Merge pull request #5 from JakeWhiteArchitecture/claude/fix-image-path-production-4BKSA
+8f5e771 Add beta testing feedback wizard for sun position verification
+e5994bf Remove shade emitters step and add orientation check modal
+564cbbd Merge pull request #4 from JakeWhiteArchitecture/claude/fix-image-path-production-4BKSA
+51aad95 Fix logo image paths to use relative URLs for production
+8da7f94 Merge pull request #3 from JakeWhiteArchitecture/claude/sunform-sun-hours-analysis-N62F0
+eb4d57a Add intelligent vertical surface selection in Step 3
+988e375 Fix viewport overlays disappearing on screen shrink
+b36ff23 Restore root index.html as single source, remove templates/ duplicate
+8100f72 Remove duplicate root index.html — Flask serves from templates/
+1fba697 Make viewport overlay layout responsive
+72f0f8e Fix grid cell Z height using highest surface instead of averaging
+444b47b Fix ray lines showing through buildings and coffee button position
+8ab0bb2 Make ray probe panel draggable and add 5/15-min time steps
+1b3cbd4 Add ray probe: click heatmap to see sun ray casting details
+fd1661c Move buy-me-a-coffee button below shortkey notes and above compass
+ce41182 Add Step 4: Exclude Shade Emitters from shadow casting
+b2e5cf4 Disable doubleClickZoom on Leaflet map to fix jump bug
+86898e4 Add index.html to project root for static file serving
+47469c5 Switch Flask to port 8080 for environment compatibility
+b2644be Revert to port 5000 and add Buy Me a Coffee button to viewport
+c0c6389 Change Flask port from 5000 to 8000
+0da4135 Add third-party software credits to disclaimer modal
+f914fab Add left/right arrow keys to cycle between analysed seasons
+2fa3de7 Fix mesh selection after fly-to-orbit transition
+0799350 Preserve camera angle when switching from fly to orbit mode
+4ac28e2 Add Escape key to exit fly mode and return to orbit
+92a076c Smooth fly mode camera look with lerp interpolation
+0df8cfc Add crosshair in fly mode and enable mesh picking from screen centre
+771ce2d Fix fly mode jank and orbit mode target after exiting fly
+dc85fb8 Remove 'No contribution or donation alters these terms' from disclaimer
+b404fec Collapse transparent padding around logo in modal and sidebar
+d8bf1d6 Replace fly mode mouse look with pointer-lock first-person camera
+377f380 Strip logo spacing artifacts — use object-fit and negative margins
+d996114 Reduce gap between tagline and steps panel
+e7af469 Make logo 30% larger and reduce top padding to push content up
+86c9bbb Centre logo, update tagline, compass only on Step 2, N rotates with needle
+0f1738e Update disclaimer text across all locations
+bea3a0c Show confirm/reset buttons after manual rotation
+2bd98b0 Add animation lock to prevent concurrent rotation loops
+304b64a Fix sidebar mousedown events reaching OrbitControls
+3daa605 Prevent sidebar double-clicks from triggering OrbitControls
+3d0ef52 Fix rotation direction, reset input, and always-visible compass
+48a8235 Simplify Step 2: replace edge selection with manual rotation buttons
+15a6c04 Add directional arcs with in-viewport rotation input
+2891971 Replace two-point orientation with single-click edge selection
+71ca309 Add event target guard to viewport click listener
+b62f2fd Add drag-distance guard to prevent spurious orient clicks from drags
+51fcf5e Disable two-point orient after use, add Clear button to re-enable
+a5bd5e6 Fix double-counting of rotation in two-point orientation
+74aa664 Revert to 0°=North azimuth, fix two-point orient math, add smooth animation
+7da076a Fix two-point orientation rotation math
+a1a2708 Fix orientation jump, add (Beta) to title, UI tweaks
+72f9790 Add two-point orientation, fix downloads, update UI
+2e387ca Change azimuth convention to AutoCAD-style, update disclaimer text
+689abaa Remove hours from UI/PDF, enlarge logos, update terms of use
+8ac0b8f Remove mesh hole healing and union step, simplify to normal filter, fix logo path
+f0b813b Merge pull request #2 from JakeWhiteArchitecture/claude/sunform-sun-hours-analysis-N62F0
+8901b32 Add professional role gate, download confirmation, mesh hole healing, logo refs
+1a499eb Fix GLB export and remove dates from season toggle buttons
+416bea8 Add WASD flight mode, cache triangle slicing, fix green accents and mesh visibility
+78c7efd Add disclaimer modal, rebrand theme to gold/teal, hide meshes post-analysis, rework PDF export
+a89936b Harden all tests against false-pass risks identified in critical review
+8f7ab17 Harden tests: fix false-pass risks, add critical accumulation proofs
+b078130 Add accumulation tests mirroring JS shared-array loop structure
+d92835f Fix test imports to work when run standalone from tests/ directory
+b3bd547 Add terrain fix, location picker, seasonal analysis, bug report, unit tests
+0f1cd4a Force cell normals upward after slicing, not before
+17a3e3b Ensure all top-surface face normals point upward before analysis
+a70beab Remove BRE compliance, hide grid, merge+extract top terrain surface
+3f38173 Slice ground mesh along grid lines for clean heatmap tiles
+b6701ae Switch from mesh triangulation to regular grid for sun hours analysis
+86f5623 Allow multiple ground mesh selection in Step 3
+0142226 Replace smooth vertex shading with flat per-face tile overlay
+837c774 Terrain-aware shading with stepped sidebar workflow
+299e4f6 Add BVH acceleration structure for 50-100x faster ray casting
+183f5de Merge pull request #1 from JakeWhiteArchitecture/claude/sunform-sun-hours-analysis-N62F0
+e752c39 Move entire analysis pipeline to client-side — zero backend dependencies
+95aa9ec Fix web-ifc WASM memory: copy vertex/index arrays before delete, use Uint32 index buffer
+826be46 Switch IFC parsing from backend ifcopenshell to client-side web-ifc + GLB pipeline
+f8cc11b Add rtree to requirements.txt (trimesh ray casting dependency)
+b8dbaff Transform StairSmith into SUNFORM — sun hours analysis tool for BRE BR209 compliance
+2908cb0 Add files via upload
+b7cb758 Initial commit
+```
diff --git a/ifcos-worker.js b/ifcos-worker.js
new file mode 100644
index 0000000..2ed22ac
--- /dev/null
+++ b/ifcos-worker.js
@@ -0,0 +1,237 @@
+/*
+ * Web Worker for Pyodide + IfcOpenShell geometry processing.
+ *
+ * Merges all IFC element geometry into a single mesh and culls
+ * duplicate/interior faces (shared between adjacent elements).
+ *
+ * Protocol (postMessage):
+ *   Main → Worker:
+ *     { type: 'init' }                          — start loading Pyodide + IfcOpenShell
+ *     { type: 'process', buffer: ArrayBuffer }   — merge geometry from IFC file
+ *
+ *   Worker → Main:
+ *     { type: 'status',  msg: string }
+ *     { type: 'ready' }
+ *     { type: 'result',  vBuf: ArrayBuffer, fBuf: ArrayBuffer, nv: N, nf: N, stats: {...} }
+ *     { type: 'error',   error: string }
+ */
+
+importScripts('https://cdn.jsdelivr.net/pyodide/v0.26.2/full/pyodide.js');
+
+let pyodide = null;
+
+async function init() {
+    if (pyodide) return;
+
+    postMessage({ type: 'status', msg: 'Loading Python runtime...' });
+
+    pyodide = await loadPyodide({
+        indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.26.2/full/'
+    });
+
+    postMessage({ type: 'status', msg: 'Installing IfcOpenShell...' });
+    await pyodide.loadPackage('micropip');
+    await pyodide.runPythonAsync(`
+import micropip
+await micropip.install("https://ifcopenshell.github.io/wasm-wheels/ifcopenshell-0.8.2+d50e806-cp312-cp312-emscripten_3_1_58_wasm32.whl")
+import ifcopenshell
+import ifcopenshell.geom
+print("IfcOpenShell", ifcopenshell.version, "loaded successfully")
+`);
+
+    postMessage({ type: 'ready' });
+}
+
+async function processIFC(buffer) {
+    await init();
+
+    postMessage({ type: 'status', msg: 'Extracting geometry with IfcOpenShell...' });
+
+    const uint8 = new Uint8Array(buffer);
+    pyodide.globals.set('ifc_bytes', uint8);
+
+    await pyodide.runPythonAsync(`
+import traceback as _tb
+try:
+    import ifcopenshell
+    import ifcopenshell.geom
+    import struct
+    import math
+
+    ifc_data = bytes(ifc_bytes.to_py())
+    tmp_path = '/tmp/model.ifc'
+    with open(tmp_path, 'wb') as f:
+        f.write(ifc_data)
+
+    model = ifcopenshell.open(tmp_path)
+    elem_count = len(model.by_type('IfcProduct'))
+    print(f"IFC schema: {model.schema}, elements: {elem_count}")
+
+    settings = ifcopenshell.geom.settings()
+    settings.set(settings.USE_WORLD_COORDS, True)
+
+    iterator = ifcopenshell.geom.iterator(settings, model)
+
+    # ── Step 1: Collect all verts and faces from all elements ──
+    all_verts = []   # flat list of floats (x,y,z,x,y,z,...)
+    all_faces = []   # flat list of ints (i0,i1,i2,...)
+    vert_offset = 0
+    elem_processed = 0
+
+    if iterator.initialize():
+        while True:
+            shape = iterator.get()
+            geom = shape.geometry
+            verts = geom.verts
+            faces = geom.faces
+            n_verts = len(verts) // 3
+            n_faces = len(faces) // 3
+
+            if n_verts > 0 and n_faces > 0:
+                all_verts.extend(verts)
+                # Offset face indices by current vertex count
+                all_faces.extend(f + vert_offset for f in faces)
+                vert_offset += n_verts
+                elem_processed += 1
+
+            if not iterator.next():
+                break
+
+    total_verts = vert_offset
+    total_faces_before = len(all_faces) // 3
+    print(f"Collected {elem_processed} elements: {total_verts} verts, {total_faces_before} faces")
+
+    # ── Step 2: Deduplicate vertices (snap to grid) ──
+    # Round vertex positions to merge coincident vertices from different elements
+    SNAP = 1e-4  # 0.1mm tolerance
+    inv_snap = 1.0 / SNAP
+    vertex_map = {}   # (rx, ry, rz) -> new_index
+    old_to_new = [0] * total_verts
+    new_verts = []
+    new_idx = 0
+
+    for i in range(total_verts):
+        x = all_verts[i*3]
+        y = all_verts[i*3+1]
+        z = all_verts[i*3+2]
+        key = (round(x * inv_snap), round(y * inv_snap), round(z * inv_snap))
+        if key in vertex_map:
+            old_to_new[i] = vertex_map[key]
+        else:
+            vertex_map[key] = new_idx
+            old_to_new[i] = new_idx
+            new_verts.extend([x, y, z])
+            new_idx += 1
+
+    print(f"Vertex dedup: {total_verts} -> {new_idx}")
+
+    # Remap face indices
+    remapped_faces = [old_to_new[fi] for fi in all_faces]
+
+    # ── Step 3: Cull duplicate faces (interior faces shared between elements) ──
+    # A face shared by two elements appears twice with opposite winding.
+    # We detect faces with the same sorted vertex indices and remove ALL copies
+    # (both sides of interior face).
+    face_count = {}  # sorted tuple -> list of face indices
+    for f in range(total_faces_before):
+        i0 = remapped_faces[f*3]
+        i1 = remapped_faces[f*3+1]
+        i2 = remapped_faces[f*3+2]
+        # Skip degenerate faces
+        if i0 == i1 or i1 == i2 or i0 == i2:
+            continue
+        key = tuple(sorted([i0, i1, i2]))
+        if key not in face_count:
+            face_count[key] = []
+        face_count[key].append(f)
+
+    # Keep only faces that appear exactly once (outer shell)
+    final_faces = []
+    interior_removed = 0
+    for key, indices in face_count.items():
+        if len(indices) == 1:
+            f = indices[0]
+            final_faces.extend([remapped_faces[f*3], remapped_faces[f*3+1], remapped_faces[f*3+2]])
+        elif len(indices) == 2:
+            interior_removed += 2  # true interior face — remove both sides
+        else:
+            # 3+ faces sharing this vertex key: complex junction, keep all copies
+            for f in indices:
+                final_faces.extend([remapped_faces[f*3], remapped_faces[f*3+1], remapped_faces[f*3+2]])
+
+    total_faces_after = len(final_faces) // 3
+    print(f"Face cull: {total_faces_before} -> {total_faces_after} (removed {interior_removed} interior faces)")
+
+    # ── Step 4: Pack into binary buffers ──
+    _vb = struct.pack(f'{len(new_verts)}f', *new_verts)
+    _fb = struct.pack(f'{len(final_faces)}I', *final_faces)
+    _nv = new_idx
+    _nf = total_faces_after
+    _stats = {
+        'elements': elem_processed,
+        'verts_before': total_verts,
+        'verts_after': new_idx,
+        'faces_before': total_faces_before,
+        'faces_after': total_faces_after,
+        'interior_removed': interior_removed,
+    }
+    _error = None
+
+except Exception as e:
+    _vb = b''
+    _fb = b''
+    _nv = 0
+    _nf = 0
+    _stats = {}
+    _error = _tb.format_exc()
+    print("IfcOpenShell error:", _error)
+`);
+
+    const error = pyodide.globals.get('_error');
+    if (error) {
+        postMessage({ type: 'error', error: String(error) });
+        return;
+    }
+
+    const nv = pyodide.globals.get('_nv');
+    const nf = pyodide.globals.get('_nf');
+
+    // Pull stats
+    const pyStats = pyodide.globals.get('_stats');
+    const stats = pyStats.toJs();
+    pyStats.destroy();
+
+    // Pull binary buffers
+    const vbPy = pyodide.globals.get('_vb');
+    const fbPy = pyodide.globals.get('_fb');
+    const vbRaw = vbPy.toJs();
+    const fbRaw = fbPy.toJs();
+    vbPy.destroy();
+    fbPy.destroy();
+
+    // Create aligned ArrayBuffers
+    const vBuf = new ArrayBuffer(vbRaw.length);
+    new Uint8Array(vBuf).set(vbRaw);
+    const fBuf = new ArrayBuffer(fbRaw.length);
+    new Uint8Array(fBuf).set(fbRaw);
+
+    // Clean up Python globals
+    pyodide.runPython('del _vb, _fb, _nv, _nf, _stats, _error');
+
+    postMessage(
+        { type: 'result', vBuf, fBuf, nv, nf, stats: Object.fromEntries(stats) },
+        [vBuf, fBuf]
+    );
+}
+
+onmessage = async (e) => {
+    try {
+        if (e.data.type === 'init') {
+            await init();
+        } else if (e.data.type === 'process') {
+            await processIFC(e.data.buffer);
+        }
+    } catch (err) {
+        postMessage({ type: 'error', error: String(err) });
+    }
+};
diff --git a/index.html b/index.html
index 3b6ccc3..0aa9f2d 100644
--- a/index.html
+++ b/index.html
@@ -289,11 +289,67 @@
             line-height: 1;
         }
 
+        /* ─── DEBUG CONSOLE ─── */
+        .debug-console {
+            display: none;
+            position: absolute;
+            bottom: 10px;
+            left: 10px;
+            z-index: 30;
+            background: rgba(0,0,0,0.88);
+            color: #ccc;
+            font-family: 'Courier New', monospace;
+            font-size: 11px;
+            border-radius: 6px;
+            max-width: 520px;
+            max-height: 460px;
+            overflow-y: auto;
+            padding: 0;
+            border: 1px solid #444;
+        }
+        .debug-console.visible { display: block; }
+        .debug-header {
+            display: flex;
+            justify-content: space-between;
+            align-items: center;
+            padding: 4px 8px;
+            background: rgba(255,255,255,0.08);
+            border-bottom: 1px solid #444;
+            cursor: pointer;
+            user-select: none;
+        }
+        .debug-header span { font-weight: 700; color: #E5A50A; }
+        .debug-body { padding: 6px 8px; }
+        .debug-body table { width: 100%; border-collapse: collapse; }
+        .debug-body td { padding: 1px 4px; }
+        .debug-body td:first-child { color: #888; white-space: nowrap; }
+        .debug-body td:last-child { color: #eee; text-align: right; }
+        .debug-section { margin-top: 6px; padding-top: 4px; border-top: 1px solid #333; }
+        .debug-section-title { color: #E5A50A; font-weight: 700; margin-bottom: 2px; }
+        .debug-ok { color: #4CAF50; }
+        .debug-warn { color: #FFC107; }
+        .debug-err { color: #ff6b6b; }
+        .debug-toggle-btn {
+            position: absolute;
+            bottom: 10px;
+            left: 10px;
+            z-index: 31;
+            background: rgba(0,0,0,0.7);
+            color: #E5A50A;
+            border: 1px solid #555;
+            border-radius: 4px;
+            padding: 3px 8px;
+            font-size: 10px;
+            cursor: pointer;
+            font-family: monospace;
+        }
+        .debug-toggle-btn:hover { background: rgba(255,255,255,0.15); }
+
         /* ─── NORTH ARROW OVERLAY ─── */
         .north-arrow {
             display: none;
             position: absolute;
-            top: 50px;
+            top: 90px;
             right: 20px;
             z-index: 10;
             text-align: center;
@@ -307,6 +363,27 @@
             height: 50px;
         }
 
+        /* ─── ORIENTATION PREVIEW OVERLAY ─── */
+        .orient-preview-container {
+            display: none;
+            position: absolute;
+            top: 0; left: 0; right: 0; bottom: 0;
+            z-index: 8;
+            background: rgba(11, 19, 43, 0.92);
+            justify-content: center;
+            align-items: center;
+            overflow: hidden;
+        }
+        .orient-preview-container.visible {
+            display: flex;
+        }
+        #orient-preview {
+            max-width: 85%;
+            max-height: 85%;
+            transition: transform 0.3s ease;
+            image-rendering: auto;
+        }
+
         /* ─── BOUNDING BOX MODE INDICATOR ─── */
         .bbox-overlay {
             display: none;
@@ -329,25 +406,6 @@
         .bbox-overlay .bbox-coords { color: #00CFC8; font-size: 12px; margin-top: 4px; font-family: monospace; }
 
         .viewport.drawing-bbox { cursor: crosshair; }
-        .viewport.picking-mesh { cursor: crosshair; }
-
-        /* ─── PICKING OVERLAY ─── */
-        .pick-overlay {
-            display: none;
-            position: absolute;
-            top: 10px;
-            left: 10px;
-            z-index: 5;
-            background: rgba(22, 33, 62, 0.95);
-            padding: 10px 14px;
-            border-radius: 6px;
-            font-size: 12px;
-            line-height: 1.6;
-            border: 1px solid #00CFC8;
-            min-width: 200px;
-        }
-
-        .pick-overlay.visible { display: block; }
 
         /* ─── STATUS OVERLAY ─── */
         .status-overlay {
@@ -400,6 +458,23 @@
             );
             position: relative;
         }
+        .legend-notch {
+            position: absolute;
+            right: -1px;
+            height: 1px;
+            background: rgba(255, 255, 255, 0.6);
+            pointer-events: none;
+        }
+        .legend-notch.hour {
+            width: 8px;
+            height: 1.5px;
+            background: rgba(255, 255, 255, 0.85);
+        }
+        .legend-notch.sub-hour {
+            width: 4px;
+            height: 1px;
+            background: rgba(255, 255, 255, 0.45);
+        }
 
         /* ─── RAY PROBE PANEL ─── */
         .ray-probe-panel {
@@ -604,14 +679,6 @@
         }
         .bug-report a:hover { color: #D4880F; text-decoration: underline; }
 
-        /* ─── SELECTED MESH INDICATOR ─── */
-        .selected-mesh-name {
-            font-size: 12px;
-            color: #00CFC8;
-            margin: 6px 0;
-            font-family: monospace;
-        }
-
         /* ─── DISCLAIMER MODAL ─── */
         .modal-overlay {
             position: fixed;
@@ -850,6 +917,43 @@
             backdrop-filter: blur(4px);
         }
 
+        /* ─── HAMBURGER MENU BUTTON ─── */
+        .hamburger-btn {
+            display: none;
+            position: fixed;
+            top: 12px;
+            left: 12px;
+            z-index: 1001;
+            width: 40px;
+            height: 40px;
+            align-items: center;
+            justify-content: center;
+            background: #16213e;
+            border: 1px solid #0f3460;
+            border-radius: 6px;
+            cursor: pointer;
+            flex-direction: column;
+            gap: 5px;
+            padding: 8px;
+        }
+        .hamburger-btn span {
+            display: block;
+            width: 22px;
+            height: 2px;
+            background: #D4880F;
+            border-radius: 1px;
+            transition: transform 0.3s ease, opacity 0.3s ease;
+        }
+        .hamburger-btn.active span:nth-child(1) {
+            transform: rotate(45deg) translate(5px, 5px);
+        }
+        .hamburger-btn.active span:nth-child(2) {
+            opacity: 0;
+        }
+        .hamburger-btn.active span:nth-child(3) {
+            transform: rotate(-45deg) translate(5px, -5px);
+        }
+
         /* ─── RESPONSIVE ─── */
         @media (max-width: 900px) {
             .panel {
@@ -889,18 +993,40 @@
 
         @media (max-width: 550px) {
             body {
-                flex-direction: column;
+                flex-direction: row;
             }
             .panel {
-                width: 100%;
+                position: fixed;
+                top: 0;
+                left: 0;
+                bottom: 0;
+                width: 85vw;
+                max-width: 340px;
                 min-width: unset;
-                max-height: 40vh;
-                border-right: none;
-                border-bottom: 1px solid #0f3460;
+                max-height: none;
+                border-right: 1px solid #0f3460;
+                border-bottom: none;
+                z-index: 1000;
+                transform: translateX(-100%);
+                transition: transform 0.3s ease;
+            }
+            .panel.open {
+                transform: translateX(0);
+            }
+            .panel-backdrop {
+                display: none;
+                position: fixed;
+                top: 0; left: 0; right: 0; bottom: 0;
+                background: rgba(0,0,0,0.5);
+                z-index: 999;
+            }
+            .panel-backdrop.visible {
+                display: block;
             }
             .viewport {
                 flex: 1;
                 min-height: 0;
+                width: 100%;
             }
             .viewport-info {
                 font-size: 8px;
@@ -914,6 +1040,18 @@
             .season-switcher {
                 top: 6px;
             }
+            .hamburger-btn {
+                display: flex;
+            }
+            .logo-img {
+                width: 80%;
+                max-height: 160px;
+                margin: -10px auto -30px auto;
+            }
+            .modal-logo {
+                max-width: 220px;
+                margin: -10px auto -20px auto;
+            }
         }
 
     </style>
@@ -922,7 +1060,7 @@
     <!-- ─── DISCLAIMER MODAL ─── -->
     <div class="modal-overlay" id="disclaimer-modal">
         <div class="modal-box">
-            <img src="/sunform-logo.png" alt="SunForm" class="modal-logo">
+            <img src="sunform-logo.png" alt="SunForm" class="modal-logo">
             <h2>SunForm &mdash; Terms of Use</h2>
 
             <div id="disclaimer-terms">
@@ -942,8 +1080,6 @@
                     <li><strong style="color:#bbb;">Three.js</strong> (r128) &mdash; 3D rendering &mdash; MIT License &mdash; &copy; Three.js Authors</li>
                     <li><strong style="color:#bbb;">web-ifc</strong> (0.0.57) &mdash; IFC file parsing &mdash; Mozilla Public License 2.0 &mdash; &copy; IFC.js Contributors</li>
                     <li><strong style="color:#bbb;">Leaflet</strong> (1.9.4) &mdash; Interactive maps &mdash; BSD-2-Clause License &mdash; &copy; Volodymyr Agafonkin</li>
-                    <li><strong style="color:#bbb;">jsPDF</strong> (2.5.2) &mdash; PDF generation &mdash; MIT License &mdash; &copy; jsPDF Contributors</li>
-                    <li><strong style="color:#bbb;">Flask</strong> (3.x) &mdash; Python web framework &mdash; BSD-3-Clause License &mdash; &copy; Pallets Projects</li>
                 </ul>
                 <p style="font-size:11px; color:#999; margin-top:8px;">Sun position calculations use the Spencer (1971) algorithm; shadow ray&ndash;triangle intersection uses the M&ouml;ller&ndash;Trumbore algorithm. Both are implemented from published academic sources and carry no third-party licence obligations.</p>
 
@@ -956,14 +1092,10 @@
             <div id="disclaimer-checkboxes">
                 <label class="checkbox-row">
                     <input type="checkbox" id="disclaimer-check1" onchange="updateDisclaimerAccept()">
-                    <span>I understand that SunForm is beta software and outputs may be inaccurate. I will not use them for any formal purpose.</span>
-                </label>
-                <label class="checkbox-row">
-                    <input type="checkbox" id="disclaimer-check2" onchange="updateDisclaimerAccept()">
                     <span>I confirm that I am competent to interpret solar analysis outputs and would be able to identify inconsistencies or errors in the results.</span>
                 </label>
                 <label class="checkbox-row">
-                    <input type="checkbox" id="disclaimer-check3" onchange="updateDisclaimerAccept()">
+                    <input type="checkbox" id="disclaimer-check2" onchange="updateDisclaimerAccept()">
                     <span>I understand that SunForm is not a substitute for professional daylighting consultancy and I will not present its outputs to others as verified analysis.</span>
                 </label>
             </div>
@@ -972,9 +1104,111 @@
         </div>
     </div>
 
-    <div class="panel">
+
+    <!-- ─── BETA FEEDBACK WIZARD MODAL ─── -->
+    <div class="modal-overlay hidden" id="beta-feedback-modal">
+        <div class="modal-box" style="max-width:520px;">
+            <!-- Step 1: Instructions + generated challenge -->
+            <div id="bf-step-1">
+                <h2 style="margin-bottom:12px;">Beta Testing Feedback</h2>
+                <p style="margin-bottom:6px;"><a id="bf-suncalc-link" href="#" target="_blank" rel="noopener" style="color:#00CFC8; text-decoration:underline; font-weight:bold;">Check this result on SunCalc.org &rarr;</a></p>
+                <p style="margin-bottom:14px; color:#aaa; font-size:12px;">Open the link, then compare the Azimuth and Altitude values shown on SunCalc with SunForm's values below.</p>
+
+                <div style="background:#0a1628; border:1px solid #0f3460; border-radius:6px; padding:12px 16px; margin-bottom:14px; font-size:13px;">
+                    <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
+                        <span style="color:#888;">Latitude:</span>
+                        <span id="bf-lat" style="color:#00CFC8; font-family:monospace;"></span>
+                    </div>
+                    <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
+                        <span style="color:#888;">Longitude:</span>
+                        <span id="bf-lng" style="color:#00CFC8; font-family:monospace;"></span>
+                    </div>
+                    <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
+                        <span style="color:#888;">Date:</span>
+                        <span id="bf-date" style="color:#00CFC8; font-family:monospace;"></span>
+                    </div>
+                    <div style="display:flex; justify-content:space-between;">
+                        <span style="color:#888;">Time (local clock):</span>
+                        <span id="bf-time" style="color:#00CFC8; font-family:monospace;"></span>
+                    </div>
+                </div>
+
+                <p style="margin-bottom:10px; font-size:12px;">Enter the values from your chosen calculator:</p>
+                <div style="display:flex; gap:12px; margin-bottom:14px;">
+                    <div style="flex:1;">
+                        <label style="font-size:11px; color:#888; display:block; margin-bottom:3px;">Azimuth (°)</label>
+                        <input type="number" id="bf-user-azimuth" step="0.01" placeholder="e.g. 165.3" style="width:100%; padding:6px 8px; background:#0a1628; border:1px solid #0f3460; color:#e0e0e0; border-radius:4px; font-size:13px;">
+                    </div>
+                    <div style="flex:1;">
+                        <label style="font-size:11px; color:#888; display:block; margin-bottom:3px;">Altitude (°)</label>
+                        <input type="number" id="bf-user-altitude" step="0.01" placeholder="e.g. 42.7" style="width:100%; padding:6px 8px; background:#0a1628; border:1px solid #0f3460; color:#e0e0e0; border-radius:4px; font-size:13px;">
+                    </div>
+                </div>
+
+                <div style="display:flex; gap:10px;">
+                    <button class="btn btn-secondary" onclick="closeBetaFeedback()" style="flex:1;">Cancel</button>
+                    <button class="btn btn-primary" onclick="checkBetaFeedback()" style="flex:1;">Check</button>
+                </div>
+            </div>
+
+            <!-- Step 2: Results comparison -->
+            <div id="bf-step-2" style="display:none;">
+                <h2 style="margin-bottom:12px;">Results Comparison</h2>
+
+                <div style="background:#0a1628; border:1px solid #0f3460; border-radius:6px; padding:12px 16px; margin-bottom:6px; font-size:13px;">
+                    <div style="font-size:11px; color:#888; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px;">Your Input (external calculator)</div>
+                    <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
+                        <span style="color:#888;">Azimuth:</span>
+                        <span id="bf-user-az-result" style="color:#e0e0e0; font-family:monospace;"></span>
+                    </div>
+                    <div style="display:flex; justify-content:space-between;">
+                        <span style="color:#888;">Altitude:</span>
+                        <span id="bf-user-alt-result" style="color:#e0e0e0; font-family:monospace;"></span>
+                    </div>
+                </div>
+
+                <div style="background:#0a1628; border:1px solid #0f3460; border-radius:6px; padding:12px 16px; margin-bottom:6px; font-size:13px;">
+                    <div style="font-size:11px; color:#888; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px;">SunForm Calculated</div>
+                    <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
+                        <span style="color:#888;">Azimuth:</span>
+                        <span id="bf-calc-az-result" style="color:#00CFC8; font-family:monospace;"></span>
+                    </div>
+                    <div style="display:flex; justify-content:space-between;">
+                        <span style="color:#888;">Altitude:</span>
+                        <span id="bf-calc-alt-result" style="color:#00CFC8; font-family:monospace;"></span>
+                    </div>
+                </div>
+
+                <div style="background:#0a1628; border:1px solid #0f3460; border-radius:6px; padding:12px 16px; margin-bottom:14px; font-size:13px;">
+                    <div style="font-size:11px; color:#888; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px;">Difference</div>
+                    <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
+                        <span style="color:#888;">Azimuth:</span>
+                        <span id="bf-diff-az" style="font-family:monospace;"></span>
+                    </div>
+                    <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
+                        <span style="color:#888;">Altitude:</span>
+                        <span id="bf-diff-alt" style="font-family:monospace;"></span>
+                    </div>
+                    <div id="bf-verdict" style="text-align:center; font-size:13px; font-weight:bold; padding:6px; border-radius:4px;"></div>
+                </div>
+
+                <div style="display:flex; gap:10px;">
+                    <button class="btn btn-secondary" onclick="closeBetaFeedback()" style="flex:1;">Close</button>
+                    <button class="btn btn-primary" onclick="sendBetaFeedback()" style="flex:1;">Send Feedback</button>
+                </div>
+            </div>
+        </div>
+    </div>
+
+    <!-- ─── MOBILE HAMBURGER & BACKDROP ─── -->
+    <button class="hamburger-btn" id="hamburger-btn" onclick="toggleMobilePanel()">
+        <span></span><span></span><span></span>
+    </button>
+    <div class="panel-backdrop" id="panel-backdrop" onclick="closeMobilePanel()"></div>
+
+    <div class="panel" id="main-panel">
       <div class="panel-scroll">
-        <img src="/sunform-logo.png" alt="SunForm" class="logo-img">
+        <img src="sunform-logo.png" alt="SunForm" class="logo-img">
         <p class="subtitle" style="text-align:center;">A free sun hours web tool (Beta)</p>
 
         <!-- STEP 1: IMPORT -->
@@ -997,78 +1231,69 @@
                 <div class="progress-bar" id="upload-progress">
                     <div class="progress-fill" style="width: 100%;"></div>
                 </div>
+                <div id="ifcos-status" style="display:none; font-size:10px; color:#aaa; margin-top:6px; padding:2px 4px;"></div>
             </div>
         </div>
 
-        <!-- STEP 2: CONFIRM ORIENTATION -->
+        <!-- STEP 2: SET ORIENTATION -->
         <div class="step upcoming" id="step-2" onclick="openStep(2)">
             <div class="step-header">
                 <div class="step-number">2</div>
-                <div class="step-title">Confirm Orientation</div>
+                <div class="step-title">Set Orientation</div>
                 <span class="step-check">&#10003;</span>
                 <span class="step-summary" id="step2-summary"></span>
             </div>
             <div class="step-body">
-                <button class="btn btn-primary" onclick="event.stopPropagation(); confirmOrientation();" style="margin-bottom:8px;">Confirm Orientation</button>
-                <button class="btn btn-secondary" id="orient-manual-btn" onclick="event.stopPropagation(); toggleManualOrient();">Set Orientation Manually</button>
-                <div id="orient-manual-panel" style="display:none; margin-top:10px;">
-                    <div style="display:flex; align-items:center; gap:4px;">
-                        <button class="btn btn-secondary" onclick="event.stopPropagation(); applyManualRotation(1);" style="margin-top:0; padding:4px 10px; font-size:16px;">&#x2190;</button>
-                        <input type="number" id="north-rotation" value="0" step="5" style="width:70px; text-align:center;">
-                        <button class="btn btn-secondary" onclick="event.stopPropagation(); applyManualRotation(-1);" style="margin-top:0; padding:4px 10px; font-size:16px;">&#x2192;</button>
-                        <span class="unit" style="margin-left:2px;">&deg;</span>
-                    </div>
+                <div style="font-size:11px; color:#aaa; margin-bottom:8px;">Rotate the plan so that <b>North is up</b>. Use the arrows or type degrees.</div>
+                <div style="display:flex; align-items:center; gap:6px; margin-bottom:10px;">
+                    <button class="btn btn-secondary" onclick="event.stopPropagation(); applyManualRotation(1);" style="margin-top:0; padding:4px 12px; font-size:16px;">&#x2190;</button>
+                    <input type="number" id="north-rotation" value="5" step="5" min="1" max="180" style="width:60px; text-align:center;">
+                    <button class="btn btn-secondary" onclick="event.stopPropagation(); applyManualRotation(-1);" style="margin-top:0; padding:4px 12px; font-size:16px;">&#x2192;</button>
+                    <span class="unit" style="margin-left:2px;">&deg;</span>
                 </div>
-                <div id="orient-post-rotation" style="display:none; margin-top:8px;">
-                    <button class="btn btn-primary" onclick="event.stopPropagation(); confirmOrientation();" style="margin-bottom:8px;">Confirm Orientation</button>
-                    <button class="btn btn-secondary" onclick="event.stopPropagation(); resetOrientation();">Reset</button>
+                <div style="display:flex; gap:8px;">
+                    <button class="btn btn-primary" onclick="event.stopPropagation(); confirmOrientation();" style="flex:1;">Confirm Orientation</button>
+                    <button class="btn btn-secondary" onclick="event.stopPropagation(); resetOrientation();" style="flex:0;">Reset</button>
                 </div>
             </div>
         </div>
 
-        <!-- STEP 3: SELECT GROUND MESH -->
+        <!-- STEP 3: SITE LOCATION -->
         <div class="step upcoming" id="step-3" onclick="openStep(3)">
             <div class="step-header">
                 <div class="step-number">3</div>
-                <div class="step-title">Select Analysis Surfaces</div>
+                <div class="step-title">Site Location</div>
                 <span class="step-check">&#10003;</span>
                 <span class="step-summary" id="step3-summary"></span>
             </div>
             <div class="step-body">
-                <p class="hint">Click ground or roof surfaces to select the whole mesh. Click vertical walls to select coplanar faces. Double-click a vertical surface to select or deselect all faces on that mesh.</p>
-                <div class="selected-mesh-name" id="selected-mesh-name">No meshes selected</div>
-                <div id="ground-suggestions" style="margin-bottom:8px;"></div>
-                <button class="btn btn-primary" id="confirm-ground-btn" onclick="event.stopPropagation(); confirmGroundMesh();" disabled>Confirm Selection</button>
+                <input type="text" class="location-search" id="location-search" placeholder="Search place name or postcode..." autocomplete="off">
+                <div class="location-map" id="location-map"></div>
+                <div class="field-row">
+                    <div class="field">
+                        <label>Latitude</label>
+                        <input type="number" id="latitude" value="51.5074" min="-90" max="90" step="0.0001">
+                    </div>
+                    <div class="field">
+                        <label>Longitude</label>
+                        <input type="number" id="longitude" value="-0.1278" min="-180" max="180" step="0.0001">
+                    </div>
+                </div>
+                <button class="btn btn-primary" onclick="event.stopPropagation(); confirmSiteLocation();" style="margin-top:10px;">Confirm Location</button>
             </div>
         </div>
 
-        <!-- STEP 4: EXCLUDE SHADE EMITTERS -->
+        <!-- STEP 4: DEFINE ANALYSIS AREA -->
         <div class="step upcoming" id="step-4" onclick="openStep(4)">
             <div class="step-header">
                 <div class="step-number">4</div>
-                <div class="step-title">Exclude Shade Emitters</div>
-                <span class="step-check">&#10003;</span>
-                <span class="step-summary" id="step4-summary"></span>
-            </div>
-            <div class="step-body">
-                <p class="hint">All non-ground meshes cast shadows by default. Click on any mesh in the 3D view to exclude it from shadow casting (e.g. space volumes). Click again to re-include.</p>
-                <div class="selected-mesh-name" id="excluded-emitters-label">0 meshes excluded</div>
-                <div id="shade-emitter-list" style="max-height:120px; overflow-y:auto; margin-bottom:8px; font-size:11px; color:#aaa;"></div>
-                <button class="btn btn-primary" id="confirm-emitters-btn" onclick="event.stopPropagation(); confirmShadeEmitters();">Confirm Shade Emitters</button>
-            </div>
-        </div>
-
-        <!-- STEP 5: DEFINE ANALYSIS AREA -->
-        <div class="step upcoming" id="step-5" onclick="openStep(5)">
-            <div class="step-header">
-                <div class="step-number">5</div>
                 <div class="step-title">Define Analysis Area</div>
                 <span class="step-check">&#10003;</span>
-                <span class="step-summary" id="step5-summary"></span>
+                <span class="step-summary" id="step4-summary"></span>
             </div>
             <div class="step-body">
                 <div style="display:flex; gap:8px; margin-bottom:10px;">
-                    <button class="btn btn-secondary" id="use-entire-btn" onclick="event.stopPropagation(); useEntireMesh();" style="flex:1; margin-top:0;">Use Entire Mesh</button>
+                    <button class="btn btn-secondary" id="use-entire-btn" onclick="event.stopPropagation(); useEntireScene();" style="flex:1; margin-top:0;">Analyse Entire Scene</button>
                     <button class="btn btn-secondary" id="bbox-btn" onclick="event.stopPropagation(); toggleBboxMode();" style="flex:1; margin-top:0;">Draw Bounding Box</button>
                 </div>
                 <div class="field-row" id="bbox-fields" style="display:none;">
@@ -1096,6 +1321,7 @@
                     <div class="field">
                         <label>Grid Resolution <span class="unit">m</span></label>
                         <select id="grid_resolution">
+                            <option value="0.25">0.25 m</option>
                             <option value="0.5">0.5 m</option>
                             <option value="1" selected>1 m</option>
                             <option value="2">2 m</option>
@@ -1104,20 +1330,6 @@
                 </div>
                 <div style="font-size:11px; color:#666; margin-bottom:8px;">Smaller grid = more detail but slower analysis.</div>
                 <hr style="border-color:#0f3460; margin:12px 0;">
-                <label style="font-size:12px; color:#aaa; margin-bottom:3px; display:block;">Site Location</label>
-                <input type="text" class="location-search" id="location-search" placeholder="Search place name or postcode..." autocomplete="off">
-                <div class="location-map" id="location-map"></div>
-                <div class="field-row">
-                    <div class="field">
-                        <label>Latitude</label>
-                        <input type="number" id="latitude" value="51.5074" min="-90" max="90" step="0.0001">
-                    </div>
-                    <div class="field">
-                        <label>Longitude</label>
-                        <input type="number" id="longitude" value="-0.1278" min="-180" max="180" step="0.0001">
-                    </div>
-                </div>
-                <hr style="border-color:#0f3460; margin:12px 0;">
                 <label style="font-size:12px; color:#aaa; margin-bottom:3px; display:block;">Seasons to Analyse</label>
                 <div class="season-toggles">
                     <div class="season-toggle" id="season-winter" onclick="toggleSeason('winter')">Winter</div>
@@ -1136,17 +1348,18 @@
                         </select>
                     </div>
                 </div>
-                <button class="btn btn-run" id="run-btn" onclick="event.stopPropagation(); runAnalysis();">Run Analysis</button>
+                <div id="run-btn-hint" style="font-size:11px; color:#666; margin-bottom:6px;">Select analysis area method above to enable.</div>
+                <button class="btn btn-run" id="run-btn" onclick="event.stopPropagation(); runAnalysis();" disabled style="opacity:0.4; cursor:not-allowed;">Run Analysis</button>
             </div>
         </div>
 
-        <!-- STEP 6: RESULTS -->
-        <div class="step upcoming" id="step-6" onclick="openStep(6)">
+        <!-- STEP 5: RESULTS -->
+        <div class="step upcoming" id="step-5" onclick="openStep(5)">
             <div class="step-header">
-                <div class="step-number">6</div>
+                <div class="step-number">5</div>
                 <div class="step-title">Results</div>
                 <span class="step-check">&#10003;</span>
-                <span class="step-summary" id="step6-summary"></span>
+                <span class="step-summary" id="step5-summary"></span>
             </div>
             <div class="step-body">
                 <div class="results-panel visible" id="results-panel">
@@ -1161,6 +1374,7 @@
                 <div class="bug-report">
                     Results look wrong? <a id="bug-report-link" href="#">Report an issue</a>
                 </div>
+                <button class="btn btn-secondary" onclick="event.stopPropagation(); openBetaFeedback();" style="margin-top:10px; width:100%; font-size:11px; padding:6px 14px;">Provide Beta Testing Feedback</button>
             </div>
         </div>
 
@@ -1204,9 +1418,8 @@
                 </svg>
             </div>
         </div>
-        <div class="pick-overlay" id="pick-overlay">
-            <div style="color:#00CFC8; font-weight:600; font-size:11px; text-transform:uppercase; letter-spacing:1px; margin-bottom:4px;">Select Analysis Surfaces</div>
-            <div style="color:#aaa; font-size:12px;">Click surfaces in the 3D view. Double-click vertical walls to select all faces.</div>
+        <div class="orient-preview-container" id="orient-preview-container">
+            <img id="orient-preview" src="" alt="Plan view">
         </div>
         <div class="bbox-overlay" id="bbox-overlay">
             <div class="bbox-title">Bounding Box Tool</div>
@@ -1214,8 +1427,8 @@
             <div class="bbox-coords" id="bbox-coords"></div>
         </div>
         <div class="colour-legend" id="colour-legend">
-            <div class="legend-label">6h+</div>
-            <div class="legend-bar-v">
+            <div class="legend-label" id="legend-top-label">6h+</div>
+            <div class="legend-bar-v" id="legend-bar">
             </div>
             <div class="legend-label">0h</div>
         </div>
@@ -1225,6 +1438,16 @@
             <button class="season-sw-btn" id="sw-summer" onclick="switchVisibleSeason('summer')">Summer</button>
         </div>
         <div class="status-overlay" id="status-overlay" style="display:none;"></div>
+        <button class="debug-toggle-btn" id="debug-toggle" onclick="toggleDebugConsole()">Debug</button>
+        <div class="debug-console" id="debug-console">
+            <div class="debug-header" onclick="toggleDebugConsole()">
+                <span>Geometry Debug Console</span>
+                <span style="color:#888;">x</span>
+            </div>
+            <div class="debug-body" id="debug-body">
+                <em style="color:#666;">Run analysis to see diagnostics...</em>
+            </div>
+        </div>
         <div class="ray-probe-panel" id="ray-probe-panel">
             <div class="probe-title">
                 <span>Sun Ray Probe</span>
@@ -1247,6 +1470,7 @@
     <script src="https://cdn.jsdelivr.net/npm/web-ifc@0.0.57/web-ifc-api-iife.js"></script>
     <!-- jsPDF for client-side PDF export -->
     <script src="https://cdn.jsdelivr.net/npm/jspdf@2.5.2/dist/jspdf.umd.min.js"></script>
+    <!-- IfcOpenShell runs inside ifcos-worker.js (Web Worker) — no main-thread Pyodide needed -->
 
     <script>
         // ─── GLOBAL STATE ───
@@ -1255,13 +1479,7 @@
         let buildingGroup = null;
         let allMeshes = [];         // individual THREE.Mesh objects from IFC
         let allMeshMeta = [];       // { mesh, expressID, ifcType, name } per mesh
-        let selectedGroundMeshes = [];  // array of selected ground THREE.Mesh objects
-        let selectedVerticalFaces = []; // Each entry: { mesh, faceIndices, normal, highlight: THREE.Mesh }
-        let groundHighlights = [];      // cyan wireframe overlays
-        let excludedEmitters = [];      // meshes excluded from shadow casting
-        let emitterHighlights = [];     // red wireframe overlays for excluded emitters
-        let emitterPickMode = false;    // pick mode for step 4 emitter exclusion
-        let shadowBVH = null;       // BVH of all meshes EXCEPT ground & excluded
+        let shadowBVH = null;       // BVH of all scene geometry for shadow casting
         let heatmapGroup = null;
         let bboxHelper = null;
         let groundPlane = null;
@@ -1269,11 +1487,14 @@
         let ifcLoaded = false;
         let lastAnalysisResults = null;
         let currentStep = 1;
-        let pickMode = false;
-        let useEntireGroundMesh = true;
-        let northRotationDeg = 0;
-        let rotationAnimFrame = null;
+        let useEntireBounds = true;
         let modelRotationGroup = null;
+        let northRotationDeg = 0;
+        let ifcosWorker = null;      // Web Worker for Pyodide + IfcOpenShell
+        let ifcosWorkerReady = false;
+        let analysisMeshes = [];    // IfcOpenShell-processed meshes for voxel/BVH (falls back to allMeshes)
+        let meshHealingNotes = [];  // Debug notes about mesh issues found during IfcOpenShell processing
+        let lastIFCArrayBuffer = null;  // Raw IFC bytes for IfcOpenShell processing
 
         // Season analysis state
         const SEASON_DATES = {
@@ -1433,8 +1654,7 @@
         function openStep(n) {
             const step = document.getElementById('step-' + n);
             if (step.classList.contains('upcoming')) return;
-            // Only allow opening completed steps or current step
-            for (let i = 1; i <= 6; i++) {
+            for (let i = 1; i <= 5; i++) {
                 const s = document.getElementById('step-' + i);
                 if (i === n) {
                     s.classList.add('active');
@@ -1452,34 +1672,32 @@
             }
             currentStep = n;
 
-            // Step-specific modes
-            if (n === 2) { switchToOrtho(); }
-            else switchToPersp();
-            setPickMode(n === 3);
-            setEmitterPickMode(n === 4);
-            if (n !== 6) clearRayProbe();
+            switchToPersp();
+            if (n !== 5) clearRayProbe();
 
-            // Show compass only during orientation step
-            document.getElementById('north-arrow').style.display = (n === 2) ? 'block' : 'none';
+            // Step 2: show orientation preview, lock controls
+            if (n === 2) {
+                showOrientationPreview();
+            } else {
+                hideOrientationPreview();
+            }
 
-            // Mesh visibility: when going back to step 3 or 4 (select/exclude mesh), show meshes
-            // and gray out previous results. On step 6 (results), hide meshes.
-            if ((n === 3 || n === 4) && Object.keys(seasonHeatmaps).length > 0) {
+            // Mesh visibility: gray out on step 4, show results on step 5
+            if (n === 4 && Object.keys(seasonHeatmaps).length > 0) {
                 showCalculationMeshes();
                 grayOutResults();
-            } else if (n === 6) {
+            } else if (n === 5) {
                 hideCalculationMeshes();
                 restoreResults();
-            } else if (n !== 3 && n !== 4) {
-                // For other steps, ensure meshes are visible and results normal
+            } else {
                 showCalculationMeshes();
                 if (Object.keys(seasonHeatmaps).length > 0) {
                     restoreResults();
                 }
             }
 
-            // Lazy-init Leaflet map when step 5 first opens
-            if (n === 5 && !mapInitialized) {
+            // Lazy-init Leaflet map when step 3 (Site Location) first opens
+            if (n === 3 && !mapInitialized) {
                 mapInitialized = true;
                 setTimeout(() => {
                     initLocationMap();
@@ -1496,7 +1714,7 @@
             if (sumEl) sumEl.textContent = summary;
             // Advance to next
             const next = n + 1;
-            if (next <= 6) {
+            if (next <= 5) {
                 const ns = document.getElementById('step-' + next);
                 ns.classList.remove('upcoming');
                 openStep(next);
@@ -1532,39 +1750,41 @@
             seasonResults = {};
             cachedCellData = null;
             cachedGridSize = null;
+            cachedCellMap = null;
+            cachedSliverIndices = null;
             visibleSeason = 'spring';
             document.getElementById('season-switcher').classList.remove('visible');
-            clearAllHighlights();
             removeBboxHelper();
             allMeshes = [];
             allMeshMeta = [];
-            selectedGroundMeshes = [];
-            for (const vf of selectedVerticalFaces) {
-                scene.remove(vf.highlight);
-                vf.highlight.geometry.dispose();
-                vf.highlight.material.dispose();
-            }
-            selectedVerticalFaces = [];
-            excludedEmitters = [];
-            clearEmitterHighlights();
+            analysisMeshes = [];
+            lastIFCArrayBuffer = null;
             shadowBVH = null;
             ifcLoaded = false;
             lastAnalysisResults = null;
-            useEntireGroundMesh = true;
+            useEntireBounds = true;
             northRotationDeg = 0;
+            hideOrientationPreview();
+            document.getElementById('orient-preview').style.transform = 'rotate(0deg)';
+            document.getElementById('north-arrow-rotator').style.transform = 'rotate(0deg)';
             document.getElementById('colour-legend').classList.remove('visible');
             document.getElementById('upload-text').textContent = 'Drop IFC file here or click to browse';
             document.getElementById('upload-filename').style.display = 'none';
             document.getElementById('upload-zone').classList.remove('loaded');
-            document.getElementById('north-rotation').value = '0';
-            document.getElementById('selected-mesh-name').textContent = 'No meshes selected';
-            document.getElementById('excluded-emitters-label').textContent = '0 meshes excluded';
-            document.getElementById('shade-emitter-list').innerHTML = '';
-            document.getElementById('ground-suggestions').innerHTML = '';
+            const ifcosStatusEl = document.getElementById('ifcos-status');
+            if (ifcosStatusEl) { ifcosStatusEl.style.display = 'none'; ifcosStatusEl.style.color = '#aaa'; }
             document.getElementById('bbox-fields').style.display = 'none';
             document.getElementById('bbox-fields2').style.display = 'none';
 
-            for (let i = 1; i <= 6; i++) {
+            // Reset run button to disabled state
+            const runBtn = document.getElementById('run-btn');
+            runBtn.disabled = true;
+            runBtn.style.opacity = '0.4';
+            runBtn.style.cursor = 'not-allowed';
+            const runHint = document.getElementById('run-btn-hint');
+            if (runHint) runHint.style.display = '';
+
+            for (let i = 1; i <= 5; i++) {
                 const s = document.getElementById('step-' + i);
                 s.classList.remove('completed', 'active', 'upcoming');
                 if (i === 1) s.classList.add('active');
@@ -1619,6 +1839,7 @@
 
             try {
                 const arrayBuffer = await file.arrayBuffer();
+                lastIFCArrayBuffer = arrayBuffer;  // Save for IfcOpenShell processing
                 const data = new Uint8Array(arrayBuffer);
                 const modelID = ifcApi.OpenModel(data);
 
@@ -1767,6 +1988,12 @@
 
                 completeStep(1, file.name);
 
+                // Capture top-down screenshot for orientation step
+                setTimeout(() => captureOrientationPreview(), 200);
+
+                // Start IfcOpenShell processing in background
+                processWithIfcOpenShell(arrayBuffer);
+
             } catch (err) {
                 console.error('IFC parse error:', err);
                 progressBar.classList.remove('visible');
@@ -1776,619 +2003,918 @@
             }
         }
 
-        // ─── STEP 2: ORIENTATION ───
-
-        function confirmOrientation() {
-            const summary = northRotationDeg === 0 ? 'North: confirmed' : 'North: rotated ' + (northRotationDeg > 0 ? '+' : '') + northRotationDeg + '\u00b0';
-            completeStep(2, summary);
+        // ─── IFCOPENSHELL VIA WEB WORKER ───
+        function initIfcosWorker() {
+            if (ifcosWorker) return;
+            ifcosWorker = new Worker('/ifcos-worker.js');
+            ifcosWorker.postMessage({ type: 'init' });
+            ifcosWorker.onmessage = (e) => {
+                const d = e.data;
+                if (d.type === 'status') {
+                    showStatus(d.msg);
+                    const statusEl = document.getElementById('ifcos-status');
+                    if (statusEl) { statusEl.textContent = d.msg; statusEl.style.display = 'block'; }
+                } else if (d.type === 'ready') {
+                    ifcosWorkerReady = true;
+                    console.log('IfcOpenShell worker ready');
+                }
+            };
+            ifcosWorker.onerror = (err) => {
+                console.error('IfcOpenShell worker error:', err);
+            };
         }
 
-        // ─── MANUAL ORIENTATION ───
+        async function processWithIfcOpenShell(arrayBuffer) {
+            const statusEl = document.getElementById('ifcos-status');
+            try {
+                if (statusEl) {
+                    statusEl.textContent = 'Loading IfcOpenShell (Web Worker)...';
+                    statusEl.style.display = 'block';
+                }
 
-        function toggleManualOrient() {
-            var panel = document.getElementById('orient-manual-panel');
-            var btn = document.getElementById('orient-manual-btn');
-            if (panel.style.display === 'none') {
-                panel.style.display = '';
-                btn.textContent = 'Hide Manual Controls';
-            } else {
-                panel.style.display = 'none';
-                btn.textContent = 'Set Orientation Manually';
+                // Ensure worker is created
+                if (!ifcosWorker) initIfcosWorker();
+
+                // Send IFC data to worker and wait for result
+                const workerResult = await new Promise((resolve, reject) => {
+                    const handler = (e) => {
+                        const d = e.data;
+                        if (d.type === 'status') {
+                            showStatus(d.msg);
+                            if (statusEl) statusEl.textContent = d.msg;
+                        } else if (d.type === 'ready') {
+                            ifcosWorkerReady = true;
+                            // Worker just finished init, don't resolve yet — wait for result
+                        } else if (d.type === 'result') {
+                            ifcosWorker.onmessage = null;
+                            resolve(d);
+                        } else if (d.type === 'error') {
+                            ifcosWorker.onmessage = null;
+                            reject(new Error(d.error));
+                        }
+                    };
+                    ifcosWorker.onmessage = handler;
+                    // Transfer the buffer to avoid copying
+                    const copy = arrayBuffer.slice(0);
+                    ifcosWorker.postMessage({ type: 'process', buffer: copy }, [copy]);
+                });
+
+                const { vBuf, fBuf, nv, nf, stats } = workerResult;
+
+                console.log(`IfcOpenShell merge+cull:`, stats);
+
+                if (nf === 0) {
+                    console.warn('IfcOpenShell returned no geometry, falling back to web-ifc meshes');
+                    analysisMeshes = [];
+                    if (statusEl) statusEl.textContent = 'IfcOpenShell: no geometry (using web-ifc)';
+                    hideStatus();
+                    return;
+                }
+
+                // Create single merged Three.js mesh (outer shell)
+                if (statusEl) statusEl.textContent = 'Creating merged shell mesh...';
+                await new Promise(r => setTimeout(r, 0));
+
+                analysisMeshes = [];
+                meshHealingNotes = [];
+
+                const verts = new Float32Array(vBuf);
+                const faceIdx = new Uint32Array(fBuf);
+
+                // Convert IFC coordinates (Z-up) to Three.js coordinates (Y-up)
+                for (let i = 0; i < nv; i++) {
+                    const ix = i * 3;
+                    const ifcX = verts[ix], ifcY = verts[ix + 1], ifcZ = verts[ix + 2];
+                    verts[ix]     = ifcX;
+                    verts[ix + 1] = ifcZ;
+                    verts[ix + 2] = -ifcY;
+                }
+
+                const geo = new THREE.BufferGeometry();
+                geo.setAttribute('position', new THREE.BufferAttribute(verts, 3));
+                geo.setIndex(new THREE.BufferAttribute(faceIdx, 1));
+                geo.computeVertexNormals();
+
+                const mat = new THREE.MeshPhongMaterial({
+                    color: 0xdddddd,
+                    flatShading: true,
+                    side: THREE.DoubleSide,
+                    visible: false,
+                });
+
+                const mesh = new THREE.Mesh(geo, mat);
+                mesh.name = 'ifcos_merged_shell';
+                if (modelRotationGroup) {
+                    modelRotationGroup.add(mesh);
+                }
+
+                analysisMeshes.push(mesh);
+
+                if (stats.interior_removed > 0) {
+                    meshHealingNotes.push({ type: 'info', elem: -1,
+                        msg: `Merged ${stats.elements} elements, removed ${stats.interior_removed} interior faces, ` +
+                             `verts ${stats.verts_before} → ${stats.verts_after}, faces ${stats.faces_before} → ${stats.faces_after}` });
+                }
+
+                console.log(`IfcOpenShell: merged shell — ${nv} verts, ${nf} faces (removed ${stats.interior_removed} interior)`);
+
+                if (statusEl) {
+                    statusEl.textContent = `IfcOpenShell: ${nf} faces (${stats.interior_removed} interior removed)`;
+                    statusEl.style.color = '#4CAF50';
+                }
+                hideStatus();
+
+            } catch (err) {
+                console.error('IfcOpenShell processing error:', err);
+                analysisMeshes = [];  // Fall back to web-ifc meshes
+                meshHealingNotes.push({ type: 'error', elem: -1, msg: 'IfcOpenShell FAILED: ' + (err.message || String(err)).substring(0, 200) });
+                if (statusEl) {
+                    statusEl.textContent = 'IfcOpenShell failed: ' + (err.message || String(err)).substring(0, 80);
+                    statusEl.style.color = '#ff6b6b';
+                }
+                hideStatus();
             }
         }
 
-        function applyManualRotation(sign) {
-            var degrees = parseFloat(document.getElementById('north-rotation').value) || 0;
-            if (degrees === 0) return;
-            var targetDeg = northRotationDeg + sign * Math.abs(degrees);
-            while (targetDeg > 180) targetDeg -= 360;
-            while (targetDeg <= -180) targetDeg += 360;
-            targetDeg = Math.round(targetDeg * 10) / 10;
-            animateRotation(targetDeg, 400, function() {
-                document.getElementById('orient-manual-panel').style.display = 'none';
-                document.getElementById('orient-manual-btn').style.display = 'none';
-                document.querySelector('#step-2 .step-body > .btn-primary').style.display = 'none';
-                document.getElementById('orient-post-rotation').style.display = '';
-            });
+        // Get the meshes to use for analysis (prefer IfcOpenShell, fall back to web-ifc)
+        // Analysis always uses web-ifc meshes (robust for voxel pipeline).
+        // IfcOpenShell meshes are used for display only (painted with analysis results).
+        function getAnalysisMeshes() {
+            return allMeshes;
         }
 
-        function resetOrientation() {
-            animateRotation(0, 400, function() {
-                document.getElementById('orient-post-rotation').style.display = 'none';
-                document.getElementById('orient-manual-btn').style.display = '';
-                document.getElementById('orient-manual-btn').textContent = 'Set Orientation Manually';
-                document.getElementById('orient-manual-panel').style.display = 'none';
-                document.getElementById('north-rotation').value = '0';
-                document.querySelector('#step-2 .step-body > .btn-primary').style.display = '';
-            });
+        // ─── DEBUG CONSOLE ───
+
+        function toggleDebugConsole() {
+            const el = document.getElementById('debug-console');
+            el.classList.toggle('visible');
         }
 
-        function animateRotation(targetDeg, duration, onComplete) {
-            if (rotationAnimFrame) cancelAnimationFrame(rotationAnimFrame);
-            duration = duration || 400;
-            const startDeg = northRotationDeg;
-            let delta = targetDeg - startDeg;
-            while (delta > 180) delta -= 360;
-            while (delta <= -180) delta += 360;
-            const endDeg = startDeg + delta;
-            const startTime = performance.now();
-
-            function tick(now) {
-                const t = Math.min((now - startTime) / duration, 1);
-                const eased = t * (2 - t); // ease-out
-                northRotationDeg = startDeg + delta * eased;
-                if (modelRotationGroup) {
-                    modelRotationGroup.rotation.y = northRotationDeg * Math.PI / 180;
-                }
-                document.getElementById('north-arrow-rotator').style.transform = 'rotate(' + (-northRotationDeg) + 'deg)';
-                if (t < 1) {
-                    rotationAnimFrame = requestAnimationFrame(tick);
-                } else {
-                    northRotationDeg = Math.round(endDeg * 10) / 10;
-                    document.getElementById('north-rotation').value = 0;
-                    if (modelRotationGroup) {
-                        modelRotationGroup.rotation.y = northRotationDeg * Math.PI / 180;
-                    }
-                    rotationAnimFrame = null;
-                    if (onComplete) onComplete();
+        function computeBBox(meshes) {
+            const min = [Infinity, Infinity, Infinity];
+            const max = [-Infinity, -Infinity, -Infinity];
+            let totalTris = 0;
+            for (const mesh of meshes) {
+                mesh.updateWorldMatrix(true, false);
+                const wm = mesh.matrixWorld;
+                const pos = mesh.geometry.attributes.position.array;
+                const idx = mesh.geometry.index ? mesh.geometry.index.array : null;
+                const nv = pos.length / 3;
+                totalTris += idx ? idx.length / 3 : nv / 3;
+                const v = new THREE.Vector3();
+                for (let i = 0; i < nv; i++) {
+                    v.set(pos[i*3], pos[i*3+1], pos[i*3+2]).applyMatrix4(wm);
+                    if (v.x < min[0]) min[0] = v.x; if (v.x > max[0]) max[0] = v.x;
+                    if (v.y < min[1]) min[1] = v.y; if (v.y > max[1]) max[1] = v.y;
+                    if (v.z < min[2]) min[2] = v.z; if (v.z > max[2]) max[2] = v.z;
                 }
             }
-            rotationAnimFrame = requestAnimationFrame(tick);
+            return { min, max, tris: totalTris };
         }
 
-        // ─── STEP 3: GROUND MESH PICKING ───
-        function setPickMode(on) {
-            pickMode = on;
-            const viewport = document.getElementById('viewport');
-            const overlay = document.getElementById('pick-overlay');
-            viewport.classList.toggle('picking-mesh', on);
-            overlay.classList.toggle('visible', on);
-        }
-
-        function clearAllHighlights() {
-            for (const hl of groundHighlights) {
-                if (hl.parent) hl.parent.remove(hl);
-                else scene.remove(hl);
-                hl.geometry.dispose();
-                hl.material.dispose();
-            }
-            groundHighlights = [];
-        }
-
-        function addHighlight(mesh) {
-            // Tint the mesh faces to cyan-ish so selection is clearly visible
-            if (!mesh.userData._origColor) {
-                mesh.userData._origColor = mesh.material.color.getHex();
-            }
-            mesh.material = mesh.material.clone();
-            mesh.material.color.setHex(0x00CFC8);
-            mesh.material.opacity = 0.7;
-            mesh.material.transparent = true;
-
-            const edges = new THREE.EdgesGeometry(mesh.geometry, 1);
-            const hl = new THREE.LineSegments(edges,
-                new THREE.LineBasicMaterial({ color: 0x0AF5E3, linewidth: 2 }));
-            hl.position.copy(mesh.position);
-            hl.rotation.copy(mesh.rotation);
-            hl.scale.copy(mesh.scale);
-            hl.userData._groundRef = mesh;
-            if (mesh.parent) {
-                mesh.parent.add(hl);
-            } else {
-                scene.add(hl);
+        function updateDebugConsole(debugData) {
+            const body = document.getElementById('debug-body');
+            if (!body) return;
+
+            const d = debugData;
+            const pct = (v, total) => total > 0 ? (v / total * 100).toFixed(1) + '%' : '0%';
+            const fmt = v => typeof v === 'number' ? v.toLocaleString() : v;
+            const fmtV = (arr) => arr.map(v => v.toFixed(2)).join(', ');
+
+            let html = '';
+
+            // Render mode
+            const mode = d.mode || 'dual-geometry';
+            const modeCls = mode === 'dual-geometry' ? 'debug-ok' : 'debug-warn';
+            html += `<div style="margin-bottom:4px;">Mode: <span class="${modeCls}">${mode}</span></div>`;
+
+            if (mode === 'voxel-only') {
+                html += `<div class="debug-warn" style="margin-bottom:6px;">IfcOpenShell not loaded — using voxel-clipped triangles for display.<br>`;
+                html += `IfcOpenShell Worker: ${ifcosWorker ? (ifcosWorkerReady ? 'ready' : 'loading') : 'not started'}<br>`;
+                // Check for IfcOpenShell error
+                const ifcosErr = meshHealingNotes.find(n => n.msg && n.msg.startsWith('IfcOpenShell FAILED'));
+                if (ifcosErr) {
+                    html += `<span class="debug-err">${ifcosErr.msg}</span><br>`;
+                }
+                const ifcosStatus = document.getElementById('ifcos-status');
+                if (ifcosStatus && ifcosStatus.textContent) {
+                    html += `Status: ${ifcosStatus.textContent}`;
+                }
+                html += `</div>`;
             }
-            groundHighlights.push(hl);
-        }
 
-        function removeHighlight(mesh) {
-            // Restore original mesh colour
-            if (mesh.userData._origColor !== undefined) {
-                mesh.material = mesh.material.clone();
-                mesh.material.color.setHex(mesh.userData._origColor);
-                mesh.material.opacity = 1.0;
-                mesh.material.transparent = false;
+            // Geometry sources
+            html += '<div class="debug-section-title">Geometry Sources</div>';
+            html += '<table>';
+            html += `<tr><td>web-ifc meshes</td><td>${fmt(d.webifcMeshCount)} (${fmt(d.webifcTris)} tris)</td></tr>`;
+            html += `<tr><td>IfcOpenShell meshes</td><td>${fmt(d.ifcosMeshCount)} (${fmt(d.ifcosTris)} tris)</td></tr>`;
+            html += '</table>';
+
+            // Bounding boxes
+            if (d.webifcBBox && d.ifcosBBox) {
+                html += '<div class="debug-section"><div class="debug-section-title">Bounding Boxes (world space)</div>';
+                html += '<table>';
+                html += `<tr><td>web-ifc min</td><td>${fmtV(d.webifcBBox.min)}</td></tr>`;
+                html += `<tr><td>web-ifc max</td><td>${fmtV(d.webifcBBox.max)}</td></tr>`;
+                html += `<tr><td>IfcOS min</td><td>${fmtV(d.ifcosBBox.min)}</td></tr>`;
+                html += `<tr><td>IfcOS max</td><td>${fmtV(d.ifcosBBox.max)}</td></tr>`;
+
+                // Offset between centres
+                const wcx = (d.webifcBBox.min[0] + d.webifcBBox.max[0]) / 2;
+                const wcy = (d.webifcBBox.min[1] + d.webifcBBox.max[1]) / 2;
+                const wcz = (d.webifcBBox.min[2] + d.webifcBBox.max[2]) / 2;
+                const icx = (d.ifcosBBox.min[0] + d.ifcosBBox.max[0]) / 2;
+                const icy = (d.ifcosBBox.min[1] + d.ifcosBBox.max[1]) / 2;
+                const icz = (d.ifcosBBox.min[2] + d.ifcosBBox.max[2]) / 2;
+                const offX = icx - wcx, offY = icy - wcy, offZ = icz - wcz;
+                const dist = Math.sqrt(offX*offX + offY*offY + offZ*offZ);
+                const cls = dist > 1 ? 'debug-err' : dist > 0.1 ? 'debug-warn' : 'debug-ok';
+                html += `<tr><td>Centre offset</td><td class="${cls}">${offX.toFixed(3)}, ${offY.toFixed(3)}, ${offZ.toFixed(3)} (${dist.toFixed(3)}m)</td></tr>`;
+                html += '</table></div>';
             }
 
-            const idx = groundHighlights.findIndex(hl => hl.userData._groundRef === mesh);
-            if (idx === -1) return;
-            const hl = groundHighlights[idx];
-            if (hl.parent) hl.parent.remove(hl);
-            else scene.remove(hl);
-            hl.geometry.dispose();
-            hl.material.dispose();
-            groundHighlights.splice(idx, 1);
-        }
+            // Voxel grid info
+            html += '<div class="debug-section"><div class="debug-section-title">Voxel Grid</div>';
+            html += '<table>';
+            html += `<tr><td>Grid size</td><td>${d.gridSize.toFixed(3)}m</td></tr>`;
+            html += `<tr><td>Voxel cells</td><td>${fmt(d.voxelCellCount)}</td></tr>`;
+            html += '</table></div>';
+
+            // Match statistics
+            html += '<div class="debug-section"><div class="debug-section-title">Triangle → Voxel Mapping</div>';
+            html += '<table>';
+            html += `<tr><td>Total triangles</td><td>${fmt(d.totalDisplayTris)}</td></tr>`;
+            const exactCls = d.exactMatches / d.totalDisplayTris > 0.7 ? 'debug-ok' : 'debug-warn';
+            html += `<tr><td>Exact voxel match</td><td class="${exactCls}">${fmt(d.exactMatches)} (${pct(d.exactMatches, d.totalDisplayTris)})</td></tr>`;
+            html += `<tr><td>Neighbour match</td><td>${fmt(d.neighbourMatches)} (${pct(d.neighbourMatches, d.totalDisplayTris)})</td></tr>`;
+            const missCls = d.misses / d.totalDisplayTris > 0.1 ? 'debug-err' : d.misses > 0 ? 'debug-warn' : 'debug-ok';
+            html += `<tr><td>No match (magenta)</td><td class="${missCls}">${fmt(d.misses)} (${pct(d.misses, d.totalDisplayTris)})</td></tr>`;
+            html += `<tr><td>Degenerate (skipped)</td><td>${fmt(d.degenerate)}</td></tr>`;
+            html += '</table></div>';
+
+            // Hours distribution
+            if (d.hoursDistribution) {
+                html += '<div class="debug-section"><div class="debug-section-title">Hours Distribution (mapped tris)</div>';
+                html += '<table>';
+                for (const [range, count] of d.hoursDistribution) {
+                    html += `<tr><td>${range}</td><td>${fmt(count)}</td></tr>`;
+                }
+                html += '</table></div>';
+            }
+
+            // Mesh healing notes
+            if (meshHealingNotes.length > 0) {
+                // Summary stats
+                const errors = meshHealingNotes.filter(n => n.type === 'error');
+                const warns = meshHealingNotes.filter(n => n.type === 'warn');
+                const titleCls = errors.length > 0 ? 'debug-err' : 'debug-warn';
+
+                html += `<div class="debug-section"><div class="debug-section-title ${titleCls}">Mesh Healing (${meshHealingNotes.length} issues)</div>`;
+                html += '<table>';
+
+                // Count unique issue types
+                const issueCounts = {};
+                for (const note of meshHealingNotes) {
+                    const cat = note.msg.split(':')[0].split('(')[0].trim();
+                    issueCounts[cat] = (issueCounts[cat] || 0) + 1;
+                }
+                for (const [cat, count] of Object.entries(issueCounts)) {
+                    html += `<tr><td>${cat}</td><td>${count} elements</td></tr>`;
+                }
+                html += '</table>';
+
+                // Show first 20 detailed notes
+                const showNotes = meshHealingNotes.slice(0, 20);
+                html += '<div style="margin-top:4px; font-size:10px; max-height:250px; overflow-y:auto;">';
+                for (const note of showNotes) {
+                    const cls = note.type === 'error' ? 'debug-err' : 'debug-warn';
+                    const prefix = note.elem >= 0 ? `elem[${note.elem}]: ` : '';
+                    const msgHtml = note.msg.replace(/\n/g, '<br>');
+                    html += `<div class="${cls}" style="margin-bottom:3px; white-space:pre-wrap;">${prefix}${msgHtml}</div>`;
+                }
+                if (meshHealingNotes.length > 20) {
+                    html += `<div style="color:#666;">...and ${meshHealingNotes.length - 20} more</div>`;
+                }
+                html += '</div></div>';
+            } else if (analysisMeshes.length > 0) {
+                html += '<div class="debug-section"><div class="debug-section-title debug-ok">Mesh Healing</div>';
+                html += '<div style="color:#4CAF50;">All elements passed health checks</div></div>';
+            }
 
-        // ─── VERTICAL SURFACE SELECTION HELPERS ───
+            body.innerHTML = html;
 
-        function isVerticalFace(normal) {
-            return Math.abs(normal.y) < Math.sin(Math.PI / 180);
+            // Auto-show if there are problems
+            if (d.misses / d.totalDisplayTris > 0.05 || meshHealingNotes.some(n => n.type === 'error')) {
+                document.getElementById('debug-console').classList.add('visible');
+            }
         }
 
-        function getCoplanarFaces(mesh, hitFaceIndex) {
-            const geo = mesh.geometry;
-            const pos = geo.attributes.position.array;
-            const idx = geo.index ? geo.index.array : null;
-            const TOLERANCE = Math.sin(Math.PI / 180); // 1 degree
+        // ─── VERTEX WELDING & DUPLICATE FACE REMOVAL ───
 
-            // Compute face normals for all triangles
-            const faceCount = idx ? idx.length / 3 : pos.length / 9;
-            const faceNormals = [];
+        // Merge vertices within a tolerance and remove duplicate/degenerate faces.
+        // This makes the concatenated IfcOpenShell mesh continuous at element seams.
+        function weldMesh(positions, indices, tolerance) {
+            tolerance = tolerance || 0.001;  // 1mm default
+            const invTol = 1.0 / tolerance;
+            const vertexCount = positions.length / 3;
+            const faceCount = indices.length / 3;
 
-            for (let f = 0; f < faceCount; f++) {
-                const i0 = idx ? idx[f*3]*3 : f*9;
-                const i1 = idx ? idx[f*3+1]*3 : f*9+3;
-                const i2 = idx ? idx[f*3+2]*3 : f*9+6;
+            // Quantise vertex positions to grid cells of size=tolerance
+            // Map quantised key → canonical vertex index
+            const keyToCanon = new Map();
+            const oldToCanon = new Uint32Array(vertexCount);
+            let canonCount = 0;
+            const canonPositions = [];  // flat x,y,z
 
-                const ax = pos[i0], ay = pos[i0+1], az = pos[i0+2];
-                const bx = pos[i1], by = pos[i1+1], bz = pos[i1+2];
-                const cx = pos[i2], cy = pos[i2+1], cz = pos[i2+2];
+            for (let v = 0; v < vertexCount; v++) {
+                const x = positions[v * 3];
+                const y = positions[v * 3 + 1];
+                const z = positions[v * 3 + 2];
 
-                const e1x = bx-ax, e1y = by-ay, e1z = bz-az;
-                const e2x = cx-ax, e2y = cy-ay, e2z = cz-az;
-                const nx = e1y*e2z - e1z*e2y;
-                const ny = e1z*e2x - e1x*e2z;
-                const nz = e1x*e2y - e1y*e2x;
-                const len = Math.sqrt(nx*nx + ny*ny + nz*nz);
+                const qx = Math.round(x * invTol);
+                const qy = Math.round(y * invTol);
+                const qz = Math.round(z * invTol);
+                const key = qx + ',' + qy + ',' + qz;
 
-                faceNormals.push(len > 0 ? [nx/len, ny/len, nz/len] : [0,1,0]);
+                if (keyToCanon.has(key)) {
+                    oldToCanon[v] = keyToCanon.get(key);
+                } else {
+                    const ci = canonCount++;
+                    keyToCanon.set(key, ci);
+                    oldToCanon[v] = ci;
+                    canonPositions.push(x, y, z);
+                }
             }
 
-            const hitNormal = faceNormals[hitFaceIndex];
+            // Remap face indices and remove degenerate + duplicate faces
+            const faceSet = new Set();
+            const newIndices = [];
+            let degenerateCount = 0;
+            let duplicateCount = 0;
 
-            // Only proceed if hit face is vertical
-            if (Math.abs(hitNormal[1]) >= TOLERANCE) return null;
-
-            // Build vertex-to-face adjacency map
-            const vertToFaces = new Map();
             for (let f = 0; f < faceCount; f++) {
-                for (let v = 0; v < 3; v++) {
-                    const vi = idx ? idx[f*3+v] : f*3+v;
-                    if (!vertToFaces.has(vi)) vertToFaces.set(vi, []);
-                    vertToFaces.get(vi).push(f);
-                }
-            }
-
-            // Flood fill — collect faces within 1 degree of hit normal, connected by shared vertices
-            const collected = new Set();
-            const queue = [hitFaceIndex];
-            collected.add(hitFaceIndex);
-
-            while (queue.length > 0) {
-                const current = queue.shift();
-
-                // Get all vertex indices for this face
-                for (let v = 0; v < 3; v++) {
-                    const vi = idx ? idx[current*3+v] : current*3+v;
-                    const neighbours = vertToFaces.get(vi) || [];
-                    for (const neighbour of neighbours) {
-                        if (collected.has(neighbour)) continue;
-                        const nn = faceNormals[neighbour];
-                        // Check within 1 degree of the ORIGINAL hit normal
-                        const dot = hitNormal[0]*nn[0] + hitNormal[1]*nn[1] + hitNormal[2]*nn[2];
-                        if (dot >= 1 - TOLERANCE && Math.abs(nn[1]) < TOLERANCE) {
-                            collected.add(neighbour);
-                            queue.push(neighbour);
-                        }
-                    }
+                let a = oldToCanon[indices[f * 3]];
+                let b = oldToCanon[indices[f * 3 + 1]];
+                let c = oldToCanon[indices[f * 3 + 2]];
+
+                // Skip degenerate faces (two or more vertices collapsed to same point)
+                if (a === b || b === c || a === c) {
+                    degenerateCount++;
+                    continue;
                 }
+
+                // Canonical face key: sorted vertex indices
+                const sorted = [a, b, c].sort((x, y) => x - y);
+                const faceKey = sorted[0] + ',' + sorted[1] + ',' + sorted[2];
+
+                if (faceSet.has(faceKey)) {
+                    duplicateCount++;
+                    continue;
+                }
+                faceSet.add(faceKey);
+
+                newIndices.push(a, b, c);
             }
 
+            const mergedVerts = vertexCount - canonCount;
+            const removedFaces = degenerateCount + duplicateCount;
+            console.log(`Vertex welding: ${vertexCount}→${canonCount} verts (${mergedVerts} merged), ` +
+                `${faceCount}→${newIndices.length / 3} faces (${degenerateCount} degenerate, ${duplicateCount} duplicate removed)`);
+
             return {
-                faceIndices: Array.from(collected),
-                normal: hitNormal,
-                mesh: mesh,
+                positions: new Float32Array(canonPositions),
+                indices: new Uint32Array(newIndices),
+                mergedVerts,
+                degenerateCount,
+                duplicateCount,
             };
         }
 
-        function addVerticalFaceHighlight(mesh, faceIndices) {
-            const geo = mesh.geometry;
-            const pos = geo.attributes.position.array;
-            const idx = geo.index ? geo.index.array : null;
-            const positions = [];
+        // ─── MANIFOLD CHECK & VOID REMOVAL ───
 
-            mesh.updateWorldMatrix(true, false);
-            const wm = mesh.matrixWorld;
+        // Make an edge key with sorted vertex indices (order-independent)
+        function edgeKey(a, b) {
+            return a < b ? a + ',' + b : b + ',' + a;
+        }
 
-            for (const f of faceIndices) {
-                for (let v = 0; v < 3; v++) {
-                    const vi = idx ? idx[f*3+v]*3 : f*9+v*3;
-                    const p = new THREE.Vector3(pos[vi], pos[vi+1], pos[vi+2]).applyMatrix4(wm);
-                    positions.push(p.x, p.y, p.z);
+        // Check manifoldness and find connected components
+        // Returns { isManifold, components: [{faces: [faceIdx,...], manifold: bool}], edgeMap }
+        function analyseMesh(positions, indices) {
+            const faceCount = indices.length / 3;
+
+            // Build edge → face list map
+            const edgeFaces = new Map();
+            for (let f = 0; f < faceCount; f++) {
+                const i0 = indices[f * 3], i1 = indices[f * 3 + 1], i2 = indices[f * 3 + 2];
+                const edges = [edgeKey(i0, i1), edgeKey(i1, i2), edgeKey(i2, i0)];
+                for (const ek of edges) {
+                    if (!edgeFaces.has(ek)) edgeFaces.set(ek, []);
+                    edgeFaces.get(ek).push(f);
                 }
             }
 
-            const hlGeo = new THREE.BufferGeometry();
-            hlGeo.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
-            const hlMat = new THREE.MeshBasicMaterial({
-                color: 0x00CFC8,
-                transparent: true,
-                opacity: 0.5,
-                side: THREE.DoubleSide,
-                depthTest: false,
-            });
-            const hlMesh = new THREE.Mesh(hlGeo, hlMat);
-            scene.add(hlMesh);
-            return hlMesh;
-        }
-
-        function updateSelectedMeshLabel() {
-            const total = selectedGroundMeshes.length + selectedVerticalFaces.length;
-            if (total === 0) {
-                document.getElementById('selected-mesh-name').textContent = 'No surfaces selected';
-                document.getElementById('confirm-ground-btn').disabled = true;
-            } else {
-                const parts = [];
-                if (selectedGroundMeshes.length > 0)
-                    parts.push(selectedGroundMeshes.length + ' ground mesh' + (selectedGroundMeshes.length > 1 ? 'es' : ''));
-                if (selectedVerticalFaces.length > 0)
-                    parts.push(selectedVerticalFaces.length + ' vertical face' + (selectedVerticalFaces.length > 1 ? 's' : ''));
-                document.getElementById('selected-mesh-name').textContent = parts.join(', ');
-                document.getElementById('confirm-ground-btn').disabled = false;
+            // Overall manifold check: every edge has exactly 2 faces
+            let isManifold = true;
+            let nonManifoldEdges = 0;
+            let boundaryEdges = 0;
+            for (const [ek, faces] of edgeFaces) {
+                if (faces.length !== 2) {
+                    isManifold = false;
+                    if (faces.length === 1) boundaryEdges++;
+                    else nonManifoldEdges++;
+                }
             }
-        }
 
-        document.getElementById('viewport').addEventListener('click', (event) => {
-            if (event.target !== renderer.domElement) return;
-            if (pickMode) {
-                handleMeshPick(event);
-                return;
-            }
-            if (emitterPickMode) {
-                handleEmitterPick(event);
-                return;
-            }
-            if (bboxMode) {
-                handleBboxClick(event);
-                return;
-            }
-            if (currentStep === 6 && Object.keys(seasonHeatmaps).length > 0) {
-                handleRayProbeClick(event);
-                return;
-            }
-        });
+            console.log(`Mesh analysis: ${faceCount} faces, ${edgeFaces.size} edges, manifold=${isManifold}, boundary=${boundaryEdges}, non-manifold=${nonManifoldEdges}`);
 
-        document.getElementById('viewport').addEventListener('dblclick', (event) => {
-            if (!pickMode) return;
-            if (event.target !== renderer.domElement) return;
+            // Find connected components via face adjacency (shared edges)
+            const faceAdj = new Array(faceCount);
+            for (let f = 0; f < faceCount; f++) faceAdj[f] = [];
 
-            const container = document.getElementById('viewport');
-            const rect = container.getBoundingClientRect();
-            const mouse = new THREE.Vector2(
-                ((event.clientX - rect.left) / rect.width) * 2 - 1,
-                -((event.clientY - rect.top) / rect.height) * 2 + 1
-            );
-            const raycaster = new THREE.Raycaster();
-            raycaster.setFromCamera(mouse, camera);
-            const hits = raycaster.intersectObjects(allMeshes, false);
-            if (hits.length === 0) return;
+            for (const [ek, faces] of edgeFaces) {
+                for (let i = 0; i < faces.length; i++) {
+                    for (let j = i + 1; j < faces.length; j++) {
+                        faceAdj[faces[i]].push(faces[j]);
+                        faceAdj[faces[j]].push(faces[i]);
+                    }
+                }
+            }
 
-            const hitMesh = hits[0].object;
-            const faceIndex = hits[0].faceIndex;
-
-            // Only applicable for vertical surfaces
-            const geo = hitMesh.geometry;
-            const pos = geo.attributes.position.array;
-            const idx = geo.index ? geo.index.array : null;
-            const i0 = idx ? idx[faceIndex*3]*3 : faceIndex*9;
-            const i1 = idx ? idx[faceIndex*3+1]*3 : faceIndex*9+3;
-            const i2 = idx ? idx[faceIndex*3+2]*3 : faceIndex*9+6;
-            const e1 = new THREE.Vector3(pos[i1]-pos[i0], pos[i1+1]-pos[i0+1], pos[i1+2]-pos[i0+2]);
-            const e2 = new THREE.Vector3(pos[i2]-pos[i0], pos[i2+1]-pos[i0+1], pos[i2+2]-pos[i0+2]);
-            const faceNormal = new THREE.Vector3().crossVectors(e1, e2).normalize();
-            const normalMatrix = new THREE.Matrix3().getNormalMatrix(hitMesh.matrixWorld);
-            faceNormal.applyMatrix3(normalMatrix).normalize();
-
-            if (!isVerticalFace(faceNormal)) return;
-
-            // Check if any faces from this mesh are already selected
-            const meshFaces = selectedVerticalFaces.filter(s => s.mesh === hitMesh);
-
-            if (meshFaces.length > 0) {
-                // Deselect all vertical faces from this mesh
-                for (const s of meshFaces) {
-                    scene.remove(s.highlight);
-                    s.highlight.geometry.dispose();
-                    s.highlight.material.dispose();
-                }
-                selectedVerticalFaces = selectedVerticalFaces.filter(s => s.mesh !== hitMesh);
-            } else {
-                // Select all vertical faces from this mesh using flood fill per unique normal
-                const faceCount = idx ? idx.length / 3 : pos.length / 9;
-                const visited = new Set();
+            const visited = new Uint8Array(faceCount);
+            const components = [];
 
-                for (let f = 0; f < faceCount; f++) {
-                    if (visited.has(f)) continue;
-                    const result = getCoplanarFaces(hitMesh, f);
-                    if (!result) { visited.add(f); continue; }
-                    // Only add if vertical
-                    const n = result.normal;
-                    if (Math.abs(n[1]) >= Math.sin(Math.PI / 180)) {
-                        result.faceIndices.forEach(fi => visited.add(fi));
-                        continue;
+            for (let f = 0; f < faceCount; f++) {
+                if (visited[f]) continue;
+                const component = [];
+                const stack = [f];
+                visited[f] = 1;
+                while (stack.length > 0) {
+                    const cur = stack.pop();
+                    component.push(cur);
+                    for (const adj of faceAdj[cur]) {
+                        if (!visited[adj]) {
+                            visited[adj] = 1;
+                            stack.push(adj);
+                        }
                     }
-                    result.faceIndices.forEach(fi => visited.add(fi));
-                    const highlight = addVerticalFaceHighlight(hitMesh, result.faceIndices);
-                    selectedVerticalFaces.push({ ...result, highlight });
                 }
+                components.push(component);
             }
 
-            updateSelectedMeshLabel();
-        });
+            // Check manifoldness per component
+            const componentInfos = components.map(comp => {
+                const faceSet = new Set(comp);
+                let compManifold = true;
+                let compBoundary = 0;
+                for (const f of comp) {
+                    const i0 = indices[f * 3], i1 = indices[f * 3 + 1], i2 = indices[f * 3 + 2];
+                    const edges = [edgeKey(i0, i1), edgeKey(i1, i2), edgeKey(i2, i0)];
+                    for (const ek of edges) {
+                        const ef = edgeFaces.get(ek);
+                        const inComp = ef.filter(ff => faceSet.has(ff));
+                        if (inComp.length !== 2) {
+                            compManifold = false;
+                            if (inComp.length === 1) compBoundary++;
+                        }
+                    }
+                }
+                return { faces: comp, manifold: compManifold, boundaryEdges: compBoundary };
+            });
 
-        function handleMeshPick(event) {
-            const container = document.getElementById('viewport');
-            const rect = container.getBoundingClientRect();
-            const mouse = flyMode
-                ? new THREE.Vector2(0, 0)
-                : new THREE.Vector2(
-                    ((event.clientX - rect.left) / rect.width) * 2 - 1,
-                    -((event.clientY - rect.top) / rect.height) * 2 + 1
-                );
-            const raycaster = new THREE.Raycaster();
-            raycaster.setFromCamera(mouse, camera);
-            const hits = raycaster.intersectObjects(allMeshes, false);
-            if (hits.length === 0) return;
+            console.log(`Found ${components.length} connected components`);
+            return { isManifold, components: componentInfos, edgeFaces };
+        }
+
+        // Determine if a point is inside a manifold mesh using ray casting (parity test)
+        // Shoots a ray in +X direction and counts intersections with the given triangles
+        function isPointInsideMesh(px, py, pz, positions, faceIndices) {
+            let crossings = 0;
+            const numFaces = faceIndices.length / 3;
+            for (let f = 0; f < numFaces; f++) {
+                const i0 = faceIndices[f * 3] * 3;
+                const i1 = faceIndices[f * 3 + 1] * 3;
+                const i2 = faceIndices[f * 3 + 2] * 3;
+
+                const ax = positions[i0] - px, ay = positions[i0 + 1] - py, az = positions[i0 + 2] - pz;
+                const bx = positions[i1] - px, by = positions[i1 + 1] - py, bz = positions[i1 + 2] - pz;
+                const cx = positions[i2] - px, cy = positions[i2 + 1] - py, cz = positions[i2 + 2] - pz;
+
+                // Möller-Trumbore for ray direction (1,0,0)
+                const ebx = bx - ax, eby = by - ay, ebz = bz - az;
+                const ecx = cx - ax, ecy = cy - ay, ecz = cz - az;
+
+                // h = cross(dir, ec) where dir = (1,0,0)
+                const hx = 0, hy = -ecz, hz = ecy;
+                const det = ebx * hx + eby * hy + ebz * hz;
+                if (Math.abs(det) < 1e-12) continue;
+
+                const invDet = 1.0 / det;
+                // s = origin - a = (-ax, -ay, -az) relative, but origin is (0,0,0) after shift
+                const sx = -ax, sy = -ay, sz = -az;
+                const u = invDet * (sx * hx + sy * hy + sz * hz);
+                if (u < 0 || u > 1) continue;
+
+                // q = cross(s, eb)
+                const qx = sy * ebz - sz * eby;
+                const qy = sz * ebx - sx * ebz;
+                const qz = sx * eby - sy * ebx;
+                const v = invDet * (1 * qx + 0 * qy + 0 * qz);  // dot(dir, q)
+                if (v < 0 || u + v > 1) continue;
+
+                const t = invDet * (ecx * qx + ecy * qy + ecz * qz);
+                if (t > 1e-6) crossings++;
+            }
+            return (crossings % 2) === 1;
+        }
 
-            const hit = hits[0];
-            const hitMesh = hit.object;
-            const faceIndex = hit.faceIndex;
-
-            // Compute hit face normal in world space
-            const geo = hitMesh.geometry;
-            const pos = geo.attributes.position.array;
-            const idx = geo.index ? geo.index.array : null;
-            const i0 = idx ? idx[faceIndex*3]*3 : faceIndex*9;
-            const i1 = idx ? idx[faceIndex*3+1]*3 : faceIndex*9+3;
-            const i2 = idx ? idx[faceIndex*3+2]*3 : faceIndex*9+6;
-            const e1 = new THREE.Vector3(pos[i1]-pos[i0], pos[i1+1]-pos[i0+1], pos[i1+2]-pos[i0+2]);
-            const e2 = new THREE.Vector3(pos[i2]-pos[i0], pos[i2+1]-pos[i0+1], pos[i2+2]-pos[i0+2]);
-            const faceNormal = new THREE.Vector3().crossVectors(e1, e2).normalize();
-
-            // Transform normal to world space
-            const normalMatrix = new THREE.Matrix3().getNormalMatrix(hitMesh.matrixWorld);
-            faceNormal.applyMatrix3(normalMatrix).normalize();
-
-            if (isVerticalFace(faceNormal)) {
-                // Vertical — coplanar flood fill selection
-                const result = getCoplanarFaces(hitMesh, faceIndex);
-                if (!result) return;
-
-                // Check if already selected — toggle off
-                const existingIdx = selectedVerticalFaces.findIndex(
-                    s => s.mesh === hitMesh && s.faceIndices[0] === result.faceIndices[0]
-                );
+        // Remove void components: find manifold closed components that are fully inside
+        // another component, and remove them from the mesh
+        function removeVoids(positions, indices) {
+            const analysis = analyseMesh(positions, indices);
+            const comps = analysis.components;
 
-                if (existingIdx !== -1) {
-                    const removed = selectedVerticalFaces.splice(existingIdx, 1)[0];
-                    scene.remove(removed.highlight);
-                    removed.highlight.geometry.dispose();
-                    removed.highlight.material.dispose();
-                } else {
-                    const highlight = addVerticalFaceHighlight(hitMesh, result.faceIndices);
-                    selectedVerticalFaces.push({ ...result, highlight });
+            if (comps.length <= 1) {
+                console.log('Single component — no voids to remove');
+                return { positions, indices, voidsRemoved: 0, analysis };
+            }
+
+            // Sort components by face count descending (largest = likely outer shell)
+            const sorted = comps.map((c, i) => ({ ...c, idx: i }))
+                .sort((a, b) => b.faces.length - a.faces.length);
+
+            // For each manifold closed component (except the largest), check if its
+            // centroid is inside any larger component. If so, mark it as a void.
+            const voidFlags = new Uint8Array(comps.length);
+            let voidsRemoved = 0;
+
+            for (let si = 1; si < sorted.length; si++) {
+                const comp = sorted[si];
+                // Only consider manifold closed components as potential voids
+                if (!comp.manifold) continue;
+
+                // Compute centroid of this component
+                let cx = 0, cy = 0, cz = 0, nv = 0;
+                const seenVerts = new Set();
+                for (const f of comp.faces) {
+                    for (let k = 0; k < 3; k++) {
+                        const vi = indices[f * 3 + k];
+                        if (!seenVerts.has(vi)) {
+                            seenVerts.add(vi);
+                            cx += positions[vi * 3];
+                            cy += positions[vi * 3 + 1];
+                            cz += positions[vi * 3 + 2];
+                            nv++;
+                        }
+                    }
                 }
-            } else {
-                // Non-vertical — existing whole-mesh toggle behaviour unchanged
-                const existingIdx = selectedGroundMeshes.indexOf(hitMesh);
-                if (existingIdx !== -1) {
-                    selectedGroundMeshes.splice(existingIdx, 1);
-                    removeHighlight(hitMesh);
-                } else {
-                    selectedGroundMeshes.push(hitMesh);
-                    addHighlight(hitMesh);
+                cx /= nv; cy /= nv; cz /= nv;
+
+                // Check if centroid is inside any larger component
+                for (let sj = 0; sj < si; sj++) {
+                    const outer = sorted[sj];
+                    if (voidFlags[outer.idx]) continue;  // Skip if already a void
+                    if (!outer.manifold) continue;  // Can only test inside manifold meshes
+
+                    // Build face index array for the outer component
+                    const outerIndices = new Uint32Array(outer.faces.length * 3);
+                    for (let fi = 0; fi < outer.faces.length; fi++) {
+                        const f = outer.faces[fi];
+                        outerIndices[fi * 3] = indices[f * 3];
+                        outerIndices[fi * 3 + 1] = indices[f * 3 + 1];
+                        outerIndices[fi * 3 + 2] = indices[f * 3 + 2];
+                    }
+
+                    if (isPointInsideMesh(cx, cy, cz, positions, outerIndices)) {
+                        voidFlags[comp.idx] = 1;
+                        voidsRemoved++;
+                        console.log(`Void detected: component ${comp.idx} (${comp.faces.length} faces) inside component ${outer.idx}`);
+                        break;
+                    }
                 }
             }
 
-            updateSelectedMeshLabel();
-        }
+            if (voidsRemoved === 0) {
+                console.log('No voids detected');
+                return { positions, indices, voidsRemoved: 0, analysis };
+            }
 
-        function confirmGroundMesh() {
-            if (selectedGroundMeshes.length === 0 && selectedVerticalFaces.length === 0) return;
-            setPickMode(false);
-            buildShadowBVH();
+            // Rebuild mesh without void components
+            const keepFaces = [];
+            for (let ci = 0; ci < comps.length; ci++) {
+                if (!voidFlags[ci]) {
+                    keepFaces.push(...comps[ci].faces);
+                }
+            }
 
-            const totalSurfaces = selectedGroundMeshes.length + selectedVerticalFaces.length;
-            completeStep(3, totalSurfaces + ' surface' + (totalSurfaces > 1 ? 's' : '') + ' selected');
-        }
+            // Remap vertices (only keep referenced ones)
+            const vertexMap = new Map();
+            let newVertIdx = 0;
+            const newIndices = [];
+            for (const f of keepFaces) {
+                for (let k = 0; k < 3; k++) {
+                    const oldV = indices[f * 3 + k];
+                    if (!vertexMap.has(oldV)) {
+                        vertexMap.set(oldV, newVertIdx++);
+                    }
+                    newIndices.push(vertexMap.get(oldV));
+                }
+            }
 
-        // ─── STEP 4: EXCLUDE SHADE EMITTERS ───
-        function setEmitterPickMode(on) {
-            emitterPickMode = on;
-            const viewport = document.getElementById('viewport');
-            const overlay = document.getElementById('pick-overlay');
-            viewport.classList.toggle('picking-mesh', on);
-            overlay.classList.toggle('visible', on);
-        }
-
-        function addEmitterHighlight(mesh) {
-            if (!mesh.userData._origColorEmitter) {
-                mesh.userData._origColorEmitter = mesh.material.color.getHex();
-                mesh.userData._origOpacityEmitter = mesh.material.opacity;
-                mesh.userData._origTransparentEmitter = mesh.material.transparent;
-            }
-            mesh.material = mesh.material.clone();
-            mesh.material.color.setHex(0xFF4444);
-            mesh.material.opacity = 0.45;
-            mesh.material.transparent = true;
-
-            const edges = new THREE.EdgesGeometry(mesh.geometry, 1);
-            const hl = new THREE.LineSegments(edges,
-                new THREE.LineBasicMaterial({ color: 0xFF2222, linewidth: 2 }));
-            hl.position.copy(mesh.position);
-            hl.rotation.copy(mesh.rotation);
-            hl.scale.copy(mesh.scale);
-            hl.userData._emitterRef = mesh;
-            if (mesh.parent) {
-                mesh.parent.add(hl);
-            } else {
-                scene.add(hl);
+            const newPositions = new Float32Array(newVertIdx * 3);
+            for (const [oldV, newV] of vertexMap) {
+                newPositions[newV * 3] = positions[oldV * 3];
+                newPositions[newV * 3 + 1] = positions[oldV * 3 + 1];
+                newPositions[newV * 3 + 2] = positions[oldV * 3 + 2];
             }
-            emitterHighlights.push(hl);
+
+            const removedFaces = indices.length / 3 - newIndices.length / 3;
+            console.log(`Removed ${voidsRemoved} void components (${removedFaces} faces)`);
+
+            return {
+                positions: newPositions,
+                indices: new Uint32Array(newIndices),
+                voidsRemoved,
+                analysis
+            };
         }
 
-        function removeEmitterHighlight(mesh) {
-            if (mesh.userData._origColorEmitter !== undefined) {
-                mesh.material = mesh.material.clone();
-                mesh.material.color.setHex(mesh.userData._origColorEmitter);
-                mesh.material.opacity = mesh.userData._origOpacityEmitter;
-                mesh.material.transparent = mesh.userData._origTransparentEmitter;
-            }
 
-            const idx = emitterHighlights.findIndex(hl => hl.userData._emitterRef === mesh);
-            if (idx === -1) return;
-            const hl = emitterHighlights[idx];
-            if (hl.parent) hl.parent.remove(hl);
-            else scene.remove(hl);
-            hl.geometry.dispose();
-            hl.material.dispose();
-            emitterHighlights.splice(idx, 1);
+        // ─── ORIENT NORMALS OUTWARD ───
+
+        // Compute face normal (unnormalized) for face f
+        function faceNormal(positions, indices, f) {
+            const i0 = indices[f * 3] * 3, i1 = indices[f * 3 + 1] * 3, i2 = indices[f * 3 + 2] * 3;
+            const ax = positions[i1] - positions[i0], ay = positions[i1 + 1] - positions[i0 + 1], az = positions[i1 + 2] - positions[i0 + 2];
+            const bx = positions[i2] - positions[i0], by = positions[i2 + 1] - positions[i0 + 1], bz = positions[i2 + 2] - positions[i0 + 2];
+            return { x: ay * bz - az * by, y: az * bx - ax * bz, z: ax * by - ay * bx };
         }
 
-        function clearEmitterHighlights() {
-            for (const hl of emitterHighlights) {
-                if (hl.parent) hl.parent.remove(hl);
-                else scene.remove(hl);
-                hl.geometry.dispose();
-                hl.material.dispose();
+        // Face centroid
+        function faceCentroid(positions, indices, f) {
+            const i0 = indices[f * 3] * 3, i1 = indices[f * 3 + 1] * 3, i2 = indices[f * 3 + 2] * 3;
+            return {
+                x: (positions[i0] + positions[i1] + positions[i2]) / 3,
+                y: (positions[i0 + 1] + positions[i1 + 1] + positions[i2 + 1]) / 3,
+                z: (positions[i0 + 2] + positions[i1 + 2] + positions[i2 + 2]) / 3
+            };
+        }
+
+        // Get the directed half-edge (v0→v1) for a face's edge
+        // Returns which order the two vertices appear when traversing face f's winding
+        function faceEdgeDirection(indices, f, va, vb) {
+            const i0 = indices[f * 3], i1 = indices[f * 3 + 1], i2 = indices[f * 3 + 2];
+            // Check if edge va→vb appears in the face's winding order
+            if ((i0 === va && i1 === vb) || (i1 === va && i2 === vb) || (i2 === va && i0 === vb)) {
+                return 1;  // same direction as winding
             }
-            emitterHighlights = [];
-            // Restore original materials
-            for (const mesh of excludedEmitters) {
-                if (mesh.userData._origColorEmitter !== undefined) {
-                    mesh.material = mesh.material.clone();
-                    mesh.material.color.setHex(mesh.userData._origColorEmitter);
-                    mesh.material.opacity = mesh.userData._origOpacityEmitter;
-                    mesh.material.transparent = mesh.userData._origTransparentEmitter;
+            return -1;  // opposite direction
+        }
+
+        // Orient all face normals outward.
+        // Strategy:
+        //   1. Build edge→face adjacency and connected components
+        //   2. For manifold components: BFS winding propagation from a seed face
+        //      - Seed face orientation determined by ray-cast parity test
+        //      - Neighbours sharing an edge must have OPPOSITE half-edge directions
+        //        (i.e., if face A has edge v0→v1, face B must have v1→v0 for consistent winding)
+        //   3. For non-manifold components: per-face ray-cast parity test
+        function orientNormalsOutward(positions, indices) {
+            const faceCount = indices.length / 3;
+            if (faceCount === 0) return 0;
+
+            // Build edge → face map with directed edge info
+            const edgeFaces = new Map();  // edgeKey → [{face, va, vb}, ...]
+            for (let f = 0; f < faceCount; f++) {
+                const i0 = indices[f * 3], i1 = indices[f * 3 + 1], i2 = indices[f * 3 + 2];
+                const pairs = [[i0, i1], [i1, i2], [i2, i0]];
+                for (const [va, vb] of pairs) {
+                    const ek = edgeKey(va, vb);
+                    if (!edgeFaces.has(ek)) edgeFaces.set(ek, []);
+                    edgeFaces.get(ek).push({ face: f, va, vb });
                 }
             }
-        }
 
-        function updateExcludedEmittersLabel() {
-            const count = excludedEmitters.length;
-            document.getElementById('excluded-emitters-label').textContent =
-                count + ' mesh' + (count !== 1 ? 'es' : '') + ' excluded';
+            // Build face adjacency
+            const faceAdj = new Array(faceCount);
+            for (let f = 0; f < faceCount; f++) faceAdj[f] = [];
+            for (const [ek, entries] of edgeFaces) {
+                if (entries.length === 2) {
+                    // Manifold edge — record adjacency with directed edge info
+                    const a = entries[0], b = entries[1];
+                    faceAdj[a.face].push({ neighbor: b.face, aVa: a.va, aVb: a.vb, bVa: b.va, bVb: b.vb });
+                    faceAdj[b.face].push({ neighbor: a.face, aVa: b.va, aVb: b.vb, bVa: a.va, bVb: a.vb });
+                }
+                // Non-manifold edges (1 or 3+ faces) are skipped for winding propagation
+            }
 
-            const listEl = document.getElementById('shade-emitter-list');
-            if (count === 0) {
-                listEl.innerHTML = '';
-            } else {
-                const names = excludedEmitters.map(m => {
-                    const meta = allMeshMeta.find(mm => mm.mesh === m);
-                    return meta ? meta.name : m.name;
-                });
-                listEl.innerHTML = names.map(n =>
-                    '<div style="padding:2px 0; border-bottom:1px solid #1a1a2e;">' + n + '</div>'
-                ).join('');
+            // Find connected components
+            const compId = new Int32Array(faceCount).fill(-1);
+            const components = [];
+            for (let f = 0; f < faceCount; f++) {
+                if (compId[f] >= 0) continue;
+                const cid = components.length;
+                const comp = [];
+                const stack = [f];
+                compId[f] = cid;
+                while (stack.length > 0) {
+                    const cur = stack.pop();
+                    comp.push(cur);
+                    for (const adj of faceAdj[cur]) {
+                        if (compId[adj.neighbor] < 0) {
+                            compId[adj.neighbor] = cid;
+                            stack.push(adj.neighbor);
+                        }
+                    }
+                }
+                components.push(comp);
             }
-        }
 
-        function handleEmitterPick(event) {
-            const container = document.getElementById('viewport');
-            const rect = container.getBoundingClientRect();
-            const mouse = flyMode
-                ? new THREE.Vector2(0, 0)
-                : new THREE.Vector2(
-                    ((event.clientX - rect.left) / rect.width) * 2 - 1,
-                    -((event.clientY - rect.top) / rect.height) * 2 + 1
-                );
-            const raycaster = new THREE.Raycaster();
-            raycaster.setFromCamera(mouse, camera);
+            let totalFlipped = 0;
+
+            // Process each component
+            for (const comp of components) {
+                if (comp.length === 0) continue;
+
+                // BFS winding propagation
+                // First, determine correct orientation of seed face using ray-cast
+                const seedFace = comp[0];
+                const seedNorm = faceNormal(positions, indices, seedFace);
+                const len = Math.sqrt(seedNorm.x * seedNorm.x + seedNorm.y * seedNorm.y + seedNorm.z * seedNorm.z);
+                if (len < 1e-12) continue;
+                const nx = seedNorm.x / len, ny = seedNorm.y / len, nz = seedNorm.z / len;
+
+                const cent = faceCentroid(positions, indices, seedFace);
+
+                // Ray-cast from centroid along the face normal direction
+                // Count crossings with ALL mesh faces (not just this component)
+                // Odd crossings → normal points inward → seed should be flipped
+                let crossings = 0;
+                for (let tf = 0; tf < faceCount; tf++) {
+                    if (tf === seedFace) continue;
+                    const ti0 = indices[tf * 3] * 3, ti1 = indices[tf * 3 + 1] * 3, ti2 = indices[tf * 3 + 2] * 3;
+
+                    const ax = positions[ti0] - cent.x, ay = positions[ti0 + 1] - cent.y, az = positions[ti0 + 2] - cent.z;
+                    const bx = positions[ti1] - cent.x, by = positions[ti1 + 1] - cent.y, bz = positions[ti1 + 2] - cent.z;
+                    const cx = positions[ti2] - cent.x, cy = positions[ti2 + 1] - cent.y, cz = positions[ti2 + 2] - cent.z;
+
+                    // Möller-Trumbore for ray direction (nx, ny, nz)
+                    const ebx = bx - ax, eby = by - ay, ebz = bz - az;
+                    const ecx = cx - ax, ecy = cy - ay, ecz = cz - az;
+
+                    const hx = ny * ecz - nz * ecy, hy = nz * ecx - nx * ecz, hz = nx * ecy - ny * ecx;
+                    const det = ebx * hx + eby * hy + ebz * hz;
+                    if (Math.abs(det) < 1e-12) continue;
+
+                    const invDet = 1.0 / det;
+                    const sx = -ax, sy = -ay, sz = -az;
+                    const u = invDet * (sx * hx + sy * hy + sz * hz);
+                    if (u < 0 || u > 1) continue;
+
+                    const qx = sy * ebz - sz * eby, qy = sz * ebx - sx * ebz, qz = sx * eby - sy * ebx;
+                    const v = invDet * (nx * qx + ny * qy + nz * qz);
+                    if (v < 0 || u + v > 1) continue;
+
+                    const t = invDet * (ecx * qx + ecy * qy + ecz * qz);
+                    if (t > 1e-4) crossings++;
+                }
 
-            // Only allow picking non-ground meshes
-            const groundSet = new Set(selectedGroundMeshes);
-            const pickable = allMeshes.filter(m => !groundSet.has(m));
-            const hits = raycaster.intersectObjects(pickable, false);
-            if (hits.length === 0) return;
+                // If odd crossings, the seed normal points inward — need to flip seed
+                const seedNeedsFlip = (crossings % 2) === 1;
+
+                // BFS to propagate consistent winding from seed
+                const flipFlag = new Uint8Array(faceCount);  // 1 = this face needs flipping
+                const visited = new Uint8Array(faceCount);
+                visited[seedFace] = 1;
+                if (seedNeedsFlip) flipFlag[seedFace] = 1;
+
+                const queue = [seedFace];
+                let qi = 0;
+                while (qi < queue.length) {
+                    const cur = queue[qi++];
+                    const curFlipped = flipFlag[cur];
+
+                    for (const adj of faceAdj[cur]) {
+                        if (visited[adj.neighbor]) continue;
+                        visited[adj.neighbor] = 1;
+
+                        // For consistent outward normals, two faces sharing a manifold edge
+                        // must traverse the shared edge in OPPOSITE directions.
+                        // If face A has half-edge va→vb, face B should have vb→va.
+                        // Check: do both faces traverse the shared edge in the same direction?
+                        const sameDirection = (adj.aVa === adj.bVa && adj.aVb === adj.bVb);
+                        // sameDirection means they have the SAME half-edge order for this edge
+                        // which means their normals point in OPPOSITE directions (inconsistent)
+                        // So: neighbor needs flip if:
+                        //   - same direction + cur NOT flipped → neighbor must flip (to become consistent then flip outward)
+                        //   - opposite direction + cur flipped → neighbor must flip
+                        // Simplified: neighborFlip = curFlipped XOR !sameDirection
+                        // Wait, let me think more carefully:
+                        //   Consistent winding: shared edge traversed in opposite directions
+                        //   sameDirection = true → currently INCONSISTENT → neighbor needs flip relative to cur
+                        //   sameDirection = false → currently CONSISTENT → neighbor same as cur
+                        const neighborFlip = sameDirection ? !curFlipped : curFlipped;
+                        flipFlag[adj.neighbor] = neighborFlip ? 1 : 0;
+
+                        queue.push(adj.neighbor);
+                    }
+                }
+
+                // Also handle faces not reached by BFS (non-manifold boundaries within component)
+                // These get individual ray-cast tests
+                for (const f of comp) {
+                    if (visited[f]) continue;
+
+                    const fn = faceNormal(positions, indices, f);
+                    const fnLen = Math.sqrt(fn.x * fn.x + fn.y * fn.y + fn.z * fn.z);
+                    if (fnLen < 1e-12) continue;
+                    const fnx = fn.x / fnLen, fny = fn.y / fnLen, fnz = fn.z / fnLen;
+                    const fc = faceCentroid(positions, indices, f);
+
+                    let fc_crossings = 0;
+                    for (let tf = 0; tf < faceCount; tf++) {
+                        if (tf === f) continue;
+                        const ti0 = indices[tf * 3] * 3, ti1 = indices[tf * 3 + 1] * 3, ti2 = indices[tf * 3 + 2] * 3;
+
+                        const ax = positions[ti0] - fc.x, ay = positions[ti0 + 1] - fc.y, az = positions[ti0 + 2] - fc.z;
+                        const bx = positions[ti1] - fc.x, by = positions[ti1 + 1] - fc.y, bz = positions[ti1 + 2] - fc.z;
+                        const cx = positions[ti2] - fc.x, cy = positions[ti2 + 1] - fc.y, cz = positions[ti2 + 2] - fc.z;
+
+                        const ebx = bx - ax, eby = by - ay, ebz = bz - az;
+                        const ecx = cx - ax, ecy = cy - ay, ecz = cz - az;
+                        const hx = fny * ecz - fnz * ecy, hy = fnz * ecx - fnx * ecz, hz = fnx * ecy - fny * ecx;
+                        const det = ebx * hx + eby * hy + ebz * hz;
+                        if (Math.abs(det) < 1e-12) continue;
+                        const invDet = 1.0 / det;
+                        const sx = -ax, sy = -ay, sz = -az;
+                        const u = invDet * (sx * hx + sy * hy + sz * hz);
+                        if (u < 0 || u > 1) continue;
+                        const qx = sy * ebz - sz * eby, qy = sz * ebx - sx * ebz, qz = sx * eby - sy * ebx;
+                        const v = invDet * (fnx * qx + fny * qy + fnz * qz);
+                        if (v < 0 || u + v > 1) continue;
+                        const t = invDet * (ecx * qx + ecy * qy + ecz * qz);
+                        if (t > 1e-4) fc_crossings++;
+                    }
 
-            const hitMesh = hits[0].object;
-            const existingIdx = excludedEmitters.indexOf(hitMesh);
+                    if ((fc_crossings % 2) === 1) flipFlag[f] = 1;
+                }
 
-            if (existingIdx !== -1) {
-                // Re-include — toggle off exclusion
-                excludedEmitters.splice(existingIdx, 1);
-                removeEmitterHighlight(hitMesh);
-            } else {
-                // Exclude — toggle on
-                excludedEmitters.push(hitMesh);
-                addEmitterHighlight(hitMesh);
+                // Apply flips
+                let compFlipped = 0;
+                for (const f of comp) {
+                    if (flipFlag[f]) {
+                        // Swap indices[f*3+1] and indices[f*3+2] to reverse winding
+                        const tmp = indices[f * 3 + 1];
+                        indices[f * 3 + 1] = indices[f * 3 + 2];
+                        indices[f * 3 + 2] = tmp;
+                        compFlipped++;
+                    }
+                }
+                totalFlipped += compFlipped;
+            }
+
+            console.log(`Normal orientation: flipped ${totalFlipped}/${faceCount} faces across ${components.length} components`);
+            return totalFlipped;
+        }
+
+
+        document.getElementById('viewport').addEventListener('click', (event) => {
+            if (event.target !== renderer.domElement) return;
+            if (bboxMode) {
+                handleBboxClick(event);
+                return;
+            }
+            if (currentStep === 5 && Object.keys(seasonHeatmaps).length > 0) {
+                handleRayProbeClick(event);
+                return;
             }
+        });
 
-            updateExcludedEmittersLabel();
-        }
-
-        function confirmShadeEmitters() {
-            setEmitterPickMode(false);
-            clearEmitterHighlights();
-
-            buildShadowBVH();
-
-            const excluded = excludedEmitters.length;
-            const total = allMeshes.length - selectedGroundMeshes.length;
-            const active = total - excluded;
-            const summary = active + ' caster' + (active !== 1 ? 's' : '') +
-                (excluded > 0 ? ' (' + excluded + ' excluded)' : '');
-            completeStep(4, summary);
-        }
-
-        // ─── BUILD SHADOW BVH (all meshes except ground & excluded) ───
+        // ─── BUILD SHADOW BVH (all scene geometry) ───
         function buildShadowBVH() {
             showStatus('Building BVH for shadow casters...');
-            // Concatenate all non-ground mesh triangles into one set of arrays
             const allVerts = [];
             const allIdx = [];
             let offset = 0;
-
-            const skipSet = new Set([...selectedGroundMeshes, ...excludedEmitters]);
-            for (const mesh of allMeshes) {
-                if (skipSet.has(mesh)) continue;
+            const meshes = getAnalysisMeshes();
+            for (const mesh of meshes) {
                 const geo = mesh.geometry;
                 const pos = geo.attributes.position.array;
                 const idx = geo.index ? geo.index.array : null;
-
-                // Apply world matrix to get transformed positions
                 mesh.updateWorldMatrix(true, false);
                 const wm = mesh.matrixWorld;
-
                 const numVerts = pos.length / 3;
                 for (let v = 0; v < numVerts; v++) {
                     const p = new THREE.Vector3(pos[v*3], pos[v*3+1], pos[v*3+2]);
                     p.applyMatrix4(wm);
                     allVerts.push(p.x, p.y, p.z);
                 }
-
                 if (idx) {
-                    for (let i = 0; i < idx.length; i++) {
-                        allIdx.push(idx[i] + offset);
-                    }
+                    for (let i = 0; i < idx.length; i++) allIdx.push(idx[i] + offset);
                 } else {
-                    for (let i = 0; i < numVerts; i++) {
-                        allIdx.push(i + offset);
-                    }
+                    for (let i = 0; i < numVerts; i++) allIdx.push(i + offset);
                 }
                 offset += numVerts;
             }
-
             if (allVerts.length > 0) {
                 shadowBVH = new BVH(new Float32Array(allVerts), new Uint32Array(allIdx));
                 console.log('Shadow BVH built:', (allIdx.length / 3) + ' triangles');
@@ -2398,9 +2924,100 @@
             hideStatus();
         }
 
+        // ─── STEP 2: SET ORIENTATION (2D Screenshot Preview) ───
+        function captureOrientationPreview() {
+            if (!buildingGroup) return;
+            // Save current camera
+            const savedCamera = camera;
+            const savedRotateEnabled = controls.enableRotate;
+            const savedPanEnabled = controls.enablePan;
+
+            // Set up ortho camera centred on building
+            updateOrthoCamera();
+            camera = orthoCamera;
+
+            // Render to canvas and capture
+            renderer.render(scene, orthoCamera);
+            const dataURL = renderer.domElement.toDataURL('image/png');
+
+            // Restore perspective camera
+            camera = savedCamera;
+            controls.object = camera;
+            controls.enableRotate = savedRotateEnabled;
+            controls.enablePan = savedPanEnabled;
+            controls.update();
+
+            // Set the preview image
+            document.getElementById('orient-preview').src = dataURL;
+        }
+
+        function showOrientationPreview() {
+            document.getElementById('orient-preview-container').classList.add('visible');
+            document.getElementById('north-arrow').style.display = 'block';
+            // Lock 3D controls during orientation
+            controls.enableRotate = false;
+            controls.enablePan = false;
+        }
+
+        function hideOrientationPreview() {
+            document.getElementById('orient-preview-container').classList.remove('visible');
+            document.getElementById('north-arrow').style.display = 'none';
+            // Restore controls
+            controls.enableRotate = true;
+            controls.enablePan = true;
+        }
+
+        function confirmOrientation() {
+            // Apply the chosen rotation to the model group
+            if (modelRotationGroup) {
+                modelRotationGroup.rotation.y = northRotationDeg * Math.PI / 180;
+            }
+            hideOrientationPreview();
+            const summary = northRotationDeg === 0
+                ? 'North: confirmed'
+                : 'North: rotated ' + (northRotationDeg > 0 ? '+' : '') + northRotationDeg + '\u00b0';
+            completeStep(2, summary);
+        }
+
+        function applyManualRotation(sign) {
+            const degrees = parseFloat(document.getElementById('north-rotation').value) || 5;
+            northRotationDeg += sign * Math.abs(degrees);
+            // Wrap to -180..180
+            while (northRotationDeg > 180) northRotationDeg -= 360;
+            while (northRotationDeg <= -180) northRotationDeg += 360;
+            northRotationDeg = Math.round(northRotationDeg * 10) / 10;
+
+            // Rotate the 2D preview image via CSS
+            document.getElementById('orient-preview').style.transform = 'rotate(' + northRotationDeg + 'deg)';
+            // Rotate north arrow inversely
+            document.getElementById('north-arrow-rotator').style.transform = 'rotate(' + (-northRotationDeg) + 'deg)';
+        }
+
+        function resetOrientation() {
+            northRotationDeg = 0;
+            document.getElementById('orient-preview').style.transform = 'rotate(0deg)';
+            document.getElementById('north-arrow-rotator').style.transform = 'rotate(0deg)';
+        }
+
+        // ─── STEP 3: SITE LOCATION ───
+        function confirmSiteLocation() {
+            const lat = parseFloat(document.getElementById('latitude').value) || 51.5074;
+            const lng = parseFloat(document.getElementById('longitude').value) || -0.1278;
+            completeStep(3, lat.toFixed(2) + ', ' + lng.toFixed(2));
+        }
+
         // ─── STEP 4: ANALYSIS AREA ───
-        function useEntireMesh() {
-            useEntireGroundMesh = true;
+        function enableRunButton() {
+            const btn = document.getElementById('run-btn');
+            btn.disabled = false;
+            btn.style.opacity = '';
+            btn.style.cursor = '';
+            const hint = document.getElementById('run-btn-hint');
+            if (hint) hint.style.display = 'none';
+        }
+
+        function useEntireScene() {
+            useEntireBounds = true;
             document.getElementById('use-entire-btn').style.background = '#D4880F';
             document.getElementById('use-entire-btn').style.color = '#fff';
             document.getElementById('bbox-btn').style.background = '';
@@ -2408,6 +3025,7 @@
             document.getElementById('bbox-fields').style.display = 'none';
             document.getElementById('bbox-fields2').style.display = 'none';
             removeBboxHelper();
+            enableRunButton();
         }
 
         // ─── BVH (Bounding Volume Hierarchy) for fast ray casting ───
@@ -2557,7 +3175,7 @@
                     + Math.cos(latRad) * Math.cos(declination) * Math.cos(hourAngle);
                 const altitude = Math.asin(Math.max(-1, Math.min(1, sinAlt)));
 
-                if (altitude <= 0) continue;
+                if (altitude * 180 / Math.PI <= -0.833) continue;
 
                 const cosAz = (Math.sin(declination) - Math.sin(latRad) * sinAlt)
                     / (Math.cos(latRad) * Math.cos(altitude));
@@ -2590,97 +3208,75 @@
             return new THREE.Vector3(ifcX, ifcZ, -ifcY).normalize();
         }
 
-        // ─── TRIANGLE-GRID CLIPPING HELPERS ───
-        function lerpVert(a, b, t) {
-            return [
-                a[0] + t * (b[0] - a[0]),
-                a[1] + t * (b[1] - a[1]),
-                a[2] + t * (b[2] - a[2]),
-            ];
-        }
-
-        // Split an array of triangles along an axis-aligned plane (axis: 0=X, 2=Z)
-        function splitTrisAlongPlane(tris, axis, value) {
+        // ─── SUTHERLAND-HODGMAN POLYGON CLIPPING ───
+        function clipPolygonToPlane(vertices, axis, value, keepAbove) {
+            if (vertices.length === 0) return [];
             const result = [];
-            for (const tri of tris) {
-                const [a, b, c] = tri;
-                const da = a[axis] - value;
-                const db = b[axis] - value;
-                const dc = c[axis] - value;
-                const sa = da >= 0;
-                const sb = db >= 0;
-                const sc = dc >= 0;
-
-                if (sa === sb && sb === sc) {
-                    result.push(tri);
-                    continue;
-                }
-
-                // Find the lone vertex (the one on its own side)
-                let lone, pair1, pair2, dLone, dPair1, dPair2;
-                if (sa !== sb && sa !== sc) {
-                    lone = a; pair1 = b; pair2 = c;
-                    dLone = da; dPair1 = db; dPair2 = dc;
-                } else if (sb !== sa && sb !== sc) {
-                    lone = b; pair1 = a; pair2 = c;
-                    dLone = db; dPair1 = da; dPair2 = dc;
-                } else {
-                    lone = c; pair1 = a; pair2 = b;
-                    dLone = dc; dPair1 = da; dPair2 = db;
+            const n = vertices.length;
+            for (let i = 0; i < n; i++) {
+                const curr = vertices[i];
+                const next = vertices[(i + 1) % n];
+                const currInside = keepAbove ? curr[axis] >= value - 1e-10 : curr[axis] <= value + 1e-10;
+                const nextInside = keepAbove ? next[axis] >= value - 1e-10 : next[axis] <= value + 1e-10;
+                if (currInside) {
+                    result.push(curr);
+                    if (!nextInside) {
+                        const t = (value - curr[axis]) / (next[axis] - curr[axis]);
+                        result.push([
+                            curr[0] + t * (next[0] - curr[0]),
+                            curr[1] + t * (next[1] - curr[1]),
+                            curr[2] + t * (next[2] - curr[2]),
+                        ]);
+                    }
+                } else if (nextInside) {
+                    const t = (value - curr[axis]) / (next[axis] - curr[axis]);
+                    result.push([
+                        curr[0] + t * (next[0] - curr[0]),
+                        curr[1] + t * (next[1] - curr[1]),
+                        curr[2] + t * (next[2] - curr[2]),
+                    ]);
                 }
-
-                const t1 = dLone / (dLone - dPair1);
-                const m1 = lerpVert(lone, pair1, t1);
-                const t2 = dLone / (dLone - dPair2);
-                const m2 = lerpVert(lone, pair2, t2);
-
-                // Lone side: 1 triangle
-                result.push([lone, m1, m2]);
-                // Pair side: quad = 2 triangles
-                result.push([m1, pair1, pair2]);
-                result.push([m1, pair2, m2]);
             }
             return result;
         }
 
-        // Clip a single triangle against all grid lines it crosses
-        function clipTriToGrid(tri, gridSize) {
-            let tris = [tri];
-
-            // Find X grid lines this triangle crosses
-            const minX = Math.min(tri[0][0], tri[1][0], tri[2][0]);
-            const maxX = Math.max(tri[0][0], tri[1][0], tri[2][0]);
-            const firstX = Math.ceil(minX / gridSize) * gridSize;
-            for (let x = firstX; x < maxX; x += gridSize) {
-                tris = splitTrisAlongPlane(tris, 0, x);
+        function clipTriangleToVoxel(tri, minX, minY, minZ, maxX, maxY, maxZ) {
+            let poly = [tri[0], tri[1], tri[2]];
+            poly = clipPolygonToPlane(poly, 0, minX, true);
+            if (poly.length < 3) return [];
+            poly = clipPolygonToPlane(poly, 0, maxX, false);
+            if (poly.length < 3) return [];
+            poly = clipPolygonToPlane(poly, 1, minY, true);
+            if (poly.length < 3) return [];
+            poly = clipPolygonToPlane(poly, 1, maxY, false);
+            if (poly.length < 3) return [];
+            poly = clipPolygonToPlane(poly, 2, minZ, true);
+            if (poly.length < 3) return [];
+            poly = clipPolygonToPlane(poly, 2, maxZ, false);
+            return poly;
+        }
+
+        function triangulatePolygon(vertices) {
+            if (vertices.length < 3) return [];
+            const tris = [];
+            for (let i = 1; i < vertices.length - 1; i++) {
+                tris.push([vertices[0], vertices[i], vertices[i + 1]]);
             }
-
-            // Find Z grid lines the (now-split) triangles cross
-            let minZ = Infinity, maxZ = -Infinity;
-            for (const t of tris) {
-                for (const v of t) {
-                    if (v[2] < minZ) minZ = v[2];
-                    if (v[2] > maxZ) maxZ = v[2];
-                }
-            }
-            const firstZ = Math.ceil(minZ / gridSize) * gridSize;
-            for (let z = firstZ; z < maxZ; z += gridSize) {
-                tris = splitTrisAlongPlane(tris, 2, z);
-            }
-
             return tris;
         }
 
-        // ─── PREPARE GRID CELLS (merge + slice — done ONCE, cached) ───
-        let cachedCellData = null;  // reused across seasons
+        // ─── VOXEL-BASED ANALYSIS PIPELINE ───
+        let cachedCellData = null;
         let cachedGridSize = null;
+        let cachedCellMap = null;
+        let cachedSliverIndices = null;
 
-        async function prepareGridCells() {
+        async function prepareVoxelCells() {
             const gridSize = parseFloat(document.getElementById('grid_resolution').value) || 1.0;
 
             // Apply bbox filter if set
             let bboxFilter = null;
-            if (!useEntireGroundMesh) {
+            if (!useEntireBounds) {
                 const bx1 = parseFloat(document.getElementById('bbox_min_x').value);
                 const by1 = parseFloat(document.getElementById('bbox_min_y').value);
                 const bx2 = parseFloat(document.getElementById('bbox_max_x').value);
@@ -2691,222 +3287,359 @@
                 }
             }
 
-            // 1. Merge all selected ground mesh fragments into one unified set
-            showStatus('Merging ground mesh fragments...');
+            // Step 1: Voxelise all IFC geometry
+            showStatus('Voxelising geometry...');
             await new Promise(r => setTimeout(r, 0));
-            const mergedVerts = [];
-            const mergedIdx = [];
-            let vertOffset = 0;
-
-            for (const gm of selectedGroundMeshes) {
-                gm.updateWorldMatrix(true, false);
-                const wm = gm.matrixWorld;
-                const geo = gm.geometry;
+
+            const voxelGrid = new Map();
+            const allWorldTris = [];
+            let sceneMinY = Infinity;
+
+            const meshes = getAnalysisMeshes();
+            for (const mesh of meshes) {
+                mesh.updateWorldMatrix(true, false);
+                const wm = mesh.matrixWorld;
+                const geo = mesh.geometry;
                 const pos = geo.attributes.position.array;
                 const idx = geo.index ? geo.index.array : null;
-                const numVerts = pos.length / 3;
-
-                for (let v = 0; v < numVerts; v++) {
-                    const p = new THREE.Vector3(pos[v*3], pos[v*3+1], pos[v*3+2]).applyMatrix4(wm);
-                    mergedVerts.push(p.x, p.y, p.z);
-                }
+                const faceCount = idx ? idx.length / 3 : pos.length / 9;
 
-                if (idx) {
-                    for (let i = 0; i < idx.length; i++) mergedIdx.push(idx[i] + vertOffset);
-                } else {
-                    for (let i = 0; i < numVerts; i++) mergedIdx.push(i + vertOffset);
+                for (let f = 0; f < faceCount; f++) {
+                    const i0 = idx ? idx[f*3]*3 : f*9;
+                    const i1 = idx ? idx[f*3+1]*3 : f*9+3;
+                    const i2 = idx ? idx[f*3+2]*3 : f*9+6;
+
+                    const a = new THREE.Vector3(pos[i0], pos[i0+1], pos[i0+2]).applyMatrix4(wm);
+                    const b = new THREE.Vector3(pos[i1], pos[i1+1], pos[i1+2]).applyMatrix4(wm);
+                    const c = new THREE.Vector3(pos[i2], pos[i2+1], pos[i2+2]).applyMatrix4(wm);
+
+                    const tri = [[a.x, a.y, a.z], [b.x, b.y, b.z], [c.x, c.y, c.z]];
+                    const triIdx = allWorldTris.length;
+                    allWorldTris.push(tri);
+
+                    sceneMinY = Math.min(sceneMinY, a.y, b.y, c.y);
+
+                    const tMinX = Math.min(a.x, b.x, c.x), tMaxX = Math.max(a.x, b.x, c.x);
+                    const tMinY = Math.min(a.y, b.y, c.y), tMaxY = Math.max(a.y, b.y, c.y);
+                    const tMinZ = Math.min(a.z, b.z, c.z), tMaxZ = Math.max(a.z, b.z, c.z);
+
+                    const ixMin = Math.floor(tMinX / gridSize);
+                    const ixMax = Math.floor(tMaxX / gridSize);
+                    const iyMin = Math.floor(tMinY / gridSize);
+                    const iyMax = Math.floor(tMaxY / gridSize);
+                    const izMin = Math.floor(tMinZ / gridSize);
+                    const izMax = Math.floor(tMaxZ / gridSize);
+
+                    for (let ix = ixMin; ix <= ixMax; ix++) {
+                        for (let iy = iyMin; iy <= iyMax; iy++) {
+                            for (let iz = izMin; iz <= izMax; iz++) {
+                                const key = ix + ',' + iy + ',' + iz;
+                                if (!voxelGrid.has(key)) {
+                                    voxelGrid.set(key, { triIndices: [], ix, iy, iz });
+                                }
+                                voxelGrid.get(key).triIndices.push(triIdx);
+                            }
+                        }
+                    }
                 }
-                vertOffset += numVerts;
             }
 
-            // Build all merged triangles as arrays
-            const allMergedTris = [];
-            const faceCount = mergedIdx.length / 3;
-            for (let f = 0; f < faceCount; f++) {
-                const i0 = mergedIdx[f * 3], i1 = mergedIdx[f * 3 + 1], i2 = mergedIdx[f * 3 + 2];
-                allMergedTris.push([
-                    [mergedVerts[i0*3], mergedVerts[i0*3+1], mergedVerts[i0*3+2]],
-                    [mergedVerts[i1*3], mergedVerts[i1*3+1], mergedVerts[i1*3+2]],
-                    [mergedVerts[i2*3], mergedVerts[i2*3+1], mergedVerts[i2*3+2]],
-                ]);
-            }
+            showStatus(`Voxelised: ${voxelGrid.size} cells from ${allWorldTris.length} triangles`);
+            await new Promise(r => setTimeout(r, 0));
 
-            // 2. Filter to upward-facing surfaces only (reject walls, soffits, bottoms)
-            showStatus(`Filtering ${allMergedTris.length} faces to upward-facing surfaces...`);
+            // Step 2: Clip geometry per voxel and remove phantom voxels
+            // (AABB registration creates phantom voxels where the triangle's bounding
+            //  box overlaps but the triangle itself doesn't — these must be removed
+            //  before outer shell extraction to avoid making real cells look interior)
+            showStatus('Clipping geometry per voxel...');
             await new Promise(r => setTimeout(r, 0));
 
-            const worldTris = [];
-            const MIN_UPWARD_NY = 0.1;
-            for (let f = 0; f < allMergedTris.length; f++) {
-                const tri = allMergedTris[f];
-                const [a, b, c] = tri;
-                const e1x = b[0]-a[0], e1y = b[1]-a[1], e1z = b[2]-a[2];
-                const e2x = c[0]-a[0], e2y = c[1]-a[1], e2z = c[2]-a[2];
-                const fnx = e1y*e2z - e1z*e2y;
-                const fny = e1z*e2x - e1x*e2z;
-                const fnz = e1x*e2y - e1y*e2x;
-                const fnLen = Math.sqrt(fnx*fnx + fny*fny + fnz*fnz);
-                if (fnLen === 0) continue;
-                // Keep only faces whose normal has a meaningful upward (+Y) component
-                if (fny / fnLen < MIN_UPWARD_NY) continue;
-
-                worldTris.push(tri);
-            }
-
-            showStatus(`Upward faces: ${worldTris.length} of ${allMergedTris.length} kept`);
-
-            // 2b. Append vertical face triangles without normal filtering
-            for (const vf of selectedVerticalFaces) {
-                vf.mesh.updateWorldMatrix(true, false);
-                const wm = vf.mesh.matrixWorld;
-                const vGeo = vf.mesh.geometry;
-                const vPos = vGeo.attributes.position.array;
-                const vIdx = vGeo.index ? vGeo.index.array : null;
-
-                for (const f of vf.faceIndices) {
-                    const vi0 = vIdx ? vIdx[f*3]*3 : f*9;
-                    const vi1 = vIdx ? vIdx[f*3+1]*3 : f*9+3;
-                    const vi2 = vIdx ? vIdx[f*3+2]*3 : f*9+6;
-
-                    const a = new THREE.Vector3(vPos[vi0], vPos[vi0+1], vPos[vi0+2]).applyMatrix4(wm);
-                    const b = new THREE.Vector3(vPos[vi1], vPos[vi1+1], vPos[vi1+2]).applyMatrix4(wm);
-                    const c = new THREE.Vector3(vPos[vi2], vPos[vi2+1], vPos[vi2+2]).applyMatrix4(wm);
-
-                    worldTris.push([
-                        [a.x, a.y, a.z],
-                        [b.x, b.y, b.z],
-                        [c.x, c.y, c.z],
-                    ]);
+            const clippedVoxels = new Map(); // key → { ix, iy, iz, tris, area, centroid, normal }
+            let clipCount = 0;
+            const voxelKeys = Array.from(voxelGrid.keys());
+
+            for (let vi = 0; vi < voxelKeys.length; vi++) {
+                const key = voxelKeys[vi];
+                const cell = voxelGrid.get(key);
+                const { ix, iy, iz, triIndices } = cell;
+
+                // Skip cells below ground
+                const cellCentroidY = (iy + 0.5) * gridSize;
+                if (cellCentroidY < sceneMinY) continue;
+
+                const vMinX = ix * gridSize, vMinY = iy * gridSize, vMinZ = iz * gridSize;
+                const vMaxX = vMinX + gridSize, vMaxY = vMinY + gridSize, vMaxZ = vMinZ + gridSize;
+
+                // Bbox spatial filter (X-Z plane)
+                if (bboxFilter) {
+                    const vcx = (vMinX + vMaxX) / 2;
+                    const vcz = (vMinZ + vMaxZ) / 2;
+                    const ifcX = vcx, ifcY = -vcz;
+                    if (ifcX < bboxFilter.minX || ifcX > bboxFilter.maxX ||
+                        ifcY < bboxFilter.minY || ifcY > bboxFilter.maxY) continue;
                 }
-            }
-
-            if (selectedVerticalFaces.length > 0) {
-                showStatus(`Total analysis triangles (incl. vertical): ${worldTris.length}`);
-            }
 
-            // 3. Slice every triangle along grid lines
-            showStatus(`Slicing ${worldTris.length} triangles along ${gridSize}m grid...`);
-            await new Promise(r => setTimeout(r, 0));
-
-            const cells = new Map();
-            for (let ti = 0; ti < worldTris.length; ti++) {
-                const subTris = clipTriToGrid(worldTris[ti], gridSize);
-                for (const st of subTris) {
-                    const [a, b, c] = st;
-                    const cx = (a[0] + b[0] + c[0]) / 3;
-                    const cy = (a[1] + b[1] + c[1]) / 3;
-                    const cz = (a[2] + b[2] + c[2]) / 3;
-
-                    if (bboxFilter) {
-                        const ifcX = cx, ifcY = -cz;
-                        if (ifcX < bboxFilter.minX || ifcX > bboxFilter.maxX ||
-                            ifcY < bboxFilter.minY || ifcY > bboxFilter.maxY) continue;
+                // Clip all registered triangles to this voxel
+                let totalArea = 0;
+                let sumCx = 0, sumCy = 0, sumCz = 0;
+                let sumNx = 0, sumNy = 0, sumNz = 0;
+                const clippedTris = [];
+
+                for (const ti of triIndices) {
+                    const tri = allWorldTris[ti];
+                    const clippedPoly = clipTriangleToVoxel(tri, vMinX, vMinY, vMinZ, vMaxX, vMaxY, vMaxZ);
+                    if (clippedPoly.length < 3) continue;
+
+                    const subTris = triangulatePolygon(clippedPoly);
+                    for (const ct of subTris) {
+                        const [a, b, c] = ct;
+                        const e1x = b[0]-a[0], e1y = b[1]-a[1], e1z = b[2]-a[2];
+                        const e2x = c[0]-a[0], e2y = c[1]-a[1], e2z = c[2]-a[2];
+                        const nx = e1y*e2z - e1z*e2y;
+                        const ny = e1z*e2x - e1x*e2z;
+                        const nz = e1x*e2y - e1y*e2x;
+                        const len = Math.sqrt(nx*nx + ny*ny + nz*nz);
+                        if (len === 0) continue;
+
+                        const area = len * 0.5;
+                        const cx = (a[0] + b[0] + c[0]) / 3;
+                        const cy = (a[1] + b[1] + c[1]) / 3;
+                        const cz = (a[2] + b[2] + c[2]) / 3;
+
+                        totalArea += area;
+                        sumCx += cx * area;
+                        sumCy += cy * area;
+                        sumCz += cz * area;
+                        sumNx += (nx / len) * area;
+                        sumNy += (ny / len) * area;
+                        sumNz += (nz / len) * area;
+
+                        clippedTris.push(ct);
                     }
+                }
 
-                    const col = Math.floor(cx / gridSize);
-                    const row = Math.floor(cz / gridSize);
-                    const key = col + ',' + row;
-
+                // Skip phantom voxels (AABB overlap but no actual geometry)
+                if (clippedTris.length === 0 || totalArea === 0) continue;
+
+                // Keep all clipped triangles — layer selection happens in Step 3
+                // after we know the cell's outward direction
+                let layerArea = 0, lsCx = 0, lsCy = 0, lsCz = 0;
+                let lsNx = 0, lsNy = 0, lsNz = 0;
+                const layerTris = [];
+                for (const tri of clippedTris) {
+                    layerTris.push(tri);
+                    const [a, b, c] = tri;
                     const e1x = b[0]-a[0], e1y = b[1]-a[1], e1z = b[2]-a[2];
                     const e2x = c[0]-a[0], e2y = c[1]-a[1], e2z = c[2]-a[2];
                     const nx = e1y*e2z - e1z*e2y;
                     const ny = e1z*e2x - e1x*e2z;
                     const nz = e1x*e2y - e1y*e2x;
                     const len = Math.sqrt(nx*nx + ny*ny + nz*nz);
-                    const area = len * 0.5;
+                    if (len === 0) continue;
+                    const a2 = len * 0.5;
+                    layerArea += a2;
+                    lsCx += ((a[0]+b[0]+c[0])/3) * a2;
+                    lsCy += ((a[1]+b[1]+c[1])/3) * a2;
+                    lsCz += ((a[2]+b[2]+c[2])/3) * a2;
+                    lsNx += (nx/len) * a2;
+                    lsNy += (ny/len) * a2;
+                    lsNz += (nz/len) * a2;
+                }
+                if (layerArea === 0) continue;
 
-                    if (!cells.has(key)) {
-                        cells.set(key, { tris: [], area: 0,
-                            sumCx: 0, sumCy: 0, sumCz: 0,
-                            sumNx: 0, sumNy: 0, sumNz: 0 });
-                    }
-                    const cell = cells.get(key);
-                    cell.tris.push(st);
-                    cell.area += area;
-                    cell.sumCx += cx * area;
-                    cell.sumCy += cy * area;
-                    cell.sumCz += cz * area;
-                    if (len > 0) {
-                        const sign = ny >= 0 ? 1 : -1;
-                        cell.sumNx += sign * (nx / len) * area;
-                        cell.sumNy += sign * (ny / len) * area;
-                        cell.sumNz += sign * (nz / len) * area;
-                    }
+                const centroid = {
+                    x: lsCx / layerArea,
+                    y: lsCy / layerArea,
+                    z: lsCz / layerArea,
+                };
+
+                let nLen = Math.sqrt(lsNx*lsNx + lsNy*lsNy + lsNz*lsNz);
+                let normal;
+                if (nLen > 0) {
+                    normal = { x: lsNx / nLen, y: lsNy / nLen, z: lsNz / nLen };
+                } else {
+                    normal = { x: 0, y: 1, z: 0 };
                 }
-                if (ti % 500 === 0 && ti > 0) {
-                    showStatus(`Slicing triangles... ${Math.round(ti / worldTris.length * 100)}%`);
+
+                clippedVoxels.set(key, {
+                    ix, iy, iz, tris: layerTris, area: layerArea, centroid, normal,
+                });
+                clipCount++;
+
+                if (vi % 500 === 0 && vi > 0) {
+                    showStatus(`Clipping voxels... ${Math.round(vi / voxelKeys.length * 100)}%`);
                     await new Promise(r => setTimeout(r, 0));
                 }
             }
 
-            if (cells.size === 0) {
-                throw new Error('No grid cells found on the selected ground meshes');
-            }
+            showStatus(`Clipped: ${clipCount} voxels with geometry (${voxelGrid.size - clipCount} phantom voxels removed)`);
+            await new Promise(r => setTimeout(r, 0));
+
+            // Step 3: Extract outer shell from the cleaned grid
+            // For sun analysis, orient normals upward: the sun is always above,
+            // so we always want the top-facing side of any surface.
+            showStatus('Extracting outer shell...');
+            await new Promise(r => setTimeout(r, 0));
 
-            const cellKeys = Array.from(cells.keys());
-            const cellData = cellKeys.map(k => {
-                const c = cells.get(k);
-                // Find the highest triangle centroid Y in this cell
-                let maxY = -Infinity;
-                for (const tri of c.tris) {
-                    const [a, b, cc] = tri;
-                    const ty = (a[1] + b[1] + cc[1]) / 3;
-                    if (ty > maxY) maxY = ty;
+            const NEIGHBOURS = [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]];
+            const cellData = [];
+            const targetFaceArea = gridSize * gridSize;
+
+            for (const [key, cell] of clippedVoxels) {
+                const { ix, iy, iz } = cell;
+                // Check which face-neighbours are empty in the CLEANED grid
+                const emptyDirs = [];
+                for (const [dx, dy, dz] of NEIGHBOURS) {
+                    if (!clippedVoxels.has((ix+dx) + ',' + (iy+dy) + ',' + (iz+dz))) {
+                        emptyDirs.push([dx, dy, dz]);
+                    }
                 }
-                // Recompute centroid & normal using only triangles near the highest surface
-                const HEIGHT_TOL = 0.5; // metres
-                let sumCx = 0, sumCy = 0, sumCz = 0, area = 0;
+                if (emptyDirs.length === 0) continue; // fully interior
+
+                // Compute reference "outward" direction from empty neighbours.
+                // This is purely topological (independent of mesh winding).
+                // Each triangle's normal is oriented to agree with this reference.
+                let refX = 0, refY = 0, refZ = 0;
+                for (const [dx, dy, dz] of emptyDirs) {
+                    refX += dx; refY += dy; refZ += dz;
+                }
+                // Add a small upward bias: for cells with equal empty above/below,
+                // prefer upward (sun is above). The bias is small enough not to
+                // override horizontal directions for walls.
+                refY += 0.05;
+                let refLen = Math.sqrt(refX*refX + refY*refY + refZ*refZ);
+                if (refLen > 0) { refX /= refLen; refY /= refLen; refZ /= refLen; }
+                else { refX = 0; refY = 1; refZ = 0; }
+
+                // Recompute normal from clipped triangles, using the reference
+                // direction to orient each triangle (winding-independent).
                 let sumNx = 0, sumNy = 0, sumNz = 0;
-                const topTris = [];
-                for (const tri of c.tris) {
-                    const [a, b, cc] = tri;
-                    const ty = (a[1] + b[1] + cc[1]) / 3;
-                    if (ty < maxY - HEIGHT_TOL) continue;
-                    topTris.push(tri);
-                    const cx = (a[0] + b[0] + cc[0]) / 3;
-                    const cy = ty;
-                    const cz = (a[2] + b[2] + cc[2]) / 3;
+
+                for (const tri of cell.tris) {
+                    const [a, b, c] = tri;
                     const e1x = b[0]-a[0], e1y = b[1]-a[1], e1z = b[2]-a[2];
-                    const e2x = cc[0]-a[0], e2y = cc[1]-a[1], e2z = cc[2]-a[2];
-                    const nx = e1y*e2z - e1z*e2y;
-                    const ny = e1z*e2x - e1x*e2z;
-                    const nz = e1x*e2y - e1y*e2x;
+                    const e2x = c[0]-a[0], e2y = c[1]-a[1], e2z = c[2]-a[2];
+                    let nx = e1y*e2z - e1z*e2y;
+                    let ny = e1z*e2x - e1x*e2z;
+                    let nz = e1x*e2y - e1y*e2x;
                     const len = Math.sqrt(nx*nx + ny*ny + nz*nz);
-                    const ta = len * 0.5;
-                    area += ta;
-                    sumCx += cx * ta;
-                    sumCy += cy * ta;
-                    sumCz += cz * ta;
-                    if (len > 0) {
-                        const sign = ny >= 0 ? 1 : -1;
-                        sumNx += sign * (nx / len) * ta;
-                        sumNy += sign * (ny / len) * ta;
-                        sumNz += sign * (nz / len) * ta;
-                    }
+                    if (len === 0) continue;
+                    const area = len * 0.5;
+
+                    // Orient this triangle's normal to agree with the reference
+                    const dot = nx * refX + ny * refY + nz * refZ;
+                    if (dot < 0) { nx = -nx; ny = -ny; nz = -nz; }
+
+                    sumNx += (nx / len) * area;
+                    sumNy += (ny / len) * area;
+                    sumNz += (nz / len) * area;
                 }
-                const a2 = area || 1;
-                const nLen = Math.sqrt(sumNx*sumNx + sumNy*sumNy + sumNz*sumNz);
-                return {
-                    key: k,
-                    tris: topTris,
-                    area: area,
-                    centroid: { x: sumCx / a2, y: sumCy / a2, z: sumCz / a2 },
-                    normal: (nLen > 0 && sumNy > 0)
-                        ? { x: sumNx / nLen, y: sumNy / nLen, z: sumNz / nLen }
-                        : { x: 0, y: 1, z: 0 },
-                };
-            });
+
+                let nLen = Math.sqrt(sumNx*sumNx + sumNy*sumNy + sumNz*sumNz);
+                let normal;
+                if (nLen > 0) {
+                    normal = { x: sumNx / nLen, y: sumNy / nLen, z: sumNz / nLen };
+                } else {
+                    normal = { x: 0, y: 1, z: 0 };
+                }
+
+                // Discard cells whose normal points significantly downward
+                // (underside surfaces that can't receive sunlight)
+                if (normal.y < -0.5) continue;
+                // Keep any cell with a horizontal empty neighbour — outer wall surface
+                const hasHorizontalEmpty = emptyDirs.some(([dx, dy, dz]) =>
+                    (dx !== 0 || dz !== 0) && dy === 0
+                );
+                if (normal.y < 0 && !hasHorizontalEmpty) continue;
+
+                // For upward-facing cells (roofs, ground), apply topmost layer
+                // filter to discard lower slabs in the same voxel column.
+                // For wall cells (horizontal refDir), keep all triangles —
+                // the layer filter is meaningless for vertical surfaces.
+                let displayTris = cell.tris;
+                if (refY > 0.5) {
+                    // Predominantly upward cell — filter to topmost layer only
+                    const HEIGHT_TOL = gridSize * 0.15;
+                    const trisByY = cell.tris.map(tri => ({
+                        tri,
+                        y: (tri[0][1] + tri[1][1] + tri[2][1]) / 3
+                    }));
+                    trisByY.sort((a, b) => b.y - a.y);
+                    const topY = trisByY[0].y;
+                    displayTris = trisByY
+                        .filter(t => t.y >= topY - HEIGHT_TOL)
+                        .map(t => t.tri);
+                }
+
+                cellData.push({
+                    key,
+                    ix, iy, iz,
+                    tris: displayTris,
+                    area: cell.area,
+                    centroid: cell.centroid,
+                    normal,
+                });
+            }
+
+            if (cellData.length === 0) {
+                throw new Error('No analysis cells found in scene geometry');
+            }
+
+            showStatus(`Outer shell: ${cellData.length} cells`);
+            await new Promise(r => setTimeout(r, 0));
+
+            // Step 4: Small cell inheritance markers
+            const sliverThreshold = 0.1 * targetFaceArea;
+            const cellMap = new Map();
+            for (let i = 0; i < cellData.length; i++) {
+                cellMap.set(cellData[i].key, i);
+            }
+            const sliverIndices = [];
+            for (let i = 0; i < cellData.length; i++) {
+                if (cellData[i].area < sliverThreshold) {
+                    sliverIndices.push(i);
+                    cellData[i]._isSliver = true;
+                }
+            }
+            if (sliverIndices.length > 0) {
+                showStatus(`Marking ${sliverIndices.length} sliver cells for inheritance...`);
+            }
 
             cachedCellData = cellData;
             cachedGridSize = gridSize;
-            showStatus(`Grid prepared: ${cellData.length} cells at ${gridSize}m resolution`);
+            cachedCellMap = cellMap;
+            cachedSliverIndices = sliverIndices;
+            showStatus(`Voxel grid prepared: ${cellData.length} cells at ${gridSize}m resolution (${sliverIndices.length} slivers)`);
             return cellData;
         }
 
+        // Apply sliver cell inheritance after ray casting
+        function applySmallCellInheritance(cellData, cellSunHours) {
+            if (!cachedSliverIndices || cachedSliverIndices.length === 0) return;
+            const NEIGHBOURS = [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]];
+            for (const si of cachedSliverIndices) {
+                const cell = cellData[si];
+                let bestNeighbour = -1;
+                let bestArea = -1;
+                for (const [dx, dy, dz] of NEIGHBOURS) {
+                    const nk = (cell.ix+dx) + ',' + (cell.iy+dy) + ',' + (cell.iz+dz);
+                    const ni = cachedCellMap.get(nk);
+                    if (ni === undefined || cellData[ni]._isSliver) continue;
+                    if (cellData[ni].area > bestArea) {
+                        bestArea = cellData[ni].area;
+                        bestNeighbour = ni;
+                    }
+                }
+                if (bestNeighbour >= 0) {
+                    cellSunHours[si] = cellSunHours[bestNeighbour];
+                }
+            }
+        }
+
         // ─── RAY CAST SUN HOURS (uses cached cell data) ───
         async function runTerrainAnalysis(latitude, longitude, timeStep, dateStr, cellData) {
             if (!shadowBVH) {
-                throw new Error('Shadow casters must be set');
+                throw new Error('Shadow BVH not built');
             }
 
             const sunPositions = getSunPositions(latitude, longitude, dateStr, timeStep);
@@ -2937,9 +3670,12 @@
 
                     for (let j = i; j < end; j++) {
                         const cd = cellData[j];
-                        const ox = cd.centroid.x + cd.normal.x * 0.01;
-                        const oy = cd.centroid.y + cd.normal.y * 0.01;
-                        const oz = cd.centroid.z + cd.normal.z * 0.01;
+                        // Skip sliver cells — they inherit values later
+                        if (cd._isSliver) continue;
+
+                        const ox = cd.centroid.x + cd.normal.x * 0.05;
+                        const oy = cd.centroid.y + cd.normal.y * 0.05;
+                        const oz = cd.centroid.z + cd.normal.z * 0.05;
 
                         if (!shadowBVH.intersectsAny(ox, oy, oz, dx, dy, dz)) {
                             cellSunHours[j] += timeStep;
@@ -2955,6 +3691,9 @@
                 }
             }
 
+            // Apply small cell inheritance (sliver cells get neighbour values)
+            applySmallCellInheritance(cellData, cellSunHours);
+
             // Compute summary statistics
             let totalArea = 0;
             let minHours = Infinity, maxHours = -Infinity;
@@ -2984,31 +3723,80 @@
             };
         }
 
+        // ─── LEGEND NOTCH BUILDER ───
+        function buildLegendNotches(timeStep) {
+            const bar = document.getElementById('legend-bar');
+            const topLabel = document.getElementById('legend-top-label');
+            // Clear existing notches
+            bar.querySelectorAll('.legend-notch').forEach(n => n.remove());
+
+            const maxH = legendMaxHours;
+
+            // Rebuild the CSS gradient to match the current colour ramp
+            const stops = HEAT_COLOUR_STOPS.map(([s, r, g, b]) => {
+                const pct = (s * 100).toFixed(1);
+                return `rgb(${Math.round(r*255)},${Math.round(g*255)},${Math.round(b*255)}) ${pct}%`;
+            });
+            bar.style.background = `linear-gradient(to top, ${stops.join(', ')})`;
+
+            // Always add hour notches
+            for (let h = 1; h < maxH; h++) {
+                const pct = (h / maxH) * 100;
+                const notch = document.createElement('div');
+                notch.className = 'legend-notch hour';
+                notch.style.bottom = pct + '%';
+                notch.title = h + 'h';
+                bar.appendChild(notch);
+            }
+
+            // Add sub-hour notches if timeStep < 1
+            if (timeStep < 1) {
+                for (let t = timeStep; t < maxH; t += timeStep) {
+                    // Skip full hours (already drawn)
+                    if (Math.abs(t - Math.round(t)) < 0.001) continue;
+                    const pct = (t / maxH) * 100;
+                    const notch = document.createElement('div');
+                    notch.className = 'legend-notch sub-hour';
+                    notch.style.bottom = pct + '%';
+                    const mins = Math.round((t % 1) * 60);
+                    notch.title = Math.floor(t) + 'h ' + mins + 'm';
+                    bar.appendChild(notch);
+                }
+            }
+
+            topLabel.textContent = maxH + 'h';
+        }
+
         // ─── HEAT MAP COLOUR GRADIENT ───
-        const HEAT_COLOURS = [
-            [0, 0.15, 0.0, 0.25],
-            [1, 0.8, 0.1, 0.1],
-            [2, 1.0, 0.5, 0.0],
-            [3, 1.0, 0.85, 0.0],
-            [4, 1.0, 1.0, 0.2],
-            [6, 1.0, 1.0, 0.8],
+        // Normalised colour stops (0..1) – scaled to legendMaxHours at paint time
+        const HEAT_COLOUR_STOPS = [
+            [0.00, 0.15, 0.0, 0.25],
+            [0.17, 0.8, 0.1, 0.1],
+            [0.33, 1.0, 0.5, 0.0],
+            [0.50, 1.0, 0.85, 0.0],
+            [0.67, 1.0, 1.0, 0.2],
+            [1.00, 1.0, 1.0, 0.8],
         ];
+        let legendMaxHours = 6; // updated after analysis
 
         function lerpColour(hours) {
-            if (hours <= HEAT_COLOURS[0][0]) return [HEAT_COLOURS[0][1], HEAT_COLOURS[0][2], HEAT_COLOURS[0][3]];
-            if (hours >= HEAT_COLOURS[HEAT_COLOURS.length-1][0]) {
-                const c = HEAT_COLOURS[HEAT_COLOURS.length-1];
+            const t = legendMaxHours > 0 ? hours / legendMaxHours : 0;
+            const clamped = Math.max(0, Math.min(1, t));
+            const stops = HEAT_COLOUR_STOPS;
+            if (clamped <= stops[0][0]) return [stops[0][1], stops[0][2], stops[0][3]];
+            if (clamped >= stops[stops.length-1][0]) {
+                const c = stops[stops.length-1];
                 return [c[1], c[2], c[3]];
             }
-            for (let i = 0; i < HEAT_COLOURS.length - 1; i++) {
-                const [h0, r0, g0, b0] = HEAT_COLOURS[i];
-                const [h1, r1, g1, b1] = HEAT_COLOURS[i + 1];
-                if (hours >= h0 && hours <= h1) {
-                    const t = (hours - h0) / (h1 - h0);
-                    return [r0 + t * (r1 - r0), g0 + t * (g1 - g0), b0 + t * (b1 - b0)];
+            for (let i = 0; i < stops.length - 1; i++) {
+                const [s0, r0, g0, b0] = stops[i];
+                const [s1, r1, g1, b1] = stops[i + 1];
+                if (clamped >= s0 && clamped <= s1) {
+                    const f = (clamped - s0) / (s1 - s0);
+                    return [r0 + f * (r1 - r0), g0 + f * (g1 - g0), b0 + f * (b1 - b0)];
                 }
             }
-            const c = HEAT_COLOURS[HEAT_COLOURS.length-1];
+            const c = stops[stops.length-1];
             return [c[1], c[2], c[3]];
         }
 
@@ -3018,42 +3806,227 @@
             group.name = 'heatmap_' + (results.season || 'default');
             if (!results.cellData || results.cellData.length === 0) return group;
 
-            const off = 0.02; // 20mm offset above surface
-
-            const tilePositions = [];
-            const tileColors = [];
+            const gridSize = cachedGridSize || 1.0;
 
+            // Build voxel lookup: key → sun hours
+            const voxelHours = new Map();
             for (let i = 0; i < results.cellData.length; i++) {
-                const cd = results.cellData[i];
-                const hours = results.cellSunHours[i];
-                const [r, g, b] = lerpColour(hours);
-                const n = cd.normal;
+                voxelHours.set(results.cellData[i].key, results.cellSunHours[i]);
+            }
+
+            // Determine which meshes to paint:
+            // If IfcOpenShell meshes exist, paint those (high detail display).
+            // Otherwise, fall back to the voxel-clipped triangles.
+            const displayMeshes = analysisMeshes.length > 0 ? analysisMeshes : null;
+
+            if (displayMeshes) {
+                // ─── DUAL-GEOMETRY MODE ───
+                // Paint IfcOpenShell triangles using voxel sun hours lookup
+                const off = 0.005; // small offset to prevent z-fighting
+
+                const tilePositions = [];
+                const tileColors = [];
+
+                // Debug counters
+                let dbgExact = 0, dbgNeighbour = 0, dbgMiss = 0, dbgDegen = 0;
+                let dbgTotalTris = 0;
+                const hoursHist = [0, 0, 0, 0, 0, 0]; // 0h, 0-1h, 1-2h, 2-4h, 4-6h, 6h+
+
+                for (const mesh of displayMeshes) {
+                    mesh.updateWorldMatrix(true, false);
+                    const wm = mesh.matrixWorld;
+                    const geo = mesh.geometry;
+                    const pos = geo.attributes.position.array;
+                    const idx = geo.index ? geo.index.array : null;
+                    const faceCount = idx ? idx.length / 3 : pos.length / 9;
+
+                    for (let f = 0; f < faceCount; f++) {
+                        dbgTotalTris++;
+                        const i0 = idx ? idx[f*3]*3 : f*9;
+                        const i1 = idx ? idx[f*3+1]*3 : f*9+3;
+                        const i2 = idx ? idx[f*3+2]*3 : f*9+6;
+
+                        // Get world-space positions
+                        const a = new THREE.Vector3(pos[i0], pos[i0+1], pos[i0+2]).applyMatrix4(wm);
+                        const b = new THREE.Vector3(pos[i1], pos[i1+1], pos[i1+2]).applyMatrix4(wm);
+                        const c = new THREE.Vector3(pos[i2], pos[i2+1], pos[i2+2]).applyMatrix4(wm);
+
+                        // Check for degenerate triangle
+                        const e1x = b.x-a.x, e1y = b.y-a.y, e1z = b.z-a.z;
+                        const e2x = c.x-a.x, e2y = c.y-a.y, e2z = c.z-a.z;
+                        let nx = e1y*e2z - e1z*e2y;
+                        let ny = e1z*e2x - e1x*e2z;
+                        let nz = e1x*e2y - e1y*e2x;
+                        const nlen = Math.sqrt(nx*nx + ny*ny + nz*nz);
+                        if (nlen < 1e-10) { dbgDegen++; continue; }
+                        nx /= nlen; ny /= nlen; nz /= nlen;
+
+                        // Triangle centroid
+                        const cx = (a.x + b.x + c.x) / 3;
+                        const cy = (a.y + b.y + c.y) / 3;
+                        const cz = (a.z + b.z + c.z) / 3;
+
+                        // Look up which voxel cell this triangle centroid falls in
+                        const vix = Math.floor(cx / gridSize);
+                        const viy = Math.floor(cy / gridSize);
+                        const viz = Math.floor(cz / gridSize);
+                        const vkey = vix + ',' + viy + ',' + viz;
+
+                        let hours = voxelHours.get(vkey);
+                        let matchType = 'exact';
+
+                        // If no exact match, check the 26 neighbours (triangle may straddle boundary)
+                        if (hours === undefined) {
+                            matchType = 'neighbour';
+                            for (let dx = -1; dx <= 1 && hours === undefined; dx++) {
+                                for (let dy = -1; dy <= 1 && hours === undefined; dy++) {
+                                    for (let dz = -1; dz <= 1 && hours === undefined; dz++) {
+                                        if (dx === 0 && dy === 0 && dz === 0) continue;
+                                        const nkey = (vix+dx) + ',' + (viy+dy) + ',' + (viz+dz);
+                                        const nh = voxelHours.get(nkey);
+                                        if (nh !== undefined) hours = nh;
+                                    }
+                                }
+                            }
+                        }
+
+                        let r, g, b2;
+                        if (hours === undefined) {
+                            // No match — render in magenta so it's visible in debug
+                            dbgMiss++;
+                            r = 1.0; g = 0.0; b2 = 1.0; // magenta
+                        } else {
+                            if (matchType === 'exact') dbgExact++; else dbgNeighbour++;
+                            [r, g, b2] = lerpColour(hours);
+                            // Hours histogram
+                            if (hours === 0) hoursHist[0]++;
+                            else if (hours < 1) hoursHist[1]++;
+                            else if (hours < 2) hoursHist[2]++;
+                            else if (hours < 4) hoursHist[3]++;
+                            else if (hours < 6) hoursHist[4]++;
+                            else hoursHist[5]++;
+                        }
 
-                for (const tri of cd.tris) {
-                    for (const v of tri) {
                         tilePositions.push(
-                            v[0] + n.x * off,
-                            v[1] + n.y * off,
-                            v[2] + n.z * off
+                            a.x + nx*off, a.y + ny*off, a.z + nz*off,
+                            b.x + nx*off, b.y + ny*off, b.z + nz*off,
+                            c.x + nx*off, c.y + ny*off, c.z + nz*off
                         );
-                        tileColors.push(r, g, b);
+                        tileColors.push(r, g, b2, r, g, b2, r, g, b2);
                     }
                 }
-            }
 
-            if (tilePositions.length > 0) {
-                const tileGeo = new THREE.BufferGeometry();
-                tileGeo.setAttribute('position', new THREE.Float32BufferAttribute(tilePositions, 3));
-                tileGeo.setAttribute('color', new THREE.Float32BufferAttribute(tileColors, 3));
+                if (tilePositions.length > 0) {
+                    const tileGeo = new THREE.BufferGeometry();
+                    tileGeo.setAttribute('position', new THREE.Float32BufferAttribute(tilePositions, 3));
+                    tileGeo.setAttribute('color', new THREE.Float32BufferAttribute(tileColors, 3));
+                    tileGeo.computeVertexNormals();
 
-                const tileMat = new THREE.MeshBasicMaterial({
-                    vertexColors: true,
-                    side: THREE.DoubleSide,
+                    const tileMat = new THREE.MeshBasicMaterial({
+                        vertexColors: true,
+                        side: THREE.DoubleSide,
+                    });
+
+                    const tileMesh = new THREE.Mesh(tileGeo, tileMat);
+                    tileMesh.name = 'heatmap_mesh';
+                    group.add(tileMesh);
+                }
+
+                // Populate debug console
+                const webifcBBox = allMeshes.length > 0 ? computeBBox(allMeshes) : null;
+                const ifcosBBox = analysisMeshes.length > 0 ? computeBBox(analysisMeshes) : null;
+
+                updateDebugConsole({
+                    webifcMeshCount: allMeshes.length,
+                    webifcTris: webifcBBox ? webifcBBox.tris : 0,
+                    ifcosMeshCount: analysisMeshes.length,
+                    ifcosTris: ifcosBBox ? ifcosBBox.tris : 0,
+                    webifcBBox,
+                    ifcosBBox,
+                    gridSize,
+                    voxelCellCount: voxelHours.size,
+                    totalDisplayTris: dbgTotalTris,
+                    exactMatches: dbgExact,
+                    neighbourMatches: dbgNeighbour,
+                    misses: dbgMiss,
+                    degenerate: dbgDegen,
+                    hoursDistribution: [
+                        ['0h exactly', hoursHist[0]],
+                        ['0-1h', hoursHist[1]],
+                        ['1-2h', hoursHist[2]],
+                        ['2-4h', hoursHist[3]],
+                        ['4-6h', hoursHist[4]],
+                        ['6h+', hoursHist[5]],
+                    ],
+                    mode: 'dual-geometry',
                 });
+            } else {
+                // ─── VOXEL-ONLY MODE (fallback, no IfcOpenShell) ───
+                // Paint clipped voxel triangles directly
+                const off = 0.02;
+                const tilePositions = [];
+                const tileColors = [];
+
+                for (let i = 0; i < results.cellData.length; i++) {
+                    const cd = results.cellData[i];
+                    const hours = results.cellSunHours[i];
+                    const [r, g, b] = lerpColour(hours);
+                    const n = cd.normal;
+
+                    for (const tri of cd.tris) {
+                        for (const v of tri) {
+                            tilePositions.push(
+                                v[0] + n.x * off,
+                                v[1] + n.y * off,
+                                v[2] + n.z * off
+                            );
+                            tileColors.push(r, g, b);
+                        }
+                    }
+                }
+
+                if (tilePositions.length > 0) {
+                    const tileGeo = new THREE.BufferGeometry();
+                    tileGeo.setAttribute('position', new THREE.Float32BufferAttribute(tilePositions, 3));
+                    tileGeo.setAttribute('color', new THREE.Float32BufferAttribute(tileColors, 3));
+                    tileGeo.computeVertexNormals();
+
+                    const tileMat = new THREE.MeshBasicMaterial({
+                        vertexColors: true,
+                        side: THREE.DoubleSide,
+                    });
 
-                const tileMesh = new THREE.Mesh(tileGeo, tileMat);
-                tileMesh.name = 'heatmap_mesh';
-                group.add(tileMesh);
+                    const tileMesh = new THREE.Mesh(tileGeo, tileMat);
+                    tileMesh.name = 'heatmap_mesh';
+                    group.add(tileMesh);
+                }
+
+                // Debug console for voxel-only mode
+                let voxelTris = 0;
+                for (let i = 0; i < results.cellData.length; i++) {
+                    voxelTris += results.cellData[i].tris.length;
+                }
+
+                updateDebugConsole({
+                    webifcMeshCount: allMeshes.length,
+                    webifcTris: allMeshes.reduce((s, m) => {
+                        const idx = m.geometry.index;
+                        return s + (idx ? idx.count / 3 : m.geometry.attributes.position.count / 3);
+                    }, 0),
+                    ifcosMeshCount: 0,
+                    ifcosTris: 0,
+                    webifcBBox: allMeshes.length > 0 ? computeBBox(allMeshes) : null,
+                    ifcosBBox: null,
+                    gridSize,
+                    voxelCellCount: voxelHours.size,
+                    totalDisplayTris: voxelTris,
+                    exactMatches: voxelTris,
+                    neighbourMatches: 0,
+                    misses: 0,
+                    degenerate: 0,
+                    hoursDistribution: null,
+                    mode: 'voxel-only',
+                });
             }
 
             return group;
@@ -3062,8 +4035,8 @@
         // ─── RUN ANALYSIS (multi-season) ───
         async function runAnalysis() {
             const btn = document.getElementById('run-btn');
-            if (!ifcLoaded || selectedGroundMeshes.length === 0) {
-                alert('Please complete previous steps first.');
+            if (!ifcLoaded) {
+                alert('Please import an IFC file first.');
                 return;
             }
 
@@ -3092,8 +4065,11 @@
                 const lng = parseFloat(document.getElementById('longitude').value);
                 const timeStep = parseFloat(document.getElementById('time_step').value);
 
-                // Prepare grid cells ONCE (merge + slice + top-surface extraction)
-                const cellData = await prepareGridCells();
+                // Build BVH from all scene geometry
+                buildShadowBVH();
+
+                // Prepare voxel cells (voxelise + outer shell + clip + probe placement)
+                const cellData = await prepareVoxelCells();
 
                 for (let si = 0; si < seasons.length; si++) {
                     const season = seasons[si];
@@ -3112,6 +4088,27 @@
                     hm.visible = false; // hide initially
                 }
 
+                // Compute global max hours across all seasons, round up to next whole hour
+                let globalMax = 0;
+                for (const s of seasons) {
+                    const mx = parseFloat(seasonResults[s].summary.max_hours);
+                    if (mx > globalMax) globalMax = mx;
+                }
+                legendMaxHours = Math.max(1, Math.ceil(globalMax));
+
+                // Rebuild heatmaps now that legendMaxHours is set
+                for (const s of seasons) {
+                    scene.remove(seasonHeatmaps[s]);
+                    seasonHeatmaps[s].traverse(c => {
+                        if (c.geometry) c.geometry.dispose();
+                        if (c.material) c.material.dispose();
+                    });
+                    const hm = createHeatmapGroup(seasonResults[s]);
+                    seasonHeatmaps[s] = hm;
+                    scene.add(hm);
+                    hm.visible = false;
+                }
+
                 // Show first analysed season
                 visibleSeason = seasons[0];
                 seasonHeatmaps[visibleSeason].visible = true;
@@ -3133,8 +4130,9 @@
                     switcher.classList.remove('visible');
                 }
 
-                // Show colour legend
+                // Show colour legend with notches
                 document.getElementById('colour-legend').classList.add('visible');
+                buildLegendNotches(timeStep);
 
                 const totalCells = seasonResults[visibleSeason].cellData.length;
                 showStatus(`Analysis complete \u2014 ${seasons.length} season(s), ${totalCells} grid cells`);
@@ -3145,7 +4143,10 @@
                     const label = s === 'spring' ? 'Spr' : s === 'winter' ? 'Win' : 'Sum';
                     return label + ' ' + seasonResults[s].summary.avg_hours + 'h';
                 });
-                completeStep(5, avgList.join(' | '));
+                // Complete step 4 which opens step 5 (results)
+                completeStep(4, '');
+                const s5sum = document.getElementById('step5-summary');
+                if (s5sum) s5sum.textContent = avgList.join(' | ');
 
                 // Hide the IFC meshes so only heatmap is visible
                 hideCalculationMeshes();
@@ -3194,9 +4195,39 @@
                 // Convert vertex-color MeshBasicMaterial to MeshStandardMaterial for GLB compat
                 hmClone.traverse(c => {
                     if (c.isMesh && c.material) {
+                        // Ensure consistent upward-facing normals by flipping
+                        // triangles whose face normal points downward (negative Y)
+                        const geo = c.geometry;
+                        const pos = geo.attributes.position.array;
+                        const col = geo.attributes.color ? geo.attributes.color.array : null;
+                        const v0 = new THREE.Vector3(), v1 = new THREE.Vector3(), v2 = new THREE.Vector3();
+                        for (let i = 0; i < pos.length; i += 9) {
+                            v0.set(pos[i], pos[i+1], pos[i+2]);
+                            v1.set(pos[i+3], pos[i+4], pos[i+5]);
+                            v2.set(pos[i+6], pos[i+7], pos[i+8]);
+                            const edge1 = new THREE.Vector3().subVectors(v1, v0);
+                            const edge2 = new THREE.Vector3().subVectors(v2, v0);
+                            const faceNormal = new THREE.Vector3().crossVectors(edge1, edge2);
+                            if (faceNormal.y < 0) {
+                                // Swap v1 and v2 to flip winding
+                                pos[i+3] = v2.x; pos[i+4] = v2.y; pos[i+5] = v2.z;
+                                pos[i+6] = v1.x; pos[i+7] = v1.y; pos[i+8] = v1.z;
+                                if (col) {
+                                    // Color array has same layout as position (3 per vertex, 9 per tri)
+                                    const r1 = col[i+3], g1 = col[i+4], b1 = col[i+5];
+                                    const r2 = col[i+6], g2 = col[i+7], b2 = col[i+8];
+                                    col[i+3] = r2; col[i+4] = g2; col[i+5] = b2;
+                                    col[i+6] = r1; col[i+7] = g1; col[i+8] = b1;
+                                }
+                            }
+                        }
+                        geo.attributes.position.needsUpdate = true;
+                        if (col) geo.attributes.color.needsUpdate = true;
+                        geo.computeVertexNormals();
+
                         const newMat = new THREE.MeshStandardMaterial({
                             vertexColors: c.material.vertexColors,
-                            side: THREE.DoubleSide,
+                            side: THREE.FrontSide,
                             roughness: 1.0,
                             metalness: 0.0,
                         });
@@ -3264,22 +4295,33 @@
                 const savedRotateEnabled = controls.enableRotate;
 
                 // Set up ortho camera for true plan view
-                updateOrthoCamera();
-                // Compute tight bounds around heatmap/building
-                const targetGroup = buildingGroup || scene;
-                const bb = new THREE.Box3().setFromObject(targetGroup);
+                // Compute tight bounds around heatmap + selected ground meshes
+                const bb = new THREE.Box3();
+                // Include all season heatmaps
+                for (const group of Object.values(seasonHeatmaps)) {
+                    bb.expandByObject(group);
+                }
+                // Include all meshes for context
+                for (const mesh of allMeshes) {
+                    mesh.updateWorldMatrix(true, false);
+                    bb.expandByObject(mesh);
+                }
+                // Fallback to building group if bounds are empty
+                if (bb.isEmpty() && buildingGroup) {
+                    bb.setFromObject(buildingGroup);
+                }
                 const cx = (bb.min.x + bb.max.x) / 2;
                 const cz = (bb.min.z + bb.max.z) / 2;
                 const extX = (bb.max.x - bb.min.x) / 2 + 2;
                 const extZ = (bb.max.z - bb.min.z) / 2 + 2;
 
-                // Fit ortho camera to bounds
+                // Fit ortho camera to bounds (frustum is camera-local, position handles centering)
                 const planAspect = (pageW - 40) / (pageH - 60);
                 const orthoExtent = Math.max(extX, extZ / planAspect, extZ, extX / planAspect);
-                orthoCamera.left = cx - orthoExtent * planAspect;
-                orthoCamera.right = cx + orthoExtent * planAspect;
-                orthoCamera.top = cz + orthoExtent;
-                orthoCamera.bottom = cz - orthoExtent;
+                orthoCamera.left = -orthoExtent * planAspect;
+                orthoCamera.right = orthoExtent * planAspect;
+                orthoCamera.top = orthoExtent;
+                orthoCamera.bottom = -orthoExtent;
                 orthoCamera.position.set(cx, 500, cz);
                 orthoCamera.lookAt(cx, 0, cz);
                 orthoCamera.updateProjectionMatrix();
@@ -3294,11 +4336,9 @@
                     return { x: px, y: py };
                 }
 
-                // Collect non-ground mesh edges for vector overlay
-                const groundSet = new Set(selectedGroundMeshes);
+                // Collect mesh edges for vector overlay
                 const edgeLines = []; // [{x1,y1,x2,y2}, ...]
                 for (const mesh of allMeshes) {
-                    if (groundSet.has(mesh)) continue;
                     mesh.updateWorldMatrix(true, false);
                     const wm = mesh.matrixWorld;
                     const edges = new THREE.EdgesGeometry(mesh.geometry, 15);
@@ -3322,7 +4362,6 @@
                     // ── Render heatmap-only plan view as PNG ──
                     // Hide ALL meshes, show only this season's heatmap
                     for (const mesh of allMeshes) mesh.visible = false;
-                    for (const hl of groundHighlights) hl.visible = false;
                     for (const [k, group] of Object.entries(seasonHeatmaps)) {
                         group.visible = (k === season);
                     }
@@ -3366,12 +4405,10 @@
                     doc.text('Generated: ' + new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' }), pageW - 20, pageH - 5, { align: 'right' });
                 }
 
-                // Restore scene state — show non-ground meshes, hide ground (step 5)
-                const pdfGroundSet = new Set(selectedGroundMeshes);
+                // Restore scene state — hide all meshes (results view)
                 for (const mesh of allMeshes) {
-                    mesh.visible = !pdfGroundSet.has(mesh);
+                    mesh.visible = false;
                 }
-                for (const hl of groundHighlights) hl.visible = false;
                 for (const [k, group] of Object.entries(seasonHeatmaps)) {
                     group.visible = (k === visibleSeason);
                 }
@@ -3398,7 +4435,7 @@
 
         function toggleBboxMode() {
             bboxMode = !bboxMode;
-            useEntireGroundMesh = false;
+            useEntireBounds = false;
             const overlay = document.getElementById('bbox-overlay');
             const viewport = document.getElementById('viewport');
             const btn = document.getElementById('bbox-btn');
@@ -3422,6 +4459,7 @@
                 controls.enabled = true;
                 removeTempBbox();
             }
+            enableRunButton();
         }
 
         function removeTempBbox() {
@@ -3627,7 +4665,6 @@
             if (key === 'escape') {
                 if (flyMode) { enableOrbitMode(); return; }
                 if (bboxMode) toggleBboxMode();
-                if (pickMode) setPickMode(false);
                 return;
             }
 
@@ -3783,7 +4820,7 @@
                 '',
             ].join('\n');
             const link = document.getElementById('bug-report-link');
-            link.href = 'mailto:jake@jakewhitearchitecture.com?subject=' +
+            link.href = 'mailto:sunform@jakewhitearchitecture.com?subject=' +
                 encodeURIComponent('SunForm Bug Report') +
                 '&body=' + encodeURIComponent(body);
         }
@@ -3792,8 +4829,7 @@
         function updateDisclaimerAccept() {
             const c1 = document.getElementById('disclaimer-check1').checked;
             const c2 = document.getElementById('disclaimer-check2').checked;
-            const c3 = document.getElementById('disclaimer-check3').checked;
-            const allChecked = c1 && c2 && c3;
+            const allChecked = c1 && c2;
             document.getElementById('disclaimer-accept-btn').disabled = !allChecked;
         }
 
@@ -3801,6 +4837,26 @@
             document.getElementById('disclaimer-modal').classList.add('hidden');
         }
 
+        // ─── MOBILE SLIDE PANEL ───
+        function toggleMobilePanel() {
+            const panel = document.getElementById('main-panel');
+            const backdrop = document.getElementById('panel-backdrop');
+            const btn = document.getElementById('hamburger-btn');
+            const isOpen = panel.classList.contains('open');
+            if (isOpen) {
+                closeMobilePanel();
+            } else {
+                panel.classList.add('open');
+                backdrop.classList.add('visible');
+                btn.classList.add('active');
+            }
+        }
+        function closeMobilePanel() {
+            document.getElementById('main-panel').classList.remove('open');
+            document.getElementById('panel-backdrop').classList.remove('visible');
+            document.getElementById('hamburger-btn').classList.remove('active');
+        }
+
         // ─── DOWNLOAD CONFIRMATION ───
         let pendingDownloadType = null;
 
@@ -3830,29 +4886,16 @@
 
         // ─── MESH VISIBILITY MANAGEMENT ───
         function hideCalculationMeshes() {
-            // Hide only the ground meshes used for calculation (to avoid aliasing)
-            // Keep all non-ground building meshes visible
-            const groundSet = new Set(selectedGroundMeshes);
+            // Hide ALL meshes when showing results
             for (const mesh of allMeshes) {
-                if (groundSet.has(mesh)) {
-                    mesh.visible = false;
-                }
-            }
-            for (const hl of groundHighlights) {
-                hl.visible = false;
+                mesh.visible = false;
             }
         }
 
         function showCalculationMeshes() {
-            // Reinstate ground mesh visibility (e.g. when going back to select mesh)
-            const groundSet = new Set(selectedGroundMeshes);
+            // Show ALL meshes
             for (const mesh of allMeshes) {
-                if (groundSet.has(mesh)) {
-                    mesh.visible = true;
-                }
-            }
-            for (const hl of groundHighlights) {
-                hl.visible = true;
+                mesh.visible = true;
             }
         }
 
@@ -3951,7 +4994,7 @@
 
         function handleRayProbeClick(event) {
             // Only works when results are showing
-            if (currentStep !== 6) return;
+            if (currentStep !== 5) return;
             if (!seasonResults[visibleSeason]) return;
 
             const container = document.getElementById('viewport');
@@ -4086,9 +5129,186 @@
         // ─── INIT ───
         initThree();
         initWebIfc();
+        initIfcosWorker();  // Start Pyodide+IfcOpenShell download in background worker
         initProbeDrag();
-        // Leaflet must init after DOM is ready and step-5 is visible at least once
-        // We defer map init to when step 4 opens
+        // ─── BETA FEEDBACK WIZARD ───
+        let bfChallenge = {};  // stores the generated challenge data
+
+        function openBetaFeedback() {
+            const lat = parseFloat(document.getElementById('latitude').value) || 51.5074;
+            const lng = parseFloat(document.getElementById('longitude').value) || -0.1278;
+
+            // Pick a random date spread across the year
+            const month = Math.floor(Math.random() * 12);
+            const day = Math.floor(Math.random() * 28) + 1;
+            const year = new Date().getFullYear();
+            const dateStr = year + '-' + String(month + 1).padStart(2, '0') + '-' + String(day).padStart(2, '0');
+
+            // Get all sun positions for that date at 1-hour steps
+            const positions = getSunPositions(lat, lng, dateStr, 1);
+            if (positions.length === 0) {
+                alert('No visible sun positions found for this date and location. Please set your site coordinates first.');
+                return;
+            }
+
+            // Pick a random hour from those where the sun is up
+            const pick = positions[Math.floor(Math.random() * positions.length)];
+
+            bfChallenge = {
+                lat: lat,
+                lng: lng,
+                dateStr: dateStr,
+                hour: pick.hour,
+                localHour: null,  // set below after BST calc
+                calcAzimuth: pick.azimuth,
+                calcAltitude: pick.altitude
+            };
+
+            // Convert UTC hour to local clock time (UK: UTC in winter, UTC+1 in BST)
+            function isUKBST(dateStr) {
+                const y = parseInt(dateStr.split('-')[0]);
+                const m = parseInt(dateStr.split('-')[1]);
+                const d = parseInt(dateStr.split('-')[2]);
+                if (m < 3 || m > 10) return false;
+                if (m > 3 && m < 10) return true;
+                // March: BST starts last Sunday
+                if (m === 3) {
+                    const lastDay = new Date(y, 2, 31).getDay();
+                    const lastSun = 31 - lastDay;
+                    return d >= lastSun;
+                }
+                // October: BST ends last Sunday
+                const lastDay = new Date(y, 9, 31).getDay();
+                const lastSun = 31 - lastDay;
+                return d < lastSun;
+            }
+
+            const bstOffset = isUKBST(dateStr) ? 1 : 0;
+            const localHour = pick.hour + bstOffset;
+            bfChallenge.localHour = localHour;
+            bfChallenge.utcOffset = bstOffset;
+
+            // Build SunCalc URL: https://www.suncalc.org/#/{lat},{lon},{zoom}/{YYYY.MM.DD}/{HH:MM}/1/3
+            const suncalcDate = dateStr.replace(/-/g, '.');
+            const suncalcTime = String(localHour).padStart(2, '0') + ':00';
+            const suncalcUrl = 'https://www.suncalc.org/#/' + lat.toFixed(4) + ',' + lng.toFixed(4) + ',9/' + suncalcDate + '/' + suncalcTime + '/1/3';
+            document.getElementById('bf-suncalc-link').href = suncalcUrl;
+
+            // Populate the wizard
+            document.getElementById('bf-lat').textContent = lat.toFixed(4);
+            document.getElementById('bf-lng').textContent = lng.toFixed(4);
+            document.getElementById('bf-date').textContent = dateStr;
+            document.getElementById('bf-time').textContent = suncalcTime;
+            document.getElementById('bf-user-azimuth').value = '';
+            document.getElementById('bf-user-altitude').value = '';
+
+            // Show step 1, hide step 2
+            document.getElementById('bf-step-1').style.display = '';
+            document.getElementById('bf-step-2').style.display = 'none';
+            document.getElementById('beta-feedback-modal').classList.remove('hidden');
+        }
+
+        function closeBetaFeedback() {
+            document.getElementById('beta-feedback-modal').classList.add('hidden');
+        }
+
+        function checkBetaFeedback() {
+            const userAz = parseFloat(document.getElementById('bf-user-azimuth').value);
+            const userAlt = parseFloat(document.getElementById('bf-user-altitude').value);
+            if (isNaN(userAz) || isNaN(userAlt)) {
+                alert('Please enter both azimuth and altitude values.');
+                return;
+            }
+
+            const calcAz = bfChallenge.calcAzimuth;
+            const calcAlt = bfChallenge.calcAltitude;
+            const diffAz = Math.abs(userAz - calcAz);
+            const diffAlt = Math.abs(userAlt - calcAlt);
+            const pctAz = calcAz !== 0 ? (diffAz / Math.abs(calcAz)) * 100 : diffAz;
+            let pctAlt = calcAlt !== 0 ? (diffAlt / Math.abs(calcAlt)) * 100 : diffAlt;
+
+            // For near-horizon altitudes, use absolute difference instead of percentage
+            if (Math.abs(calcAlt) < 5) {
+                // When altitude < 5°, percentage is misleading; use degree threshold instead
+                // Treat <0.5° diff as good, <1° as acceptable
+                pctAlt = diffAlt <= 0.5 ? 0.5 : diffAlt <= 1 ? 1.5 : 3;
+            }
+
+            // Store for email
+            bfChallenge.userAzimuth = userAz;
+            bfChallenge.userAltitude = userAlt;
+            bfChallenge.diffAz = diffAz;
+            bfChallenge.diffAlt = diffAlt;
+
+            // Populate results
+            document.getElementById('bf-user-az-result').textContent = userAz.toFixed(2) + '\u00b0';
+            document.getElementById('bf-user-alt-result').textContent = userAlt.toFixed(2) + '\u00b0';
+            document.getElementById('bf-calc-az-result').textContent = calcAz.toFixed(2) + '\u00b0';
+            document.getElementById('bf-calc-alt-result').textContent = calcAlt.toFixed(2) + '\u00b0';
+
+            const diffAzEl = document.getElementById('bf-diff-az');
+            const diffAltEl = document.getElementById('bf-diff-alt');
+            diffAzEl.textContent = diffAz.toFixed(2) + '\u00b0 (' + pctAz.toFixed(1) + '%)';
+            diffAltEl.textContent = diffAlt.toFixed(2) + '\u00b0 (' + pctAlt.toFixed(1) + '%)';
+            diffAzEl.style.color = pctAz <= 1 ? '#4CAF50' : pctAz <= 2 ? '#FFA726' : '#FF5252';
+            diffAltEl.style.color = pctAlt <= 1 ? '#4CAF50' : pctAlt <= 2 ? '#FFA726' : '#FF5252';
+
+            const maxPct = Math.max(pctAz, pctAlt);
+            const verdict = document.getElementById('bf-verdict');
+            if (maxPct <= 1) {
+                verdict.textContent = 'Good match — within 1%';
+                verdict.style.background = 'rgba(76,175,80,0.15)';
+                verdict.style.color = '#4CAF50';
+            } else if (maxPct <= 2) {
+                verdict.textContent = 'Acceptable match — within 2%';
+                verdict.style.background = 'rgba(255,167,38,0.15)';
+                verdict.style.color = '#FFA726';
+            } else {
+                verdict.textContent = 'Significant difference detected';
+                verdict.style.background = 'rgba(255,82,82,0.15)';
+                verdict.style.color = '#FF5252';
+            }
+
+            // Switch to step 2
+            document.getElementById('bf-step-1').style.display = 'none';
+            document.getElementById('bf-step-2').style.display = '';
+        }
+
+        function sendBetaFeedback() {
+            const c = bfChallenge;
+            const emailMaxPct = Math.max(
+                c.diffAz / Math.abs(bfChallenge.calcAzimuth) * 100,
+                c.diffAlt / Math.abs(bfChallenge.calcAltitude) * 100
+            );
+            const matchStatus = emailMaxPct <= 1 ? 'GOOD MATCH' : emailMaxPct <= 2 ? 'ACCEPTABLE MATCH' : 'DIFFERENCE DETECTED';
+
+            const subject = encodeURIComponent('SunForm Beta Feedback — ' + matchStatus);
+            const body = encodeURIComponent(
+                'SunForm Beta Testing Feedback\n' +
+                '================================\n\n' +
+                'Site Location\n' +
+                '  Latitude:   ' + c.lat.toFixed(4) + '\n' +
+                '  Longitude:  ' + c.lng.toFixed(4) + '\n\n' +
+                'Test Parameters\n' +
+                '  Date:       ' + c.dateStr + '\n' +
+                '  Time:       ' + String(c.localHour).padStart(2, '0') + ':00 (UTC+' + c.utcOffset + ') / ' + String(c.hour).padStart(2, '0') + ':00 (UTC)\n\n' +
+                'User Input (external calculator)\n' +
+                '  Azimuth:    ' + c.userAzimuth.toFixed(2) + '\u00b0\n' +
+                '  Altitude:   ' + c.userAltitude.toFixed(2) + '\u00b0\n\n' +
+                'SunForm Calculated\n' +
+                '  Azimuth:    ' + c.calcAzimuth.toFixed(2) + '\u00b0\n' +
+                '  Altitude:   ' + c.calcAltitude.toFixed(2) + '\u00b0\n\n' +
+                'Difference\n' +
+                '  Azimuth:    ' + c.diffAz.toFixed(2) + '\u00b0\n' +
+                '  Altitude:   ' + c.diffAlt.toFixed(2) + '\u00b0\n\n' +
+                'Verdict: ' + matchStatus + '\n'
+            );
+
+            window.location.href = 'mailto:sunform@jakewhitearchitecture.com?subject=' + subject + '&body=' + body;
+        }
+
+        // Leaflet must init after DOM is ready
+        // We defer map init to when step 4 (Site Location) opens
         let mapInitialized = false;
     </script>
 </body>
```
