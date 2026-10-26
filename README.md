# Analisis Sentimen Wisata Air Terjun Lau Berte

Aplikasi web berbasis **Streamlit** untuk menganalisis sentimen komentar pengguna TikTok mengenai wisata Air Terjun Lau Berte di Kabupaten Langkat, Sumatera Utara. Sistem ini menggunakan algoritma **Multinomial Naive Bayes** dengan pembobotan fitur **TF-IDF** untuk mengklasifikasikan komentar ke dalam tiga kategori sentimen, yaitu positif, negatif, dan netral.

## Latar Belakang

Media sosial menjadi salah satu sumber informasi yang dapat digunakan untuk memahami opini masyarakat terhadap suatu destinasi wisata. Melalui TikTok, pengguna dapat membagikan pengalaman dan memberikan tanggapan melalui kolom komentar. Namun, banyaknya komentar membuat analisis secara manual membutuhkan waktu dan tenaga lebih.

Proyek ini merupakan implementasi penelitian skripsi yang bertujuan mengolah dan mengklasifikasikan komentar TikTok secara otomatis. Hasil analisis diharapkan dapat memberikan gambaran mengenai persepsi pengguna terhadap wisata Air Terjun Lau Berte.

**Tujuan penelitian:**
- Menerapkan algoritma Multinomial Naive Bayes untuk mengklasifikasikan sentimen komentar TikTok.
- Mengolah teks melalui tahapan preprocessing dan pembobotan fitur TF-IDF.
- Mengevaluasi kinerja model menggunakan accuracy, precision, recall, dan F1-score.
- Menampilkan hasil analisis melalui visualisasi yang mudah dipahami.

**Metodologi:** CRISP-DM (*Cross-Industry Standard Process for Data Mining*).

**Dataset:** Sebanyak 634 komentar, terdiri dari 507 data latih dan 127 data uji.

### Hasil Evaluasi

| Metrik | Hasil |
|---|---:|
| Accuracy | 80% |
| Precision | 80% |
| Recall | 82% |
| F1-Score | 79% |

Hasil evaluasi menunjukkan tingkat kesesuaian prediksi model terhadap label sentimen berbasis leksikon pada dataset yang digunakan.

## Fitur Utama

| Fitur | Deskripsi |
|---|---|
| **Scraping Komentar TikTok** | Mengambil komentar dari video TikTok menggunakan Apify API dan menyediakan hasilnya dalam format CSV. |
| **Unggah Dataset CSV** | Memproses dan menganalisis kumpulan komentar dari file CSV yang disediakan pengguna. |
| **Analisis Satu Komentar** | Menganalisis komentar secara individual, mulai dari preprocessing hingga prediksi sentimen dan nilai log posterior. |
| **Visualisasi Sentimen** | Menampilkan distribusi sentimen melalui pie chart, word cloud untuk setiap kelas, dan confusion matrix. |
| **Evaluasi Model** | Menghitung accuracy, precision, recall, dan F1-score berbobot (*weighted*). |
| **Ekspor Hasil Analisis** | Mengunduh hasil scraping, preprocessing, dan prediksi dalam format CSV. |

## Alur Kerja Sistem

Proses analisis sentimen dilakukan melalui beberapa tahapan berikut:

1. **Pengumpulan data:** komentar diperoleh melalui scraping TikTok atau unggahan dataset CSV.
2. **Text preprocessing:** membersihkan dan menyiapkan teks sebelum dianalisis.
3. **Pelabelan sentimen:** menentukan label positif, negatif, atau netral menggunakan kamus sentimen berbasis leksikon.
4. **Ekstraksi fitur:** mengubah teks menjadi representasi numerik menggunakan TF-IDF.
5. **Klasifikasi:** memprediksi kategori sentimen menggunakan Multinomial Naive Bayes.
6. **Evaluasi dan visualisasi:** menyajikan metrik evaluasi serta visualisasi hasil analisis.

### 1. Text Preprocessing

Tahap preprocessing bertujuan mengurangi variasi penulisan dan mempersiapkan teks agar dapat diproses oleh model. Tahapan yang diterapkan meliputi:

- **Case folding:** mengubah seluruh huruf menjadi huruf kecil.
- **Cleaning:** menghapus URL, mention, hashtag, angka, emoji, tanda baca, dan karakter selain huruf.
- **Normalisasi:** memperbaiki kata tidak baku, mengganti frasa tertentu, serta menyederhanakan huruf yang berulang.
- **Tokenisasi:** memisahkan teks menjadi token atau kata.
- **Stopword removal:** menghapus kata umum yang terdapat dalam daftar stopword, dengan tetap mempertahankan kata negasi.
- **Stemming:** mengubah kata menjadi bentuk dasarnya menggunakan Sastrawi, dengan pengecualian untuk kata tertentu agar bentuk katanya tidak berubah secara keliru.

Proses ini menggunakan kamus normalisasi kata dan frasa, daftar stopword, serta daftar pengecualian stemming yang disimpan dalam folder dataset.

### 2. Pelabelan Sentimen Berbasis Leksikon

Pelabelan dilakukan dengan mencocokkan kata-kata hasil preprocessing terhadap kamus sentimen berbahasa Indonesia yang berisi 1.738 kata dengan rentang skor -5 hingga +5.

Skor setiap kata dijumlahkan untuk memperoleh skor sentimen keseluruhan. Sistem juga mempertimbangkan kata negasi yang muncul tepat sebelum kata bersentimen dengan membalik skor kata tersebut.

Penentuan label dilakukan berdasarkan aturan berikut:

| Total Skor | Label |
|---|---|
| Lebih dari 0 | Positif |
| Kurang dari 0 | Negatif |
| Sama dengan 0 | Netral |

Label yang dihasilkan digunakan sebagai label acuan dalam proses evaluasi model.

### 3. Ekstraksi Fitur dan Klasifikasi

Teks hasil preprocessing diubah menjadi vektor numerik menggunakan `TfidfVectorizer` dari scikit-learn. Konfigurasi yang digunakan mencakup 739 fitur kosakata, pendekatan unigram, dan normalisasi L2.

Selanjutnya, algoritma **Multinomial Naive Bayes** digunakan untuk memprediksi kelas sentimen berdasarkan fitur tersebut. Model juga menghasilkan nilai log posterior untuk kelas negatif, netral, dan positif yang ditampilkan pada hasil analisis komentar.

### 4. Evaluasi Model

Evaluasi dilakukan dengan membandingkan hasil prediksi Multinomial Naive Bayes terhadap label acuan yang dihasilkan melalui pelabelan berbasis leksikon.

Metrik evaluasi yang digunakan meliputi:

- Accuracy
- Precision
- Recall
- F1-score

**Catatan:** karena label acuan berasal dari leksikon, hasil evaluasi menggambarkan kesesuaian prediksi model terhadap pelabelan tersebut. Hasil ini tidak secara langsung menunjukkan tingkat kesesuaian model terhadap penilaian manusia.

## Struktur Proyek

```text
SENTIMEN LAU BERTE/
├── dataset/
│   ├── dataset.csv
│   ├── data_train.csv
│   ├── data_test.csv
│   ├── sentiwords_id.txt
│   ├── kamus_normalisasi.csv
│   ├── phrase_normalisasi.csv
│   ├── stopword.txt
│   └── exception_stemming.txt
├── model/
│   ├── naive_bayes_model.pkl
│   └── tfidf_vectorizer.pkl
└── streamlit/
    ├── Beranda.py
    ├── pages/
    │   └── 1_Analisis_Sentimen.py
    └── assets/
```

**Keterangan direktori:**

- `dataset/`: menyimpan data komentar, dataset latih dan uji, kamus sentimen, serta konfigurasi preprocessing.
- `model/`: menyimpan model Naive Bayes dan TF-IDF Vectorizer yang telah dilatih.
- `streamlit/`: berisi aplikasi web, halaman analisis sentimen, dan aset visual.

Dataset penelitian terdiri dari 634 komentar, dengan pembagian 507 data latih dan 127 data uji. Distribusi awal data latih mencakup 238 komentar positif, 142 komentar negatif, dan 127 komentar netral.

## Instalasi dan Menjalankan Aplikasi

### Prasyarat

- Python 3.9 atau versi yang lebih baru.
- Git.
- API Token Apify jika ingin menggunakan fitur scraping TikTok.

### 1. Clone Repositori

```bash
git clone https://github.com/<username>/<nama-repo>.git
cd <nama-repo>
```

Ganti `<username>` dan `<nama-repo>` dengan informasi repositori GitHub yang sebenarnya.

### 2. Membuat Virtual Environment

Langkah ini bersifat opsional, tetapi disarankan untuk memisahkan dependensi proyek dari lingkungan Python lainnya.

```bash
python -m venv venv
```

Aktifkan virtual environment sesuai sistem operasi.

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 3. Menginstal Dependensi

```bash
pip install streamlit pandas matplotlib wordcloud Sastrawi apify-client scikit-learn==1.6.1
```

### 4. Menjalankan Aplikasi

Masuk ke direktori `streamlit` terlebih dahulu, kemudian jalankan aplikasi:

```bash
cd streamlit
streamlit run Beranda.py
```

Aplikasi dapat diakses melalui browser pada alamat `http://localhost:8501`.

**Hal yang perlu diperhatikan:**

- Jalankan aplikasi dari direktori `streamlit` agar pemanggilan aset gambar melalui path relatif dapat berjalan sesuai konfigurasi.
- Gunakan `scikit-learn==1.6.1` untuk menyesuaikan versi yang digunakan ketika model disimpan. Versi berbeda dapat memunculkan peringatan kompatibilitas dan berpotensi memengaruhi hasil prediksi.

## Panduan Penggunaan

### A. Analisis Satu Komentar

1. Buka halaman **Analisis Sentimen**.
2. Pilih mode **Analisis 1 Komentar**.
3. Masukkan komentar yang ingin dianalisis, misalnya `Tempatnya bagus banget, adem dan bersih.`
4. Klik tombol **Analisis Komentar**.
5. Lihat hasil preprocessing, label leksikon, prediksi Naive Bayes, dan nilai log posterior yang ditampilkan.

### B. Analisis Dataset CSV

1. Pilih mode **Upload Dataset CSV**.
2. Unggah file CSV yang memiliki kolom bernama `text`.
3. Pastikan file menggunakan pemisah titik koma (`;`).
4. Tunggu hingga proses analisis selesai.
5. Lihat hasil preprocessing, prediksi sentimen, visualisasi, metrik evaluasi, dan confusion matrix yang tersedia.
6. Unduh hasil analisis jika diperlukan.

### C. Scraping Komentar TikTok

1. Buat akun melalui [Apify Console](https://console.apify.com).
2. Salin API Token melalui menu **Settings → API & Integrations**.
3. Masukkan token dan URL video TikTok, dengan satu URL pada setiap baris.
4. Klik **Mulai Scraping** untuk mengambil komentar.
5. Hasil scraping akan diproses dan dapat diunduh dalam format CSV.

Jumlah komentar yang diambil dibatasi hingga maksimal 1.000 komentar per video sesuai konfigurasi aplikasi.

**Keamanan API Token:** token digunakan selama sesi aplikasi berjalan dan tidak disimpan secara permanen. Hindari memasukkan token ke dalam kode atau mengunggahnya ke repositori publik.

## Teknologi yang Digunakan

| Teknologi | Kegunaan |
|---|---|
| [Python](https://www.python.org/) | Bahasa pemrograman utama. |
| [Streamlit](https://streamlit.io/) | Membangun antarmuka aplikasi web interaktif. |
| [scikit-learn](https://scikit-learn.org/) | Implementasi TF-IDF, Multinomial Naive Bayes, dan metrik evaluasi. |
| [Sastrawi](https://github.com/har07/PySastrawi) | Melakukan stemming untuk teks berbahasa Indonesia. |
| [pandas](https://pandas.pydata.org/) | Membaca, mengolah, dan mengelola dataset. |
| [Matplotlib](https://matplotlib.org/) | Membuat visualisasi hasil analisis. |
| [WordCloud](https://github.com/amueller/word_cloud) | Menampilkan kata-kata yang sering muncul dalam setiap kelas sentimen. |
| [Apify Client](https://docs.apify.com/api/client/python/) | Mengintegrasikan proses pengambilan komentar TikTok. |

## Keterbatasan Sistem

Beberapa keterbatasan yang perlu diperhatikan dalam penggunaan aplikasi ini:

- Pendeteksian negasi hanya mempertimbangkan satu kata sebelum kata yang memiliki skor sentimen.
- Emoji, angka, dan tanda baca dihapus saat cleaning sehingga informasi sentimen yang terkandung di dalamnya tidak digunakan.
- Hasil klasifikasi bergantung pada kelengkapan kamus sentimen dan kamus normalisasi, terutama untuk bahasa gaul dan campuran bahasa daerah.
- Ukuran dataset latih relatif terbatas, sehingga performa pada komentar di luar konteks wisata Air Terjun Lau Berte belum tentu sama.
- Evaluasi model menggunakan label berbasis leksikon sebagai acuan, sehingga hasilnya belum menggambarkan kesesuaian dengan anotasi manual manusia.
