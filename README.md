# SunForm

Free, browser-based sun hours and solar shading analysis for architects and designers.

SunForm imports an IFC or BIM model and visualises direct sunlight hours across roofs, ground surfaces and vertical facades as a smooth, per-pixel 3D heatmap. Everything runs client-side in the browser: there is no login, no upload of your model to a server, and nothing to install for end users.

Live tool: [www.jakewhitearchitecture.com/sunform](https://www.jakewhitearchitecture.com/sunform)

## Features

- Sun hours analysis on roofs, ground surfaces and vertical facades
- Solar shading and shadow studies driven by real sun paths
- Direct IFC and BIM model import via [web-ifc](https://github.com/ThatOpen/engine_web-ifc)
- Smooth, per-pixel 3D sunlight heatmap with no visible grid
- Seasonal comparison across winter, spring, autumn and summer
- Click any surface to probe its sun hours
- Export coloured GLB models and dimensioned PDF plans

SunForm is beta software and an indicative design aid only. It does not verify compliance and is not a substitute for professional daylighting or right to light consultancy. All outputs must be independently checked by a competent person before use.

## How it works

The entire application is a single self-contained `index.html` file. All geometry
processing and ray casting runs in the browser:

- **Rendering** uses [Three.js](https://threejs.org/) r128 (loaded via classic
  script tags).
- **IFC import** uses web-ifc compiled to WebAssembly.
- **Analysis** subdivides each surface to a maximum edge length, casts a ray from
  every vertex toward the sun at each time step (accelerated with a BVH), and maps
  the resulting sun hours to a colour ramp in a GLSL shader. Ray casting runs in a
  Web Worker so the 3D view stays interactive while seasons compute in the
  background.

`app.py` is a minimal Flask server whose only job is to serve `index.html` with
no-cache headers. It performs no analysis.

## Running locally

```bash
pip install -r requirements.txt
python app.py
```

Then open <http://localhost:8080>.

Because the tool is a single static file, you can also open `index.html` directly
in a browser, or serve the folder with any static file server, for example:

```bash
python -m http.server 8080
```

## Analysis engine and tests

`sunform_engine.py` is a deterministic Python mirror of the browser analysis
pipeline (subdivision, unique-vertex building, vertex normals and Voronoi areas,
per-vertex sun hours, self-shadow exclusion, coincident-face de-duplication and
field smoothing). It exists as a reference implementation and to make the core
maths testable outside the browser.

Run the test suite with:

```bash
pip install pytest
pytest
```

## Project layout

| Path                | Purpose                                                        |
| ------------------- | ------------------------------------------------------------- |
| `index.html`        | The entire client-side application (UI, rendering, analysis)  |
| `app.py`            | Minimal Flask server that serves `index.html`                 |
| `sunform_engine.py` | Deterministic Python mirror of the analysis pipeline          |
| `tests/`            | pytest regression tests for the engine                        |
| `sunform-logo.png`  | Logo asset                                                     |
| `requirements.txt`  | Python dependencies (Flask)                                   |

## License

Released under the [MIT License](LICENSE). Copyright (c) 2026 Jake White Architecture.
