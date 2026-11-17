# MCP servers

MCP servers let the agent drive engineering tools instead of only advising. This folder has one
setup guide per server, named after it: `freecad.md`, `konnect.md`.

Each guide says:

1. What the server does and which work it is for.
2. The pinned version and its [source registry](../sources/registry.yaml) entry.
3. How to install it on Windows, Linux and macOS.
4. The config block for `.mcp.json`.
5. A health check, and what to do when it fails.
6. Known traps.

## Config

`.mcp.json` holds paths on your own machine, so it is gitignored. Copy
[`.mcp.example.json`](../.mcp.example.json) to `.mcp.json` at the workspace root and fill in the
`<…>` placeholders. MCP servers are set up at the workspace root because every project uses the
same tools; a project's own `.mcp.json` would not load when you open the workspace.

The FreeCAD and Konnect guides are written in Phase 5, or move here from OrbiBot if it comes in
first.
