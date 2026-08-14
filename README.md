# 📱 TikTok Wallpaper Downloader (Flask)

[English](#english) | [ไทย](#thai)

<a id="english"></a>
<details open>
<summary><b>🇬🇧 English</b></summary>

## ✨ Features

- 📝 Paste multiple TikTok links (videos + photo/slideshow), one per line
- 🖼️ Supports photo posts (`/photo/`) and video posts (`/video/`)
- ⚡ Background downloading with real-time status
- 📦 Auto-packages everything into a single `.zip`
- 📱 Mobile-friendly dark UI
- 🚫 **No Cookie / No yt-dlp / No ffmpeg required**

## 📂 Project Structure

```text
tiktok_wallpaper/
├── app.py          # Entire app (Flask + embedded HTML)
├── README.md       # This file
└── downloads/      # Auto-created (temporary zips)
```

## 🔧 Requirements

| Component | Install |
|-----------|---------|
| Python    | `>= 3.8` |
| Flask     | `pip install flask` |
| requests  | `pip install requests` |

> ✅ No need for `yt-dlp`, `ffmpeg`, or `cookies.txt`

## 🚀 Quick Start

```bash
cd tiktok_wallpaper
pip install flask requests
python app.py
```

Open: `http://localhost:5000`

## 📲 Use on Phone

1. Find your PC LAN IP (e.g. `192.168.0.100`):
   ```bash
   # Windows
   ipconfig
   # Linux / macOS
   hostname -I
   ```
2. Phone must be on the **same Wi-Fi**.
3. Open browser on phone → `http://192.168.0.100:5000`
4. Paste TikTok links (one per line), tap **Download Wallpapers** → wait → tap **⬇️ Download All (.zip)**.
5. Extract zip and set as wallpaper (see below).

## 🖼️ Set as Mobile Wallpaper

**Android (Live Video):** Extract MP4/JPG → use *"Video Live Wallpaper"* or *"Wallpaper Studio 4K"* app.

**iOS (Live Photo):** iOS needs a Live Photo. Use *"IntoLive"* or *"Lively"* → import MP4 → convert to Live Photo → set via Photos app.

## ⚠️ Notes

- Free APIs may have rate limits (don't bulk-download hundreds at once).
- If you see *"all methods failed"*, retry later (server may be temporary down).
- Uses `tikwm.com` and `tiklydown.eu.org` APIs. If they shut down, update URLs in `try_tikwm` / `try_tiklydown`.

## ⚖️ Legal

Only download content you own or have permission to use. Downloading copyrighted material without authorization may violate TikTok ToS and local copyright laws. Author is not responsible for misuse.

## 📄 License

MIT

</details>

<a id="thai"></a>
<details>
<summary><b>🇹🇭 ไทย</b></summary>

## ✨ ฟีเจอร์

- 📝 วางลิงก์ TikTok ได้หลายอัน (วิดิโอ + รูป/สไลด์โชว์) หนึ่งลิงก์ต่อบรรทัด
- 🖼️ รองรับโพสต์รูป (`/photo/`) และวิดิโอ (`/video/`)
- ⚡ ดาวน์โหลดเบื้องหลัง + แสดงสถานะแบบเรียลไทม์
- 📦 แพ็คทุกไฟล์เป็น `.zip` ให้ดาวน์โหลดครั้งเดียว
- 📱 UI มือถือ (ธีมมืด)
- 🚫 **ไม่ต้องใช้ Cookie / ไม่ต้องลง yt-dlp / ffmpeg**

## 📂 โครงสร้างโปรเจกต์

```text
tiktok_wallpaper/
├── app.py          # แอปทั้งหมด (Flask + HTML ฝังตัว)
├── README.md       # ไฟล์นี้
└── downloads/      # สร้างอัตโนมัติ (เก็บ zip ชั่วคราว)
```

## 🔧 ความต้องการของระบบ

| สิ่งที่ต้องมี | วิธีติดตั้ง |
|--------------|-------------|
| Python       | `>= 3.8` |
| Flask        | `pip install flask` |
| requests     | `pip install requests` |

> ✅ ไม่จำเป็นต้องลง `yt-dlp`, `ffmpeg` หรือเตรียม `cookies.txt`

## 🚀 เริ่มใช้งาน

```bash
cd tiktok_wallpaper
pip install flask requests
python app.py
```

เปิด: `http://localhost:5000`

## 📲 วิธีใช้งานบนมือถือ

1. หา IP ของเครื่องคอม (เช่น `192.168.0.100`):
   ```bash
   # Windows
   ipconfig
   # Linux / macOS
   hostname -I
   ```
2. มือถือต้องต่อ **Wi-Fi เครือข่ายเดียวกับคอม**
3. เปิดเบราว์เซอร์มือถือ → `http://192.168.0.100:5000`
4. วางลิงก์ TikTok (หนึ่งลิงก์ต่อบรรทัด) → กด **Download Wallpapers** → รอ → กด **⬇️ โหลดทั้งหมด (.zip)**
5. แตก zip แล้วนำไปตั้งเป็นวอลเปเปอร์ (ดูด้านล่าง)

## 🖼️ ตั้งเป็นวอลเปเปอร์มือถือ

**Android (วิดิโอสด):** แตก MP4/JPG → ใช้แอป *"Video Live Wallpaper"* หรือ *"Wallpaper Studio 4K"*

**iOS (Live Photo):** iOS ต้องใช้ Live Photo → ใช้แอป *"IntoLive"* หรือ *"Lively"* → นำเข้า MP4 → แปลงเป็น Live Photo → ตั้งผ่านแอป Photos

## ⚠️ ข้อควรระวัง

- บริการฟรีอาจมี rate limit (อย่าโหลดทีละหลายร้อยรูปพร้อมกัน)
- หากเจอ *"ทุกวิธีล้มเหลว"* ให้ลองใหม่ภายหลัง (เซิร์ฟเวอร์อาจชั่วคราว)
- ใช้ API ของ `tikwm.com` และ `tiklydown.eu.org` หากปิดบริการ ให้แก้ URL ในฟังก์ชัน `try_tikwm` / `try_tiklydown`

## ⚖️ กฎหมาย

ดาวน์โหลดเฉพาะคลิป/รูปที่คุณเป็นเจ้าของ หรือได้รับอนุญาต การดาวน์โหลดลิขสิทธิ์โดยไม่ได้รับอนุญาต อาจผิด ToS ของ TikTok และกฎหมายท้องถิ่น ผู้จัดทำไม่รับผิดชอบต่อการนำไปใช้ผิดวัตถุประสงค์

## 📄 สัญญาอนุญาต

MIT

</details>
