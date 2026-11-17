---
description: Move a general lesson from a project into the workspace wiki or a skill, with the project's names removed.
argument-hint: <project> [the lesson]
---

Promote a lesson from **$ARGUMENTS** into the workspace.

1. **Find the lessons.** Use the lesson given, or read "Lessons to promote" in
   `projects/<project>/PROJECT.md`.
2. **Is it general?** It must help someone building a different robot. If it only holds for this
   project, say so and leave it there.
3. **Find its place** with "Where does it go?" in [AGENTS.md](../../AGENTS.md). Prefer adding to
   an existing page or skill; make a new one from a template only when nothing fits.
4. **Write it generally.** Remove the project's name, paths and private details. Use
   `evidence: built`. As its source, link the project's repo if `visibility` is `public`;
   if private, write "a private build" and the date, with no name.
5. **Mark it promoted** in the project's `PROJECT.md`, with the workspace path it went to. That is
   a project file: it is committed in the project's repo, not the workspace.
6. **Finish:** run `uv run tools/build_index.py` and `uv run tools/lint.py`. Report what moved where,
   and which repo each changed file belongs to.
