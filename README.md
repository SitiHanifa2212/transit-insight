# Transit Insight: Dashboard Analisis Transaksi TransJakarta
## 1. Deskripsi Proyek
Transit Insight merupakan proyek data pipeline dan visualisasi berbasis web untuk menganalisis data transaksi TransJakarta pada April 2023. Proyek ini mengintegrasikan dua sistem manajemen basis data (DBMS), yaitu PostgreSQL dan SQLite, menggunakan Python dan Pandas. Hasil integrasi disajikan melalui dashboard interaktif menggunakan Streamlit dan Plotly.
Proyek ini dibuat untuk memenuhi tugas mengenai integrasi multi-DBMS, pengolahan data, dan visualisasi web interaktif.

## 2. Tujuan Proyek
- Mengolah dan membersihkan data transaksi TransJakarta.
- Mengimplementasikan dua DBMS dengan fungsi berbeda.
- Menggabungkan data dari kedua DBMS menggunakan Pandas.
- Menyajikan informasi transaksi melalui visualisasi interaktif.
- Menerapkan deployment dashboard agar dapat diakses secara publik.

## 3. Sumber Data
Dataset utama berasal dari Kaggle:
- [TransJakarta Transportation Transaction Dataset](https://www.kaggle.com/datasets/dikisahkan/transjakarta-transportation-transaction)
Dataset tersebut digunakan sebagai sumber data transaksi untuk proses pengolahan dan analisis.

## 4. Teknologi yang Digunakan
| Teknologi | Fungsi |
|---|---|
| Python | Bahasa pemrograman utama |
| PostgreSQL | Menyimpan data transaksi utama |
| SQLite | Menyimpan data referensi halte dan koridor |
| Pandas | Membersihkan, mengolah, dan menggabungkan data |
| SQLAlchemy dan psycopg | Mendukung konektivitas PostgreSQL |
| Streamlit | Membangun aplikasi dashboard web |
| Plotly | Membuat visualisasi data interaktif |
| GitHub | Menyimpan dan mendokumentasikan kode sumber |
| Streamlit Community Cloud | Melakukan deployment dashboard |

## 5. Arsitektur Data Pipeline
Proyek ini menggunakan dua DBMS dengan fungsi yang berbeda.
### DBMS 1: PostgreSQL
PostgreSQL digunakan untuk menyimpan data transaksi TransJakarta yang telah melalui proses pembersihan. Data transaksi menjadi sumber utama untuk analisis jumlah perjalanan, tarif, waktu transaksi, dan koridor.
### DBMS 2: SQLite
SQLite digunakan untuk menyimpan data referensi yang berkaitan dengan koridor dan halte. Database referensi ini dibuat melalui skrip Python `buat_sqlite.py`.
### Integrasi Data
Data transaksi dari PostgreSQL dan data referensi dari SQLite diambil melalui skrip Python, kemudian digabungkan menggunakan Pandas.
Hasil integrasi disimpan sebagai data keluaran pipeline dan disiapkan dalam berkas `dashboard_data.csv` untuk digunakan oleh dashboard publik.
Alur pipeline:
```text
Dataset TransJakarta dari Kaggle
              |
              v
      Pembersihan Data
              |
              v
         PostgreSQL
     Data transaksi utama

          SQLite
   Data referensi halte
      dan koridor
              |
              v
      Python + Pandas
    Integrasi kedua data
              |
              v
      Hasil Pipeline CSV
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
**Catatan implementasi:** Proses penggabungan data PostgreSQL dan SQLite dijalankan melalui pipeline Python. Dashboard yang telah di-deploy membaca hasil pipeline dari `dashboard_data.csv`, sehingga tidak memerlukan koneksi langsung ke database lokal ketika diakses oleh pengguna.

## 6. Fitur Dashboard
Dashboard Transit Insight menyediakan beberapa fitur analisis:
- Filter berdasarkan rentang tanggal.
- Filter berdasarkan koridor.
- Ringkasan jumlah transaksi.
- Total nilai tarif berdasarkan data yang dianalisis.
- Rata-rata tarif dan durasi perjalanan.
- Grafik pola transaksi berdasarkan jam tap-in.
- Visualisasi 10 koridor dengan jumlah transaksi terbanyak.
- Grafik 10 halte tap-in teratas.
- Distribusi nilai tarif.
- Tabel untuk melihat rincian transaksi.
Visualisasi membantu pengguna mengeksplorasi pola transaksi berdasarkan filter yang dipilih.
**Catatan:** Nilai tarif yang ditampilkan merupakan hasil perhitungan dari kolom `payAmount` pada dataset, bukan pernyataan mengenai pendapatan resmi TransJakarta.

## 7. Struktur File Proyek
| File | Keterangan |
|---|---|
| `app.py` | Kode utama dashboard Streamlit |
| `bersihkan_data.py` | Skrip pembersihan data transaksi |
| `impor_postgres.py` | Skrip untuk memasukkan data ke PostgreSQL |
| `buat_sqlite.py` | Skrip untuk membuat database referensi SQLite |
| `uji_pipeline.py` | Skrip pengujian integrasi data menggunakan Pandas |
| `cek_data.py` | Skrip pemeriksaan data |
| `transit_reference.db` | Database SQLite untuk referensi halte dan koridor |
| `dashboard_data.csv` | Data hasil pipeline yang digunakan dashboard |
| `requirements.txt` | Daftar dependensi Python |
| `transjakarta-eda-kmeans.ipynb` | Notebook analisis data |
| `.gitignore` | Daftar file yang tidak perlu dimasukkan ke Git |

## 8. Cara Menjalankan Proyek
### Persyaratan
Pastikan Python telah terpasang di komputer dan database PostgreSQL telah dikonfigurasi sesuai kebutuhan skrip.
### Instalasi Dependensi
Buka terminal di folder proyek, kemudian jalankan:
```bash
python -m pip install -r requirements.txt
```
### Menjalankan Pipeline
Jalankan skrip sesuai urutan proses dan konfigurasi database yang digunakan:
1. `bersihkan_data.py` untuk membersihkan data.
2. `impor_postgres.py` untuk memasukkan data transaksi ke PostgreSQL.
3. `buat_sqlite.py` untuk menyiapkan database referensi SQLite.
4. `uji_pipeline.py` untuk menjalankan dan menguji integrasi data.
Pastikan konfigurasi koneksi PostgreSQL telah disiapkan sebelum menjalankan skrip yang membutuhkannya.
Setelah pipeline berhasil, siapkan hasil integrasi sebagai `dashboard_data.csv` di folder proye
### Menjalankan Dashboard
Jalankan perintah berikut:
```bash
python -m streamlit run app.py
```
Streamlit akan menampilkan alamat lokal yang dapat dibuka melalui browser.

## 9. Deployment
Dashboard telah dipublikasikan melalui Streamlit Community Cloud dan dapat diakses melalui tautan berikut:
**[Buka Dashboard Transit Insight](https://transit-insight-siti.streamlit.app/)**
Aplikasi publik membaca `dashboard_data.csv` sebagai sumber data dashboard. Pendekatan ini memungkinkan dashboard diakses tanpa membuka kredensial database lokal.

## 10. Referensi Proyek
Salah satu proyek publik yang relevan untuk dipelajari sebagai referensi arsitektur dan analisis TransJakarta adalah:
- [TransJakarta Data Vault](https://github.com/radisahussein/transjakarta_datavault)
Repositori tersebut dapat dijadikan referensi pembanding untuk mempelajari pengolahan data dan penyajian analitik terkait TransJakarta. Proyek ini memiliki implementasi teknologi yang berbeda dari Transit Insight.

## 11. Pengembang
**Nama:** Siti Hanifa
**Proyek:** Transit Insight — Dashboard Analisis Transaksi TransJakarta
