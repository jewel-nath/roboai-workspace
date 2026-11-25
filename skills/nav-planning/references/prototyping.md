# Prototyping planners outside ROS

Part of [nav-planning](../SKILL.md). For trying an algorithm, teaching it, or checking a map before
writing a plugin. PythonRobotics (MIT) was read at commit ef64608 (2026-11-10); the script below was
written for this skill and not run.

## Where each algorithm lives

| Algorithm | Try it in | In Nav2 |
|---|---|---|
| Dijkstra, A* on a grid | `PathPlanning/AStar/a_star.py`, the script below | NavFn (`use_astar`), Smac 2D |
| Theta* (any-angle) | `PathPlanning/ThetaStar/theta_star.py` | `nav2_theta_star_planner` |
| Hybrid A* (Reeds-Shepp) | `PathPlanning/HybridAStar/hybrid_a_star.py` | Smac Hybrid-A* |
| State lattice | the Smac generator, [planners.md](planners.md) | Smac State Lattice |
| RRT, RRT* | `PathPlanning/RRT/rrt.py`, `PathPlanning/RRTStar/rrt_star.py`, `RRTStarReedsShepp/` | none; a custom plugin ([plugin-planner.md](plugin-planner.md)), e.g. on OMPL (`ros-jazzy-ompl` 1.7.0) |
| D*, D* Lite (replanning) | `PathPlanning/DStar/`, `PathPlanning/DStarLite/` | none |
| Grid sweep coverage | `PathPlanning/GridBasedSweepCPP/` | opennav_coverage, [coverage.md](coverage.md) |

Sampling planners (RRT, RRT*, PRM) pay off in high-dimensional spaces such as arms; for arms use MoveIt 2
with OMPL ([manip-moveit2](../../manip-moveit2/SKILL.md)). On a 2D costmap the search-based Smac planners are the
maintained path.

## PythonRobotics

```bash
python3 -m venv ~/venvs/planning          # keep it apart from the ROS Python
~/venvs/planning/bin/pip install numpy scipy matplotlib pillow pyyaml
git clone --depth 1 https://github.com/AtsushiSakai/PythonRobotics.git ~/src/PythonRobotics
cd ~/src/PythonRobotics
~/venvs/planning/bin/python PathPlanning/AStar/a_star.py
~/venvs/planning/bin/python PathPlanning/HybridAStar/hybrid_a_star.py
~/venvs/planning/bin/python PathPlanning/RRTStar/rrt_star.py
```

Its README asks for Python 3.13 and pins exact versions in `requirements/requirements.txt`; Ubuntu 24.04
ships 3.12, so the unpinned install above is the practical route (not verified on every script). Each
script animates with matplotlib; set its module-level `show_animation = False` to run headless.

Things to know before reusing the code:

- `AStarPlanner(ox, oy, resolution, rr)` takes obstacle points in metres and builds its grid by testing
  every cell against every obstacle point, which is slow on a real map: downsample first or use the
  script below. `planning()` returns `rx, ry` from the goal back to the start.
- `RRT` and `RRTStar` take circular obstacles `[(x, y, radius), ...]`, a sampling range `rand_area=[min,
  max]` and `robot_radius`; the returned path also runs goal to start.
- Hybrid A* reads the vehicle from `PathPlanning/HybridAStar/car.py`: `WB = 3.0` m wheelbase,
  `MAX_STEER = 0.6` rad, a 3.3 m by 2.0 m body. Edit those for a small robot, and pass grid
  (`XY_GRID_RESOLUTION` 2.0 m) and heading (15°) resolutions that suit it.

## A* on a saved Nav2 map

Loads a `map_server` YAML and image the way `nav2_map_server` does in trinary mode, inflates by the
robot radius, and plans 8-connected A* with the octile heuristic.

```python
#!/usr/bin/env python3
"""Plan A* on a Nav2 map: grid_astar.py <map.yaml> <start_x> <start_y> <goal_x> <goal_y> [radius]."""
import heapq
import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import yaml
from PIL import Image
from scipy.ndimage import distance_transform_edt


def load_map(yaml_path):
    """Return (grid, resolution, origin); grid row 0 is the lowest y, 0 free, 100 occupied, -1 unknown."""
    meta = yaml.safe_load(Path(yaml_path).read_text())
    pixels = np.asarray(Image.open(Path(yaml_path).parent / meta["image"]).convert("L")) / 255.0
    occ = pixels if meta.get("negate", 0) else 1.0 - pixels
    grid = np.full(occ.shape, -1, dtype=np.int8)
    grid[occ <= meta["free_thresh"]] = 0
    grid[occ >= meta["occupied_thresh"]] = 100
    return np.flipud(grid), meta["resolution"], meta["origin"]  # assumes origin yaw 0


def astar(blocked, start, goal):
    rows, cols = blocked.shape
    moves = [(dr, dc, math.hypot(dr, dc)) for dr in (-1, 0, 1) for dc in (-1, 0, 1) if dr or dc]

    def h(cell):
        dr, dc = abs(cell[0] - goal[0]), abs(cell[1] - goal[1])
        return max(dr, dc) + (math.sqrt(2) - 1) * min(dr, dc)

    g, parent, closed = {start: 0.0}, {start: None}, set()
    heap = [(h(start), start)]
    while heap:
        _, cell = heapq.heappop(heap)
        if cell in closed:
            continue
        if cell == goal:
            path = []
            while cell is not None:
                path.append(cell)
                cell = parent[cell]
            return path[::-1]
        closed.add(cell)
        for dr, dc, step in moves:
            nxt = (cell[0] + dr, cell[1] + dc)
            if not (0 <= nxt[0] < rows and 0 <= nxt[1] < cols) or blocked[nxt] or nxt in closed:
                continue
            cost = g[cell] + step
            if cost < g.get(nxt, math.inf):
                g[nxt], parent[nxt] = cost, cell
                heapq.heappush(heap, (cost + h(nxt), nxt))
    return None


def main():
    yaml_path, sx, sy, gx, gy = sys.argv[1], *map(float, sys.argv[2:6])
    radius = float(sys.argv[6]) if len(sys.argv) > 6 else 0.25
    grid, res, origin = load_map(yaml_path)
    # Unknown and occupied cells block; free cells closer than the radius block too
    blocked = distance_transform_edt(grid == 0) * res <= radius

    def to_cell(x, y):
        return int((y - origin[1]) / res), int((x - origin[0]) / res)

    start, goal = to_cell(sx, sy), to_cell(gx, gy)
    if blocked[start] or blocked[goal]:
        sys.exit("start or goal is blocked after inflation")
    path = astar(blocked, start, goal)
    if path is None:
        sys.exit("no path")
    xs = [origin[0] + (c + 0.5) * res for _, c in path]
    ys = [origin[1] + (r + 0.5) * res for r, _ in path]
    length = sum(math.dist(a, b) for a, b in zip(zip(xs, ys), zip(xs[1:], ys[1:])))
    print(f"{len(path)} cells, {length:.2f} m")
    extent = [origin[0], origin[0] + grid.shape[1] * res, origin[1], origin[1] + grid.shape[0] * res]
    plt.imshow(np.where(grid == 0, 1.0, 0.0), cmap="gray", origin="lower", extent=extent)
    plt.plot(xs, ys, "r-")
    plt.show()


if __name__ == "__main__":
    main()
```

Run it with `~/venvs/planning/bin/python grid_astar.py ~/maps/my_map.yaml 0.0 0.0 3.5 2.0 0.25`.
Unlike Nav2 it has no cost gradient, so its paths hug the inflated boundary; that is the reason Nav2's
planners want a wide, gentle inflation layer.

## Reading Nav2 costmaps live

- `/global_costmap/costmap` and `/local_costmap/costmap` are `nav_msgs/OccupancyGrid`: Nav2 maps its
  internal costs to 0 (free), 1 to 98 (inflated), 99 (inscribed), 100 (lethal) and -1 (unknown).
- `/global_costmap/costmap_raw` is `nav2_msgs/Costmap` with the internal 0 to 255 values (253 inscribed,
  254 lethal, 255 unknown).
- Both are row-major from the lower-left cell at `info.origin`. Mixing the two scales (testing an
  OccupancyGrid cell against 253) is a common bug.

## Boustrophedon by hand

For one obstacle-free rectangle, lanes spaced by the tool width with alternating direction are enough:
emit the lane end points in the map frame and send them through `NavigateThroughPoses` or the waypoint
follower ([nav-nav2](../../nav-nav2/SKILL.md)). Real rooms need a cell decomposition first; PythonRobotics'
`GridBasedSweepCPP` sweeps a polygon on a grid, and opennav_coverage does headlands, swath angles and
turns properly.
