import math
from logging import debug
from typing import List

import numpy as np
from pepeline import Point, Bresenham, Bezier

from pepedd.core.objects.safe_rng import SafeRNG


def get_radius_point(
    cx: float, cy: float, r: float, angle_deg: float, size: int
) -> tuple:
    theta = angle_deg * math.pi / 180.0
    px = cx + r * math.cos(theta)
    py = cy + r * math.sin(theta)

    is_outside = px < 0 or py < 0

    if not is_outside:
        return int(round(px)), int(round(py)), size, False

    dx = px - cx
    dy = py - cy
    t = 1.0

    if px < 0 and dx != 0:
        t = min(t, -cx / dx)
    if py < 0 and dy != 0:
        t = min(t, -cy / dy)

    new_x = cx + t * dx
    new_y = cy + t * dy
    new_size = max(1, int(round(size * t)))

    return int(round(new_x)), int(round(new_y)), new_size, True


def random_point(rng, h, w, size: List[int]):
    x, y, size = (
        rng.safe_randint([0, h]),
        rng.safe_randint([0, w]),
        rng.safe_randint(size),
    )
    debug(f"        random_point x={x} y={y} size={size}")
    return Point(x, y, size)


def get_parallel_line(canvas_width, canvas_height, angle, offset, s0, s1):
    angle_rad = math.radians(angle)

    dx = math.cos(angle_rad)
    dy = math.sin(angle_rad)

    perp_dx = -dy
    perp_dy = dx

    corners = [
        (0, 0),
        (canvas_width, 0),
        (0, canvas_height),
        (canvas_width, canvas_height),
    ]

    projections = [corner[0] * perp_dx + corner[1] * perp_dy for corner in corners]
    min_proj = min(projections)

    base_offset = min_proj + offset
    offset_x = base_offset * perp_dx
    offset_y = base_offset * perp_dy

    intersections = []
    epsilon = 1e-10

    if abs(dx) > epsilon:
        t = (0 - offset_x) / dx
        y = offset_y + t * dy
        if -epsilon <= y <= canvas_height + epsilon:
            intersections.append((0, max(0, min(canvas_height, y))))

    if abs(dx) > epsilon:
        t = (canvas_width - offset_x) / dx
        y = offset_y + t * dy
        if -epsilon <= y <= canvas_height + epsilon:
            intersections.append((canvas_width, max(0, min(canvas_height, y))))

    if abs(dy) > epsilon:
        t = (0 - offset_y) / dy
        x = offset_x + t * dx
        if -epsilon <= x <= canvas_width + epsilon:
            intersections.append((max(0, min(canvas_width, x)), 0))

    if abs(dy) > epsilon:
        t = (canvas_height - offset_y) / dy
        x = offset_x + t * dx
        if -epsilon <= x <= canvas_width + epsilon:
            intersections.append((max(0, min(canvas_width, x)), canvas_height))

    unique_intersections = []
    for point in intersections:
        if not any(
            math.isclose(point[0], p[0], abs_tol=0.1)
            and math.isclose(point[1], p[1], abs_tol=0.1)
            for p in unique_intersections
        ):
            unique_intersections.append(point)

    if len(unique_intersections) >= 2:
        ui0, ui1 = unique_intersections[0], unique_intersections[1]
        debug(
            f"        parallel_line x0={ui0[0]} y0={ui0[1]} x1={ui1[0]} y1={ui1[1]} s0={s0} s1={s1} offset={offset}"
        )
        return Bresenham(
            Point(int(ui0[0]), int(ui0[1]), s0), Point(int(ui1[0]), int(ui1[1]), s1)
        )
    else:
        return None


def uniform_circle(
    h: int,
    w: int,
    rng: SafeRNG,
    r0: List[float],
    r1: List[float],
    s0: List[int],
    s1: List[int],
    a0: List[float],
    a1: List[float],
    n_lines: List[int],
):
    x, y = float(rng.safe_randint([0, w])), float(rng.safe_randint([0, h]))
    r0_v, r1_v = rng.safe_uniform(r0), rng.safe_uniform(r1)
    s0_v, s1_v = rng.safe_randint(s0), rng.safe_randint(s1)
    a0_v, a1_v = rng.safe_uniform(a0), rng.safe_uniform(a1)
    n_lines_v = rng.safe_randint(n_lines)
    lines_list = []
    debug(
        f"    uniform_circle h={h} w={w} n_lines={n_lines_v} r0= {r0_v} r1= {r1_v} s0= {s0_v} s1={s1_v}"
    )
    for a in np.linspace(a0_v, a1_v, n_lines_v):
        px1, py1, sz1, out1 = get_radius_point(x, y, r0_v, a, s0_v)
        px2, py2, sz2, out2 = get_radius_point(x, y, r1_v, a, s1_v)
        if out1 and out2:
            if px1 == px2 and py1 == py2:
                continue
        debug(
            f"        circle_point angle= {a} x0= {px1} y0= {py1} x1= {px2} y1= {py2} rs0= {sz1} rs1= {sz2}"
        )
        lines_list.append(Bresenham(Point(px1, py1, sz1), Point(px2, py2, sz2)))
    return lines_list


def random_circle(
    h: int,
    w: int,
    rng: SafeRNG,
    r0: List[float],
    r1: List[float],
    s0: List[int],
    s1: List[int],
    a0: List[float],
    a1: List[float],
    n_lines: List[int],
):
    x, y = float(rng.safe_randint([0, w])), float(rng.safe_randint([0, h]))

    a0_v, a1_v = rng.safe_uniform(a0), rng.safe_uniform(a1)
    n_lines_v = rng.safe_randint(n_lines)
    lines_list = []
    debug(f"    random_circle h={h} w={w} n_lines={n_lines_v}")
    for _ in range(n_lines_v):
        a = rng.uniform(a0_v, a1_v)
        r0_v, r1_v = rng.safe_uniform(r0), rng.safe_uniform(r1)
        s0_v, s1_v = rng.safe_randint(s0), rng.safe_randint(s1)
        px1, py1, sz1, out1 = get_radius_point(x, y, r0_v, a, s0_v)
        px2, py2, sz2, out2 = get_radius_point(x, y, r1_v, a, s1_v)
        if out1 and out2:
            if px1 == px2 and py1 == py2:
                continue
        debug(
            f"        circle_point r0= {r0_v} r1= {r1_v} s0= {s0_v} s1= {s1_v} angle= {a} x0= {px1} y0= {py1} x1= {px2} y1= {py2} s0= {sz1} s1= {sz2}"
        )
        lines_list.append(Bresenham(Point(px1, py1, sz1), Point(px2, py2, sz2)))
    return lines_list


def uniform_rays(
    h,
    w,
    rng: SafeRNG,
    l0: List[float],
    l1: List[float],
    s0: List[int],
    s1: List[int],
    a0: List[float],
    n_lines: List[int],
):
    lines = []
    l0_v, l1_v = rng.safe_uniform(l0), rng.safe_uniform(l1)
    l0_v, l1_v = sorted([l0_v, l1_v])

    n_lines_v = rng.safe_randint(n_lines)
    s0_v, s1_v = rng.safe_randint(s0), rng.safe_randint(s1)
    a0_v = rng.safe_uniform(a0)
    angle_rad = math.radians(a0_v)
    perp_dx = -math.sin(angle_rad)
    perp_dy = math.cos(angle_rad)
    corners = [(0, 0), (w, 0), (0, h), (w, h)]
    projections = [corner[0] * perp_dx + corner[1] * perp_dy for corner in corners]
    min_proj = min(projections)
    max_proj = max(projections)
    total_distance = max_proj - min_proj
    debug(
        f"    uniform_rays h={h} w={w} n_lines={n_lines_v} angle= {a0_v} line_range: {l0_v * total_distance}x{l1_v * total_distance}"
    )
    for offset in np.linspace(l0_v * total_distance, l1_v * total_distance, n_lines_v):
        one_line = get_parallel_line(w, h, a0_v, offset, s0_v, s1_v)
        if one_line:
            lines.append(one_line)

    return lines


def random_rays(
    h,
    w,
    rng: SafeRNG,
    l0: List[float],
    l1: List[float],
    s0: List[int],
    s1: List[int],
    a0: List[float],
    n_lines: List[int],
):
    lines = []
    l0_v, l1_v = rng.safe_uniform(l0), rng.safe_uniform(l1)
    l0_v, l1_v = sorted([l0_v, l1_v])

    n_lines_v = rng.safe_randint(n_lines)

    a0_v = rng.safe_uniform(a0)
    angle_rad = math.radians(a0_v)
    perp_dx = -math.sin(angle_rad)
    perp_dy = math.cos(angle_rad)
    corners = [(0, 0), (w, 0), (0, h), (w, h)]
    projections = [corner[0] * perp_dx + corner[1] * perp_dy for corner in corners]
    min_proj = min(projections)
    max_proj = max(projections)
    total_distance = max_proj - min_proj
    debug(
        f"    random_rays h={h} w={w} n_lines={n_lines_v} angle= {a0_v} line_range: {l0_v * total_distance}x{l1_v * total_distance}"
    )
    for offset in range(n_lines_v):
        offset = rng.safe_uniform([l0_v * total_distance, l1_v * total_distance])
        s0_v, s1_v = rng.safe_randint(s0), rng.safe_randint(s1)
        one_line = get_parallel_line(w, h, a0_v, offset, s0_v, s1_v)
        if one_line:
            lines.append(one_line)

    return lines


def random_lines(
    h: int, w: int, rng: SafeRNG, s0: List[int], s1: List[int], n_lines: List[int]
):
    n_lines_v = rng.safe_randint(n_lines)
    result_lines = []
    debug(f"    random_lines h={h} w={w} n_lines={n_lines_v}")
    for _ in range(n_lines_v):
        result_lines.append(
            Bresenham(random_point(rng, h, w, s0), random_point(rng, h, w, s1))
        )
        debug("")
    return result_lines


def random_beziers(
    h: int, w: int, rng: SafeRNG, s0: List[int], s1: List[int], n_lines: List[int]
):
    n_lines_v = rng.safe_randint(n_lines)
    result_lines = []
    debug(f"    random_beziers h={h} w={w} n_lines={n_lines_v}")
    for _ in range(n_lines_v):
        result_lines.append(
            Bezier(
                random_point(rng, h, w, s0),
                random_point(rng, h, w, s1),
                random_point(rng, h, w, s0),
                random_point(rng, h, w, s1),
                0.01,
            )
        )
    return result_lines
