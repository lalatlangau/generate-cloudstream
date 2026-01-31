

---

# 🎬 Cloudstream Plugin Generator Suite

**Penjana (Generator) automatik untuk membina plugin Cloudstream** dengan sokongan pelbagai laman web dan templat.

## 📦 Apa yang Ada dalam Pakej Ini?

### 🔧 Alatan Utama

1. **advanced_cloudstream_generator.py** ⭐
* Penjana utama dengan ciri lengkap
* Sokongan 3 templat berbeza
* Mod interaktif & mod kelompok (batch)
* Kesan nama plugin secara automatik daripada domain


2. **generate_cloudstream.py**
* Penjana versi ringkas (khusus untuk DutaMovie)
* Sesuai untuk pemula


3. **batch_config.json**
* Templat konfigurasi untuk mod kelompok
* Contoh: jana 4 plugin secara serentak



### 📚 Dokumentasi

* **QUICKSTART.md** - Panduan pantas langkah demi langkah
* **DOCUMENTATION.md** - Dokumentasi lengkap bersama penyelesaian masalah (troubleshooting)
* **README.md** (fail ini) - Gambaran keseluruhan pakej

### 🎯 Plugin yang Telah Dijana (Contoh)

1. **cloudstream-dutamovie/** - DutaMovie (hidekielectronics.com)
2. **cloudstream-lk21/** - LK21 (lk21official.net)
3. **cloudstream-rebahin/** - Rebahin (rebahinz.com)
4. **cloudstream-filmapik/** - FilmApik (filmapik.wiki)

---

## 🚀 Mula Pantas (Quick Start)

### Cara Terpantas (3 Langkah)

```bash
# 1. Jana plugin untuk laman web anda
python3 advanced_cloudstream_generator.py

# Masukkan:
# - Domain: https://namawebsite.com
# - Plugin Name: (tekan enter untuk auto)
# - Template: pilih 1-3

# 2. Muat naik ke GitHub
cd cloudstream-namaPlugin
git init
git add .
git commit -m "Init"
git remote add origin https://github.com/USERNAME/repo.git
git push -u origin master

# 3. Tambah dalam Aplikasi Cloudstream
# Tetapan (Settings) → Extensions → Add Repository
# Tampal (Paste) URL repo.json anda

```

**Baca QUICKSTART.md untuk tutorial lengkap!**

---

## 🎨 Templat yang Tersedia

| Templat | Sesuai Untuk | Contoh Laman Web |
| --- | --- | --- |
| **wordpress_movie** | Laman filem berasaskan WordPress | DutaMovie, Rebahin, IndoXXI |
| **lk21_clone** | LK21 dan klon daripadanya | LK21, LayarKaca21, Nonton |
| **custom_streaming** | Laman penstriman kustom | FilmApik, BioskopKeren |

### Bagaimana Cara Memilih Templat?

1. **Lihat kod sumber laman web** (Tekan Ctrl+U pada pelayar web)
2. Cari kata kunci:
* Ada `wp-content` → wordpress_movie
* Ada `lk21` atau `layarkaca` → lk21_clone
* Lain-lain → custom_streaming



---

## 📖 Mod Penggunaan

### 1. Mod Interaktif (Paling Mudah)

```bash
python3 advanced_cloudstream_generator.py

```

Program akan bertanya satu demi satu:

* Domain apa?
* Nama plugin?
* Templat mana?

### 2. Mod Baris Arahan (Command Line)

```bash
# Asas
python3 advanced_cloudstream_generator.py https://example.com

# Dengan nama kustom
python3 advanced_cloudstream_generator.py https://example.com MyPlugin

# Dengan templat kustom
python3 advanced_cloudstream_generator.py https://example.com MyPlugin lk21_clone

```

### 3. Mod Kelompok (Jana Banyak Serentak)

```bash
# Edit fail batch_config.json terlebih dahulu
python3 advanced_cloudstream_generator.py --batch batch_config.json

```

---

## 🎯 Ciri-Ciri Unggulan

✅ **Jana Segalanya Secara Automatik**

* Kod plugin (.kt)
* Fail binaan (build files - .gradle)
* GitHub Actions (bina automatik)
* Dokumentasi (README)

✅ **Pelbagai Templat**

* Tema WordPress Movie
* Klon LK21
* Penstriman Kustom

✅ **Pengesanan Pintar**

* Nama plugin automatik daripada domain
* Pemetaan *selector* yang bijak
* Penjanaan konfigurasi nyahpepijat (debug)

✅ **Sedia untuk Produksi**

* Integrasi GitHub Actions
* Bina automatik semasa "push"
* Manifes repositori

---

## 📁 Struktur Output

Setiap plugin yang dijana akan mengandungi:

```
cloudstream-namaPlugin/
├── 📄 NamaPlugin.kt          ← Kod utama plugin
├── 📄 build.gradle.kts       ← Konfigurasi binaan
├── 📄 settings.gradle.kts    ← Tetapan Gradle
├── 📄 repo.json              ← Manifes repositori
├── 📄 config.json            ← Info debug (selector, dll)
├── 📄 README.md              ← Dokumentasi
└── 📁 .github/
    └── workflows/
        └── build.yml         ← Binaan automatik GitHub Actions

```

---

## 🔧 Kustomisasi

### Tambah Templat Baru

Edit fail `advanced_cloudstream_generator.py`:

```python
WEBSITE_TEMPLATES = {
    "template_baru": {
        "name": "Nama Template",
        "selectors": {
            "movie_list": "div.film",
            "title": "h2 a",
            # ... dan seterusnya
        },
        "pages": {
            "search": "/cari/",
            # ... dan seterusnya
        }
    }
}

```

### Edit Selector

Lihat fail `config.json` yang dijana untuk menyemak (debug) selector.

---

## 🐛 Penyelesaian Masalah (Troubleshooting)

### Plugin tidak memaparkan filem?

→ Semak selector `movie_list` di dalam `config.json`

### Carian (Search) tidak berfungsi?

→ Uji URL carian secara manual di pelayar web terlebih dahulu

### Video tidak boleh dimainkan?

→ Semak selector `iframe` dan `download_links`

**Lihat DOCUMENTATION.md untuk panduan penyelesaian masalah yang lengkap!**

---

## 📊 Perbandingan: Ringkas vs Lanjutan

| Ciri | generate_cloudstream.py | advanced_cloudstream_generator.py |
| --- | --- | --- |
| Templat | 1 (WordPress) | 3 (WordPress, LK21, Custom) |
| Mod Interaktif | ❌ | ✅ |
| Mod Kelompok | ❌ | ✅ |
| Nama Plugin Auto | ❌ | ✅ |
| Konfigurasi Debug | ❌ | ✅ (config.json) |
| Sesuai untuk | DutaMovie sahaja | Mana-mana laman penstriman |

**Saranan: Gunakan advanced_cloudstream_generator.py**

---

## 📞 Sokongan

Jika terdapat masalah:

1. Semak `config.json` untuk nyahpepijat selector
2. Baca DOCUMENTATION.md
3. Guna *inspect element* pada laman web sasaran
4. Laraskan selector dalam fail `.kt`

---

## 📄 Lesen

HAK CIPTA TERPELIHARA.

---

## ⭐ Tip

💡 **Simpan batch_config.json** untuk laman web kegemaran anda.

💡 **Fork templat** untuk laman web yang mempunyai struktur unik.

💡 **Dokumentasikan perubahan** anda dalam README plugin tersebut.

💡 **Uji dahulu di pelayar web** sebelum mengedit selector.

---

**Dibuat dengan ❤️ oleh MICROTECH.STORE (MTS)**

🎬 Selamat Menstrim! 🍿

---


