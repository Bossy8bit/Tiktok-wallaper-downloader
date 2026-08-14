import os
import uuid
import zipfile
import threading
from flask import Flask, request, send_file, jsonify, render_template_string
import yt_dlp

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# In-memory job store (use Redis/DB for production)
jobs = {}


def download_url(url: str, job_folder: str) -> dict:
    """Download a single TikTok video (prefer no-watermark) as MP4."""
    ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "outtmpl": os.path.join(job_folder, "%(id)s.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
        "merge_output_format": "mp4",
        "postprocessors": [
            {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
        ],
        "extractor_args": {"tiktok": {"api_hostname": "api.tiktokv.com"}},
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            fname = ydl.prepare_filename(info)
            base, _ = os.path.splitext(fname)
            mp4 = base + ".mp4"
            return {
                "url": url,
                "file": mp4 if os.path.exists(mp4) else fname,
                "title": info.get("title", "video"),
                "status": "ok",
            }
    except Exception as e:
        return {"url": url, "error": str(e), "status": "error"}


def worker(job_id: str, urls: list):
    job_folder = os.path.join(DOWNLOAD_FOLDER, job_id)
    os.makedirs(job_folder, exist_ok=True)

    results = [download_url(u, job_folder) for u in urls]

    zip_path = os.path.join(DOWNLOAD_FOLDER, f"{job_id}.zip")
    with zipfile.ZipFile(zip_path, "w") as zf:
        for r in results:
            if r.get("status") == "ok" and os.path.exists(r["file"]):
                zf.write(r["file"], os.path.basename(r["file"]))

    jobs[job_id].update({"results": results, "zip": zip_path, "status": "done"})


@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/download", methods=["POST"])
def download():
    raw = request.form.get("urls", "")
    urls = [u.strip() for u in raw.splitlines() if u.strip()]
    if not urls:
        return jsonify({"error": "No URLs provided"}), 400

    job_id = uuid.uuid4().hex
    jobs[job_id] = {"status": "processing", "results": [], "zip": None}
    threading.Thread(target=worker, args=(job_id, urls), daemon=True).start()
    return jsonify({"job_id": job_id})


@app.route("/status/<job_id>")
def status(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(job)


@app.route("/get_zip/<job_id>")
def get_zip(job_id):
    job = jobs.get(job_id)
    if not job or not job.get("zip") or not os.path.exists(job["zip"]):
        return jsonify({"error": "Zip not ready"}), 404
    return send_file(
        job["zip"],
        as_attachment=True,
        download_name="tiktok_wallpapers.zip",
    )


HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>TikTok Wallpaper Downloader</title>
  <style>
    :root { --bg:#0f0f0f; --card:#1c1c1e; --accent:#fe2c55; --txt:#fff; }
    * { box-sizing: border-box; }
    body { margin:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; background:var(--bg); color:var(--txt); display:flex; justify-content:center; }
    .container { width:100%; max-width:520px; padding:20px; }
    h1 { font-size:1.4rem; text-align:center; }
    textarea { width:100%; height:160px; background:var(--card); color:var(--txt); border:1px solid #333; border-radius:12px; padding:12px; font-size:15px; resize:vertical; }
    button { width:100%; margin-top:14px; padding:14px; border:none; border-radius:12px; background:var(--accent); color:#fff; font-size:16px; font-weight:600; cursor:pointer; }
    button:disabled { opacity:.5; }
    #status { margin-top:16px; text-align:center; font-size:14px; color:#aaa; min-height:20px; }
    .result-card { background:var(--card); border-radius:12px; padding:12px; margin-top:10px; font-size:14px; }
    .ok { color:#4ade80; }
    .err { color:#f87171; }
    a.dl { display:block; text-align:center; margin-top:16px; padding:14px; background:#25f4ee; color:#000; border-radius:12px; font-weight:700; text-decoration:none; }
  </style>
</head>
<body>
  <div class="container">
    <h1>📱 TikTok Wallpaper Downloader</h1>
    <p style="text-align:center;font-size:13px;color:#888;">Paste one TikTok link per line (supports multiple)</p>
    <textarea id="urls" placeholder="https://www.tiktok.com/@user/video/1234567890&#10;https://vt.tiktok.com/xxxxxxxx/"></textarea>
    <button id="btn" onclick="start()">Download Wallpapers</button>
    <div id="status"></div>
    <div id="result"></div>
  </div>
  <script>
    let timer = null;
    let currentJobId = null;

    function start() {
      const btn = document.getElementById("btn");
      const statusEl = document.getElementById("status");
      const resultEl = document.getElementById("result");
      const urls = document.getElementById("urls").value;

      if (!urls.trim()) { statusEl.textContent = "Please paste at least one link."; return; }

      btn.disabled = true;
      statusEl.textContent = "Processing... ⏳";
      resultEl.innerHTML = "";

      fetch("/download", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: "urls=" + encodeURIComponent(urls)
      })
      .then(r => r.json())
      .then(data => {
        if (data.error) { statusEl.textContent = data.error; btn.disabled = false; return; }
        currentJobId = data.job_id;
        poll();
      })
      .catch(e => { statusEl.textContent = "Error: " + e; btn.disabled = false; });
    }

    function poll() {
      timer = setInterval(() => {
        fetch("/status/" + currentJobId)
        .then(r => r.json())
        .then(job => {
          if (job.status === "done") {
            clearInterval(timer);
            render(job);
          } else {
            document.getElementById("status").textContent = "Downloading videos... ⏳";
          }
        });
      }, 1500);
    }

    function render(job) {
      document.getElementById("status").textContent = "Done! ✅";
      document.getElementById("btn").disabled = false;

      let html = '<a class="dl" href="/get_zip/' + currentJobId + '">⬇️ Download All (.zip)</a>';
      job.results.forEach(r => {
        if (r.status === "ok") {
          html += '<div class="result-card"><span class="ok">✔</span> ' + escapeHtml(r.title) + '</div>';
        } else {
          html += '<div class="result-card"><span class="err">✖</span> ' + escapeHtml(r.url) + ' — ' + escapeHtml(r.error) + '</div>';
        }
      });
      document.getElementById("result").innerHTML = html;
    }

    function escapeHtml(s) {
      return String(s).replace(/[&<>"']/g, c => (
        {"&":"&amp;","<":"&lt;",">":"&gt;","\\"":"&quot;","'":"&#39;"}[c]
      ));
    }
  </script>
</body>
</html>"""


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)