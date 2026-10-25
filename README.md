# Transit Insight — Dashboard Analisis Transaksi TransJakarta

## 1. Deskripsi Proyek

**Transit Insight** merupakan proyek pengolahan dan visualisasi data transaksi transportasi TransJakarta menggunakan Python, PostgreSQL, SQLite, Pandas, dan Streamlit.

Proyek ini mengintegrasikan data transaksi yang disimpan dalam PostgreSQL dengan data referensi koridor dan halte yang disimpan dalam SQLite. Integrasi dilakukan menggunakan Python dan Pandas untuk menghasilkan dataset gabungan yang digunakan sebagai sumber data dashboard interaktif.

Dashboard dirancang untuk membantu pengguna memahami pola transaksi, distribusi tarif, aktivitas perjalanan berdasarkan waktu, serta koridor dan halte yang sering digunakan.

## 2. Tujuan Proyek

Proyek ini bertujuan untuk:

1. Menerapkan penggunaan dua DBMS berbeda, yaitu PostgreSQL dan SQLite, dalam satu alur pengolahan data.
2. Mengintegrasikan data dari kedua DBMS menggunakan Python dan Pandas.
3. Mengolah dan menggabungkan data transaksi dengan informasi referensi koridor dan halte.
4. Menyajikan hasil pengolahan data melalui dashboard interaktif berbasis web.
5. Menyediakan visualisasi yang membantu pengguna mengeksplorasi pola transaksi TransJakarta berdasarkan periode waktu dan koridor.

## 3. Sumber Data

Dataset utama yang digunakan dalam proyek ini berasal dari Kaggle.

- **Nama dataset:** TransJakarta Transportation Transaction
- **Sumber dataset:** [TransJakarta Transportation Transaction — Kaggle](https://www.kaggle.com/datasets/dikisahkan/transjakarta-transportation-transaction)

Dataset digunakan sebagai sumber data transaksi yang kemudian dibersihkan dan dipersiapkan sebelum dimasukkan ke dalam basis data.

## 4. Teknologi yang Digunakan

| Teknologi | Fungsi |
|---|---|
| Python | Bahasa pemrograman utama untuk pengolahan dan integrasi data. |
| PostgreSQL | Menyimpan data transaksi TransJakarta. |
| SQLite | Menyimpan data referensi koridor dan halte. |
| Pandas | Membersihkan, mengolah, dan menggabungkan data dari kedua DBMS. |
| SQLAlchemy | Mengelola koneksi Python ke PostgreSQL. |
| Psycopg | Driver untuk menghubungkan Python dengan PostgreSQL. |
| Streamlit | Membangun dashboard interaktif berbasis web. |
| Plotly | Membuat visualisasi data interaktif. |
| GitHub | Menyimpan kode sumber dan dokumentasi proyek. |
| Streamlit Community Cloud | Men-deploy dashboard agar dapat diakses secara daring. |

## 5. Arsitektur Sistem

Transit Insight menggunakan pendekatan integrasi data pada tingkat aplikasi (*application-level data integration*). Data dari PostgreSQL dan SQLite dibaca menggunakan Python, kemudian digabungkan menggunakan Pandas.

### Diagram Arsitektur

```text
                  Dataset TransJakarta
                          |
                          v
                  bersihkan_data.py
                          |
                          v
                transjakarta_clean.csv
                          |
               +----------+----------+
               |                     |
               v                     v
       impor_postgres.py       buat_sqlite.py
               |                     |
               v                     v
          PostgreSQL               SQLite
        Data Transaksi       Data Referensi
                              Koridor & Halte
               |                     |
               +----------+----------+
                          |
                          v
                   uji_pipeline.py
                          |
                          v
                  Integrasi Pandas
                          |
                          v
                  dashboard_data.csv
                          |
                          v
                        app.py
                          |
                          v
                 Streamlit Dashboard
```

### Peran Masing-Masing Komponen

**PostgreSQL**

PostgreSQL digunakan untuk menyimpan data transaksi TransJakarta, seperti identitas transaksi, koridor, halte keberangkatan dan tujuan, waktu transaksi, serta tarif perjalanan.

**SQLite**

SQLite digunakan untuk menyimpan data referensi dalam tabel `koridor` dan `halte`. Data ini membantu melengkapi informasi transaksi dengan referensi koridor serta koordinat halte yang tersedia.

**Pandas**

Pandas digunakan untuk membaca data dari kedua DBMS, menggabungkan data transaksi dengan data referensi, serta menghasilkan dataset gabungan dalam format CSV.

**Streamlit**

Streamlit digunakan untuk menampilkan dataset hasil integrasi dalam bentuk dashboard interaktif. Pada implementasi ini, dashboard membaca file `dashboard_data.csv`, bukan mengakses PostgreSQL dan SQLite secara langsung ketika aplikasi dibuka.

## 6. Fitur Dashboard

Dashboard Transit Insight menyediakan beberapa fitur berikut.

### 6.1 Filter Periode Waktu

Pengguna dapat memilih rentang tanggal untuk melihat data transaksi pada periode tertentu.

### 6.2 Filter Koridor

Pengguna dapat memilih koridor tertentu untuk mengeksplorasi transaksi berdasarkan koridor yang tersedia dalam dataset.

### 6.3 Ringkasan Indikator Utama

Dashboard menampilkan sejumlah indikator ringkasan, antara lain:

- Jumlah transaksi.
- Total pendapatan berdasarkan nilai tarif yang tercatat.
- Rata-rata tarif transaksi.
- Rata-rata durasi perjalanan.

Nilai indikator mengikuti data yang tersedia dan filter yang sedang diterapkan pada dashboard.

### 6.4 Visualisasi Aktivitas Berdasarkan Waktu

Grafik aktivitas per jam membantu pengguna mengamati perubahan jumlah transaksi berdasarkan waktu *tap-in*.

### 6.5 Analisis Koridor dan Halte

Dashboard menyajikan visualisasi koridor dan halte dengan jumlah transaksi tertinggi berdasarkan data yang tersedia.

### 6.6 Distribusi Tarif

Histogram tarif digunakan untuk melihat distribusi nilai tarif transaksi.

### 6.7 Pratinjau Data

Pengguna dapat melihat sebagian data hasil integrasi dalam bentuk tabel untuk memahami struktur data yang digunakan dalam visualisasi.

## 7. Struktur Proyek

Struktur file utama proyek adalah sebagai berikut.

```text
transit-insight/
│
├── app.py
├── bersihkan_data.py
├── impor_postgres.py
├── buat_sqlite.py
├── uji_pipeline.py
├── schema.sql
├── requirements.txt
├── README.md
│
├── transjakarta_clean.csv
├── transit_reference.db
└── dashboard_data.csv
```

**Keterangan file:**

| File | Fungsi |
|---|---|
| `app.py` | Kode sumber dashboard Streamlit. |
| `bersihkan_data.py` | Skrip pembersihan dan persiapan data. |
| `impor_postgres.py` | Skrip untuk memasukkan data transaksi ke PostgreSQL. |
| `buat_sqlite.py` | Skrip untuk membangun basis data referensi SQLite. |
| `uji_pipeline.py` | Skrip integrasi data dari PostgreSQL dan SQLite. |
| `schema.sql` | Definisi struktur tabel PostgreSQL dan indeksnya. |
| `requirements.txt` | Daftar dependensi Python. |
| `README.md` | Dokumentasi proyek. |
| `transjakarta_clean.csv` | Dataset hasil pembersihan. |
| `transit_reference.db` | Basis data referensi SQLite. |
| `dashboard_data.csv` | Dataset hasil integrasi yang digunakan dashboard. |

File CSV dan basis data yang dihasilkan selama proses pengolahan dapat dibuat ulang dengan menjalankan skrip terkait. Apabila file-file tersebut tidak disertakan dalam repositori, pengguna perlu menyiapkannya terlebih dahulu sebelum menjalankan tahap berikutnya.

## 8. Persyaratan Sistem

Sebelum menjalankan proyek secara lokal, pastikan perangkat telah memiliki:

- Python.
- PostgreSQL.
- Git, jika ingin mengunduh proyek melalui GitHub.
- Dataset TransJakarta yang digunakan dalam proyek.
- Dependensi Python yang tercantum pada `requirements.txt`.

Selain itu, basis data PostgreSQL harus tersedia dan dapat diakses oleh skrip Python. Nama basis data, nama tabel, serta konfigurasi koneksi harus sesuai dengan pengaturan yang digunakan dalam skrip.

## 9. Instalasi dan Menjalankan Proyek

### 9.1 Mengunduh Repositori

Unduh repositori proyek melalui GitHub:

[Transit Insight — GitHub Repository](https://github.com/SitiHanifa2212/transit-insight)

Atau jalankan perintah berikut:

```bash
git clone https://github.com/SitiHanifa2212/transit-insight.git
cd transit-insight
```

### 9.2 Membuat Virtual Environment

Buat lingkungan Python terpisah agar dependensi proyek tidak bercampur dengan proyek lain.

```bash
python -m venv .venv
```

Aktifkan virtual environment pada Windows:

```cmd
.venv\Scripts\activate
```

### 9.3 Menginstal Dependensi

Jalankan perintah berikut:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 9.4 Menyiapkan Dataset

Unduh dataset dari sumber yang dicantumkan pada bagian **Sumber Data**.

Tempatkan file dataset pada lokasi yang sesuai dengan konfigurasi `bersihkan_data.py`, atau sesuaikan path file pada skrip tersebut.

Jalankan proses pembersihan:

```bash
python bersihkan_data.py
```

Pastikan proses berhasil menghasilkan file `transjakarta_clean.csv`.

### 9.5 Menyiapkan PostgreSQL

Pastikan layanan PostgreSQL sedang berjalan.

Buat basis data bernama `transit_insight` jika belum tersedia. Siapkan tabel transaksi sesuai struktur pada `schema.sql` dan konfigurasi koneksi yang digunakan oleh `impor_postgres.py`.

Jalankan skrip impor:

```bash
python impor_postgres.py
```

**Catatan:** Perhatikan cara skrip `impor_postgres.py` membuat tabel. Jika skrip menggunakan `if_exists="replace"`, tabel yang sudah ada akan diganti sehingga indeks yang dibuat sebelumnya dapat hilang. Jika indeks perlu dipertahankan, sesuaikan urutan pembuatan tabel, impor data, dan penerapan indeks dengan implementasi skrip.

### 9.6 Membuat Basis Data SQLite

Jalankan perintah berikut:

```bash
python buat_sqlite.py
```

Skrip akan membangun file `transit_reference.db` beserta tabel `koridor` dan `halte`.

Pastikan file tersebut berada di lokasi yang dapat ditemukan oleh `uji_pipeline.py`.

### 9.7 Menjalankan Pipeline Integrasi

Jalankan:

```bash
python uji_pipeline.py
```

Masukkan kata sandi PostgreSQL apabila diminta oleh program.

Jika seluruh proses berhasil, skrip akan menghasilkan:

```text
dashboard_data.csv
```

File tersebut merupakan hasil integrasi data transaksi dan data referensi dari kedua DBMS.

**Hasil pengujian pipeline pada data yang digunakan:**

| Komponen | Jumlah |
|---|---:|
| Data transaksi PostgreSQL | 37.900 baris |
| Data referensi koridor SQLite | 221 baris |
| Data referensi halte SQLite | 3.601 baris |
| Hasil integrasi | 37.900 baris |
| Jumlah kolom hasil integrasi | 14 kolom |
| Baris yang berhasil dilengkapi koordinat halte | 36.687 baris |

Sebagian data masih belum memiliki koordinat yang dapat dicocokkan dengan referensi halte. Angka-angka tersebut merupakan hasil pengujian pada data yang digunakan dan dapat berubah apabila dataset diperbarui.

### 9.8 Menjalankan Dashboard

Setelah `dashboard_data.csv` tersedia, jalankan:

```bash
python -m streamlit run app.py
```

Streamlit akan menampilkan alamat lokal yang dapat dibuka melalui browser.

Gunakan alamat lokal yang ditampilkan oleh terminal untuk mengakses dashboard pada perangkat sendiri.

## 10. Deployment Dashboard

Dashboard Transit Insight telah dipublikasikan melalui Streamlit Community Cloud.

**Akses dashboard:**

[Transit Insight — Live Dashboard](https://transit-insight-siti.streamlit.app/)

**Repositori kode sumber:**

[Transit Insight — GitHub](https://github.com/SitiHanifa2212/transit-insight)

Pada implementasi saat ini, dashboard membaca file `dashboard_data.csv` sebagai sumber data visualisasi. Dashboard tidak membuat koneksi langsung ke PostgreSQL dan SQLite saat pengguna membuka aplikasi.

Dengan demikian, proses integrasi data dilakukan melalui pipeline Python terlebih dahulu, sedangkan aplikasi Streamlit berfokus pada penyajian dan eksplorasi data hasil integrasi.

## 11. Keamanan dan Pengelolaan Kredensial

Informasi autentikasi basis data harus dikelola dengan hati-hati.

Praktik keamanan yang perlu diterapkan dan dipertahankan dalam proyek ini meliputi:

1. Tidak menuliskan kata sandi PostgreSQL secara langsung di dalam kode sumber.
2. Meminta kata sandi melalui mekanisme input tersembunyi apabila skrip menggunakan `getpass`.
3. Tidak mengunggah file yang berisi kata sandi, token, atau kredensial ke repositori publik.
4. Menggunakan pengaturan rahasia yang sesuai apabila aplikasi membutuhkan kredensial saat deployment.
5. Memastikan file konfigurasi lokal yang sensitif dikecualikan melalui `.gitignore`.

Dashboard saat ini membaca file CSV hasil pipeline dan tidak membutuhkan kredensial PostgreSQL maupun SQLite untuk menampilkan visualisasi. Kredensial diperlukan pada tahap pengolahan data yang terhubung ke PostgreSQL.

## 12. Referensi Kode

Proyek ini juga menggunakan repositori berikut sebagai salah satu referensi untuk mempelajari pengolahan data TransJakarta:

[TransJakarta Data Vault — GitHub](https://github.com/radisahussein/transjakarta_datavault)

Repositori tersebut dicantumkan sebagai referensi kode, bukan sebagai pengganti kode sumber utama proyek Transit Insight.

## 13. Batasan Proyek

Beberapa batasan implementasi yang perlu diperhatikan adalah:

1. Kelengkapan koordinat halte bergantung pada kecocokan data transaksi dengan data referensi halte.
2. Dashboard menggunakan file `dashboard_data.csv` yang dihasilkan oleh pipeline. Oleh karena itu, perubahan pada basis data tidak otomatis tercermin sampai pipeline dijalankan kembali dan file hasilnya diperbarui.
3. Hasil analisis bergantung pada kualitas, kelengkapan, dan periode data yang digunakan.
4. Visualisasi menggambarkan pola berdasarkan data yang tersedia dan tidak dengan sendirinya menjelaskan penyebab di balik pola transaksi.

## 14. Pengembang

- **Nama:** Siti Hanifa
- **Proyek:** Transit Insight — Dashboard Analisis Transaksi TransJakarta
- **Bidang:** Integrasi Basis Data dan Visualisasi Data
- **Platform Dashboard:** Streamlit Community Cloud
