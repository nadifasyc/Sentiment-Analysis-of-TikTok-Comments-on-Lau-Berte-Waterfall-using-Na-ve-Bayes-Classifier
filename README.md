# 🌊 Analisis Sentimen Wisata Air Terjun Lau Berte

Aplikasi web berbasis **Streamlit** untuk menganalisis sentimen komentar media sosial (TikTok) terhadap wisata **Air Terjun Lau Berte** (Kabupaten Langkat, Sumatera Utara) menggunakan algoritma **Multinomial Naive Bayes** dengan fitur **TF-IDF**. Komentar diklasifikasikan secara otomatis ke dalam tiga kelas: **positif**, **negatif**, dan **netral**.

---

## 🎓 Latar Belakang Penelitian

Aplikasi ini adalah implementasi dari penelitian skripsi tentang analisis sentimen komentar TikTok terhadap Wisata Air Terjun Lau Berte.

Media sosial menghasilkan data opini publik dalam jumlah besar yang dapat dimanfaatkan untuk mengetahui persepsi masyarakat terhadap suatu destinasi wisata. TikTok banyak dipakai untuk berbagi pengalaman wisata, dan banyaknya komentar membuat identifikasi sentimen secara manual kurang efektif, sehingga diperlukan klasifikasi otomatis.

**Tujuan:** menerapkan algoritma Naïve Bayes untuk menganalisis sentimen komentar pengguna TikTok dan mengevaluasi kinerjanya dengan akurasi, presisi, recall, dan F1-score.

**Metode:** [CRISP-DM](https://en.wikipedia.org/wiki/Cross-industry_standard_process_for_data_mining) (Cross-Industry Standard Process for Data Mining).

**Data:** 634 komentar, dibagi menjadi 507 data latih dan 127 data uji.

**Tahapan:** text preprocessing (case folding, cleaning, normalisasi, tokenisasi, stopword removal, stemming), pelabelan sentimen berbasis leksikon, pembobotan fitur TF-IDF, lalu klasifikasi Naïve Bayes.

### Hasil

| Accuracy | Precision | Recall | F1-Score |
|:---:|:---:|:---:|:---:|
| 80% | 80% | 82% | 79% |

Naïve Bayes dinilai mampu mengklasifikasikan sentimen komentar pengguna TikTok dengan baik sekaligus memberi gambaran persepsi masyarakat terhadap Wisata Air Terjun Lau Berte.

---

## ✨ Fitur

| Fitur | Keterangan |
|---|---|
| **Scraping TikTok** | Mengambil komentar dari URL video TikTok lewat [Apify](https://apify.com) (butuh API Token), hasilnya bisa diunduh sebagai CSV. |
| **Upload Dataset CSV** | Menganalisis ribuan komentar sekaligus dari file CSV sendiri. |
| **Analisis 1 Komentar** | Mengetik satu komentar dan melihat setiap tahap preprocessing, label, serta nilai log posterior. |
| **Visualisasi** | Pie chart distribusi sentimen, word cloud per kelas, dan confusion matrix. |
| **Evaluasi** | Accuracy, Precision, Recall, dan F1-Score (weighted). |
| **Ekspor hasil** | Unduh hasil scraping, hasil preprocessing, dan hasil prediksi dalam format CSV. |

---

## 🧠 Cara Kerja Sistem

```
Komentar mentah
      │
      ▼
┌───────────────────────────── Preprocessing ─────────────────────────────┐
│ 1. Case folding        → huruf kecil                                    │
│ 2. Cleaning            → hapus URL, @mention, #hashtag, angka & simbol  │
│ 3. Normalisasi         → hapus huruf berulang, ganti frasa & kata tidak │
│                          baku (kamus normalisasi)                       │
│ 4. Tokenisasi          → pisah per kata                                 │
│ 5. Stopword removal    → buang kata umum (stopword.txt)                 │
│ 6. Stemming            → Sastrawi (kecuali kata di exception_stemming)  │
└─────────────────────────────────────────────────────────────────────────┘
      │  final_text
      ├───────────────────────────────┬─────────────────────────────────┐
      ▼                               ▼                                 │
 Pelabelan Lexicon              TF-IDF Vectorizer                       │
 (sentiwords_id.txt)                  │                                 │
      │                               ▼                                 │
 label_aktual                  Multinomial Naive Bayes                  │
      │                               │                                 │
      │                        prediksi_sentimen + log posterior        │
      └──────────────► Evaluasi (accuracy, precision, recall, F1) ◄─────┘
```

### 1. Preprocessing
Semua fungsi ada di `streamlit/pages/1_Analisis_Sentimen.py` (`preprocessing_pipeline`).

- **Cleaning** – menghapus `http...`, `@user`, `#tag`, dan semua karakter selain huruf (angka, emoji, tanda baca ikut hilang).
- **Normalisasi** – (a) huruf yang berulang ≥3 kali dipadatkan (`cantikkk` → `cantik`), (b) frasa diganti memakai `phrase_normalisasi.csv` (mis. `masya allah` → `masyaallah`), (c) kata tidak baku diganti memakai `kamus_normalisasi.csv` (mis. `udh` → `sudah`, `gk` → `ga`).
- **Stopword** – daftar 80 kata di `stopword.txt`. Kata negasi (`tidak`, `ga`, `gak`, `nggak`, `tak`) sengaja *tidak* dibuang agar bisa dipakai pada pelabelan.
- **Stemming** – stemmer **Sastrawi**; kata yang ada di `exception_stemming.txt` (mis. `pemandangan`, `pengen`) dilewati supaya tidak rusak.

### 2. Pelabelan dengan Lexicon (`label_aktual`)
Setiap kata hasil stemming dicocokkan dengan kamus `sentiwords_id.txt` (format `kata:skor`, skor −5 s.d. +5, 1.738 kata). Skor seluruh kata dijumlahkan; jika kata sebelumnya adalah **negasi**, skor kata tersebut dibalik (× −1).

| Total skor | Label |
|---|---|
| > 0 | `positif` |
| < 0 | `negatif` |
| = 0 | `netral` |

### 3. Klasifikasi Naive Bayes (`prediksi_sentimen`)
Teks akhir diubah menjadi vektor oleh `TfidfVectorizer` (739 fitur kosakata, unigram, normalisasi L2), lalu diprediksi oleh `MultinomialNB` (`alpha=1.0`). Model juga mengeluarkan **log posterior** untuk tiap kelas (`negatif`, `netral`, `positif`) yang ditampilkan pada hasil.

### 4. Evaluasi
Metrik dihitung dengan membandingkan **prediksi Naive Bayes** terhadap **label dari lexicon** (`label_aktual`), bukan terhadap label manual dari anotator.

> ⚠️ **Catatan:** karena `label_aktual` berasal dari lexicon, angka evaluasi di aplikasi menunjukkan seberapa jauh model Naive Bayes *menyerupai* pelabelan lexicon pada data yang diunggah, bukan akurasi terhadap penilaian manusia.

---

## 📁 Struktur Proyek

```
SENTIMEN LAU BERTE/
├── dataset/
│   ├── dataset.csv               # komentar mentah hasil scraping (kolom: text)
│   ├── data_train.csv            # 507 data latih (final_text, label)
│   ├── data_test.csv             # 127 data uji (kolom: text)
│   ├── sentiwords_id.txt         # lexicon sentimen (kata:skor)
│   ├── kamus_normalisasi.csv     # kata tidak baku → baku
│   ├── phrase_normalisasi.csv    # frasa tidak baku → baku
│   ├── stopword.txt              # daftar stopword
│   └── exception_stemming.txt    # kata yang tidak di-stem
├── model/
│   ├── naive_bayes_model.pkl     # MultinomialNB terlatih
│   └── tfidf_vectorizer.pkl      # TfidfVectorizer terlatih
└── streamlit/
    ├── Beranda.py                # halaman utama (entry point)
    ├── pages/
    │   └── 1_Analisis_Sentimen.py  # halaman analisis
    └── assets/                   # gambar latar & foto air terjun
```

**Pembagian data:** 634 komentar → 507 data latih + 127 data uji.

**Data latih:** 507 komentar (238 positif, 142 negatif, 127 netral). Model yang tersimpan memiliki 238 sampel per kelas, sehingga kemungkinan data latih diseimbangkan (oversampling) sebelum pelatihan.

---

## 🚀 Instalasi & Menjalankan

**Prasyarat:** Python 3.9+

```bash
# 1. Clone repositori
git clone https://github.com/<username>/<nama-repo>.git
cd <nama-repo>

# 2. (Opsional) buat virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependensi
pip install streamlit pandas matplotlib wordcloud Sastrawi apify-client scikit-learn==1.6.1

# 4. Jalankan dari dalam folder streamlit
cd streamlit
streamlit run Beranda.py
```

Aplikasi akan terbuka di `http://localhost:8501`.

> **Penting:**
> - Jalankan perintah dari folder `streamlit/`, karena gambar dibaca lewat path relatif `assets/...`.
> - Gunakan `scikit-learn==1.6.1`. File `.pkl` dilatih dengan versi tersebut; versi lain memunculkan `InconsistentVersionWarning` dan berisiko menghasilkan prediksi yang berbeda.

---

## 📖 Panduan Penggunaan

### A. Analisis 1 Komentar
1. Buka halaman **Analisis Sentimen**, pilih **Analisis 1 Komentar**.
2. Ketik komentar, contoh: `Tempatnya bagus banget, adem dan bersih.`
3. Klik **Analisis Komentar** untuk melihat tiap tahap preprocessing, label lexicon, prediksi Naive Bayes, dan log posterior.

### B. Upload Dataset CSV
1. Pilih **Upload Dataset CSV**.
2. Unggah file CSV dengan **kolom bernama `text`** dan pemisah **titik koma (`;`)**. File satu kolom seperti `dataset/dataset.csv` dapat langsung dipakai.
3. Aplikasi menampilkan hasil preprocessing, prediksi, pie chart, word cloud, metrik evaluasi, dan confusion matrix.

### C. Scraping TikTok
1. Daftar akun gratis di [console.apify.com](https://console.apify.com).
2. Salin API Token dari **Settings → API & Integrations**.
3. Tempel token dan URL video TikTok (satu URL per baris), lalu klik **Mulai Scraping**.
4. Komentar yang berhasil diambil (maks. 1000 per video) langsung dianalisis dan bisa diunduh sebagai CSV.

> API Token hanya dipakai saat sesi berjalan dan tidak disimpan. Jangan pernah meng-commit token ke repositori.

---

## 🛠️ Teknologi

- [Streamlit](https://streamlit.io) – antarmuka web
- [scikit-learn](https://scikit-learn.org) – TF-IDF, Multinomial Naive Bayes, metrik evaluasi
- [Sastrawi](https://github.com/har07/PySastrawi) – stemmer Bahasa Indonesia
- [pandas](https://pandas.pydata.org) – pengolahan data
- [Matplotlib](https://matplotlib.org) & [WordCloud](https://github.com/amueller/word_cloud) – visualisasi
- [Apify Client](https://docs.apify.com/api/client/python/) – scraping komentar TikTok

---

## ⚠️ Keterbatasan

- Negasi hanya dideteksi pada **satu kata sebelum** kata sentimen.
- Emoji, angka, dan tanda baca dibuang saat cleaning sehingga informasi sentimen dari emoji hilang.
- Kualitas hasil bergantung pada kelengkapan lexicon dan kamus normalisasi, terutama untuk bahasa gaul dan campuran bahasa daerah.
- Dataset relatif kecil (±500 data latih), sehingga performa pada komentar di luar domain wisata ini bisa menurun.

---

## 📄 Lisensi

Proyek ini dibuat untuk keperluan akademik/penelitian. Tambahkan lisensi sesuai kebutuhan (mis. MIT) sebelum dipublikasikan.
