# Analisis Sentimen Wisata Air Terjun Lau Berte

Proyek ini merupakan implementasi penelitian skripsi untuk menganalisis sentimen komentar TikTok mengenai wisata Air Terjun Lau Berte menggunakan algoritma Naïve Bayes. Proyek dikembangkan menggunakan Python dengan menerapkan proses pengumpulan data, data cleaning, preprocessing teks, pelabelan sentimen otomatis, dan Machine Learning untuk mengklasifikasikan sentimen komentar ke dalam kategori positif, negatif, dan netral.

## Latar Belakang

Media sosial menjadi salah satu sumber informasi bagi masyarakat dalam mencari dan berbagi pengalaman mengenai destinasi wisata. Komentar yang diberikan pengguna dapat menjadi gambaran mengenai persepsi dan pengalaman pengunjung terhadap suatu destinasi.

Melalui analisis sentimen, komentar tersebut dapat diolah untuk mengetahui kecenderungan sentimen masyarakat terhadap wisata Air Terjun Lau Berte.

## Tujuan

- Menganalisis sentimen komentar TikTok mengenai wisata Air Terjun Lau Berte.
- Melakukan data cleaning dan preprocessing untuk mempersiapkan data sebelum analisis.
- Menerapkan pelabelan sentimen otomatis untuk mengategorikan komentar.
- Menggunakan algoritma Naïve Bayes untuk klasifikasi sentimen.
- Menyajikan hasil analisis melalui visualisasi data dan aplikasi berbasis web.

## Teknologi dan Tools

- Python
- Pandas
- Scikit-learn
- Streamlit
- Sastrawi
- Apify
- Google Colab
- TF-IDF
- Naïve Bayes
- Matplotlib
- WordCloud

## Metodologi

Proses pengembangan proyek terdiri dari beberapa tahapan:

### 1. Pengumpulan Data

Data komentar dikumpulkan dari TikTok menggunakan Apify. Data yang diperoleh kemudian digabungkan menjadi satu dataset untuk digunakan dalam proses analisis.

### 2. Data Cleaning

Melakukan pembersihan data untuk mempersiapkan dataset sebelum proses analisis, meliputi pemeriksaan data duplikat, data kosong, serta penyesuaian format data komentar.

### 3. Preprocessing Teks

Melakukan tahapan preprocessing terhadap komentar untuk mengurangi variasi teks dan mempersiapkan data sebelum proses pelabelan dan pemodelan, meliputi:

- Case folding
- Normalisasi teks
- Tokenisasi
- Stopword removal
- Stemming

### 4. Pelabelan Sentimen Otomatis

Menerapkan pendekatan lexicon-based untuk memberikan label sentimen secara otomatis berdasarkan skor sentimen teks. Data komentar dikategorikan ke dalam tiga kelas:

- Positif
- Negatif
- Netral

Hasil pelabelan digunakan sebagai data berlabel untuk proses pemodelan Machine Learning.

### 5. Pembobotan Fitur

Menggunakan metode Term Frequency-Inverse Document Frequency (TF-IDF) untuk mengubah teks menjadi representasi numerik yang dapat digunakan dalam proses klasifikasi.

### 6. Pemodelan Machine Learning

Menerapkan algoritma Multinomial Naïve Bayes untuk membangun model klasifikasi sentimen berdasarkan data latih.

Dataset yang digunakan terdiri dari 634 data, dengan pembagian:

- Data latih: 507 data
- Data uji: 127 data

Proses pemodelan dilakukan menggunakan Google Colab.

### 7. Visualisasi Data

Menyajikan hasil analisis melalui visualisasi untuk membantu memahami distribusi dan kecenderungan sentimen komentar, meliputi:

- Pie chart untuk menampilkan distribusi sentimen.
- Word cloud untuk menampilkan kata-kata yang sering muncul dalam komentar.

### 8. Implementasi Aplikasi

Model yang telah dibangun diintegrasikan ke dalam aplikasi berbasis Streamlit untuk mendukung proses analisis sentimen dan menampilkan hasil klasifikasi secara interaktif.

## Fitur Aplikasi

- Pengumpulan komentar TikTok melalui Apify.
- Data cleaning dan preprocessing teks.
- Pelabelan sentimen otomatis menggunakan pendekatan lexicon-based.
- Prediksi sentimen menggunakan model Naïve Bayes.
- Visualisasi distribusi sentimen menggunakan pie chart.
- Visualisasi kata yang sering muncul menggunakan word cloud.
- Analisis sentimen terhadap komentar secara individual.

## Hasil Proyek

Proyek ini menghasilkan aplikasi analisis sentimen berbasis web yang dapat digunakan untuk mengolah komentar TikTok, melakukan klasifikasi sentimen, dan menampilkan hasil analisis melalui visualisasi data.

Proyek ini menjadi penerapan konsep data processing, data visualization, dan Machine Learning dalam penelitian di bidang Sistem Informasi.
