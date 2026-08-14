import os
import re
import uuid
import zipfile
import threading
import requests
from flask import Flask, request, send_file, jsonify, render_template_string

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

jobs = {}
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

print(">>> LOADED app.py v5 (3rd-party API - no cookies needed) <<<")


def get_session():
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Referer": "https://www.tiktok.com/"})
    return s


def save_file(url, session, job_folder, filename):
    try:
        r = session.get(url, timeout=40, stream=True)
        r.raise_for_status()
        path = os.path.join(job_folder, filename)
        with open(path, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        return path
    except Exception as e:
        print("save err:", e)
        return None


def clean_title(t):
    if not t:
        return "tiktok"
    t = re.sub(r'[\\/:*?"<>|]', '', t).strip()
    return t[:50] or "tiktok"


def try_tikwm(url, s, job_folder):
    try:
        r = s.get("https://www.tikwm.com/api/", params={"url": url, "hd": 1}, timeout=30)
        if r.status_code != 200:
            return None
        d = r.json()
        if d.get("code") != 0:
            return None
        data = d.get("data", {})
        title = clean_title(data.get("title"))
        imgs = data.get("images") or []
        if imgs:
            files = []
            for i, img in enumerate(imgs):
                u = img.get("url") if isinstance(img, dict) else img
                if not u:
                    continue
                ext = ".png" if "png" in str(u).lower() else ".jpg"
                f = save_file(u, s, job_folder, f"photo_{i}{ext}")
                if f:
                    files.append(f)
            if files:
                return {"url": url, "files": files, "title": title, "count": len(files), "status": "ok"}
        vurl = data.get("play") or data.get("wmplay") or data.get("video")
        if vurl:
            f = save_file(vurl, s, job_folder, f"{title}.mp4")
            if f:
                return {"url": url, "file": f, "title": title, "count": 1, "status": "ok"}
        return None
    except Exception as e:
        print("tikwm err:", e)
        return None


def try_tiklydown(url, s, job_folder):
    try:
        r = s.get("https://api.tiklydown.eu.org/api/download", params={"url": url}, timeout=30)
        if r.status_code != 200:
            return None
        d = r.json()
        if not d.get("ok"):
            return None
        res = d.get("result", {})
        title = clean_title(res.get("desc") or res.get("title"))
        imgs = res.get("images") or []
        if imgs:
            files = []
            for i, img in enumerate(imgs):
                u = img.get("url") if isinstance(img, dict) else img
                if not u:
                    continue
                ext = ".png" if "png" in str(u).lower() else ".jpg"
                f = save_file(u, s, job_folder, f"photo_{i}{ext}")
                if f:
                    files.append(f)
            if files:
                return {"url": url, "files": files, "title": title, "count": len(files), "status": "ok"}
        vurl = None
        if isinstance(res.get("video"), dict):
            vurl = res["video"].get("noWatermark") or res["video"].get("url")
        else:
            vurl = res.get("video")
        if vurl:
            f = save_file(vurl, s, job_folder, f"{title}.mp4")
            if f:
                return {"url": url, "file": f, "title": title, "count": 1, "status": "ok"}
        return None
    except Exception as e:
        print("tiklydown err:", e)
        return None


def download_url(url, job_folder):
    s = get_session()
    for fn in (try_tikwm, try_tiklydown):
        res = fn(url, s, job_folder)
        if res:
            return res
    return {"url": url, "error": "ทุกวิธีล้มเหลว (ลองใหม่ภายหลัง)", "status": "error"}


def worker(job_id, urls):
    job_folder = os.path.join(DOWNLOAD_FOLDER, job_id)
    os.makedirs(job_folder, exist_ok=True)
    results = [download_url(u, job_folder) for u in urls]
    zip_path = os.path.join(DOWNLOAD_FOLDER, f"{job_id}.zip")
    with zipfile.ZipFile(zip_path, "w") as zf:
        for r in results:
            if r.get("status") != "ok":
                continue
            if r.get("files"):
                for f in r["files"]:
                    if os.path.exists(f):
                        zf.write(f, os.path.basename(f))
            elif r.get("file") and os.path.exists(r["file"]):
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
    return send_file(job["zip"], as_attachment=True, download_name="tiktok_wallpapers.zip")


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
    .hint { text-align:center; font-size:12px; color:#888; margin-top:10px; }
  </style>
</head>
<body>
  <div class="container">
    <h1>📱 TikTok Wallpaper Downloader</h1>
    <p style="text-align:center;font-size:13px;color:#888;">วางลิงก์ TikTok video หรือ photo (หนึ่งลิงก์ต่อบรรทัด)</p>
    <textarea id="urls" placeholder="https://www.tiktok.com/@user/video/123&#10;https://www.tiktok.com/@user/photo/456"></textarea>
    <button id="btn" onclick="start()">Download Wallpapers</button>
    <div id="status"></div>
    <div id="result"></div>
    <p class="hint">ใช้บริการโหลดฟรี (ไม่ต้อง cookies) — ถ้ารูปโหลดไม่ได้ชั่วคราว ให้ลองใหม่ภายหลัง</p>
  </div>
  <script>
    let timer = null;
    let currentJobId = null;
    function start() {
      const btn = document.getElementById("btn");
      const statusEl = document.getElementById("status");
      const resultEl = document.getElementById("result");
      const urls = document.getElementById("urls").value;
      if (!urls.trim()) { statusEl.textContent = "กรุณาวางลิงก์อย่างน้อย 1 อัน"; return; }
      btn.disabled = true;
      statusEl.textContent = "กำลังประมวลผล... ⏳";
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
          if (job.status === "done") { clearInterval(timer); render(job); }
          else { document.getElementById("status").textContent = "กำลังโหลด... ⏳"; }
        });
      }, 1500);
    }
    function render(job) {
      document.getElementById("status").textContent = "เสร็จแล้ว! ✅";
      document.getElementById("btn").disabled = false;
      let html = '<a class="dl" href="/get_zip/' + currentJobId + '">⬇️ โหลดทั้งหมด (.zip)</a>';
      job.results.forEach(r => {
        if (r.status === "ok") {
          const label = (r.count > 1) ? (r.title + " (" + r.count + " รูป)") : r.title;
          html += '<div class="result-card"><span class="ok">✔</span> ' + escapeHtml(label) + '</div>';
        } else {
          html += '<div class="result-card"><span class="err">✖</span> ' + escapeHtml(r.url) + ' — ' + escapeHtml(r.error) + '</div>';
        }
      });
      document.getElementById("result").innerHTML = html;
    }
    function escapeHtml(s) {
      const map = { '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' };
      return String(s).replace(/[&<>"']/g, c => map[c]);
    }
  </script>
</body>
</html>"""


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
