#!/usr/bin/env python3
"""Local web app for DestiNA DGL / SMART PNA probe design.

Run it and a browser tab opens:

    python destina_probe_app.py            # http://127.0.0.1:8765
    python destina_probe_app.py --port 9000 --no-browser

Paste a target sequence, choose the blank monomer and which positions are
gamma-modified, and it scans the target, ranks designs, picks a panel and
computes construct and labelled-product masses. There is also a box to weigh
and locate an existing probe written in DestiNA notation.

Uses only the Python standard library for the server and UI; the science comes
from pna_design / pna_chem next to this file, which is the same code the CLI
and the skill use - there is no second implementation to drift.
"""
from __future__ import annotations

import argparse
import csv
import html
import io
import json
import os
import sys
import threading
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pna_chem as pc          # noqa: E402
import pna_design as pd_       # noqa: E402

TAGGED = "SMART-C-REX-PEG12-biotin"
DEFAULT_TARGET = "UGGAGUGUGACAAUGGUGUUUG"
_LAST = {}          # id -> {"csv name": text}, for the download links

CSS = """
:root{--ink:#16202b;--mut:#64748b;--line:#e2e8f0;--bg:#f8fafc;--acc:#1f5fa9}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
 font:14px/1.5 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif}
header{background:#fff;border-bottom:1px solid var(--line);padding:14px 22px}
header h1{margin:0;font-size:17px;font-weight:650;letter-spacing:-.01em}
header p{margin:3px 0 0;color:var(--mut);font-size:12.5px}
main{max-width:1180px;margin:0 auto;padding:20px 22px 60px}
.card{background:#fff;border:1px solid var(--line);border-radius:10px;
 padding:16px 18px;margin-bottom:18px}
.card h2{margin:0 0 12px;font-size:14px;font-weight:650;text-transform:uppercase;
 letter-spacing:.05em;color:var(--mut)}
label{display:block;font-size:12px;color:var(--mut);margin:0 0 4px}
input,select,textarea{width:100%;padding:7px 9px;border:1px solid var(--line);
 border-radius:6px;font:13px ui-monospace,SFMono-Regular,Consolas,monospace;
 background:#fff;color:var(--ink)}
textarea{resize:vertical}
.row{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
 gap:12px;margin-bottom:12px}
button{background:var(--acc);color:#fff;border:0;border-radius:6px;
 padding:9px 18px;font-size:13px;font-weight:600;cursor:pointer}
button:hover{filter:brightness(1.08)}
table{border-collapse:collapse;width:100%;font-size:12.5px}
th,td{border-bottom:1px solid var(--line);padding:6px 9px;text-align:left;
 white-space:nowrap}
th{color:var(--mut);font-weight:600;font-size:11px;text-transform:uppercase;
 letter-spacing:.04em}
tbody tr:hover{background:#f1f5f9}
code,.mono{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}
.seq{font-family:ui-monospace,monospace;font-size:13px;letter-spacing:.5px}
.blank{color:#c2410c;font-weight:700}
.gam{color:#1f5fa9;font-weight:700}
.note{background:#fffbeb;border:1px solid #fde68a;border-radius:8px;
 padding:11px 13px;font-size:12.5px;color:#713f12;margin-bottom:16px}
.err{background:#fef2f2;border:1px solid #fecaca;color:#991b1b;
 border-radius:8px;padding:11px 13px;margin-bottom:16px}
.dl a{display:inline-block;margin-right:12px;font-size:12.5px;color:var(--acc)}
.scroll{overflow-x:auto}
.k{color:var(--mut)}
"""


def esc(x):
    return html.escape(str(x))


def seq_html(display, gamma=()):
    out = []
    for i, ch in enumerate(display, 1):
        if ch == "_":
            out.append('<span class="blank">_</span>')
        elif i in gamma:
            out.append(f'<span class="gam">{ch}</span>')
        else:
            out.append(ch)
    return "".join(out)


def table(rows, cols):
    if not rows:
        return "<p class='k'>no rows</p>"
    h = "".join(f"<th>{esc(c[1])}</th>" for c in cols)
    body = []
    for r in rows:
        tds = []
        for key, _lab in cols:
            v = r.get(key, "")
            tds.append(f"<td>{v if key.endswith('_html') else esc(v)}</td>")
        body.append("<tr>" + "".join(tds) + "</tr>")
    return (f"<div class='scroll'><table><thead><tr>{h}</tr></thead>"
            f"<tbody>{''.join(body)}</tbody></table></div>")


def to_csv(rows):
    if not rows:
        return ""
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(rows[0]), extrasaction="ignore")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def parse_gamma(arg, n):
    if not arg or arg.strip() in ("", "none"):
        return {}
    if arg.strip() == "all":
        return {i: "Glu" for i in range(1, n + 1)}
    out = {}
    for tok in arg.replace(" ", "").split(","):
        if not tok:
            continue
        pos, _, side = tok.partition(":")
        out[int(pos)] = side or "Glu"
    return out


def form(values):
    g = lambda k, d="": esc(values.get(k, d))
    blanks = "".join(
        f"<option{' selected' if values.get('blank', 'L-Ser') == b else ''}>{b}</option>"
        for b in sorted(pc.BLANK_TYPES))
    return f"""
<form method="post" action="/">
 <div class="card">
  <h2>Target</h2>
  <label>Sequence (DNA or RNA, 5'&rarr;3')</label>
  <textarea name="target" rows="2" spellcheck="false">{g('target', DEFAULT_TARGET)}</textarea>
  <div class="row" style="margin-top:12px">
   <div><label>Name</label><input name="id" value="{g('id','target')}"></div>
   <div><label>Abasic blank monomer</label><select name="blank">{blanks}</select></div>
   <div><label>Gamma positions (all / none / 7,12,15)</label>
        <input name="gamma" value="{g('gamma','')}"></div>
   <div><label>Probe lengths</label><input name="len_range" value="{g('len_range','9-18')}"></div>
   <div><label>Min matched flank</label><input name="min_arm" value="{g('min_arm','4')}"></div>
   <div><label>Preferred min Tm (&deg;C)</label><input name="min_tm" value="{g('min_tm','55')}"></div>
  </div>
  <label>Optional - weigh an existing probe (DestiNA notation)</label>
  <div class="row" style="margin-bottom:0">
   <div style="grid-column:span 3"><input name="probe" class="mono"
     placeholder="x x C A C C A T Tglu G T *L-Ser* A Cglu A C Tglu C C A"
     value="{g('probe')}"></div>
   <div><input name="probe_name" placeholder="label e.g. DGL-122_4.6"
     value="{g('probe_name')}"></div>
  </div>
  <div style="margin-top:14px"><button type="submit">Design probes</button></div>
 </div>
</form>"""


def page(body, values=None):
    return f"""<!doctype html><html><head><meta charset="utf-8">
<title>DestiNA DGL probe design</title><style>{CSS}</style></head><body>
<header><h1>DestiNA DGL / SMART PNA probe design</h1>
<p>Scan a target, place the abasic blank, pick the SMART reagent, weigh the construct.</p>
</header><main>{form(values or {})}{body}</main></body></html>"""


def analyse(v):
    target = "".join(c for c in v.get("target", "").upper() if not c.isspace())
    bad = sorted(set(target) - set("ACGTU"))
    if not target:
        raise ValueError("Enter a target sequence.")
    if bad:
        raise ValueError(f"Target contains non-ACGTU characters: {', '.join(bad)}")
    tid = v.get("id") or "target"
    if v.get("len_range"):
        lo, hi = (int(x) for x in v["len_range"].split("-"))
        pd_.LEN_RANGE = (lo, hi)
    if v.get("min_arm"):
        pd_.MIN_ARM = int(v["min_arm"])
    blank = v.get("blank", "L-Ser")
    min_tm = float(v.get("min_tm") or 55)

    scan, designs = pd_.scan_target(target, tid)
    if not designs:
        raise ValueError(
            f"No valid designs: the target is {len(target)} nt but needs at "
            f"least {2 * pd_.MIN_ARM + 1} nt to place a blank with "
            f"{pd_.MIN_ARM} matched bases on each side.")
    unreachable = pd_.uncovered_positions(target, scan)

    panel = []
    for rg in ("CCHO", "GCHO", "ACHO", "TCHO"):
        sub = [d for d in designs if d.smart_reagent == rg]
        warm = [d for d in sub if d.tm_pna >= min_tm] or sub
        if warm:
            panel.append(warm[0])

    prow = []
    for n, d in enumerate(panel, 1):
        gm = parse_gamma(v.get("gamma"), d.probe_len)
        mol = pc.build_pna(d.pna_display, gamma=gm, blank_type=blank)
        m = pc.masses(mol)
        lp = pc.labelled_product(mol, pc.SMART_TAGGED[TAGGED])
        prow.append(dict(
            name=f"{tid}_P{n}", seq_html=seq_html(d.pna_display, gm),
            pna_display=d.pna_display,
            reads=f"{d.interrogated_base}{d.interrogated_pos}",
            smart_reagent=d.smart_reagent, probe_len=d.probe_len,
            window=f"{d.target_start}-{d.target_end}",
            blank=f"{d.blank_pos}/{d.blank_from_cterm}",
            tm_pna=d.tm_pna, score=d.score, formula=m["formula"],
            avg=m["average"], mono=m["monoisotopic"], tagged_avg=lp["average"]))

    probe_html = ""
    if v.get("probe", "").strip():
        p = pc.parse_probe(v["probe"])
        # pin a supplied probe into the panel: a validated sequence should be
        # shown beside the candidates whatever the heuristic ranks first
        _h = [d for d in designs if d.pna_display == p["display"]]
        if _h:
            _d = _h[0]
            _m = pc.build_probe(v["probe"])
            _ms, _lp = pc.masses(_m), pc.labelled_product(_m, pc.SMART_TAGGED[TAGGED])
            prow.insert(0, dict(
                name=v.get("probe_name") or "supplied",
                seq_html=seq_html(_d.pna_display, p["gamma"]),
                pna_display=_d.pna_display,
                reads=f"{_d.interrogated_base}{_d.interrogated_pos}",
                smart_reagent=_d.smart_reagent, probe_len=_d.probe_len,
                window=f"{_d.target_start}-{_d.target_end}",
                blank=f"{_d.blank_pos}/{_d.blank_from_cterm}",
                tm_pna=_d.tm_pna, score=f"{_d.score} (rank {designs.index(_d)+1})",
                formula=_ms["formula"], avg=_ms["average"],
                mono=_ms["monoisotopic"], tagged_avg=_lp["average"]))
        mol = pc.build_probe(v["probe"])
        m, lp = pc.masses(mol), pc.labelled_product(mol, pc.SMART_TAGGED[TAGGED])
        hit = [d for d in designs if d.pna_display == p["display"]]
        loc = (f"reads {hit[0].interrogated_base}{hit[0].interrogated_pos} via "
               f"{hit[0].smart_reagent}, Tm {hit[0].tm_pna} &deg;C, rank "
               f"{designs.index(hit[0]) + 1}/{len(designs)}" if hit
               else "<span class='k'>does not match any window of this target</span>")
        probe_html = f"""<div class="card"><h2>Supplied probe</h2>
<p class="seq">{seq_html(p['display'], p['gamma'])}
 &nbsp;<span class="k">{p['n_residues']}-mer</span></p>
<table><tbody>
<tr><th>blank</th><td>*{esc(p['blank_type'])}* at {p['blank_pos']} from N /
 {p['blank_from_cterm']} from C</td></tr>
<tr><th>gamma</th><td>{esc(sorted(p['gamma']) or 'none')}</td></tr>
<tr><th>formula</th><td class="mono">{esc(m['formula'])}</td></tr>
<tr><th>mass</th><td>monoisotopic {m['monoisotopic']} &nbsp; average {m['average']}</td></tr>
<tr><th>labelled</th><td>{lp['average']} &nbsp;(+{lp['d_average']} with {TAGGED})</td></tr>
<tr><th>on target</th><td>{loc}</td></tr>
</tbody></table></div>"""

    _LAST[tid] = {"scan.csv": to_csv(scan),
                  "designs.csv": to_csv([pd_.asdict(d) for d in designs]),
                  "panel.csv": to_csv([{k: x[k] for k in x if k != "seq_html"}
                                       for x in prow])}
    dl = " ".join(f"<a href='/dl?id={urllib.parse.quote(tid)}&f={f}'>{f}</a>"
                  for f in _LAST[tid])

    warn = ""
    if unreachable:
        warn = (f"<div class='note'><b>Not interrogable</b> with "
                f"{pd_.MIN_ARM} matched bases each side: positions "
                f"{', '.join(map(str, unreachable))}. Extend the target to read them."
                f"</div>")

    scan_cols = [("interrogated_pos", "pos"), ("interrogated_base", "base"),
                 ("smart_reagent", "reagent"), ("n_designs", "designs"),
                 ("best_score", "score"), ("best_len", "L"),
                 ("best_window", "window"), ("best_blank_pos", "blank N"),
                 ("best_blank_from_cterm", "blank C"), ("best_tm", "Tm"),
                 ("tm_min", "Tm min"), ("tm_max", "Tm max"),
                 ("best_pna", "probe N->C")]
    panel_cols = [("name", "probe"), ("seq_html", "sequence N->C"),
                  ("reads", "reads"), ("smart_reagent", "reagent"),
                  ("probe_len", "L"), ("window", "window"), ("blank", "blank N/C"),
                  ("tm_pna", "Tm"), ("score", "score"), ("formula", "formula"),
                  ("avg", "avg mass"), ("tagged_avg", "+ tagged")]
    return f"""{warn}
<div class="card"><h2>Panel &mdash; one probe per SMART reagent</h2>
{table(prow, panel_cols)}
<p class="k" style="margin:10px 0 0">Blank <span class="blank">_</span>,
 gamma-modified positions <span class="gam">in blue</span>.
 Masses are for H-{'X' * 2}-[PNA]-Lys-NH2 with blank *{esc(blank)}*.</p></div>
{probe_html}
<div class="card"><h2>Scan &mdash; every interrogable position</h2>
{table(scan, scan_cols)}
<p class="dl" style="margin-top:10px">Download: {dl}</p></div>
<div class="note"><b>Read this with the numbers.</b> Tm is the Giesen PNA/DNA
regression (&plusmn;5 K for &gt;90% of sequences) &mdash; rank with it, do not
quote it as a prediction; an RNA target is folded to DNA and PNA&middot;RNA is
more stable, so values are conservative. Gamma stabilisation is not quantified
(offset defaults to 0). Mass windows must use the <b>tagged</b> reagent
increment. Off-target cross-hybridisation is <b>not</b> screened. The score is a
<b>screening heuristic, not a yield model</b> &mdash; an experimentally validated
probe outranks it; paste it above and it is pinned into the panel.</div>"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, body, ctype="text/html; charset=utf-8", extra=None):
        data = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        if u.path == "/dl":
            q = urllib.parse.parse_qs(u.query)
            tid, f = q.get("id", [""])[0], q.get("f", [""])[0]
            body = _LAST.get(tid, {}).get(f)
            if body is None:
                self._send(page("<div class='err'>No such download.</div>"))
                return
            self._send(body, "text/csv; charset=utf-8",
                       {"Content-Disposition": f'attachment; filename="{tid}_{f}"'})
            return
        if u.path != "/":
            self._send(page("<div class='err'>Not found.</div>"))
            return
        self._send(page(""))

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(n).decode("utf-8")
        v = {k: vs[0] for k, vs in urllib.parse.parse_qs(raw, keep_blank_values=True).items()}
        try:
            body = analyse(v)
        except Exception as exc:
            body = f"<div class='err'><b>{type(exc).__name__}:</b> {esc(exc)}</div>"
        self._send(page(body, v))

    def log_message(self, *a):
        pass


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--no-browser", action="store_true")
    a = ap.parse_args(argv)
    pc.validate()
    srv = ThreadingHTTPServer((a.host, a.port), Handler)
    url = f"http://{a.host}:{a.port}"
    print(f"DestiNA probe design app -> {url}   (Ctrl-C to stop)")
    if not a.no_browser:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")


if __name__ == "__main__":
    main()
