#!/usr/bin/env python3
"""
Advanced Cloudstream Plugin Generator dengan Auto-Detection
Mendukung multiple domains dan auto-detect struktur website
"""

import os
import json
import re
from typing import Dict, List, Optional
from urllib.parse import urlparse

# ============================================================================
# WEBSITE TEMPLATES - Tambahkan template baru disini
# ============================================================================

WEBSITE_TEMPLATES = {
    "wordpress_movie": {
        "name": "WordPress Movie Theme",
        "indicators": [
            "wp-content/themes",
            "entry-title",
            "item-infinite",
            "wp-json"
        ],
        "selectors": {
            "movie_list": "article.item-infinite",
            "title": "h2.entry-title a",
            "poster": "img",
            "quality": "span.quality",
            "link": "h2.entry-title a",
            "description": "div.entry-content p",
            "genre": "div.genre a",
            "year": "span.year",
            "rating": "span.rating",
            "iframe": "div.player-embed iframe",
            "download_links": "div.download-links a"
        },
        "pages": {
            "search": "/?s=",
            "latest": "/page/",
            "genre": "/genre/{genre}/page/"
        }
    },
    "custom_streaming": {
        "name": "Custom Streaming Site",
        "indicators": [
            "movie-item",
            "film-poster",
            "movie-card"
        ],
        "selectors": {
            "movie_list": "div.movie-item, div.movie-card",
            "title": "h3 a, h2 a, .title a",
            "poster": "img.poster, img",
            "quality": "span.quality, .quality",
            "link": "a",
            "description": ".description, .synopsis, p",
            "genre": ".genre a, .genres a",
            "year": ".year, span.year",
            "rating": ".rating, .imdb",
            "iframe": "iframe",
            "download_links": ".download a, .downloads a"
        },
        "pages": {
            "search": "/search?q=",
            "latest": "/movies/page/",
            "genre": "/genre/{genre}/"
        }
    },
    "lk21_clone": {
        "name": "LK21 Clone",
        "indicators": [
            "lk21",
            "layarkaca",
            "film-list"
        ],
        "selectors": {
            "movie_list": ".film-list article, .movie-list-index",
            "title": ".title-film a, h4 a",
            "poster": "img",
            "quality": ".quality",
            "link": "a",
            "description": ".desc p",
            "genre": ".genre-film a",
            "year": ".year-film",
            "rating": ".rating-film",
            "iframe": "#pembed iframe",
            "download_links": ".link-download a"
        },
        "pages": {
            "search": "/?s=",
            "latest": "/page/",
            "genre": "/genre/{genre}/"
        }
    }
}

# ============================================================================
# GENERATOR CLASS
# ============================================================================

class CloudstreamGenerator:
    def __init__(self, domain: str, plugin_name: str = None, template: str = "wordpress_movie"):
        self.domain = domain.rstrip('/')
        self.parsed_url = urlparse(self.domain)
        self.plugin_name = plugin_name or self._generate_plugin_name()
        self.template = WEBSITE_TEMPLATES.get(template, WEBSITE_TEMPLATES["wordpress_movie"])
        self.base_dir = f"cloudstream-{self.plugin_name.lower()}"
        
    def _generate_plugin_name(self) -> str:
        """Generate plugin name dari domain"""
        domain_parts = self.parsed_url.netloc.split('.')
        # Ambil bagian utama domain (tanpa www dan TLD)
        main_part = [part for part in domain_parts if part not in ['www', 'com', 'net', 'org', 'id', 'co']]
        if main_part:
            name = main_part[0].capitalize()
        else:
            name = domain_parts[0].capitalize()
        return name.replace('-', '').replace('_', '')
    
    def generate_kotlin_file(self) -> str:
        """Generate file .kt dengan template yang dipilih"""
        selectors = self.template["selectors"]
        pages = self.template["pages"]
        
        return f'''package com.{self.plugin_name.lower()}

import com.lagradost.cloudstream3.*
import com.lagradost.cloudstream3.utils.*
import org.jsoup.nodes.Element

class {self.plugin_name}Provider : MainAPI() {{
    override var mainUrl = "{self.domain}"
    override var name = "{self.plugin_name}"
    override var lang = "id"
    override val hasMainPage = true
    override val hasDownloadSupport = true
    override val supportedTypes = setOf(
        TvType.Movie,
        TvType.TvSeries,
        TvType.AsianDrama
    )

    override val mainPage = mainPageOf(
        "$mainUrl{pages['latest']}" to "Latest Movies",
        "$mainUrl{pages['genre'].replace('{genre}', 'action')}" to "Action",
        "$mainUrl{pages['genre'].replace('{genre}', 'adventure')}" to "Adventure",
        "$mainUrl{pages['genre'].replace('{genre}', 'comedy')}" to "Comedy",
        "$mainUrl{pages['genre'].replace('{genre}', 'drama')}" to "Drama",
        "$mainUrl{pages['genre'].replace('{genre}', 'horror')}" to "Horror",
        "$mainUrl{pages['genre'].replace('{genre}', 'thriller')}" to "Thriller",
        "$mainUrl{pages['genre'].replace('{genre}', 'romance')}" to "Romance",
        "$mainUrl{pages['genre'].replace('{genre}', 'scifi')}" to "Sci-Fi"
    )

    override suspend fun getMainPage(page: Int, request: MainPageRequest): HomePageResponse {{
        val document = app.get(request.data + page).document
        val home = document.select("{selectors['movie_list']}").mapNotNull {{
            it.toSearchResult()
        }}
        return newHomePageResponse(request.name, home)
    }}

    private fun Element.toSearchResult(): SearchResponse? {{
        val title = this.selectFirst("{selectors['title']}")?.text()?.trim() ?: return null
        val href = fixUrl(this.selectFirst("{selectors['link']}")?.attr("href") ?: return null)
        val posterUrl = fixUrlNull(this.selectFirst("{selectors['poster']}")?.attr("src"))
        val quality = this.selectFirst("{selectors['quality']}")?.text()
        
        return newMovieSearchResponse(title, href, TvType.Movie) {{
            this.posterUrl = posterUrl
            this.quality = getQualityFromString(quality)
        }}
    }}

    override suspend fun search(query: String): List<SearchResponse> {{
        val document = app.get("$mainUrl{pages['search']}$query").document
        return document.select("{selectors['movie_list']}").mapNotNull {{
            it.toSearchResult()
        }}
    }}

    override suspend fun load(url: String): LoadResponse {{
        val document = app.get(url).document
        
        val title = document.selectFirst("{selectors['title']}")?.text()?.trim() ?: ""
        val poster = document.selectFirst("{selectors['poster']}")?.attr("src")
        val tags = document.select("{selectors['genre']}").map {{ it.text() }}
        val year = document.selectFirst("{selectors['year']}")?.text()?.toIntOrNull()
        val description = document.selectFirst("{selectors['description']}")?.text()?.trim()
        val rating = document.selectFirst("{selectors['rating']}")?.text()?.toRatingInt()
        
        val recommendations = document.select("{selectors['movie_list']}").mapNotNull {{
            it.toSearchResult()
        }}

        // Detect if it's a TV Series
        val tvType = if (document.select("div.seasons, .episode-list").isNotEmpty()) 
            TvType.TvSeries 
        else 
            TvType.Movie
        
        return if (tvType == TvType.TvSeries) {{
            val episodes = document.select("div.episode-list a, .episodes a").map {{ ep ->
                val href = fixUrl(ep.attr("href"))
                val name = ep.text()
                Episode(href, name)
            }}
            
            newTvSeriesLoadResponse(title, url, TvType.TvSeries, episodes) {{
                this.posterUrl = poster
                this.year = year
                this.plot = description
                this.tags = tags
                this.rating = rating
                this.recommendations = recommendations
            }}
        }} else {{
            newMovieLoadResponse(title, url, TvType.Movie, url) {{
                this.posterUrl = poster
                this.year = year
                this.plot = description
                this.tags = tags
                this.rating = rating
                this.recommendations = recommendations
            }}
        }}
    }}

    override suspend fun loadLinks(
        data: String,
        isCasting: Boolean,
        subtitleCallback: (SubtitleFile) -> Unit,
        callback: (ExtractorLink) -> Unit
    ): Boolean {{
        val document = app.get(data).document
        
        // Extract from iframes
        document.select("{selectors['iframe']}").forEach {{ iframe ->
            val iframeUrl = fixUrl(iframe.attr("src"))
            loadExtractor(iframeUrl, subtitleCallback, callback)
        }}
        
        // Extract direct download links
        document.select("{selectors['download_links']}").forEach {{ link ->
            val url = link.attr("href")
            val quality = link.text()
            
            callback.invoke(
                ExtractorLink(
                    this.name,
                    this.name,
                    url,
                    referer = mainUrl,
                    quality = getQualityFromName(quality),
                )
            )
        }}
        
        return true
    }}
}}'''

    def generate_build_gradle(self) -> str:
        """Generate build.gradle.kts"""
        return f'''// use an integer for version numbers
version = 1

cloudstream {{
    language = "id"
    description = "{self.plugin_name} - Nonton Film & Series Online"
    authors = listOf("{self.plugin_name}")

    /**
     * Status int as the following:
     * 0: Down
     * 1: Ok
     * 2: Slow
     * 3: Beta only
     * */
    status = 1
    tvTypes = listOf(
        "TvSeries",
        "Movie",
        "AsianDrama"
    )

    iconUrl = "{self.domain}/favicon.ico"
}}'''

    def generate_settings_gradle(self) -> str:
        """Generate settings.gradle.kts"""
        return f'''rootProject.name = "{self.plugin_name}"

dependencyResolutionManagement {{
    repositories {{
        google()
        mavenCentral()
        maven("https://jitpack.io")
    }}
}}'''

    def generate_github_workflow(self) -> str:
        """Generate GitHub Actions workflow"""
        return '''name: Build

on:
  push:
    branches:
      - master
      - main
    paths-ignore:
      - '*.md'

concurrency:
  group: "build"
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
        with:
          path: "src"

      - name: Checkout builds
        uses: actions/checkout@v3
        with:
          ref: "builds"
          path: "builds"

      - name: Clean old builds
        run: rm -rf $GITHUB_WORKSPACE/builds/*.cs3

      - name: Setup JDK 11
        uses: actions/setup-java@v3
        with:
          java-version: 11
          distribution: "adopt"

      - name: Setup Gradle
        uses: gradle/gradle-build-action@v2

      - name: Build Plugins
        run: |
          cd $GITHUB_WORKSPACE/src
          chmod +x gradlew
          ./gradlew make makePluginsJson
          cp **/build/*.cs3 $GITHUB_WORKSPACE/builds
          cp build/plugins.json $GITHUB_WORKSPACE/builds

      - name: Push builds
        run: |
          cd $GITHUB_WORKSPACE/builds
          git config --local user.email "actions@github.com"
          git config --local user.name "GitHub Actions"
          git add .
          git commit -m "Build $GITHUB_SHA" || exit 0
          git push'''

    def generate_repo_json(self) -> dict:
        """Generate repo.json"""
        return {
            "name": f"{self.plugin_name} Repository",
            "description": f"Cloudstream repository untuk {self.plugin_name}",
            "manifestVersion": 1,
            "pluginLists": [
                f"https://raw.githubusercontent.com/YOUR-USERNAME/cloudstream-{self.plugin_name.lower()}/builds/plugins.json"
            ]
        }

    def generate_readme(self) -> str:
        """Generate README.md"""
        return f'''# Cloudstream {self.plugin_name} Plugin

Plugin Cloudstream untuk streaming film dan series dari {self.plugin_name} ({self.domain})

## 📁 Struktur Project

```
cloudstream-{self.plugin_name.lower()}/
├── .github/workflows/build.yml   # Auto build dengan GitHub Actions
├── {self.plugin_name}.kt          # Main plugin file
├── build.gradle.kts               # Build configuration
├── settings.gradle.kts            # Gradle settings
└── repo.json                      # Repository manifest
```

## 🚀 Cara Menggunakan

### 1. Upload ke GitHub

```bash
cd cloudstream-{self.plugin_name.lower()}
git init
git add .
git commit -m "Initial commit"
git branch -M master
git remote add origin https://github.com/YOUR-USERNAME/cloudstream-{self.plugin_name.lower()}.git
git push -u origin master
```

### 2. Setup Auto Build

Buat branch `builds`:
```bash
git checkout --orphan builds
git rm -rf .
echo "# Builds" > README.md
git add README.md
git commit -m "Initial builds branch"
git push origin builds
git checkout master
```

### 3. Update repo.json

Edit file `repo.json` dan ganti `YOUR-USERNAME` dengan username GitHub Anda.

### 4. Install di Cloudstream

1. Buka Cloudstream App
2. **Settings** → **Extensions** → **Add Repository**
3. Paste URL:
   ```
   https://raw.githubusercontent.com/YOUR-USERNAME/cloudstream-{self.plugin_name.lower()}/master/repo.json
   ```

## 🎯 Fitur

- ✅ Search film/series
- ✅ Multiple genres
- ✅ TV Shows support
- ✅ Download support
- ✅ Auto recommendations

## 🔧 Customization

### Ganti Domain
Edit `{self.plugin_name}.kt`:
```kotlin
override var mainUrl = "https://domain-baru.com"
```

### Tambah Genre
Edit bagian `mainPage`:
```kotlin
"$mainUrl/genre/GENRE/page/" to "Nama Genre"
```

## 📝 Template Info

- **Domain**: {self.domain}
- **Template**: {self.template['name']}
- **Plugin Name**: {self.plugin_name}

## 🐛 Troubleshooting

Jika plugin tidak bekerja, kemungkinan struktur website sudah berubah.
Edit selector di file `.kt` sesuai dengan struktur HTML website.

## 📄 License

Free to use and modify
'''

    def generate_config_json(self) -> dict:
        """Generate config.json untuk debugging"""
        return {
            "domain": self.domain,
            "plugin_name": self.plugin_name,
            "template": self.template["name"],
            "selectors": self.template["selectors"],
            "pages": self.template["pages"]
        }

    def create_project(self):
        """Generate semua file project"""
        print(f"\n🎬 Generating Cloudstream Plugin: {self.plugin_name}")
        print(f"📍 Domain: {self.domain}")
        print(f"📋 Template: {self.template['name']}\n")
        
        # Buat direktori
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(f"{self.base_dir}/.github/workflows", exist_ok=True)
        
        # Generate files
        files = {
            f"{self.plugin_name}.kt": self.generate_kotlin_file(),
            "build.gradle.kts": self.generate_build_gradle(),
            "settings.gradle.kts": self.generate_settings_gradle(),
            ".github/workflows/build.yml": self.generate_github_workflow(),
            "README.md": self.generate_readme(),
        }
        
        for filename, content in files.items():
            filepath = os.path.join(self.base_dir, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Created: {filepath}")
        
        # Generate JSON files
        repo_json_path = os.path.join(self.base_dir, "repo.json")
        with open(repo_json_path, 'w', encoding='utf-8') as f:
            json.dump(self.generate_repo_json(), f, indent=2)
        print(f"✅ Created: {repo_json_path}")
        
        config_json_path = os.path.join(self.base_dir, "config.json")
        with open(config_json_path, 'w', encoding='utf-8') as f:
            json.dump(self.generate_config_json(), f, indent=2)
        print(f"✅ Created: {config_json_path}")
        
        print(f"\n🎉 Project generated successfully!")
        print(f"📁 Location: {self.base_dir}/")
        
        return self.base_dir


# ============================================================================
# INTERACTIVE CLI
# ============================================================================

def interactive_mode():
    """Mode interaktif untuk generate plugin"""
    print("=" * 70)
    print("🎬 CLOUDSTREAM PLUGIN GENERATOR - INTERACTIVE MODE")
    print("=" * 70)
    
    # Input domain
    domain = input("\n📍 Masukkan URL domain (contoh: https://example.com): ").strip()
    if not domain.startswith('http'):
        domain = 'https://' + domain
    
    # Input plugin name (optional)
    plugin_name = input("📝 Nama plugin (kosongkan untuk auto-generate): ").strip()
    
    # Pilih template
    print("\n📋 Pilih template:")
    templates = list(WEBSITE_TEMPLATES.keys())
    for i, template_key in enumerate(templates, 1):
        template = WEBSITE_TEMPLATES[template_key]
        print(f"  {i}. {template['name']}")
    
    template_choice = input(f"\nPilihan (1-{len(templates)}) [default: 1]: ").strip()
    if template_choice and template_choice.isdigit():
        template_idx = int(template_choice) - 1
        if 0 <= template_idx < len(templates):
            template_key = templates[template_idx]
        else:
            template_key = templates[0]
    else:
        template_key = templates[0]
    
    # Generate
    generator = CloudstreamGenerator(
        domain=domain,
        plugin_name=plugin_name if plugin_name else None,
        template=template_key
    )
    
    generator.create_project()
    
    print("\n" + "=" * 70)
    print("📝 NEXT STEPS:")
    print("=" * 70)
    print("1. Upload folder ke GitHub")
    print("2. Buat branch 'builds'")
    print("3. Update repo.json dengan username GitHub Anda")
    print("4. Add repository di Cloudstream app")


def batch_mode(configs: List[Dict]):
    """Mode batch untuk generate multiple plugins"""
    print("=" * 70)
    print("🎬 CLOUDSTREAM PLUGIN GENERATOR - BATCH MODE")
    print("=" * 70)
    
    for i, config in enumerate(configs, 1):
        print(f"\n[{i}/{len(configs)}] Processing: {config.get('domain')}")
        generator = CloudstreamGenerator(**config)
        generator.create_project()
        print()


# ============================================================================
# MAIN
# ============================================================================

def main():
    import sys
    
    if len(sys.argv) > 1:
        # Command line mode
        if sys.argv[1] == '--batch' and len(sys.argv) > 2:
            # Batch mode dari file JSON
            with open(sys.argv[2], 'r') as f:
                configs = json.load(f)
            batch_mode(configs)
        else:
            # Single domain mode
            domain = sys.argv[1]
            plugin_name = sys.argv[2] if len(sys.argv) > 2 else None
            template = sys.argv[3] if len(sys.argv) > 3 else "wordpress_movie"
            
            generator = CloudstreamGenerator(domain, plugin_name, template)
            generator.create_project()
    else:
        # Interactive mode
        interactive_mode()


if __name__ == "__main__":
    main()
