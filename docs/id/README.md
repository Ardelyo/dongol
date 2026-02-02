# DONGOL 🇮🇩

**Sistem Manajemen Tugas Paralel Berbasis Arsitektur Terdistribusi Modern**

<p>
  <a href="../../README.md">🇬🇧 English</a> | 
  <a href="README.md">🇮🇩 Bahasa Indonesia</a>
</p>

---

## 🎯 Apa itu DONGOL?

**DONGOL** (**D**istributed **O**rchestration for **N**avigating **G**oals and **O**perational **L**ogic) adalah sistem manajemen tugas paralel yang dirancang untuk meningkatkan efisiensi pemrosesan data melalui:

- **Parallel Thinking Matrix** - Eksekusi multi-stream berpikir secara simultan
- **Intelligent Chunking** - Dekomposisi cerdas dengan pelacakan dependensi
- **Agent-Native Design** - Dirancang untuk workflow AI agents

### Moto Kami
> *"Berpikir Paralel. Eksekusi Lebih Cepat. 🇮🇩"*

Dibuat dengan ❤️ di Indonesia oleh **Ardellio Satria Anindito** (SMA Kartika XIX-1 Bandung)

---

## 🚀 Instalasi

### Via pip (Rekomendasi)

```bash
# Instalasi dasar
pip install dongol

# Dengan semua fitur
pip install dongol[all]

# Versi development
pip install dongol[dev]
```

### Dari Source

```bash
git clone https://github.com/dongol-org/dongol.git
cd dongol
pip install -e ".[all]"
```

### Menggunakan Docker

```bash
docker pull dongol/dongol:latest
docker run -it dongol/dongol
```

### Windows (PowerShell)

```powershell
# Instalasi cepat
Invoke-RestMethod https://get.dongol.io/install.ps1 | Invoke-Expression
```

---

## 💡 Penggunaan Dasar

### Command Line Interface (CLI)

```bash
# Analisis proyek
dongol analyze ./proyek-saya

# Proses paralel
dongol think "Optimasi query database" --parallel --workers 8

# Pecah file besar
dongol chunk file-besar.txt --size 1000

# Cek status sistem
dongol status

# Dapatkan bantuan
dongol --help
```

### Python API

```python
import asyncio
from dongol import DongolEngine

async def proses_data():
    # Inisialisasi mesin
    mesin = await DongolEngine.create()
    
    # Buat tugas paralel
    tugas = await mesin.create_task(
        name="Proses Dataset",
        content="Data besar...",
        auto_chunk=True,
        parallel=True
    )
    
    # Eksekusi
    hasil = await mesin.execute_task(tugas.id)
    print(f"Selesai dalam {hasil.duration_ms:.2f}ms")

asyncio.run(proses_data())
```

---

## 📊 Performa

| Metrik | Sekuensial | DONGOL | Peningkatan |
|--------|-----------|--------|-------------|
| **Pembuatan Tugas** | - | 48.713/detik | **5x target** |
| **Proses File** | 43.7/detik | 196.5/detik | **4.5x** |
| **Throughput** | 365 MB/detik | 1.644 MB/detik | **4.5x** |
| **Latency** | - | <1ms | **✓** |

> Diuji pada 2.979 file nyata (23,12 GB) dari drive D:

---

## 🏗️ Arsitektur Sistem

```
┌─────────────────────────────────────────────────────────────┐
│  🖥️ ANTARMUKA UNIVERSAL                                      │
│  CLI • REST API • WebSocket • SDK • Web UI                  │
├─────────────────────────────────────────────────────────────┤
│  ⚙️ MESIN INTI TERPADU                                      │
│  Async Event Loop • Task Scheduler • State Machine          │
├─────────────────────────────────────────────────────────────┤
│  🔄 LAYER PROSES PARALEL                                    │
│  Thinker Matrix • Chunking Engine • Context Memory          │
├─────────────────────────────────────────────────────────────┤
│  💾 LAYER PERSISTENSI                                       │
│  SQLite • Sled • File System • Cloud                        │
└─────────────────────────────────────────────────────────────┘
```

---

## ✨ Fitur Unggulan

### 1. Parallel Thinking Matrix 🚀
Sistem unik yang memungkinkan multiple "thought streams" berjalan secara paralel dengan dependency tracking otomatis.

### 2. Intelligent Chunking 🧩
Tiga strategi chunking:
- **Token-based** - Berbasis token dengan preservasi batas kalimat
- **Structure-based** - Mempertahankan hierarki JSON/XML
- **Semantic** - Menggunakan embeddings (dengan LLM)

### 3. Agent-Native Design 🤖
Dirancang khusus untuk AI agents dengan dukungan Model Context Protocol (MCP).

### 4. Zero-Latency Design ⚡
- Task creation: <1ms
- Context switch: <100μs
- Memory: ~35 bytes per task

### 5. Made in Indonesia 🇮🇩
Dibuat oleh siswa SMA Indonesia untuk komunitas global!

---

## 📚 Dokumentasi

### Tutorial

1. [Panduan Instalasi](installation.md)
2. [Tutorial Cepat](quickstart.md)
3. [Referensi API](api.md)
4. [Arsitektur Detail](architecture.md)
5. [Contoh Penggunaan](examples.md)

### Studi Kasus

- [Analisis Drive](case-studies/drive-analysis.md)
- [Proyek Data Science](case-studies/data-science.md)
- [Automation Workflow](case-studies/automation.md)

---

## 🌏 Komunitas Indonesia

Bergabung dengan komunitas tech Indonesia:

### Telegram Groups
- 🇮🇩 [Python Indonesia](https://t.me/pythonid) - Komunitas Python terbesar
- 🇮🇩 [Surabaya Tech](https://t.me/surabayatech) - Tech community Surabaya
- 🇮🇩 [Bandung Tech](https://t.me/bandungtech) - Tech community Bandung

### Meetups
- 🗓️ **PythonID Meetup** - Bulanan di berbagai kota
- 🗓️ **Surabaya.py** - Meetup Python Surabaya
- 🗓️ **Bandung.py** - Meetup Python Bandung

### Media Sosial
- 🐦 Twitter: [@dongol_io](https://twitter.com/dongol_io)
- 💬 Discord: [discord.gg/dongol](https://discord.gg/dongol)
- 📧 Email: [contact@dongol.io](mailto:contact@dongol.io)

---

## 🤝 Berkontribusi

Kami sangat menghargai kontribusi dari semua orang!

### Cara Berkontribusi

1. **Fork** repository ini
2. **Clone** ke lokal Anda
3. Buat **branch** baru: `git checkout -b fitur/fitur-anda`
4. **Commit** perubahan: `git commit -m "feat: tambah fitur"`
5. **Push** ke branch: `git push origin fitur/fitur-anda`
6. Buat **Pull Request**

Lihat [CONTRIBUTING.md](../../CONTRIBUTING.md) untuk panduan lengkap.

### Kontributor Indonesia

Kami bangga dengan kontributor Indonesia kami:

<a href="https://github.com/dongol-org/dongol/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=dongol-org/dongol" />
</a>

---

## 📖 Kutipan Akademik

Jika Anda menggunakan DONGOL dalam penelitian:

```bibtex
@software{dongol2024,
  author = {Anindito, Ardellio Satria},
  title = {DONGOL: Sistem Manajemen Tugas Paralel},
  year = {2024},
  school = {SMA Kartika XIX-1 Bandung},
  address = {Indonesia},
  url = {https://github.com/dongol-org/dongol}
}
```

---

## 📜 Lisensi

Proyek ini dilisensikan di bawah MIT License - lihat file [LICENSE](../../LICENSE).

```
MIT License
Copyright (c) 2024-2025 Ardellio Satria Anindito & Kontributor DONGOL
Dibuat di Indonesia 🇮🇩
```

---

## 🙏 Ucapan Terima Kasih

- **Komunitas Python Indonesia** - Inspirasi dan dukungan
- **SMA Kartika XIX-1 Bandung** - Fondasi pendidikan
- **Kontributor** - Yang membuat proyek ini lebih baik
- **Pengguna** - Yang menggunakan dan memberi feedback

---

<div align="center">

**[⬆ Kembali ke Atas](#-apa-itu-dongol)**

*Dibuat dengan ❤️ dan ☕ di Indonesia*

🇮🇩 🇮🇩 🇮🇩

**Bhinneka Tunggal Ika - Unity in Diversity**

</div>
