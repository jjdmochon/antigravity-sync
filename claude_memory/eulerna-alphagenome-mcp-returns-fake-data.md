---
name: eulerna-alphagenome-mcp-returns-fake-data
description: "The Eulerna AlphaGenome MCP server and its scan script return hardcoded fabricated values, not model predictions — never use them for analysis"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6fdf762e-195e-4e0c-9cd2-a882d42bcc2b
  modified: 2026-09-20T21:09:42.147Z
---

The AlphaGenome MCP server at `K:\Mi unidad\Eulerna\alphagenome_agent\dist\alphagenome-agent\mcp\alphagenome-mcp\alphagenome_server.py` does **not** call AlphaGenome. `alphagenome_score_variant` returns the same hardcoded dict for every input: `avi_impact_score` 0.84, `predicted_expression_log2fc` −1.35, `chromatin_accessibility_change` −0.62, `disrupted_motifs` NF-kB / STAT3 / AP-1. It reads `ALPHAGENOME_API_KEY` only to set an `api_connected` boolean, then ignores it. `alphagenome_scan_enhancer_locus` and `C:\Users\Juanjo\.claude\skills\alphagenome-eulerna\scripts\run_eulerna_enhancer_scan.py` likewise emit fixed fake hotspots (offsets +342 and +815, "criticality" 0.94 / 0.89).

**Why:** these look authoritative — registered MCP tools with plausible JSON — so fabricated numbers can pass silently into a scientific report. Verified by reading the source on 2026-09-20.

**How to apply:** for any real AlphaGenome work use the DeepMind client instead — `C:\Users\Juanjo\.claude\skills\alphagenome-variant-impact-score\scripts\alphagenome_atlas_avi.py`, which needs `ALPHAGENOME_API_KEY` (not stored on this machine; Juanjo supplies it per session). On Windows `uv run` fails on the `pysam` dependency, which is imported at module scope but used only by the VCF `annotate` paths — a venv without pysam plus a stub on PYTHONPATH makes `query`, `region`, `gtf` and `metadata` work. If any document contains AlphaGenome figures whose provenance is not a logged live run, treat them as suspect. See [[irf2bpl-thomas-project]].
