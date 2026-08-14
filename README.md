# 📱 TikTok Wallpaper Downloader (Flask)

A lightweight, single-file Flask web app that lets you **batch-download TikTok videos (no watermark)** so you can use them as phone wallpapers / live wallpapers. Works great on mobile browsers.

---

## ✨ Features

- 📝 Paste **multiple TikTok links** (one per line)
- ⚡ Background downloading with live status polling
- 📦 Auto-packages everything into a single `.zip`
- 📱 Mobile-friendly UI (dark theme)
- 🧩 **Single Python file** — no template folder needed
- 🖼️ **Photo / slideshow posts** (`/photo/` URLs) → downloads clean images, no watermark
---

## 📂 Project Structure

```text
tiktok_wallpaper/
├── app.py          # The entire application (Flask + embedded HTML)
├── README.md       # This file
└── downloads/      # Auto-created: stores jobs & zips
```

---

## 🔧 Requirements

| Component | Install Command / Notes |
|-----------|--------------------------|
| Python    | `>= 3.8` |
| Flask     | `pip install flask` |
| yt-dlp    | `pip install yt-dlp` |
| FFmpeg    | **System-level** (see below) |

### Install FFmpeg (required by `yt-dlp`)

- **Ubuntu / Debian:** `sudo apt install ffmpeg`
- **macOS:** `brew install ffmpeg`
- **Windows:** Download from https://ffmpeg.org → extract → add `bin/` to your `PATH`

---

## 🚀 Quick Start

```bash
# 1. Clone or create your project folder
mkdir tiktok_wallpaper && cd tiktok_wallpaper

# 2. Save the single-file app as app.py (from the previous step)

# 3. Install dependencies
pip install flask yt-dlp

# 4. Run the server
python app.py
```

The server starts at:

```
http://localhost:5000
```

---

## 📲 How to Use (on your phone)

1. **Find your computer's LAN IP** (e.g. `192.168.1.10`):
   ```bash
   # Linux/macOS
   hostname -I
   # Windows
   ipconfig
   ```

2. **Make sure your phone is on the same Wi-Fi** as your computer.

3. Open your phone browser and go to:
   ```
   http://192.168.1.10:5000
   ```

4. **Paste TikTok links** — one per line:
   ```text
   https://www.tiktok.com/@user/video/1234567890
   https://vt.tiktok.com/xxxxxxxx/
   ```

5. Tap **"Download Wallpapers"** ⏳ → wait for the progress → tap the **⬇️ Download All (.zip)** button.

6. Extract the `.zip` and set the videos as wallpaper (see below).

---

## 🖼️ Setting Videos as Mobile Wallpaper

<details>
<summary><b>Android — Live Video Wallpaper</b></summary>

1. Extract the MP4 files from the downloaded `.zip`.
2. Install an app like **"Video Live Wallpaper"** or **"Wallpaper Studio 4K"** from the Play Store.
3. Open the app → select the MP4 → set as **home** and/or **lock-screen** live wallpaper.

</details>

<details>
<summary><b>iOS — Live Photo Wallpaper</b></summary>

> iOS cannot use a raw MP4 directly as a Live Wallpaper; it needs a Live Photo (`.mov` + `.heic` pair).

1. Extract the MP4 from the `.zip`.
2. Use a free app like **"IntoLive"** or **"Lively"** → import the MP4 → convert to Live Photo.
3. In the Photos app: `Settings → Wallpaper → Choose a New Wallpaper → Live Photo`.

</details>

---

## 🛠️ Configuration

You can change the port or host in the last lines of `app.py`:

```python
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
```

- `host="0.0.0.0"` → accessible from other devices on the network (needed for phone access)
- `port=5000` → change if blocked by firewall

> ⚠️ **Do NOT use `debug=True` in production.** Set it to `False` and use a WSGI server like `gunicorn` for public deployment.

---

## 🔄 Updating `yt-dlp`

TikTok's internal API changes often. If downloads start failing:

```bash
pip install -U yt-dlp
```

---

## ⚠️ Legal / Terms of Service

- Only download content you **own** or have **explicit permission** to use.
- Downloading or redistributing copyrighted material without authorization may violate TikTok's Terms of Service and local copyright laws.
- The author is **not responsible** for misuse of this tool.

---

## 📄 License

MIT — free to use, modify, and distribute.
