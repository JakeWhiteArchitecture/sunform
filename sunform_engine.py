"""
SunForm — Pure-Python analysis engine.

Mirrors the client-side JavaScript sun position calculator and ray-triangle
intersection logic so they can be tested deterministically with pytest.
"""

import math
from typing import List, Tuple, Optional

Vec3 = Tuple[float, float, float]
Triangle = Tuple[Vec3, Vec3, Vec3]


# ── Sun Position (Spencer 1971) ──────────────────────────────────────────

def get_day_of_year(year: int, month: int, day: int) -> int:
    """Day-of-year (1-indexed)."""
    from datetime import date
    return (date(year, month, day) - date(year, 1, 1)).days + 1


def get_sun_positions(
    latitude: float, longitude: float,
    year: int, month: int, day: int,
    time_step: float = 1.0,
) -> List[dict]:
    """Return list of {'azimuth': deg, 'altitude': deg, 'hour': h} dicts."""
    doy = get_day_of_year(year, month, day)
    lat_rad = math.radians(latitude)

    B = (doy - 1) * 2 * math.pi / 365
    decl = (0.006918
            - 0.399912 * math.cos(B) + 0.070257 * math.sin(B)
            - 0.006758 * math.cos(2*B) + 0.000907 * math.sin(2*B)
            - 0.002697 * math.cos(3*B) + 0.00148 * math.sin(3*B))

    eot = 229.18 * (0.000075
                     + 0.001868 * math.cos(B) - 0.032077 * math.sin(B)
                     - 0.014615 * math.cos(2*B) - 0.04089 * math.sin(2*B))

    positions = []
    hour = 0.0
    while hour < 24.0:
        solar_time = hour + (eot + 4 * longitude) / 60
        hour_angle = math.radians((solar_time - 12) * 15)

        sin_alt = (math.sin(lat_rad) * math.sin(decl)
                   + math.cos(lat_rad) * math.cos(decl) * math.cos(hour_angle))
        altitude = math.asin(max(-1.0, min(1.0, sin_alt)))

        if altitude > 0:
            cos_az = ((math.sin(decl) - math.sin(lat_rad) * sin_alt)
                      / (math.cos(lat_rad) * math.cos(altitude)))
            azimuth = math.acos(max(-1.0, min(1.0, cos_az)))
            if hour_angle > 0:
                azimuth = 2 * math.pi - azimuth

            positions.append({
                'azimuth': math.degrees(azimuth),
                'altitude': math.degrees(altitude),
                'hour': hour,
            })

        hour += time_step

    return positions


def sun_direction(azimuth_deg: float, altitude_deg: float) -> Vec3:
    """Convert azimuth/altitude to a Three.js direction vector (X, Y, Z).

    Azimuth convention: 0°=North, 90°=East, 180°=South, 270°=West (CW from North).
    """
    az = math.radians(azimuth_deg)
    alt = math.radians(altitude_deg)
    ifc_x = math.sin(az) * math.cos(alt)
    ifc_y = math.cos(az) * math.cos(alt)
    ifc_z = math.sin(alt)
    # Three.js: X=east, Y=up, Z=-north
    length = math.sqrt(ifc_x**2 + ifc_z**2 + ifc_y**2)
    return (ifc_x / length, ifc_z / length, -ifc_y / length)


# ── Ray-Triangle Intersection (Möller-Trumbore) ─────────────────────────

def ray_triangle_intersect(
    origin: Vec3, direction: Vec3, tri: Triangle, eps: float = 1e-10,
    min_t: float = 1e-4,
) -> Optional[float]:
    """Return hit distance t, or None if miss."""
    (ax, ay, az), (bx, by, bz), (cx, cy, cz) = tri
    dx, dy, dz = direction

    e1x, e1y, e1z = bx-ax, by-ay, bz-az
    e2x, e2y, e2z = cx-ax, cy-ay, cz-az
    px = dy*e2z - dz*e2y
    py = dz*e2x - dx*e2z
    pz = dx*e2y - dy*e2x
    det = e1x*px + e1y*py + e1z*pz
    if abs(det) < eps:
        return None
    inv_det = 1.0 / det
    tx, ty, tz = origin[0]-ax, origin[1]-ay, origin[2]-az
    u = (tx*px + ty*py + tz*pz) * inv_det
    if u < 0 or u > 1:
        return None
    qx = ty*e1z - tz*e1y
    qy = tz*e1x - tx*e1z
    qz = tx*e1y - ty*e1x
    v = (dx*qx + dy*qy + dz*qz) * inv_det
    if v < 0 or u + v > 1:
        return None
    t = (e2x*qx + e2y*qy + e2z*qz) * inv_det
    if t > min_t:
        return t
    return None


def ray_hits_any_triangle(
    origin: Vec3, direction: Vec3, triangles: List[Triangle],
    min_t: float = 1e-4,
) -> bool:
    """Return True if the ray hits any triangle in the list."""
    for tri in triangles:
        if ray_triangle_intersect(origin, direction, tri, min_t=min_t) is not None:
            return True
    return False


# ── Edge-split subdivision + per-vertex analysis ─────────────────────────

def subdivide_to_max_edge(triangles, max_edge: float = 0.5):
    """Recursively bisect the longest edge of any triangle whose longest edge
    exceeds ``max_edge``. Returns a new list of triangles with no edge longer
    than the threshold. Mirrors the JS subdivideToMaxEdge.
    """
    out = []
    stack = list(triangles)
    max_e2 = max_edge * max_edge
    while stack:
        tri = stack.pop()
        a, b, c = tri[0], tri[1], tri[2]
        e2 = []
        for (p, q) in ((a, b), (b, c), (c, a)):
            dx, dy, dz = q[0]-p[0], q[1]-p[1], q[2]-p[2]
            e2.append(dx*dx + dy*dy + dz*dz)
        longest = max(range(3), key=lambda i: e2[i])
        if e2[longest] <= max_e2:
            out.append((a, b, c))
            continue
        # Bisect the longest edge; split into two triangles
        if longest == 0:
            m = tuple((a[i]+b[i])/2 for i in range(3))
            stack.append((a, m, c))
            stack.append((m, b, c))
        elif longest == 1:
            m = tuple((b[i]+c[i])/2 for i in range(3))
            stack.append((a, b, m))
            stack.append((a, m, c))
        else:
            m = tuple((c[i]+a[i])/2 for i in range(3))
            stack.append((a, b, m))
            stack.append((m, b, c))
    return out


def build_unique_vertices(triangles, quant: float = 1e-4):
    """Deduplicate shared vertices. Returns (vertices, tri_indices) where
    vertices is a list of Vec3 and tri_indices is a list of (i0, i1, i2).
    Adjacent triangles share edge vertices (midpoints quantize identically).
    """
    verts = []
    index_of = {}
    tri_indices = []
    inv = 1.0 / quant
    for tri in triangles:
        idxs = []
        for v in tri[:3]:
            key = (round(v[0]*inv), round(v[1]*inv), round(v[2]*inv))
            i = index_of.get(key)
            if i is None:
                i = len(verts)
                index_of[key] = i
                verts.append((v[0], v[1], v[2]))
            idxs.append(i)
        tri_indices.append(tuple(idxs))
    return verts, tri_indices


def _tri_normal_area(a, b, c):
    e1 = (b[0]-a[0], b[1]-a[1], b[2]-a[2])
    e2 = (c[0]-a[0], c[1]-a[1], c[2]-a[2])
    n = (e1[1]*e2[2]-e1[2]*e2[1], e1[2]*e2[0]-e1[0]*e2[2], e1[0]*e2[1]-e1[1]*e2[0])
    length = math.sqrt(n[0]*n[0] + n[1]*n[1] + n[2]*n[2])
    return n, length * 0.5


def compute_vertex_normals(verts, tri_indices, upward: bool = True):
    """Area-weighted per-vertex normals. With upward=True each face normal is
    sign-flipped to ny >= 0 first (roof/ground convention)."""
    acc = [[0.0, 0.0, 0.0] for _ in verts]
    for (i0, i1, i2) in tri_indices:
        n, area = _tri_normal_area(verts[i0], verts[i1], verts[i2])
        if area == 0:
            continue
        length = area * 2.0
        nx, ny, nz = n[0]/length, n[1]/length, n[2]/length
        if upward and ny < 0:
            nx, ny, nz = -nx, -ny, -nz
        for i in (i0, i1, i2):
            acc[i][0] += nx * area
            acc[i][1] += ny * area
            acc[i][2] += nz * area
    out = []
    for v in acc:
        length = math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])
        if length > 0:
            out.append((v[0]/length, v[1]/length, v[2]/length))
        else:
            out.append((0.0, 1.0, 0.0))
    return out


def compute_vertex_voronoi_areas(verts, tri_indices):
    """One-third of each adjacent triangle's area per vertex."""
    areas = [0.0] * len(verts)
    for (i0, i1, i2) in tri_indices:
        _, area = _tri_normal_area(verts[i0], verts[i1], verts[i2])
        third = area / 3.0
        areas[i0] += third
        areas[i1] += third
        areas[i2] += third
    return areas


def compute_sun_hours_per_vertex(
    verts, normals,
    shadow_triangles: List[Triangle],
    sun_positions: List[dict],
    time_step: float,
    min_t: float = 1e-4,
    offset: float = 0.01,
    batch_size: int = 2000,
) -> List[float]:
    """Per-vertex sun hours. Mirrors the JS loop structure: shared array
    initialised once to zeros; outer loop over sun positions; inner loop over
    vertices in batches; accumulation via hours[j] += time_step. Each vertex
    origin is offset along its own normal.
    """
    n = len(verts)
    hours = [0.0] * n
    sun_dirs = [sun_direction(sp['azimuth'], sp['altitude']) for sp in sun_positions]
    for d in sun_dirs:
        for i in range(0, n, batch_size):
            end = min(i + batch_size, n)
            for j in range(i, end):
                vx, vy, vz = verts[j]
                nx, ny, nz = normals[j]
                origin = (vx + nx*offset, vy + ny*offset, vz + nz*offset)
                if not ray_hits_any_triangle(origin, d, shadow_triangles, min_t=min_t):
                    hours[j] += time_step
    return hours


def smooth_vertex_field(values, tri_indices, iterations: int = 2, lam: float = 0.5):
    """Neighbour-averaged (Laplacian) smoothing of a per-vertex scalar field.

    Per-vertex shadow tests are binary per sun position, so a sharp shadow
    terminator sampled at finite vertex spacing aliases into a zigzag that
    follows the triangulation. Averaging each vertex with its edge-adjacent
    neighbours filters that high-frequency zigzag (roughly a one-vertex-spacing
    penumbra) while leaving flat regions exactly unchanged.
    """
    n = len(values)
    nbrs = [set() for _ in range(n)]
    for (a, b, c) in tri_indices:
        nbrs[a].update((b, c))
        nbrs[b].update((a, c))
        nbrs[c].update((a, b))
    v = list(values)
    for _ in range(iterations):
        nv = list(v)
        for i in range(n):
            if not nbrs[i]:
                continue
            avg = sum(v[j] for j in nbrs[i]) / len(nbrs[i])
            nv[i] = (1 - lam) * v[i] + lam * avg
        v = nv
    return v


# ── Self-shadow exclusion (ignore a surface's own near-coplanar geometry) ──

def ray_hits_real_occluder(
    origin: Vec3, direction: Vec3, triangles: List[Triangle],
    surface_normal: Vec3,
    min_t: float = 1e-4, self_gap: float = 1.0, coplanar_dot: float = 0.9,
) -> bool:
    """Like ``ray_hits_any_triangle`` but ignores the surface's OWN near-coplanar
    geometry — a duplicate/overlapping copy of the very surface the sample sits on.

    A hit is skipped (not treated as shadow) when BOTH:
      - the occluder is nearly parallel to ``surface_normal`` (|n·n| > coplanar_dot), and
      - its perpendicular gap from the origin is small (< ``self_gap`` metres).

    This removes spurious self/duplicate-sheet shadow while keeping genuine
    obstructions: tilted occluders (low |n·n|) and distant parallel surfaces
    (gap >= self_gap, e.g. a real higher roof) still count.
    """
    snx, sny, snz = surface_normal
    for tri in triangles:
        t = ray_triangle_intersect(origin, direction, tri, min_t=min_t)
        if t is None:
            continue
        (ax, ay, az), (bx, by, bz), (cx, cy, cz) = tri
        e1x, e1y, e1z = bx-ax, by-ay, bz-az
        e2x, e2y, e2z = cx-ax, cy-ay, cz-az
        nx = e1y*e2z - e1z*e2y
        ny = e1z*e2x - e1x*e2z
        nz = e1x*e2y - e1y*e2x
        nlen = math.sqrt(nx*nx + ny*ny + nz*nz) or 1.0
        nx, ny, nz = nx/nlen, ny/nlen, nz/nlen
        absdot = abs(nx*snx + ny*sny + nz*snz)
        gap = t * abs(direction[0]*nx + direction[1]*ny + direction[2]*nz)
        if absdot > coplanar_dot and gap < self_gap:
            continue  # the surface's own near-parallel geometry — not a real shadow
        return True
    return False


# ── De-duplicate coincident faces (double-sided IFC geometry) ─────────────

def dedupe_triangles(triangles, quant: int = 1000):
    """Collapse faces sharing the same 3 vertices (within 1/quant metres, any
    winding) to a single representative. Mirrors the JS dedupeTriangles used to
    remove double-sided / inverted-twin faces before analysis and shadow casting.
    """
    seen = set()
    out = []
    for tri in triangles:
        ks = sorted(
            (round(v[0]*quant), round(v[1]*quant), round(v[2]*quant))
            for v in tri
        )
        key = tuple(ks)
        if key in seen:
            continue
        seen.add(key)
        out.append(tri)
    return out
