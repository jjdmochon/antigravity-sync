---
name: google-drive-breaks-node-tooling
description: npm/Vite/Gradle fail on the Google Drive mounts K:\ and G:\ (EBADF, EPERM, half-written node_modules); keep sources on Drive, install and build on C:
metadata:
  type: project
---

Google Drive for Desktop (`K:\Mi unidad`, `G:\Mi unidad`) breaks Node and Gradle tooling in every project, not just one:
`npm install` dies with `EBADF` / `TAR_ENTRY_ERROR` / `EPERM`, leaves corrupt packages that fail misleadingly
(`tsc` exiting 0 without checking anything, `vite` missing `bin/vite.js`), Drive rejects junctions
(`mklink /J` → "Se requieren volúmenes NTFS locales"), and failed deletes leave ghost paths with "Acceso denegado" until Drive restarts.

**Why:** Drive's streaming FS locks files mid-sync. Learned twice independently in two QFDOS projects (2026-08-28 and 2026-09-24) before being promoted here.

**How to apply:** sources stay on K:/G:; `node_modules`, dev servers and builds run from a local mirror on C: (robocopy src across). Existing mirrors: `C:\Users\Juanjo\qfdos-v3-node` (via `dev.ps1`) and `%USERPROFILE%\dev\qfdos-web-v3-app` (Capacitor/Android). If a Node tool behaves inexplicably on Drive, check package integrity first (`node node_modules/<pkg>/... --version`). Project-level detail lives in the QFDOS project memories.
