# Transit Insight: Dashboard Analisis Transaksi TransJakarta

## 1. Deskripsi Proyek
Transit Insight merupakan proyek data pipeline dan visualisasi berbasis web untuk menganalisis data transaksi TransJakarta pada April 2023. Proyek ini mengintegrasikan dua sistem manajemen basis data (*Database Management System* atau DBMS), yaitu PostgreSQL dan SQLite, menggunakan Python dan Pandas.
PostgreSQL digunakan untuk menyimpan data transaksi, sedangkan SQLite digunakan untuk menyimpan data referensi koridor dan halte. Data dari kedua DBMS tersebut digabungkan menggunakan Pandas, kemudian disiapkan untuk visualisasi melalui dashboard interaktif menggunakan Streamlit dan Plotly.

Proyek ini dibuat untuk memenuhi tugas mengenai integrasi multi-DBMS, pengolahan data, dan visualisasi web interaktif.

## 2. Tujuan Proyek
Tujuan pengembangan Transit Insight adalah:
- Mengolah dan membersihkan data transaksi TransJakarta.
- Mengimplementasikan dua DBMS dengan fungsi yang berbeda.
- Menggabungkan data dari PostgreSQL dan SQLite menggunakan Pandas.
- Menyajikan informasi transaksi melalui visualisasi interaktif.
- Membangun dashboard web yang dapat diakses secara publik.
- Menerapkan proses data pipeline dari data mentah hingga data siap divisualisasikan.

## 3. Sumber Data
Dataset utama yang digunakan berasal dari Kaggle:
**TransJakarta Transportation Transaction Dataset**

Sumber dataset:
https://www.kaggle.com/datasets/dikisahkan/transjakarta-transportation-transaction
Dataset tersebut digunakan sebagai sumber data transaksi untuk proses pembersihan, pengolahan, integrasi, dan analisis.

## 4. Teknologi yang Digunakan
| Teknologi | Fungsi |
|---|---|
| Python | Bahasa pemrograman utama |
| PostgreSQL | Menyimpan data transaksi utama |
| SQLite | Menyimpan data referensi koridor dan halte |
| Pandas | Membersihkan, mengolah, dan menggabungkan data |
| SQLAlchemy | Menghubungkan aplikasi Python dengan PostgreSQL |
| psycopg | Driver koneksi PostgreSQL |
| Streamlit | Membangun aplikasi dashboard web |
| Plotly | Membuat visualisasi data interaktif |
| GitHub | Menyimpan dan mendokumentasikan kode sumber |
| Streamlit Community Cloud | Melakukan deployment dashboard |

## 5. Arsitektur Data Pipeline
Transit Insight menggunakan dua DBMS dengan fungsi yang berbeda.
### 5.1. PostgreSQL
PostgreSQL digunakan untuk menyimpan data transaksi TransJakarta yang telah melalui proses pembersihan. Data transaksi disimpan dalam tabel `transaksi` dan menjadi sumber utama untuk analisis jumlah perjalanan, tarif, waktu transaksi, serta koridor.
### 5.2. SQLite
SQLite digunakan untuk menyimpan data referensi yang berkaitan dengan koridor dan halte. Database referensi disimpan dalam file `transit_reference.db`, yang dibentuk melalui script `buat_sqlite.py`.
Database SQLite memiliki tabel:
- `koridor`: menyimpan informasi referensi koridor.
- `halte`: menyimpan informasi referensi halte, termasuk kode, nama, dan koordinat yang tersedia.
### 5.3. Integrasi Data
Data transaksi dari PostgreSQL dan data referensi dari SQLite diambil melalui script Python, kemudian digabungkan menggunakan Pandas pada tingkat aplikasi.
Hasil integrasi disimpan sebagai `hasil_pipeline.csv`. Data yang disiapkan untuk dashboard disimpan dalam `dashboard_data.csv`.

### Diagram Alur Pipeline
```text
       Dataset TransJakarta
                |
                v
       bersihkan_data.py
                |
                v
     transjakarta_clean.csv
                |
          +-----+-----+
          |           |
          v           v
      PostgreSQL    SQLite
      transaksi     koridor & halte
          |           |
          +-----+-----+
                |
                v
          uji_pipeline.py
         (Integrasi Pandas)
                |
                v
       hasil_pipeline.csv
                |
                v
       dashboard_data.csv
                |
                v
        Streamlit + Plotly
                |
                v
        Dashboard Publik
```
**Catatan implementasi:** integrasi PostgreSQL dan SQLite dilakukan melalui pipeline Python menggunakan Pandas. Dashboard publik membaca hasil integrasi dari file `dashboard_data.csv`, sehingga tidak memerlukan koneksi langsung ke database lokal ketika diakses oleh pengguna.

Dengan demikian, proses integrasi data dan proses penyajian dashboard merupakan dua tahap yang terpisah.

## 6. Fitur Dashboard
Dashboard Transit Insight menyediakan beberapa fitur analisis:
- **Filter tanggal:** membatasi data berdasarkan rentang tanggal transaksi.
- **Filter koridor:** menampilkan data berdasarkan koridor yang dipilih.
- **Jumlah transaksi:** menampilkan jumlah transaksi sesuai filter.
- **Total nilai tarif:** menjumlahkan nilai pada kolom `payAmount`.
- **Rata-rata tarif:** menghitung rata-rata nilai `payAmount`.
- **Rata-rata durasi perjalanan:** menampilkan rata-rata durasi dalam menit.
- **Pola transaksi berdasarkan jam:** menampilkan distribusi transaksi berdasarkan waktu tap-in.
- **Top 10 koridor:** menampilkan koridor dengan jumlah transaksi tertinggi.
- **Top 10 halte tap-in:** menampilkan halte awal dengan jumlah transaksi tertinggi.
- **Distribusi tarif:** menampilkan persebaran nilai tarif melalui histogram.
- **Pratinjau transaksi:** menampilkan sebagian data transaksi dalam bentuk tabel.

Fitur-fitur tersebut membantu pengguna mengeksplorasi pola transaksi berdasarkan tanggal dan koridor yang dipilih.
**Catatan interpretasi:** nilai tarif yang ditampilkan dihitung dari kolom `payAmount` pada dataset. Nilai tersebut tidak diklaim sebagai pendapatan resmi TransJakarta.

## 7. Struktur File Proyek
Repository Transit Insight memiliki struktur file sebagai berikut:
```text
transit-insight/
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
├── schema.sql
├── bersihkan_data.py
├── buat_sqlite.py
├── cek_data.py
├── impor_postgres.py
├── uji_pipeline.py
├── dashboard_data.csv
├── transit_reference.db
└── transjakarta-eda-kmeans.ipynb
```
### Keterangan File
| File | Fungsi |
|---|---|
| `app.py` | Source code utama dashboard Streamlit |
| `README.md` | Dokumentasi proyek |
| `requirements.txt` | Daftar dependensi Python |
| `.gitignore` | Mengatur file yang tidak perlu dimasukkan ke Git |
| `schema.sql` | Skrip DDL untuk mendefinisikan struktur tabel transaksi PostgreSQL |
| `bersihkan_data.py` | Membersihkan dan mempersiapkan data transaksi |
| `buat_sqlite.py` | Membentuk database referensi SQLite |
| `cek_data.py` | Script pemeriksaan data |
| `impor_postgres.py` | Mengimpor data bersih ke PostgreSQL |
| `uji_pipeline.py` | Mengintegrasikan data PostgreSQL dan SQLite menggunakan Pandas |
| `dashboard_data.csv` | Data yang dibaca oleh dashboard |
| `transit_reference.db` | Database referensi SQLite |
| `transjakarta-eda-kmeans.ipynb` | Notebook eksplorasi data, sesuai isi notebook |

**Catatan:** `transjakarta_clean.csv` dan `hasil_pipeline.csv` merupakan file keluaran dari proses pengolahan data. File tersebut tidak tercantum dalam struktur repository di atas karena keduanya digunakan sebagai hasil proses lokal dan dapat dibuat kembali melalui pipeline.

## 8. Persiapan dan Instalasi
### 8.1. Persyaratan
Pastikan perangkat telah memiliki:
- Python.
- PostgreSQL untuk menjalankan pipeline integrasi.
- Git jika ingin mengkloning repository.
SQLite menggunakan pustaka standar Python sehingga tidak memerlukan instalasi server database terpisah.
### 8.2. Mengunduh Repository
Jalankan perintah berikut pada terminal:
```bash
git clone https://github.com/SitiHanifa2212/transit-insight.git
cd transit-insight
```
### 8.3. Membuat Virtual Environment
Untuk membuat lingkungan Python terpisah, jalankan:
```bash
python -m venv .venv
```
Aktifkan virtual environment pada Windows:
```bash
.venv\Scripts\activate
```
### 8.4. Menginstal Dependensi
Jalankan perintah berikut:
```bash
python -m pip install -r requirements.txt
```

## 9. Menjalankan Pipeline Data
Pipeline digunakan untuk membersihkan data, menyimpan data pada kedua DBMS, serta mengintegrasikannya menggunakan Pandas.
### Langkah 1 — Menyiapkan Dataset
Unduh dataset dari sumber Kaggle yang tercantum pada bagian sumber data.
Pastikan file dataset mentah ditempatkan sesuai dengan lokasi yang ditentukan dalam script `bersihkan_data.py`.
### Langkah 2 — Membersihkan Data
Jalankan:
```bash
python bersihkan_data.py
```
Script ini memilih kolom yang diperlukan, mengolah kolom waktu, menghitung durasi perjalanan berdasarkan waktu tap-in dan tap-out, serta menghasilkan file `transjakarta_clean.csv`.
### Langkah 3 — Menyiapkan PostgreSQL
Pastikan layanan PostgreSQL berjalan dan database `transit_insight` telah tersedia.
Script impor menggunakan konfigurasi koneksi PostgreSQL lokal. Jika menggunakan lingkungan yang berbeda, sesuaikan konfigurasi koneksinya.
### Langkah 4 — Mengimpor Data ke PostgreSQL
Jalankan:
```bash
python impor_postgres.py
```
Masukkan password PostgreSQL ketika diminta.
Script akan memasukkan data dari `transjakarta_clean.csv` ke tabel `transaksi`.
**Perhatian:** script saat ini menggunakan `if_exists="replace"`, sehingga tabel `transaksi` akan diganti ketika proses impor dijalankan ulang.
### Langkah 5 — Membentuk Database Referensi SQLite
Jalankan:
```bash
python buat_sqlite.py
```
Script akan membentuk atau memperbarui file `transit_reference.db` beserta tabel `koridor` dan `halte`.
### Langkah 6 — Mengintegrasikan Data
Jalankan:
```bash
python uji_pipeline.py
```
Masukkan password PostgreSQL ketika diminta.
Script mengambil data transaksi dari PostgreSQL serta data referensi dari SQLite. Kedua sumber tersebut digabungkan menggunakan Pandas.
Hasil integrasi disimpan dalam file:
```text
hasil_pipeline.csv
```
### Langkah 7 — Menyiapkan Data untuk Dashboard
Dashboard membaca file `dashboard_data.csv`, sedangkan script integrasi menghasilkan `hasil_pipeline.csv`.
Jika ingin menggunakan hasil pipeline terbaru untuk dashboard, salin atau ekspor hasil integrasi tersebut menjadi `dashboard_data.csv` setelah memastikan kolom-kolomnya sesuai dengan kebutuhan aplikasi.
Pastikan file `dashboard_data.csv` tersedia di folder yang sama dengan `app.py`.
**Catatan:** menjalankan pipeline tidak otomatis memperbarui file `dashboard_data.csv` pada implementasi saat ini.

## 10. Menjalankan Dashboard secara Lokal
Dashboard dapat dijalankan secara lokal tanpa koneksi langsung ke PostgreSQL dan SQLite, selama file `dashboard_data.csv` tersedia dan memiliki kolom yang dibutuhkan oleh aplikasi.
Jalankan perintah:
```bash
python -m streamlit run app.py
```
Streamlit akan menampilkan alamat lokal yang dapat dibuka melalui browser.
Dashboard lokal menggunakan file CSV sebagai sumber data visualisasi.

## 11. Deployment Dashboard
Dashboard Transit Insight telah dipublikasikan melalui Streamlit Community Cloud.
**Dashboard publik:**
https://transit-insight-siti.streamlit.app/
**Repository GitHub:**
https://github.com/SitiHanifa2212/transit-insight
Aplikasi publik membaca `dashboard_data.csv` sebagai sumber data. Oleh karena itu, dashboard yang telah dideploy tidak terhubung secara langsung ke PostgreSQL dan SQLite lokal.
Pendekatan ini memisahkan proses integrasi data dari proses visualisasi web.

## 12. Keamanan dan Pengelolaan Data
Beberapa hal yang perlu diperhatikan dalam pengelolaan proyek:
- Password PostgreSQL diminta saat script yang memerlukan koneksi dijalankan.
- Password tidak dituliskan secara langsung dalam source code.
- File `.env` dan `.streamlit/secrets.toml` dikecualikan melalui `.gitignore`.
- Dashboard publik menggunakan file CSV yang telah disiapkan sebelumnya.
- Jika proyek dikembangkan lebih lanjut, konfigurasi kredensial sebaiknya dikelola menggunakan environment variables atau mekanisme secrets pada layanan deployment.

## 13. Referensi Proyek
Sebagai referensi pembelajaran terkait pengolahan dan visualisasi data TransJakarta, proyek ini mempelajari repository berikut:
**TransJakarta Data Vault**
https://github.com/radisahussein/transjakarta_datavault
Repository tersebut dapat digunakan sebagai referensi pembanding untuk mempelajari pengolahan data dan penyajian analitik terkait TransJakarta. Teknologi serta implementasinya berbeda dari Transit Insight.

## 14. Pengembang
**Nama:** Siti Hanifa
**Nama Proyek:** Transit Insight — Dashboard Analisis Transaksi TransJakarta
**Repository:** https://github.com/SitiHanifa2212/transit-insight
**Dashboard:** https://transit-insight-siti.streamlit.app/
