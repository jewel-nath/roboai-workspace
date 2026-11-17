---
description: Start a new robot project in projects/<name>, as its own git repo, from the project template.
argument-hint: <name> [what the robot is for]
---

Start a project from **$ARGUMENTS**, as [projects/README.md](../../projects/README.md) describes.

1. **Name.** Turn the first word of the arguments into a kebab-case slug. Stop and tell the user if
   `projects/<name>/` already exists.
2. **Copy** everything in `templates/project/`, including `.gitignore` and `docs/`, to
   `projects/<name>/`.
3. **Fill in** `PROJECT.md` from the description and this conversation: name, summary, category,
   stage `idea`, visibility `private`. Leave anything unknown empty. Replace `<Project name>` in
   `CLAUDE.md` and `README.md`.
4. **Check** the workspace ignores it: `git check-ignore projects/<name>/PROJECT.md` must print the
   path.
5. **Ask** before running `git init` in `projects/<name>/`, before its first commit, and before
   adding a remote. Commit project files only with `git -C projects/<name>`.
6. **Report** the path, and suggest next steps: requirements in `PROJECT.md`, and reference robots
   from the Robot Atlas with `/compare`.
