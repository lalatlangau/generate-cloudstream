# 🎬 Advanced Cloudstream Plugin Generator

Generator otomatis untuk membuat plugin Cloudstream dengan deteksi struktur website dan multiple template support.

## 🌟 Fitur Utama

- ✅ **Auto-Generate Plugin Name** dari domain
- ✅ **Multiple Templates** (WordPress, LK21 Clone, Custom)
- ✅ **Interactive Mode** untuk generate satu per satu
- ✅ **Batch Mode** untuk generate banyak sekaligus
- ✅ **Auto GitHub Actions** setup
- ✅ **Customizable Selectors** per template

## 📦 Template yang Tersedia

### 1. WordPress Movie Theme
Untuk website berbasis WordPress dengan theme movie streaming.

**Cocok untuk:**
- hidekielectronics.com (DutaMovie)
- rebahin.com
- indoxxi clones
- Dan website dengan struktur WordPress movie theme

**Indicators:**
- `wp-content/themes`
- `entry-title`
- `item-infinite`

### 2. LK21 Clone
Untuk website clone dari LayarKaca21 dan variannya.

**Cocok untuk:**
- lk21official.net
- layarkaca21.com
- nonton.com
- Dan website clone LK21

**Indicators:**
- `lk21`, `layarkaca` dalam HTML
- `film-list`, `movie-list-index`

### 3. Custom Streaming
Template umum untuk website streaming custom.

**Cocok untuk:**
- filmapik.wiki
- bioskopkeren.com
- Website custom dengan struktur berbeda

**Indicators:**
- `movie-item`, `movie-card`
- `film-poster`

## 🚀 Cara Menggunakan

### Mode 1: Interactive (Rekomendasi untuk Pemula)

```bash
python3 advanced_cloudstream_generator.py
```

Program akan menanyakan:
1. Domain website (contoh: https://example.com)
2. Nama plugin (opsional, bisa auto-generate)
3. Template yang akan digunakan

### Mode 2: Command Line (Cepat)

```bash
# Generate dengan auto-detect name dan template default
python3 advanced_cloudstream_generator.py https://hidekielectronics.com

# Generate dengan custom name
python3 advanced_cloudstream_generator.py https://hidekielectronics.com DutaMovie

# Generate dengan custom name dan template
python3 advanced_cloudstream_generator.py https://lk21official.net LK21 lk21_clone
```

### Mode 3: Batch (Generate Banyak Sekaligus)

1. Buat file konfigurasi JSON:

```json
[
  {
    "domain": "https://hidekielectronics.com",
    "plugin_name": "DutaMovie",
    "template": "wordpress_movie"
  },
  {
    "domain": "https://lk21official.net",
    "plugin_name": "LK21",
    "template": "lk21_clone"
  }
]
```

2. Jalankan batch mode:

```bash
python3 advanced_cloudstream_generator.py --batch batch_config.json
```

## 📁 Output Structure

Setiap plugin yang di-generate akan membuat folder dengan struktur:

```
cloudstream-namaPlugin/
├── .github/
│   └── workflows/
│       └── build.yml          # Auto-build GitHub Actions
├── NamaPlugin.kt              # Main plugin file
├── build.gradle.kts           # Build configuration
├── settings.gradle.kts        # Gradle settings
├── repo.json                  # Repository manifest
├── config.json                # Debug configuration
└── README.md                  # Documentation
```

## 🔧 Customization

### Menambah Template Baru

Edit file `advanced_cloudstream_generator.py` di bagian `WEBSITE_TEMPLATES`:

```python
"nama_template_baru": {
    "name": "Nama Template",
    "indicators": [
        "html-class-unique",
        "element-unique"
    ],
    "selectors": {
        "movie_list": "div.movie-container",
        "title": "h2.title a",
        "poster": "img.poster",
        "quality": "span.quality",
        # ... selector lainnya
    },
    "pages": {
        "search": "/search?q=",
        "latest": "/movies/",
        "genre": "/genre/{genre}/"
    }
}
```

### Mengubah Selector Existing

Edit file `config.json` yang di-generate, lalu sesuaikan selector di file `.kt`:

```json
{
  "selectors": {
    "movie_list": "article.new-selector",
    "title": "h3.new-title a"
  }
}
```

## 📝 Contoh Penggunaan

### Contoh 1: Generate untuk DutaMovie

```bash
python3 advanced_cloudstream_generator.py
```
- Domain: `https://hidekielectronics.com`
- Plugin Name: (kosongkan, auto-generate: "Hidekielectronics")
- Template: 1 (WordPress Movie Theme)

### Contoh 2: Generate Multiple Sites

Buat `my_sites.json`:
```json
[
  {"domain": "https://site1.com", "template": "wordpress_movie"},
  {"domain": "https://site2.com", "template": "lk21_clone"},
  {"domain": "https://site3.com", "template": "custom_streaming"}
]
```

Jalankan:
```bash
python3 advanced_cloudstream_generator.py --batch my_sites.json
```

## 🎯 Tips & Tricks

### 1. Cara Menemukan Selector yang Benar

Buka website target di browser:
1. Klik kanan → Inspect Element
2. Cari elemen movie/film
3. Copy selector-nya (right-click → Copy → Copy selector)
4. Update di template

### 2. Testing Plugin

Setelah generate:
1. Cek file `.kt` yang dihasilkan
2. Buka di text editor
3. Sesuaikan selector jika struktur website berbeda
4. Test dengan upload ke Cloudstream

### 3. Debugging

File `config.json` berisi semua informasi selector yang digunakan.
Gunakan ini untuk debugging jika plugin tidak berfungsi.

## 🐛 Troubleshooting

### Plugin tidak menampilkan film

**Solusi:** 
- Cek selector `movie_list` di `config.json`
- Buka website di browser, inspect element
- Update selector di file `.kt`

### Search tidak berfungsi

**Solusi:**
- Cek URL search di `config.json` → `pages.search`
- Test manual di browser: `domain.com/?s=query`
- Update format search URL

### Video tidak bisa diputar

**Solusi:**
- Cek selector `iframe` dan `download_links`
- Website mungkin pakai player berbeda
- Update selector sesuai struktur website

## 📚 Reference

### Template Selectors

| Selector | Deskripsi | Contoh |
|----------|-----------|--------|
| `movie_list` | Container list film | `article.item`, `div.movie` |
| `title` | Judul film | `h2.title a`, `h3 a` |
| `poster` | Gambar poster | `img.poster`, `img` |
| `quality` | Label kualitas | `span.quality`, `.hd` |
| `link` | Link ke detail | `a`, `a.permalink` |
| `description` | Sinopsis | `.description p`, `.synopsis` |
| `genre` | List genre | `.genre a`, `.genres a` |
| `year` | Tahun rilis | `.year`, `span.year` |
| `rating` | Rating film | `.rating`, `.imdb` |
| `iframe` | Player embed | `iframe`, `.player iframe` |
| `download_links` | Link download | `.download a`, `.downloads a` |

## 🔐 License

Free to use and modify

## 🤝 Contributing

Pull requests welcome! Silakan tambah template baru untuk website lain.

## 📞 Support

Jika ada masalah:
1. Cek file `config.json` untuk debug
2. Inspect element website target
3. Sesuaikan selector di file `.kt`
4. Test ulang

---

**Made with ❤️ for Indonesian Streaming Community**
