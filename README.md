# 📱 TikTok Wallpaper Downloader (Flask - ไม่ต้องมี Cookie)

เว็บแอป Flask สำหรับดาวน์โหลดวิดิโอและรูปภาพจาก TikTok เป็นไฟล์ `.zip` เพื่อนำไปใช้เป็นวอลเปเปอร์มือถือ

**จุดเด่น:** ใช้บริการ API ของเว็บโหลด TikTok ฟรี → **ไม่ต้องลง `yt-dlp`**, **ไม่ต้องลง `ffmpeg`**, และ **ไม่ต้องมี `cookies.txt`** ให้ยุ่งยาก

---

## ✨ ฟีเจอร์

- 📝 วางลิงก์ TikTok ได้หลายอัน (วิดิโอ + รูป/สไลด์โชว์) หนึ่งลิงก์ต่อบรรทัด
- 🖼️ รองรับโพสต์รูป (`/photo/`) และวิดิโอ (`/video/`)
- ⚡ ดาวน์โหลดเบื้องหลัง + แสดงสถานะแบบเรียลไทม์
- 📦 แพ็คทุกไฟล์เป็น `.zip` ให้ดาวน์โหลดครั้งเดียว
- 📱 UI เปิดบนมือถือได้สบาย (ธีมมืด)
- 🚫 **ไม่ต้องใช้ Cookie / ไม่ต้องลง yt-dlp / ffmpeg**

---

## 📂 โครงสร้างโปรเจกต์

```text
tiktok_wallpaper/
├── app.py          # แอปทั้งหมด (Flask + HTML ฝังตัว)
├── README.md       # ไฟล์นี้
└── downloads/      # สร้างอัตโนมัติ (เก็บ zip ชั่วคราว)
```

---

## 🔧 ความต้องการของระบบ

| สิ่งที่ต้องมี | วิธีติดตั้ง |
|--------------|-------------|
| Python       | `>= 3.8` |
| Flask        | `pip install flask` |
| requests     | `pip install requests` |

> ✅ **ไม่จำเป็นต้องลง** `yt-dlp`, `ffmpeg` หรือเตรียม `cookies.txt` แล้ว

---

## 🚀 เริ่มใช้งานอย่างไร

```bash
# 1. เข้าโฟลเดอร์โปรเจกต์
cd tiktok_wallpaper

# 2. ติดตั้งแค่ 2 ตัวนี้
pip install flask requests

# 3. รันเซิร์ฟเวอร์
python app.py
```

เปิดเบราว์เซอร์ที่:
```
http://localhost:5000
```

---

## 📲 วิธีใช้งานบนมือถือ

1. **หา IP ของเครื่องคอมพิวเตอร์** (เช่น `192.168.0.100`):
   ```bash
   # Windows
   ipconfig
   # Linux / macOS
   hostname -I
   ```
2. **มือถือต้องต่อ Wi-Fi เครือข่ายเดียวกับคอม**
3. เปิดเบราว์เซอร์มือถือ ไปที่:
   ```
   http://192.168.0.100:5000
   ```
4. วางลิงก์ TikTok (หนึ่งลิงก์ต่อบรรทัด):
   ```text
   https://www.tiktok.com/@user/video/1234567890
   https://www.tiktok.com/@user/photo/7656853975429401872?_r=1&_t=ZS-xxxx
   ```
5. กด **"Download Wallpapers"** → รอแถบสถานะ → กด **⬇️ โหลดทั้งหมด (.zip)**
6. แตก zip แล้วนำไปตั้งเป็นวอลเปเปอร์ (ดูด้านล่าง)

---

## 🖼️ ตั้งรูป/วิดิโอเป็นวอลเปเปอร์มือถือ

<details>
<summary><b>Android — Live Video Wallpaper</b></summary>

1. แตกไฟล์ `.zip` เอาไฟล์ MP4 / JPG ออกมา
2. ติดแอปเช่น **"Video Live Wallpaper"** หรือ **"Wallpaper Studio 4K"** จาก Play Store
3. เลือกไฟล์ → ตั้งเป็นวอลเปเปอร์หน้าจอหลัก/ล็อกสกรีน

</details>

<details>
<summary><b>iOS — Live Photo Wallpaper</b></summary>

> iOS ใช้ไฟล์วิดิโอเปล่าๆ ไม่ได้ ต้องแปลงเป็น Live Photo ก่อน

1. แตก zip เอา MP4 / รูปออกมา
2. ใช้แอปฟรีเช่น **"IntoLive"** หรือ **"Lively"** → นำเข้า MP4 → แปลงเป็น Live Photo
3. ในแอป Photos: `Settings → Wallpaper → Choose a New Wallpaper → Live Photo`

</details>

---

## 🧪 ทดสอบ API ก่อนรันจริง (ไม่บังคับ)

สร้างไฟล์ `test_api.py`:

```python
import requests
url = "https://www.tiktok.com/@houseofuday/photo/7667599388478426369"
r = requests.get("https://www.tikwm.com/api/", params={"url": url}, timeout=30)
print(r.status_code)
d = r.json()
print("code:", d.get("code"))
print("images:", len(d.get("data", {}).get("images", [])))
```

หากได้ `code: 0` และ `images: >0` แปลว่าใช้งานได้ปกติ

---

## ⚠️ ข้อควรระวัง

- บริการฟรีอาจมี **rate limit** (ถ้าโหลดทีละหลายร้อยรูปอาจช้า/โดนบล็อกชั่วคราว)
- หากเจอข้อความ *"ทุกวิธีล้มเหลว"* ให้ลองใหม่ภายหลัง (เซิร์ฟเวอร์อาจชั่วคราว)
- โค้ดนี้ใช้ API ของ `tikwm.com` และ `tiklydown.eu.org` — หากเจ้าของบริการปิด API ต้องปรับ URL ในฟังก์ชัน `try_tikwm` / `try_tiklydown`

---

## ⚖️ กฎหมาย / เงื่อนไขการใช้งาน

- ดาวน์โหลดเฉพาะคลิป/รูปที่คุณเป็นเจ้าของ หรือได้รับอนุญาตเท่านั้น
- การดาวน์โหลดหรือแจกจ่ายงานที่มีลิขสิทธิ์โดยไม่ได้รับอนุญาต อาจผิด Terms of Service ของ TikTok และกฎหมายลิขสิทธิ์ท้องถิ่น
- ผู้จัดทำไม่รับผิดชอบต่อการนำไปใช้งานผิดวัตถุประสงค์

---

## 📄 License

MIT — ใช้งาน / แก้ไข / แจกจ่ายได้อิสระ
