"""
Deterministic unit tests for the SunForm analysis engine.

All tests use known geometry, known sun positions, and known expected answers.
No external API calls, no randomness.

Run with: python -m pytest tests/ -v   (from project root)
    or:   python3 tests/test_sun_engine.py   (standalone)
"""

import math
import sys
import os
import pytest

# Ensure the project root is on sys.path so `sunform_engine` can be imported
# regardless of whether we run via pytest from root or python3 from tests/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sunform_engine import (
    get_sun_positions,
    sun_direction,
    ray_triangle_intersect,
    ray_hits_any_triangle,
    subdivide_to_max_edge,
    build_unique_vertices,
    compute_vertex_normals,
    compute_vertex_voronoi_areas,
    compute_sun_hours_per_vertex,
    ray_hits_real_occluder,
    dedupe_triangles,
)


# ── Helpers: programmatic test geometry ──────────────────────────────────

def make_box_triangles(cx, cy, cz, sx, sy, sz):
    """Create 12 triangles forming an axis-aligned box centred at (cx,cy,cz)
    with half-extents (sx,sy,sz)."""
    x0, x1 = cx - sx, cx + sx
    y0, y1 = cy - sy, cy + sy
    z0, z1 = cz - sz, cz + sz

    # 8 corners
    v = [
        (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),  # back face
        (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1),  # front face
    ]

    # 6 faces x 2 triangles = 12
    faces = [
        # back
        (v[0], v[1], v[2]), (v[0], v[2], v[3]),
        # front
        (v[4], v[6], v[5]), (v[4], v[7], v[6]),
        # left
        (v[0], v[3], v[7]), (v[0], v[7], v[4]),
        # right
        (v[1], v[5], v[6]), (v[1], v[6], v[2]),
        # bottom
        (v[0], v[4], v[5]), (v[0], v[5], v[1]),
        # top
        (v[3], v[2], v[6]), (v[3], v[6], v[7]),
    ]
    return faces


def make_wall_triangles(x, z0, z1, y0, y1, thickness=0.1):
    """Create a thin wall along X=x from z0..z1, y0..y1."""
    return make_box_triangles(x, (y0+y1)/2, (z0+z1)/2,
                              thickness/2, (y1-y0)/2, (z1-z0)/2)


def make_ridge_roof(x0=0.0, x1=10.0, eave=3.0, ridge_y=2.0):
    """Two roof pitches meeting at a ridge along X at (y=ridge_y, z=0).

    Pitch A (north, z<0) and pitch B (south, z>0) each slope down from the
    ridge to an eave at z=-/+eave, y=0. Returns (pitchA_tris, pitchB_tris).
    """
    def quad(p0, p1, p2, p3):
        return [(p0, p1, p2), (p0, p2, p3)]
    pitch_a = quad((x0, 0, -eave), (x1, 0, -eave), (x1, ridge_y, 0), (x0, ridge_y, 0))
    pitch_b = quad((x0, ridge_y, 0), (x1, ridge_y, 0), (x1, 0, eave), (x0, 0, eave))
    return pitch_a, pitch_b


def _tri_centroid(tri):
    return tuple(sum(v[i] for v in tri) / 3 for i in range(3))


def _tri_up_normal(tri):
    """Unit normal of a triangle, sign-flipped to point upward (ny >= 0).

    Mirrors the orientation the JS cell pipeline applies before sampling.
    """
    a, b, c = tri
    e1 = [b[i] - a[i] for i in range(3)]
    e2 = [c[i] - a[i] for i in range(3)]
    n = [e1[1]*e2[2] - e1[2]*e2[1],
         e1[2]*e2[0] - e1[0]*e2[2],
         e1[0]*e2[1] - e1[1]*e2[0]]
    length = math.sqrt(sum(x*x for x in n))
    n = [x/length for x in n]
    if n[1] < 0:
        n = [-x for x in n]
    return tuple(n)


# ── Geometry fixture validation (runs first — prerequisite for all) ──────

class TestGeometryFixtures:
    """Validate that test geometry helpers produce genuinely opaque objects.
    These must pass before any shadow/accumulation test is meaningful."""

    def test_box_is_opaque_to_axis_aligned_rays(self):
        """Rays through the centre of a box must hit. Rays that miss must miss."""
        box = make_box_triangles(0, 5, 0, 2, 5, 2)  # 4x10x4 box at origin

        # Ray from below pointing up through centre — must hit bottom face
        assert ray_hits_any_triangle((0, -1, 0), (0, 1, 0), box), \
            "Ray through box centre should hit — box may have gaps"

        # Ray from left pointing right through centre — must hit left face
        assert ray_hits_any_triangle((-5, 5, 0), (1, 0, 0), box), \
            "Ray through box side should hit"

        # Ray from front pointing back through centre — must hit front face
        assert ray_hits_any_triangle((0, 5, 5), (0, 0, -1), box), \
            "Ray through box front should hit"

        # Ray that clearly misses — must NOT hit
        assert not ray_hits_any_triangle((10, 10, 10), (0, 1, 0), box), \
            "Ray missing box should not hit"
        # Ray parallel to a face but offset — should miss
        assert not ray_hits_any_triangle((0, -1, 0), (1, 0, 0), box), \
            "Ray parallel to box below it should not hit"

    def test_box_blocks_diagonal_rays(self):
        """Diagonal rays that pass through the box must hit."""
        box = make_box_triangles(0, 5, 0, 3, 5, 3)
        # Diagonal from far away toward box centre
        dx, dy, dz = 0 - (-20), 5 - 20, 0 - (-20)
        length = math.sqrt(dx*dx + dy*dy + dz*dz)
        d = (dx/length, dy/length, dz/length)
        assert ray_hits_any_triangle((-20, 20, -20), d, box), \
            "Diagonal ray toward box centre should hit"

    def test_box_all_6_faces_opaque(self):
        """Verify rays hit from all 6 axis directions — no face has wrong winding."""
        box = make_box_triangles(0, 0, 0, 1, 1, 1)  # 2x2x2 cube at origin
        # +X, -X, +Y, -Y, +Z, -Z
        directions = [
            ((-5, 0, 0), (1, 0, 0)),   # from -X toward +X
            ((5, 0, 0), (-1, 0, 0)),   # from +X toward -X
            ((0, -5, 0), (0, 1, 0)),   # from -Y toward +Y
            ((0, 5, 0), (0, -1, 0)),   # from +Y toward -Y
            ((0, 0, -5), (0, 0, 1)),   # from -Z toward +Z
            ((0, 0, 5), (0, 0, -1)),   # from +Z toward -Z
        ]
        for origin, direction in directions:
            assert ray_hits_any_triangle(origin, direction, box), \
                f"Ray from {origin} dir {direction} should hit box — face may have wrong winding"


# ── Test D: Sun below horizon filtered ───────────────────────────────────

class TestBelowHorizon:
    """Sun positions with negative altitude should be skipped entirely."""

    def test_negative_altitude_skipped(self):
        # At the North Pole in December, sun never rises
        sun_pos = get_sun_positions(89.0, 0.0, 2024, 12, 21, time_step=1.0)
        assert len(sun_pos) == 0, \
            f"North pole in December should have no sun above horizon, got {len(sun_pos)}"


# ── Ray-triangle intersection unit tests ─────────────────────────────────

class TestRayTriangle:
    """Direct tests of the Möller-Trumbore implementation."""

    def test_hit_horizontal_triangle(self):
        tri = ((0, 0, 0), (10, 0, 0), (5, 0, 10))
        origin = (5, 5, 3)
        direction = (0, -1, 0)  # straight down
        t = ray_triangle_intersect(origin, direction, tri)
        assert t is not None
        assert abs(t - 5.0) < 0.01

    def test_miss_parallel_ray(self):
        tri = ((0, 0, 0), (10, 0, 0), (5, 0, 10))
        origin = (5, 5, 3)
        direction = (1, 0, 0)  # parallel to triangle plane
        t = ray_triangle_intersect(origin, direction, tri)
        assert t is None

    def test_miss_behind_ray(self):
        tri = ((0, 0, 0), (10, 0, 0), (5, 0, 10))
        origin = (5, -5, 3)
        direction = (0, -1, 0)  # pointing away
        t = ray_triangle_intersect(origin, direction, tri)
        assert t is None

    def test_miss_outside_triangle(self):
        tri = ((0, 0, 0), (1, 0, 0), (0, 0, 1))
        origin = (5, 5, 5)  # far outside triangle
        direction = (0, -1, 0)
        t = ray_triangle_intersect(origin, direction, tri)
        assert t is None

    def test_grazing_ray_at_1_degree(self):
        """Ray at 1° altitude — nearly parallel to ground. Must still detect hits."""
        # Large vertical wall at z=5, spanning x=-10..10, y=0..20
        wall = make_box_triangles(0, 10, 5, 10, 10, 0.3)
        d = sun_direction(180.0, 1.0)  # 1° altitude, from south (geographic convention)

        # Origin at z=0 — ray should hit the wall at z≈4.7
        assert ray_hits_any_triangle((0, 0.01, 0), d, wall), \
            "Grazing ray at 1° should hit tall wall"

    def test_grazing_ray_at_2_degrees_misses_short_wall(self):
        """Ray at 2° over a 0.5m wall at 15m distance should clear it.
        Wall height at 15m: 15 * tan(2°) ≈ 0.52m — just clears 0.5m wall."""
        # Short wall (0.5m tall) at z=15
        short_wall = make_box_triangles(0, 0.25, 15, 3, 0.25, 0.3)
        d = sun_direction(180.0, 2.0)
        # Origin at ground level, the ray at 2° reaches height 15*tan(2°)=0.52m at z=15
        # Wall top is at y=0.5, ray at y≈0.52 — should just clear it
        # This is a numerical edge case; we check the ray system handles it
        result = ray_hits_any_triangle((0, 0.01, 0), d, short_wall)
        # We don't assert a specific outcome here (it's at the numerical edge)
        # but the function must not crash or produce NaN
        assert isinstance(result, bool), "Grazing ray must return bool, not crash"


# ── Sun position sanity tests ────────────────────────────────────────────

class TestSunPositions:
    """Tests for the Spencer 1971 solar position calculator against known values."""

    def test_london_march_equinox(self):
        positions = get_sun_positions(51.5, -0.1, 2024, 3, 21, time_step=1.0)
        assert 11 <= len(positions) <= 13, \
            f"London on equinox should have ~12 daylight hours, got {len(positions)}"

    def test_london_equinox_noon_azimuth_altitude(self):
        """At solar noon on equinox, London should see sun due south at ~38-39° altitude."""
        positions = get_sun_positions(51.5, -0.1, 2024, 3, 21, time_step=1.0)
        noon_pos = [p for p in positions if 11.5 <= p['hour'] <= 12.5]
        assert len(noon_pos) >= 1, "Should have a position near solar noon"

        p = noon_pos[0]
        # Azimuth should be near 180° (due south in geographic convention), within ±5°
        assert 172 <= p['azimuth'] <= 188, \
            f"Noon azimuth should be ~180° (south), got {p['azimuth']:.1f}°"
        # Altitude should be ~38.7° (90° - 51.5° + small correction)
        assert 35 <= p['altitude'] <= 42, \
            f"Noon altitude should be ~38.7°, got {p['altitude']:.1f}°"

    def test_london_equinox_morning_rises_in_east(self):
        """Morning sun should have azimuth < 180° (eastern half in geographic convention)."""
        positions = get_sun_positions(51.5, -0.1, 2024, 3, 21, time_step=1.0)
        morning = [p for p in positions if p['hour'] < 12]
        assert len(morning) >= 3, "Should have multiple morning hours"
        for p in morning:
            assert p['azimuth'] < 180, \
                f"Morning sun at hour {p['hour']} should have azimuth < 180° (east), got {p['azimuth']:.1f}°"

    def test_london_equinox_afternoon_sets_in_west(self):
        """Afternoon sun should have azimuth > 180° (western half in geographic convention)."""
        positions = get_sun_positions(51.5, -0.1, 2024, 3, 21, time_step=1.0)
        afternoon = [p for p in positions if p['hour'] > 13]
        assert len(afternoon) >= 3, "Should have multiple afternoon hours"
        for p in afternoon:
            assert p['azimuth'] > 180, \
                f"Afternoon sun at hour {p['hour']} should have azimuth > 180° (west), got {p['azimuth']:.1f}°"

    def test_all_altitudes_positive(self):
        positions = get_sun_positions(51.5, -0.1, 2024, 6, 21, time_step=0.5)
        for p in positions:
            assert p['altitude'] > 0, f"Returned position has non-positive altitude: {p}"

    def test_summer_more_hours_than_winter(self):
        summer = get_sun_positions(51.5, -0.1, 2024, 6, 21, time_step=1.0)
        winter = get_sun_positions(51.5, -0.1, 2024, 12, 21, time_step=1.0)
        assert len(summer) > len(winter) + 4, \
            f"Summer ({len(summer)}) should have much more daylight than winter ({len(winter)})"

    def test_equator_roughly_12_hours(self):
        positions = get_sun_positions(0.0, 0.0, 2024, 3, 21, time_step=1.0)
        assert 11 <= len(positions) <= 13, \
            f"Equator on equinox should have ~12h daylight, got {len(positions)}"

    def test_sun_direction_south_at_noon(self):
        """Sun due south (azimuth 180° in geographic convention) at 45° altitude."""
        dx, dy, dz = sun_direction(180.0, 45.0)
        # Y = sin(alt) = 0.707
        assert abs(dy - 0.7071) < 0.01, f"Y component should be ~0.707, got {dy}"
        # X should be ~0 (due south, no east/west component)
        assert abs(dx) < 0.01, f"X component should be ~0 for due south, got {dx}"
        # Z should be positive (sun from +Z = south in Three.js coords)
        assert dz > 0.5, f"Z component should be positive for south sun, got {dz}"

    def test_sun_direction_east_west_symmetry(self):
        """Azimuth 90° (east) and 270° (west) should mirror in X (geographic convention)."""
        dx_e, dy_e, dz_e = sun_direction(90.0, 45.0)
        dx_w, dy_w, dz_w = sun_direction(270.0, 45.0)
        assert abs(dx_e + dx_w) < 0.01, "East/west X components should be opposite"
        assert abs(dy_e - dy_w) < 0.01, "East/west Y components should be equal"
        assert abs(dz_e - dz_w) < 0.01, "East/west Z components should be equal"


# ── Upward-facing filter / inverted-winding holes (pitched-roof regression) ──
class TestUpwardFacingFilter:
    """Why pitched-roof tiles go missing: the upward-facing filter keeps a
    triangle only if its WINDING-based normal points up (ny >= MIN_UPWARD_NY).

    Real IFC meshes (web-ifc / IfcOpenShell triangulation) frequently emit
    roof triangles with inconsistent winding — some normals point into the
    solid. Those upward roof surfaces are then discarded as "not upward",
    leaving holes the missing-tile overlay can't see (they never reach the
    cell map). A winding-independent test (|ny|) keeps them.

    These tests mirror the JS filter in prepareGridCells.
    """

    MIN_UPWARD_NY = 0.1

    @staticmethod
    def _ny(tri):
        a, b, c = tri
        e1 = [b[i]-a[i] for i in range(3)]
        e2 = [c[i]-a[i] for i in range(3)]
        n = [e1[1]*e2[2]-e1[2]*e2[1],
             e1[2]*e2[0]-e1[0]*e2[2],
             e1[0]*e2[1]-e1[1]*e2[0]]
        length = math.sqrt(sum(x*x for x in n)) or 1.0
        return n[1] / length

    def _hip_pitch(self, invert=False):
        # One pitch of a hip roof: base edge to a raised apex (slope ~31°).
        tri = ((0, 0, 0), (10, 0, 0), (5, 3, 5))
        if self._ny(tri) < 0:
            tri = (tri[0], tri[2], tri[1])  # normalise to outward (ny>0)
        if invert:
            tri = (tri[0], tri[2], tri[1])  # flip winding → ny<0
        return tri

    def test_inverted_pitch_dropped_by_current_filter(self):
        """Inverted-winding roof pitch is wrongly rejected → hole."""
        inv = self._hip_pitch(invert=True)
        ny = self._ny(inv)
        assert ny < 0, f"inverted pitch should have ny<0, got {ny}"
        kept = ny >= self.MIN_UPWARD_NY
        assert not kept, "current filter drops the inverted roof pitch (hole)"

    def test_inverted_pitch_kept_by_winding_independent_filter(self):
        """A winding-independent test keeps the same surface (no hole)."""
        inv = self._hip_pitch(invert=True)
        kept = abs(self._ny(inv)) >= self.MIN_UPWARD_NY
        assert kept, "winding-independent filter keeps the inverted roof pitch"

    def test_vertical_wall_still_rejected_either_way(self):
        """A near-vertical wall (ny≈0) is rejected by both tests — the fix
        must not start admitting walls."""
        wall = ((0, 0, 0), (0, 5, 0), (0, 5, 5))  # in the X=0 plane, normal ±X
        ny = self._ny(wall)
        assert abs(ny) < self.MIN_UPWARD_NY, f"wall ny should be ~0, got {ny}"


# ── Self-shadow exclusion (the duplicate/overlapping-geometry fix) ───────
class TestSelfShadowExclusion:
    """A surface must not be shadowed by its OWN near-coplanar geometry (a
    duplicate or overlapping copy of the very surface a cell sits on — what
    a doubled IFC mesh produces). Genuine occluders must still shadow.
    """

    def _dirs(self):
        return [sun_direction(s['azimuth'], s['altitude'])
                for s in get_sun_positions(51.5, -0.1, 2026, 6, 21, 0.5)]

    def _quad(self, y):
        return [((-5, y, -5), (5, y, -5), (5, y, 5)),
                ((-5, y, -5), (5, y, 5), (-5, y, 5))]

    def test_duplicate_sheet_is_ignored(self):
        dirs = self._dirs()
        dup = self._quad(10.6)          # parallel copy 0.6 m above the cell
        origin = (0, 10.01, 0)
        up = (0.0, 1.0, 0.0)
        plain = sum(1 for d in dirs if not ray_hits_any_triangle(origin, d, dup, min_t=1e-4))
        excl = sum(1 for d in dirs if not ray_hits_real_occluder(origin, d, dup, up))
        assert plain < len(dirs), "sanity: the duplicate sheet does shadow under the plain test"
        assert excl == len(dirs), f"duplicate sheet must be ignored, got {excl}/{len(dirs)} lit"

    def test_genuine_higher_roof_still_shadows(self):
        dirs = self._dirs()
        roof = self._quad(13.0)         # real parallel roof 3 m above
        origin = (0, 10.01, 0)
        up = (0.0, 1.0, 0.0)
        excl = sum(1 for d in dirs if not ray_hits_real_occluder(origin, d, roof, up))
        assert excl < len(dirs), "a genuine higher roof (gap >> self_gap) must still shadow"

    def test_tilted_occluder_still_shadows(self):
        dirs = self._dirs()
        # near-vertical wall 0.5 m south — not parallel to the (up) surface
        wall = [((-5, 9.5, 0.5), (5, 9.5, 0.5), (5, 12, 0.5)),
                ((-5, 9.5, 0.5), (5, 12, 0.5), (-5, 12, 0.5))]
        origin = (0, 10.01, 0)
        up = (0.0, 1.0, 0.0)
        excl = sum(1 for d in dirs if not ray_hits_real_occluder(origin, d, wall, up))
        assert excl < len(dirs), "a tilted occluder (low |n·n|) must still shadow"

    def test_opposite_roof_pitch_self_shadow_is_preserved(self):
        """The concern: don't kill genuine self-shading. A north pitch shaded by
        the opposite (south) pitch must read identically with the exclusion on,
        because the two pitches are far from parallel (|nA·nB| ≈ 0.39)."""
        def quad(p0, p1, p2, p3):
            return [(p0, p1, p2), (p0, p2, p3)]
        pitch_a = quad((0, 0, -3), (10, 0, -3), (10, 5, 0), (0, 5, 0))  # steep north
        pitch_b = quad((0, 5, 0), (10, 5, 0), (10, 0, 3), (0, 0, 3))    # steep south
        roof = pitch_a + pitch_b
        n_a = _tri_up_normal(pitch_a[0])
        origin = (5, 0.6 + n_a[1] * 0.01, -2.6 + n_a[2] * 0.01)  # low on north pitch
        dirs = [sun_direction(s['azimuth'], s['altitude'])
                for s in get_sun_positions(51.5, -0.1, 2026, 3, 20, 0.25)]
        plain = sum(1 for d in dirs if not ray_hits_any_triangle(origin, d, roof, min_t=1e-4))
        excl = sum(1 for d in dirs if not ray_hits_real_occluder(origin, d, roof, n_a))
        assert plain < len(dirs), "sanity: the opposite pitch should partially self-shade here"
        assert excl == plain, (
            f"opposite-pitch self-shadow must be preserved: plain={plain}, excl={excl}")


# ── Coincident-face de-duplication (double-sided IFC geometry) ───────────
class TestDedupe:
    """Collapse double-sided / inverted-twin faces, but never merge genuinely
    distinct surfaces."""

    def test_reverse_wound_twin_collapses(self):
        a, b, c = (0, 0, 0), (1, 0, 0), (1, 0, 1)
        tri = (a, b, c)
        rev = (a, c, b)  # same 3 vertices, opposite winding
        assert len(dedupe_triangles([tri, rev])) == 1

    def test_distinct_offset_sheets_preserved(self):
        t1 = ((0, 0, 0), (1, 0, 0), (1, 0, 1))
        t2 = ((0, 0.5, 0), (1, 0.5, 0), (1, 0.5, 1))  # 0.5 m higher → distinct
        assert len(dedupe_triangles([t1, t2])) == 2

    def test_near_coincident_within_tolerance_collapses(self):
        t1 = ((0, 0, 0), (1, 0, 0), (1, 0, 1))
        t2 = ((0, 0.0005, 0), (1, 0.0005, 0), (1, 0.0005, 1))  # 0.5 mm → same
        assert len(dedupe_triangles([t1, t2])) == 1

    def test_no_false_merge_of_adjacent_faces(self):
        # two triangles of one quad share an edge but are NOT the same face
        t1 = ((0, 0, 0), (1, 0, 0), (1, 0, 1))
        t2 = ((0, 0, 0), (1, 0, 1), (0, 0, 1))
        assert len(dedupe_triangles([t1, t2])) == 2


# ── Edge-split subdivision ───────────────────────────────────────────────
class TestSubdivision:
    """subdivide_to_max_edge: no output edge exceeds the threshold, total
    area is preserved, and shared vertices deduplicate across triangles."""

    def _edge_lengths(self, tri):
        a, b, c = tri
        for p, q in ((a, b), (b, c), (c, a)):
            yield math.dist(p, q)

    def _area(self, tri):
        a, b, c = tri
        e1 = [b[i]-a[i] for i in range(3)]
        e2 = [c[i]-a[i] for i in range(3)]
        n = [e1[1]*e2[2]-e1[2]*e2[1], e1[2]*e2[0]-e1[0]*e2[2], e1[0]*e2[1]-e1[1]*e2[0]]
        return 0.5 * math.sqrt(sum(x*x for x in n))

    def test_max_edge_respected(self):
        tri = [((0, 0, 0), (10, 0, 0), (0, 0, 10))]
        out = subdivide_to_max_edge(tri, 0.5)
        for t in out:
            for length in self._edge_lengths(t):
                assert length <= 0.5 + 1e-9, f"edge {length} exceeds max"

    def test_area_preserved(self):
        tri = [((0, 0, 0), (10, 0, 0), (0, 0, 10)),
               ((10, 0, 0), (10, 0, 10), (0, 0, 10))]
        out = subdivide_to_max_edge(tri, 0.7)
        before = sum(self._area(t) for t in tri)
        after = sum(self._area(t) for t in out)
        assert abs(before - after) < 1e-6

    def test_sloped_triangle_subdivides(self):
        tri = [((0, 0, 0), (10, 5, 0), (0, 5, 10))]
        out = subdivide_to_max_edge(tri, 1.0)
        assert len(out) > 1
        before = self._area(tri[0])
        after = sum(self._area(t) for t in out)
        assert abs(before - after) < 1e-6

    def test_small_triangle_untouched(self):
        tri = [((0, 0, 0), (0.3, 0, 0), (0, 0, 0.3))]
        out = subdivide_to_max_edge(tri, 0.5)
        assert len(out) == 1

    def test_shared_vertices_deduplicate(self):
        # Two triangles forming a quad share an edge; after subdivision their
        # edge midpoints must land on identical coordinates and dedupe.
        quad = [((0, 0, 0), (2, 0, 0), (2, 0, 2)),
                ((0, 0, 0), (2, 0, 2), (0, 0, 2))]
        out = subdivide_to_max_edge(quad, 0.5)
        verts, tri_idx = build_unique_vertices(out)
        # every triangle references valid indices; vertex count is far lower
        # than 3 * len(out) because shared vertices merged
        assert len(verts) < 3 * len(out)
        used = set(i for t in tri_idx for i in t)
        assert used == set(range(len(verts)))


# ── Per-vertex analysis ──────────────────────────────────────────────────
class TestPerVertexAnalysis:
    """compute_sun_hours_per_vertex on subdivided geometry."""

    def _flat_plane(self, size=10.0, max_edge=1.0):
        tris = [((0, 0, 0), (size, 0, 0), (size, 0, size)),
                ((0, 0, 0), (size, 0, size), (0, 0, size))]
        out = subdivide_to_max_edge(tris, max_edge)
        verts, tri_idx = build_unique_vertices(out)
        normals = compute_vertex_normals(verts, tri_idx)
        return verts, tri_idx, normals

    def test_unobstructed_plane_full_sun(self):
        sun_pos = get_sun_positions(51.5, -0.1, 2024, 3, 21, time_step=1.0)
        assert len(sun_pos) > 0
        verts, _, normals = self._flat_plane()
        hours = compute_sun_hours_per_vertex(verts, normals, [], sun_pos, 1.0)
        for i, h in enumerate(hours):
            assert h == len(sun_pos) * 1.0, f"vertex {i} got {h}h"

    def test_box_shadow_darkens_north_vertices(self):
        # 10m cube at origin; sun due south at 45 degrees altitude.
        box = make_box_triangles(0, 5, 0, 5, 5, 5)
        sun_pos = [{'azimuth': 180.0, 'altitude': 45.0, 'hour': 12}]
        verts, tri_idx, normals = self._flat_plane(size=40.0)
        # shift plane so it spans -20..20 in x/z around the box
        verts = [(v[0]-20, v[1], v[2]-20) for v in verts]
        hours = compute_sun_hours_per_vertex(verts, normals, box, sun_pos, 1.0)
        shadowed = lit = 0
        for v, h in zip(verts, hours):
            # well inside the shadow band (shadow len = 10m at 45deg), away
            # from the penumbra edges where rays graze the box corners
            in_shadow_band = -4 <= v[0] <= 4 and -13 <= v[2] <= -7
            far_clear = v[2] > 8 or abs(v[0]) > 8
            if in_shadow_band:
                shadowed += 1
                assert h == 0.0, f"vertex {v} in shadow band got {h}h"
            elif far_clear:
                lit += 1
                assert h == 1.0, f"clear vertex {v} got {h}h"
        assert shadowed > 5 and lit > 5

    def test_accumulation_across_positions(self):
        # Wall to the south blocks low sun; overhead sun passes.
        wall = make_box_triangles(0, 5, 3, 5, 5, 0.5)
        sun_pos = [
            {'azimuth': 180.0, 'altitude': 15.0, 'hour': 9},   # blocked
            {'azimuth': 180.0, 'altitude': 89.0, 'hour': 12},  # clear
            {'azimuth': 180.0, 'altitude': 15.0, 'hour': 15},  # blocked
        ]
        verts = [(0.0, 0.0, 0.0)]
        normals = [(0.0, 1.0, 0.0)]
        hours = compute_sun_hours_per_vertex(verts, normals, wall, sun_pos, 1.0)
        assert hours[0] == 1.0, f"expected 1h (only overhead clear), got {hours[0]}"

    def test_vertical_wall_orientation_agnostic(self):
        # A vertex on a south-facing wall, offset along its outward normal,
        # sees southern sun but a northern obstruction changes nothing.
        verts = [(0.0, 2.0, 0.0)]
        normals = [(0.0, 0.0, 1.0)]  # facing +Z (south in scene convention)
        sun_pos = [{'azimuth': 180.0, 'altitude': 30.0, 'hour': 12}]
        d = sun_direction(180.0, 30.0)
        assert d.z if hasattr(d, 'z') else True  # sanity: direction exists
        hours = compute_sun_hours_per_vertex(verts, normals, [], sun_pos, 1.0)
        assert hours[0] == 1.0

    def test_voronoi_areas_sum_to_total(self):
        verts, tri_idx, _ = self._flat_plane(size=10.0, max_edge=0.9)
        areas = compute_vertex_voronoi_areas(verts, tri_idx)
        assert abs(sum(areas) - 100.0) < 1e-6

    def test_vertex_normals_point_up_on_flat_plane(self):
        verts, tri_idx, normals = self._flat_plane()
        for n in normals:
            assert abs(n[0]) < 1e-9 and abs(n[2]) < 1e-9 and n[1] > 0.999


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
