# Wiki

The knowledge half of RoboAI Workspace: **one entity per page**, each with frontmatter from
[docs/frontmatter.md](../docs/frontmatter.md), written from a template in
[templates/](../templates/).

| Section | Holds | Template |
|---|---|---|
| [robots/](robots/) | The Robot Atlas: one research profile per robot | [robot.md](../templates/robot.md) |
| [parts/](parts/) | Actuators, MCUs, drivers, sensors, compute, power, materials | [part.md](../templates/part.md) |
| [tools/](tools/) | The programs and platforms you work in: CAD, EDA, simulators, ROS 2, video | [tool.md](../templates/tool.md) |
| [software/](software/) | Libraries and packages you build on: Nav2, MoveIt 2, slam_toolbox, OpenCV | [tool.md](../templates/tool.md) |
| [learning/](learning/) | Policies, foundation models, datasets | [tool.md](../templates/tool.md) |
| [concepts/](concepts/) | How things work: kinematics, PID, power budgets, design for printing | [concept.md](../templates/concept.md) |
| [guides/](guides/) | Decision guides that compare options and recommend one | [guide.md](../templates/guide.md) |

## Rules

- **File name = slug**, kebab-case: `so-101.md`, `feetech-sts3215.md`.
- **Every page** has `sources`, `evidence` and `last_verified`. A number without a source does not
  go in.
- **Our own words.** Summarise facts; link to other people's files instead of copying them.
- **Index sections are generated.** Text between `<!-- index:start -->` and `<!-- index:end -->`
  is rewritten by the index generator (Phase 1); do not edit it by hand.
- What does not earn a page goes in the triage note of its source in [sources/](../sources/), as
  an index row or a Rejected entry.
