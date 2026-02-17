import json, statistics
from urllib.parse import urlparse

RESULT_FILE = "results.json"
REPORT_HTML = "hr_payroll_report.html"

with open(RESULT_FILE, "r", encoding="utf-8") as f:
    results = json.load(f)

times = [r["load_time"] for r in results]
avg = round(statistics.mean(times), 2) if times else 0
fast = min(results, key=lambda x: x["load_time"]) if results else None
slow = max(results, key=lambda x: x["load_time"]) if results else None
fail = len([r for r in results if any("HTTP status" in i for i in r["issues"])])

sev_count = {"High": 0, "Medium": 0, "Low": 0}

# Page load time categories
good = sum(1 for r in results if 1 <= r["load_time"] <= 3)
average = sum(1 for r in results if 4 <= r["load_time"] <= 8)
poor = sum(1 for r in results if r["load_time"] >= 9)

# Shortened labels (only endpoint)
labels = []
for r in results:
    path = urlparse(r["url"]).path
    labels.append(path if path else r["url"])

cards = ""
for idx, r in enumerate(results):
    sev = "Low"
    if any("HTTP status" in i or "Console" in i or "Visit failed" in i for i in r["issues"]):
        sev = "High"
    elif any("Slow load" in i or "Redirected" in i for i in r["issues"]):
        sev = "Medium"
    sev_count[sev] += 1

    tips = []
    for i in r["issues"]:
        if "Console" in i: tips.append("Fix JavaScript errors.")
        elif "Missing H1" in i: tips.append("Add an H1 heading.")
        elif "Redirected" in i: tips.append("Reduce redirects.")
        elif "Slow load" in i: tips.append("Optimize assets for faster load.")
        elif "HTTP status" in i: tips.append("Check server response.")
        elif "Visit failed" in i: tips.append("Verify page availability.")
    suggestion = "; ".join(tips) if tips else "No issues"

    logs_html = "".join([f"<div class='log-{l['level'].lower()}'>{l['level']} - {l['message']}</div>" for l in r["js_logs"]])
    issues_display = "OK" if not r["issues"] else "Issues: " + ", ".join(r["issues"])

    cards += f"""
    <div class="card {sev}" id="card-{idx}" data-severity="{sev}" data-errorcount="{len(r['issues'])}" data-status="{issues_display}">
        <h3>{r['url']}</h3>
        <p class="status" id="status-{idx}">{issues_display}</p>
        <p><b>Load Time:</b> {r['load_time']:.2f}s | <span class="badge {sev}" id="badge-{idx}">{sev}</span></p>
        <p><b>Visited At:</b> {r['visited_time']}</p>
        <p><b>Suggestions:</b> {suggestion}</p>
        <img src="{r['screenshot']}" class="screenshot" onclick="window.open(this.src)">
        <button class="collapsible">View JS Logs</button>
        <div class="content">{logs_html or '<em>No logs</em>'}</div>
        <button class="ignore-btn" onclick="toggleIgnore({idx})">Ignore Errors</button>
    </div>
    """

html = f"""
<html>
<head>
    <title>Automation Report</title>
    <style>
        body {{ background:#1e1e1e; color:#ddd; font-family:Arial; margin:0; padding:0; }}
        h1,h2,h3 {{ color:#00aaff; }}
        .summary {{ padding:20px; }}
        .cards {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:20px; padding:20px; }}
        .card {{ background:#2b2b2b; border-radius:10px; padding:15px; box-shadow:0 0 10px rgba(0,0,0,0.6); transition:transform .2s; }}
        .card:hover {{ transform:scale(1.03); }}
        .card h3 {{ font-size:1rem; color:#00aaff; margin-bottom:10px; }}
        .screenshot {{ width:100%; border-radius:8px; margin:10px 0; cursor:pointer; }}
        .badge.High {{ background:#dc3545; padding:2px 6px; border-radius:4px; }}
        .badge.Medium {{ background:#ffc107; padding:2px 6px; border-radius:4px; color:#000; }}
        .badge.Low {{ background:#28a745; padding:2px 6px; border-radius:4px; }}
        .collapsible {{ background:#444; color:#fff; padding:5px; border:none; border-radius:4px; cursor:pointer; }}
        .ignore-btn {{ background:#007bff; color:#fff; padding:5px; border:none; margin-top:10px; border-radius:4px; cursor:pointer; }}
        .log-info {{ color:cyan; }} .log-warning {{ color:orange; }} .log-severe {{ color:red; font-weight:bold; }}
    </style>
</head>
<body>
    <div class="summary">
        <h1>Automation Report</h1>
        <p id="pageSummary"><b>Total Pages:</b> {len(results)} | <b>Failed:</b> {fail}</p>
        <p><b>Average Load:</b> {avg}s</p>
        <p><b>Fastest:</b> {fast['url'] if fast else '-'} ({fast['load_time'] if fast else '-'})</p>
        <p><b>Slowest:</b> {slow['url'] if slow else '-'} ({slow['load_time'] if slow else '-'})</p>
        <p><b>Page Load Categories:</b> Good - {good} | Average - {average} | Poor - {poor}</p>
    </div>
    <div class="cards">{cards}</div>
    <script>
        let ignored = Array({len(results)}).fill(false);

        document.querySelectorAll('.collapsible').forEach(b => b.onclick = function() {{
            this.classList.toggle('active');
            var c = this.nextElementSibling;
            c.style.display = (c.style.display === 'block') ? 'none' : 'block';
        }});
    </script>
</body>
</html>
"""

with open(REPORT_HTML, "w", encoding="utf-8") as f:
    f.write(html)
print(f"📄 Final report generated: {REPORT_HTML}")
import json, statistics
from urllib.parse import urlparse

RESULT_FILE = "results.json"
REPORT_HTML = "hr_payroll_report.html"

with open(RESULT_FILE, "r", encoding="utf-8") as f:
    results = json.load(f)

times = [r["load_time"] for r in results]
avg = round(statistics.mean(times), 2) if times else 0
fast = min(results, key=lambda x: x["load_time"]) if results else None
slow = max(results, key=lambda x: x["load_time"]) if results else None
fail = len([r for r in results if any("HTTP status" in i for i in r["issues"])])

sev_count = {"High": 0, "Medium": 0, "Low": 0}

# Page load time categories
good = sum(1 for r in results if 1 <= r["load_time"] <= 3)
average = sum(1 for r in results if 4 <= r["load_time"] <= 8)
poor = sum(1 for r in results if r["load_time"] >= 9)

# Shortened labels (only endpoint)
labels = []
for r in results:
    path = urlparse(r["url"]).path
    labels.append(path if path else r["url"])

cards = ""
for idx, r in enumerate(results):
    sev = "Low"
    if any("HTTP status" in i or "Console" in i or "Visit failed" in i for i in r["issues"]):
        sev = "High"
    elif any("Slow load" in i or "Redirected" in i for i in r["issues"]):
        sev = "Medium"
    sev_count[sev] += 1

    tips = []
    for i in r["issues"]:
        if "Console" in i: tips.append("Fix JavaScript errors.")
        elif "Missing H1" in i: tips.append("Add an H1 heading.")
        elif "Redirected" in i: tips.append("Reduce redirects.")
        elif "Slow load" in i: tips.append("Optimize assets for faster load.")
        elif "HTTP status" in i: tips.append("Check server response.")
        elif "Visit failed" in i: tips.append("Verify page availability.")
    suggestion = "; ".join(tips) if tips else "No issues"

    logs_html = "".join([f"<div class='log-{l['level'].lower()}'>{l['level']} - {l['message']}</div>" for l in r["js_logs"]])
    issues_display = "OK" if not r["issues"] else "Issues: " + ", ".join(r["issues"])

    cards += f"""
    <div class="card {sev}" id="card-{idx}" data-severity="{sev}" data-errorcount="{len(r['issues'])}" data-status="{issues_display}">
        <h3>{r['url']}</h3>
        <p class="status" id="status-{idx}">{issues_display}</p>
        <p><b>Load Time:</b> {r['load_time']:.2f}s | <span class="badge {sev}" id="badge-{idx}">{sev}</span></p>
        <p><b>Visited At:</b> {r['visited_time']}</p>
        <p><b>Suggestions:</b> {suggestion}</p>
        <img src="{r['screenshot']}" class="screenshot" onclick="window.open(this.src)">
        <button class="collapsible">View JS Logs</button>
        <div class="content">{logs_html or '<em>No logs</em>'}</div>
        <button class="ignore-btn" onclick="toggleIgnore({idx})">Ignore Errors</button>
    </div>
    """

html = f"""
<html>
<head>
    <title>Automation Report</title>
    <style>
        body {{ background:#1e1e1e; color:#ddd; font-family:Arial; margin:0; padding:0; }}
        h1,h2,h3 {{ color:#00aaff; }}
        .summary {{ padding:20px; }}
        .cards {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:20px; padding:20px; }}
        .card {{ background:#2b2b2b; border-radius:10px; padding:15px; box-shadow:0 0 10px rgba(0,0,0,0.6); transition:transform .2s; }}
        .card:hover {{ transform:scale(1.03); }}
        .card h3 {{ font-size:1rem; color:#00aaff; margin-bottom:10px; }}
        .screenshot {{ width:100%; border-radius:8px; margin:10px 0; cursor:pointer; }}
        .badge.High {{ background:#dc3545; padding:2px 6px; border-radius:4px; }}
        .badge.Medium {{ background:#ffc107; padding:2px 6px; border-radius:4px; color:#000; }}
        .badge.Low {{ background:#28a745; padding:2px 6px; border-radius:4px; }}
        .collapsible {{ background:#444; color:#fff; padding:5px; border:none; border-radius:4px; cursor:pointer; }}
        .ignore-btn {{ background:#007bff; color:#fff; padding:5px; border:none; margin-top:10px; border-radius:4px; cursor:pointer; }}
        .log-info {{ color:cyan; }} .log-warning {{ color:orange; }} .log-severe {{ color:red; font-weight:bold; }}
    </style>
</head>
<body>
    <div class="summary">
        <h1>Automation Report</h1>
        <p id="pageSummary"><b>Total Pages:</b> {len(results)} | <b>Failed:</b> {fail}</p>
        <p><b>Average Load:</b> {avg}s</p>
        <p><b>Fastest:</b> {fast['url'] if fast else '-'} ({fast['load_time'] if fast else '-'})</p>
        <p><b>Slowest:</b> {slow['url'] if slow else '-'} ({slow['load_time'] if slow else '-'})</p>
        <p><b>Page Load Categories:</b> Good - {good} | Average - {average} | Poor - {poor}</p>
    </div>
    <div class="cards">{cards}</div>
    <script>
        let ignored = Array({len(results)}).fill(false);

        document.querySelectorAll('.collapsible').forEach(b => b.onclick = function() {{
            this.classList.toggle('active');
            var c = this.nextElementSibling;
            c.style.display = (c.style.display === 'block') ? 'none' : 'block';
        }});
    </script>
</body>
</html>
"""

with open(REPORT_HTML, "w", encoding="utf-8") as f:
    f.write(html)
print(f"📄 Final report generated: {REPORT_HTML}")
