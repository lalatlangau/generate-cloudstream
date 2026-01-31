# 🚀 Quick Start Guide

## Install & Run (3 Langkah Mudah)

### 1️⃣ Untuk Satu Website

```bash
# Cara paling mudah - Interactive Mode
python3 advanced_cloudstream_generator.py

# Atau langsung command line
python3 advanced_cloudstream_generator.py https://namawebsite.com
```

### 2️⃣ Untuk Banyak Website Sekaligus

```bash
# Edit batch_config.json dulu, lalu:
python3 advanced_cloudstream_generator.py --batch batch_config.json
```

### 3️⃣ Upload ke GitHub

```bash
cd cloudstream-namaPlugin
git init
git add .
git commit -m "Initial commit"
git branch -M master
git remote add origin https://github.com/USERNAME/cloudstream-namaPlugin.git
git push -u origin master

# Buat branch builds
git checkout --orphan builds
git rm -rf .
echo "# Builds" > README.md
git add .
git commit -m "Builds branch"
git push origin builds
```

---

## 📝 Contoh Lengkap Step-by-Step

### Contoh 1: Generate untuk DutaMovie (hidekielectronics.com)

**Step 1: Generate Plugin**
```bash
python3 advanced_cloudstream_generator.py https://hidekielectronics.com DutaMovie wordpress_movie
```

Output:
```
✅ Created: cloudstream-dutamovie/DutaMovie.kt
✅ Created: cloudstream-dutamovie/build.gradle.kts
✅ Created: cloudstream-dutamovie/settings.gradle.kts
✅ Created: cloudstream-dutamovie/.github/workflows/build.yml
✅ Created: cloudstream-dutamovie/README.md
✅ Created: cloudstream-dutamovie/repo.json
✅ Created: cloudstream-dutamovie/config.json
```

**Step 2: Upload ke GitHub**
```bash
cd cloudstream-dutamovie
git init
git add .
git commit -m "DutaMovie Plugin"
git remote add origin https://github.com/yourusername/cloudstream-dutamovie.git
git push -u origin master
```

**Step 3: Setup Builds**
```bash
git checkout --orphan builds
git rm -rf .
echo "# Builds" > README.md
git add .
git commit -m "Builds"
git push origin builds
git checkout master
```

**Step 4: Update repo.json**
Edit `repo.json`:
```json
{
  "pluginLists": [
    "https://raw.githubusercontent.com/yourusername/cloudstream-dutamovie/builds/plugins.json"
  ]
}
```

Push perubahan:
```bash
git add repo.json
git commit -m "Update repo.json"
git push
```

**Step 5: Trigger Build**
GitHub Actions akan otomatis build. Tunggu ~5 menit.

**Step 6: Install di Cloudstream**
1. Buka Cloudstream App
2. Settings → Extensions → Add Repository
3. Paste: `https://raw.githubusercontent.com/yourusername/cloudstream-dutamovie/master/repo.json`
4. Install plugin "DutaMovie"

---

### Contoh 2: Generate Banyak Website Sekaligus

**Step 1: Buat File Konfigurasi**
Buat file `my_plugins.json`:
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
  },
  {
    "domain": "https://rebahinz.com",
    "plugin_name": "Rebahin",
    "template": "wordpress_movie"
  }
]
```

**Step 2: Generate Semua**
```bash
python3 advanced_cloudstream_generator.py --batch my_plugins.json
```

Output:
```
[1/3] Processing: https://hidekielectronics.com
✅ Project generated: cloudstream-dutamovie/

[2/3] Processing: https://lk21official.net
✅ Project generated: cloudstream-lk21/

[3/3] Processing: https://rebahinz.com
✅ Project generated: cloudstream-rebahin/
```

**Step 3: Upload Satu Per Satu**
```bash
# Upload DutaMovie
cd cloudstream-dutamovie
git init && git add . && git commit -m "Init"
git remote add origin https://github.com/user/cloudstream-dutamovie.git
git push -u origin master
cd ..

# Upload LK21
cd cloudstream-lk21
git init && git add . && git commit -m "Init"
git remote add origin https://github.com/user/cloudstream-lk21.git
git push -u origin master
cd ..

# Upload Rebahin
cd cloudstream-rebahin
git init && git add . && git commit -m "Init"
git remote add origin https://github.com/user/cloudstream-rebahin.git
git push -u origin master
```

---

## 🎯 Template Guide

### Kapan Pakai Template Apa?

| Website Type | Template | Contoh |
|-------------|----------|--------|
| WordPress Movie | `wordpress_movie` | DutaMovie, Rebahin, IndoXXI |
| LK21 Clone | `lk21_clone` | LK21, LayarKaca21, Nonton |
| Custom/Lainnya | `custom_streaming` | FilmApik, BioskopKeren |

### Cara Tahu Template yang Tepat?

**Method 1: Inspect Element**
1. Buka website di browser
2. Klik kanan → View Page Source
3. Cari keyword:
   - `wp-content/themes` → WordPress Movie
   - `lk21`, `layarkaca` → LK21 Clone
   - Lainnya → Custom Streaming

**Method 2: Trial & Error**
Generate dengan template berbeda, lihat mana yang paling cocok.

---

## 🔧 Customization Examples

### Custom 1: Ganti Selector
Edit file `.kt` yang dihasilkan:

**Before:**
```kotlin
val title = this.selectFirst("h2.entry-title a")?.text()
```

**After (sesuai struktur website):**
```kotlin
val title = this.selectFirst("h3.film-title a")?.text()
```

### Custom 2: Tambah Genre
Edit file `.kt`:

```kotlin
override val mainPage = mainPageOf(
    "$mainUrl/page/" to "Latest Movies",
    "$mainUrl/genre/action/page/" to "Action",
    "$mainUrl/genre/anime/page/" to "Anime",  // ← TAMBAH
    "$mainUrl/genre/kdrama/page/" to "K-Drama"  // ← TAMBAH
)
```

### Custom 3: Ganti URL Pattern
Edit bagian `search`:

**Before:**
```kotlin
val document = app.get("$mainUrl/?s=$query").document
```

**After:**
```kotlin
val document = app.get("$mainUrl/search?q=$query").document
```

---

## 🐛 Common Issues & Solutions

### Issue 1: Plugin Tidak Muncul List Film

**Penyebab:** Selector `movie_list` salah

**Solusi:**
1. Buka website di browser
2. Inspect element pada bagian list film
3. Copy selector yang benar
4. Edit di file `.kt`:
```kotlin
// Cari baris ini:
val home = document.select("article.item-infinite").mapNotNull {

// Ganti dengan selector yang benar:
val home = document.select("div.movie-card").mapNotNull {
```

### Issue 2: Judul Tidak Muncul

**Penyebab:** Selector `title` salah

**Solusi:**
Edit di fungsi `toSearchResult()`:
```kotlin
// Ganti selector title
val title = this.selectFirst("h3.judul a")?.text()?.trim() ?: return null
```

### Issue 3: Video Tidak Bisa Diputar

**Penyebab:** Selector `iframe` atau struktur player berbeda

**Solusi:**
1. Buka detail film di browser
2. Inspect element pada player video
3. Update selector iframe:
```kotlin
document.select("div.player-container iframe").forEach { iframe ->
```

### Issue 4: Search Tidak Jalan

**Penyebab:** URL search berbeda

**Solusi:**
Test manual di browser dulu:
- Coba: `domain.com/?s=avengers`
- Atau: `domain.com/search?q=avengers`
- Atau: `domain.com/cari/avengers`

Update di file `.kt`:
```kotlin
override suspend fun search(query: String): List<SearchResponse> {
    val document = app.get("$mainUrl/cari/$query").document  // ← Sesuaikan
    // ...
}
```

---

## 📊 Checklist Deployment

- [ ] Generate plugin dengan script
- [ ] Cek file `.kt` sesuai struktur website
- [ ] Test selector dengan inspect element
- [ ] Upload ke GitHub repository
- [ ] Buat branch `builds`
- [ ] Update `repo.json` dengan username GitHub
- [ ] Push dan tunggu GitHub Actions build
- [ ] Add repository di Cloudstream app
- [ ] Test search dan playback
- [ ] Dokumentasi custom changes (jika ada)

---

## 💡 Pro Tips

1. **Simpan config.json** untuk referensi selector
2. **Test di browser dulu** sebelum edit selector
3. **Gunakan batch mode** untuk generate banyak plugin sekaligus
4. **Fork & modify template** untuk website dengan struktur unik
5. **Document changes** di README untuk maintenance

---

## 📚 Resources

- [Cloudstream Docs](https://recloudstream.github.io/dokka/)
- [GitHub Actions Guide](https://docs.github.com/actions)
- [Kotlin Syntax](https://kotlinlang.org/docs/basic-syntax.html)

---

**Happy Coding! 🎉**
