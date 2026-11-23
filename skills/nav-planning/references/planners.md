# Global planners and smoothers

Part of [nav-planning](../SKILL.md). Defaults are the values the plugin code declares in Nav2 1.3.14
(`jazzy` branch, the Jazzy binary); where `nav2_bringup/params/nav2_params.yaml` sets something else, both
are named. Set only the keys you change; a key a plugin does not read is ignored without a warning.

## planner_server

```yaml
planner_server:
  ros__parameters:
    expected_planner_frequency: 20.0   # code default 1.0; only drives the "Planner loop missed" warning
    costmap_update_timeout: 1.0
    planner_plugins: ["GridBased"]     # keep this ID: the default BTs ask for planner_id "GridBased"
    GridBased:
      plugin: "nav2_smac_planner::SmacPlannerHybrid"
      # plugin parameters, prefixed by the ID
```

Several planners can be loaded side by side (`planner_plugins: ["GridBased", "Feasible"]`); the BT picks
one by `planner_id` or with the `PlannerSelector` node (see [nav-nav2](../../nav-nav2/SKILL.md)).

Plugin type strings in Jazzy use `::` (`nav2_navfn_planner::NavfnPlanner`). The Humble spellings with a
slash (`nav2_navfn_planner/NavfnPlanner`, `nav2_smac_planner/SmacPlannerHybrid`) fail to load.

## NavFn: `nav2_navfn_planner::NavfnPlanner`

Wavefront over the costmap from the goal, Dijkstra by default or A*. Treats the robot as a point on the
inflated costmap, so the inflation layer is its only notion of size. Paths are broad sweeping curves.

| Key | Default | Change when |
|---|---|---|
| `use_astar` | `false` | `true` for A* (faster, slightly less centred paths) |
| `tolerance` | 0.5 | metres the goal may move when the exact goal is blocked |
| `allow_unknown` | `true` | `false` to forbid planning through unknown cells |
| `use_final_approach_orientation` | `false` | `true` to replace the goal yaw with the approach direction |

## Theta*: `nav2_theta_star_planner::ThetaStarPlanner`

Any-angle A*: straight segments at any heading, few turns. Point robot, like NavFn.

| Key | Default | Change when |
|---|---|---|
| `how_many_corners` | 8 | 4 or 8 neighbours (any other value is reset to 8) |
| `w_euc_cost` | 1.0 | weight on path length |
| `w_traversal_cost` | 2.0 | raise to keep paths further from obstacles (uses costmap cost) |
| `allow_unknown` | `true` | as NavFn |
| `terminal_checking_interval` | 5000 | expansions between cancel and timeout checks |
| `use_final_approach_orientation` | `false` | as NavFn |

## Smac 2D: `nav2_smac_planner::SmacPlanner2D`

Cost-aware A* on the grid with a built-in smoother. For round differential and omni robots.

| Key | Default | Change when |
|---|---|---|
| `tolerance` | 0.125 | metres of goal tolerance |
| `cost_travel_multiplier` | 1.0 | raise (about 2.0) to stay in the middle of corridors |
| `allow_unknown` | `true` | |
| `max_planning_time` | 2.0 | seconds, includes smoothing |
| `max_iterations` / `max_on_approach_iterations` | 1000000 / 1000 | search limits |
| `downsample_costmap` / `downsampling_factor` | `false` / 1 | plan on a coarser grid for big maps |
| `use_final_approach_orientation` | `false` | |
| `smoother.max_iterations`, `w_smooth`, `w_data`, `tolerance` | 1000, 0.3, 0.2, 1e-10 | internal smoother (also in Hybrid and Lattice) |
| `smoother.do_refinement` / `refinement_num` | `true` / 2 | |

## Smac Hybrid-A*: `nav2_smac_planner::SmacPlannerHybrid`

Searches x, y and heading with Dubins (forward only) or Reeds-Shepp (forward and reverse) motion, and
checks the full footprint at each pose. For Ackermann, car-like and legged robots, and any robot that must
respect a turning radius.

| Key | Default | Change when |
|---|---|---|
| `motion_model_for_search` | `"DUBIN"` | `"REEDS_SHEPP"` if the robot may reverse |
| `minimum_turning_radius` | 0.4 | metres; the real value for the vehicle |
| `angle_quantization_bins` | 72 | heading bins (5°) |
| `reverse_penalty` | 2.0 | Reeds-Shepp only; raise to reverse less |
| `change_penalty` | 0.0 | penalty for switching direction |
| `non_straight_penalty` | 1.2 | penalty for turning |
| `cost_penalty` | 2.0 | raise to push paths away from obstacles |
| `retrospective_penalty` | 0.015 | small; favours later turns |
| `analytic_expansion_ratio` / `analytic_expansion_max_length` | 3.5 / 3.0 | how often and how far it tries to shoot to the goal |
| `analytic_expansion_max_cost` / `_override` | 200.0 / `false` | max cost a shot to the goal may cross |
| `tolerance` | 0.25 | metres |
| `max_planning_time` | 5.0 | seconds |
| `lookup_table_size` | 20.0 | metres of precomputed distance heuristic |
| `cache_obstacle_heuristic` | `false` | `true` in static maps with repeated plans to one goal |
| `downsample_obstacle_heuristic` | `true` | |
| `smooth_path` | `true` | |
| `allow_primitive_interpolation` | `false` | |
| `use_quadratic_cost_penalty` | `false` | |
| `debug_visualizations` | `false` | `true` publishes `expansions` and `planned_footprints`; costly |

Car-like robot that may reverse:

```yaml
    GridBased:
      plugin: "nav2_smac_planner::SmacPlannerHybrid"
      motion_model_for_search: "REEDS_SHEPP"
      minimum_turning_radius: 0.80          # measured on my_robot
      reverse_penalty: 2.0
      cost_penalty: 2.0
      tolerance: 0.25
      max_planning_time: 2.0
```

The planner needs a footprint polygon (or `robot_radius`) in the global costmap and an inflation radius
at least as large as the robot's circumscribed radius; otherwise it logs "The inflation radius (...) is
smaller than the circumscribed radius (...)" and checks the full footprint everywhere, which is slow.

## Smac State Lattice: `nav2_smac_planner::SmacPlannerLattice`

Searches over a precomputed set of motion primitives (a minimal control set), so it can plan for any drive
the primitives describe: diff-drive with in-place rotation, omni with sideways moves, Ackermann. Use it for
non-round robots that need full-footprint planning.

| Key | Default | Change when |
|---|---|---|
| `lattice_filepath` | `<nav2_smac_planner share>/sample_primitives/5cm_resolution/0.5m_turning_radius/ackermann/output.json` | always: point at primitives for your drive |
| `allow_reverse_expansion` | `false` | `true` to search backwards motions too (not for `omni` files) |
| `rotation_penalty` | 5.0 | penalty for rotating in place (diff/omni primitives) |
| `reverse_penalty`, `change_penalty`, `non_straight_penalty`, `cost_penalty`, `retrospective_penalty` | 2.0, 0.05, 1.05, 2.0, 0.015 | as Hybrid |
| `tolerance`, `max_planning_time`, `lookup_table_size`, `cache_obstacle_heuristic`, `smooth_path` | 0.25, 5.0, 20.0, `false`, `true` | as Hybrid |

The package installs sample files for 5 cm grids under `share/nav2_smac_planner/sample_primitives/5cm_resolution/`
in `0.5m_turning_radius/` and `1m_turning_radius/`, each with `ackermann/`, `diff/` and `omni/`
`output.json`. For other values, generate them with the script in the source tree:

```bash
git clone --depth 1 --branch jazzy https://github.com/ros-navigation/navigation2.git ~/src/navigation2
cd ~/src/navigation2/nav2_smac_planner/lattice_primitives
python3 -m venv ~/venvs/lattice && ~/venvs/lattice/bin/pip install -r requirements.txt   # numpy, matplotlib, Rtree
# my_lattice.json: {"motion_model": "diff", "turning_radius": 0.5, "grid_resolution": 0.05,
#                   "stopping_threshold": 5, "num_of_headings": 16}
~/venvs/lattice/bin/python generate_motion_primitives.py --config my_lattice.json \
  --output ~/my_robot_navigation/config/lattice_diff_5cm.json --visualizations /tmp/lattice_vis
```

`motion_model` is `ackermann`, `diff` or `omni`; `num_of_headings` should be a multiple of 8 (the
generator README recommends 16); `grid_resolution` must equal the global costmap resolution, and nothing in
the Jazzy planner checks it. Install the JSON with the package and point `lattice_filepath` at the
installed path.

## Smoother server

Smoothers post-process a path. The planner server does not call them: a BT must contain a `SmoothPath`
node after `ComputePathToPose` (none of the default Jazzy BTs do; editing the BT belongs to
[nav-nav2](../../nav-nav2/SKILL.md)). Smac planners already smooth internally (`smooth_path`), so a
smoother mainly helps NavFn and Theta* paths.

```yaml
smoother_server:
  ros__parameters:
    smoother_plugins: ["simple_smoother"]   # default ID and type if unset
    simple_smoother:
      plugin: "nav2_smoother::SimpleSmoother"
      tolerance: 1.0e-10
      max_its: 1000
      w_data: 0.2
      w_smooth: 0.3
      do_refinement: true
      refinement_num: 2
```

| Plugin | Use | Key parameters (Jazzy defaults) |
|---|---|---|
| `nav2_smoother::SimpleSmoother` | 2D planners; splits at reversals | `w_smooth` 0.3, `w_data` 0.2, `max_its` 1000, `do_refinement` `true`, `refinement_num` 2 |
| `nav2_smoother::SavitzkyGolaySmoother` | Light denoising, cheap | `do_refinement` `true`, `refinement_num` 2 |
| `nav2_constrained_smoother/ConstrainedSmoother` | Pushes the path away from obstacles, keeps a turning radius, Reeds-Shepp cusps | `minimum_turning_radius` 0.4, `w_curve` 30.0, `w_cost` 0.015, `w_dist` 0.0, `w_smooth` 2000000.0, `cost_check_points` `[]`, `reversing_enabled` `true`, `keep_start_orientation`/`keep_goal_orientation` `true`, `optimizer.max_iterations` 100 |

The constrained smoother keeps the old slash name and solves with Ceres (`libceres-dev`); it costs more
CPU than the others. For non-round robots set `cost_check_points` (x, y, weight triples in the robot
frame) so cost is checked at the footprint's corners, not only the centre.

The server's action is `/smooth_path` (`nav2_msgs/action/SmoothPath`: `path`, `smoother_id`,
`max_smoothing_duration`, `check_for_collisions`) and it republishes each result on `plan_smoothed`. Show
`/plan` and `/plan_smoothed` together in RViz: the smoothed path should stay out of inflated cost and keep
the start and goal poses. Error code 503 means the smoothed path was in collision.
