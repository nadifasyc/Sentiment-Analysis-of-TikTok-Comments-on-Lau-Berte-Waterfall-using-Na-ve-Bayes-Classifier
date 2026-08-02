import streamlit as st
import pandas as pd
import pickle
import os
import re
import matplotlib.pyplot as plt
import base64

from apify_client import ApifyClient
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from wordcloud import WordCloud
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

# =====================================================
# KONFIGURASI HALAMAN
# =====================================================

st.set_page_config(
    page_title="Analisis Sentimen",
    layout="wide"
)

# =====================================================
# FUNGSI BACKGROUND GAMBAR
# =====================================================

def get_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

bg_image = get_base64("assets/background1.jpeg")

# =====================================================
# CSS
# =====================================================

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    * {{
        font-family: 'Inter', sans-serif;
    }}

    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpeg;base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    [data-testid="stAppViewContainer"]::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(255,255,255,0.85);
        z-index: -1;
    }}

    [data-testid="stHeader"] {{
        background-color: rgba(0,0,0,0);
    }}

    [data-testid="stSidebar"] {{
    background: linear-gradient(135deg, #587ba8,#869dc2);
    }}

       [data-testid="stSidebar"] * {{
        color: white !important;
    }}

    [data-testid="stSidebar"] .stRadio label {{
        color: white !important;
    }}

    [data-testid="stSidebarNav"] span {{
        color: white !important;
    }}

    [data-testid="stSidebarNav"] svg {{
        fill: white !important;
    }}

    [data-testid="stSidebar"] .stButton button {{
        color: #587ba8;
    }}

    .block-container {{
        padding-top: 0.8rem;
        padding-bottom: 0.8rem;
        max-width: 1000px;
        margin: 0 auto;
    }}

    h1, h2, h3 {{
        color: #587ba8;
        font-weight: 700;
    }}

    .hero-box {{
        background: linear-gradient(135deg, #587ba8, #93C5FD);
        padding: 20px 25px;
        border-radius: 18px;
        margin-bottom: 25px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(96,165,250,0.15);
    }}

    .hero-title {{
        color: white;
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 6px;
    }}

    .hero-subtitle {{
        color: white;
        font-size: 14px;
        font-weight: 500;
    }}

    .info-card {{
        background: rgba(255,255,255,0.92);
        backdrop-filter: blur(8px);
        padding: 20px 22px;
        border-radius: 18px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border: 1px solid #DBEAFE;
    }}

    .info-title {{
        font-size: 20px;
        font-weight: 700;
        color: #587ba8;
        margin-bottom: 12px;
        border-left: 4px solid #93C5FD;
        padding-left: 14px;
    }}

    .info-text {{
        font-size: 14px;
        color: #334155;
        line-height: 1.6;
        text-align: justify;
    }}

    .metric-card {{
        background: rgba(255,255,255,0.92);
        backdrop-filter: blur(8px);
        padding: 15px;
        border-radius: 16px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        text-align: center;
        border: 1px solid #DBEAFE;
    }}

    .metric-title {{
        font-size: 13px;
        color: #6B7280;
        margin-bottom: 8px;
    }}

    .metric-value {{
        font-size: 26px;
        font-weight: 700;
        color: #587ba8;
    }}

    .stButton button {{
        background: linear-gradient(135deg, #587ba8, #93C5FD);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 8px 20px;
        font-weight: 600;
        font-size: 14px;
    }}

    div[data-testid="stFileUploader"] {{
        background: rgba(255,255,255,0.92);
        backdrop-filter: blur(8px);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #DBEAFE;
    }}

    .stDataFrame {{
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #DBEAFE;
        font-size: 13px;
    }}

    [data-testid="stDownloadButton"] button {{
        background: linear-gradient(135deg, #587ba8, #93C5FD);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 8px 20px;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        font-size: 14px;
    }}

    [data-testid="stDownloadButton"] button:hover {{
        background: linear-gradient(135deg, #93C5FD, #587ba8);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(96,165,250,0.3);
        color: white !important;
    }}

        div[data-testid="stTextInput"] {{
        background-color: rgba(255,255,255,0.92);
        padding: 15px;
        border-radius: 16px;
        border: 1px solid #DBEAFE;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 8px;
    }}
    
    div[data-testid="stTextInput"] label {{
        font-weight: 600;
        margin-bottom: 6px;
        font-size: 14px;
    }}
    
    div[data-testid="stTextInput"] input {{
        background: transparent;
        border: none;
        padding: 8px 0;
        font-size: 14px;
    }}
    
    div[data-testid="stTextInput"] input:focus {{
        outline: none;
        box-shadow: none;
    }}
    
    div[data-testid="stTextArea"] {{
        background-color: rgba(255,255,255,0.92);
        padding: 15px;
        border-radius: 16px;
        border: 1px solid #DBEAFE;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 8px;
    }}
    
    div[data-testid="stTextArea"] label {{
        font-weight: 600;
        margin-bottom: 6px;
        font-size: 14px;
    }}
    
    div[data-testid="stTextArea"] textarea {{
        background: transparent;
        border: none;
        padding: 8px 0;
        font-size: 14px;
    }}
    
    div[data-testid="stTextArea"] textarea:focus {{
        outline: none;
        box-shadow: none;
    }}


    /* ============================================= */
    /* KARTU KHUSUS ANALISIS 1 KOMENTAR              */
    /* ============================================= */

    .comment-card {{
        background: rgba(255,255,255,0.92);
        backdrop-filter: blur(8px);
        padding: 18px 22px;
        border-radius: 16px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #DBEAFE;
        margin-bottom: 16px;
    }}

    .comment-card-label {{
        font-size: 12px;
        font-weight: 700;
        color: #587ba8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }}

    .comment-card-text {{
        font-size: 15px;
        color: #1E293B;
        line-height: 1.6;
        word-wrap: break-word;
    }}

    .step-card {{
        background: rgba(255,255,255,0.92);
        backdrop-filter: blur(8px);
        border-radius: 16px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #DBEAFE;
        overflow: hidden;
        margin-bottom: 20px;
    }}

    .step-row {{
        display: flex;
        align-items: flex-start;
        gap: 14px;
        padding: 14px 20px;
        border-bottom: 1px solid #EFF6FF;
    }}

    .step-row:last-child {{
        border-bottom: none;
    }}

    .step-number {{
        flex-shrink: 0;
        width: 26px;
        height: 26px;
        border-radius: 50%;
        background: linear-gradient(135deg, #587ba8, #93C5FD);
        color: white;
        font-size: 12px;
        font-weight: 700;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 2px;
    }}

    .step-content {{
        flex: 1;
        min-width: 0;
    }}

    .step-label {{
        font-size: 13px;
        font-weight: 700;
        color: #587ba8;
        margin-bottom: 4px;
    }}

    .step-value {{
        font-size: 14px;
        color: #334155;
        line-height: 1.5;
        word-wrap: break-word;
    }}

        div[data-testid="stSelectbox"] {{
        background-color: rgba(255,255,255,0.92);
        padding: 15px;
        border-radius: 16px;
        border: 1px solid #DBEAFE;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 8px;
    }}
    
    div[data-testid="stSelectbox"] label {{
        font-weight: 600;
        margin-bottom: 6px;
        font-size: 14px;
        color: #334155;
    }}
    
    div[data-testid="stSelectbox"] select {{
        background: transparent;
        border: none;
        padding: 8px 0;
        font-size: 14px;
    }}
    
    div[data-testid="stSelectbox"] select:focus {{
        outline: none;
        box-shadow: none;
    }}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="hero-box">
    <div class="hero-title">
        Sistem Analisis Sentimen
    </div>
    <div class="hero-subtitle">
        Wisata Air Terjun Lau Berte Menggunakan
        Algoritma Naive Bayes
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# SUMBER DATA
# =====================================================

pilihan_data = st.selectbox(
    "Pilih Sumber Data",
    [
        "Scraping TikTok",
        "Upload Dataset CSV",
        "Analisis 1 Komentar"
    ]
)

# =====================================================
# RESET STATE SAAT PILIHAN SUMBER DATA BERUBAH
# =====================================================

if "last_pilihan_data" not in st.session_state:
    st.session_state["last_pilihan_data"] = pilihan_data

if st.session_state["last_pilihan_data"] != pilihan_data:
    st.session_state.pop("df_scraping", None)
    st.session_state["last_pilihan_data"] = pilihan_data

df = None

# =====================================================
# SCRAPING TIKTOK
# =====================================================

if pilihan_data == "Scraping TikTok":

    st.markdown("""
    <div class="info-card">
        <div class="info-title">
            Panduan Penggunaan
        </div>
        <div class="info-text">
            1. Buka situs <a href="https://console.apify.com" target="_blank">https://console.apify.com</a> dan daftar akun gratis menggunakan email atau akun Google.<br>
            2. Setelah login, klik menu Settings di sidebar kiri. Pilih menu API & Integrations dan salin API Token.<br>
            3. Masukkan API Token yang sudah disalin ke kolom di bawah.<br>
            4. Masukkan URL video TikTok yang ingin diambil komentarnya.<br>
            5. Klik tombol Mulai Scraping dan tunggu proses pengambilan data selesai.
        </div>
    </div>
    """, unsafe_allow_html=True)

    api_token = st.text_input(
        "API Token Apify",
        type="password"
    )

    tiktok_url = st.text_area(
        "URL Video TikTok",
        height=100
    )

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        mulai_scraping = st.button(
            "Mulai Scraping",
            use_container_width=True
        )

    if mulai_scraping:

        if api_token == "" or tiktok_url == "":
            st.warning("API Token dan URL wajib diisi.")
            st.stop()

        with st.spinner("Sedang mengambil komentar..."):

            client = ApifyClient(api_token)

            urls = [
                url.strip()
                for url in tiktok_url.split("\n")
                if url.strip()
            ]

            run_input = {
                "commentsPerPost":1000,
                "excludePinnedPosts":False,
                "maxRepliesPerComment":10,
                "postURLs":urls,
                "resultsPerPage":100
            }

            run = client.actor(
                "BDec00yAmCm1QbMEI"
            ).call(
                run_input=run_input
            )

            items = list(
                client.dataset(
                    run.default_dataset_id
                ).iterate_items()
            )

            comments = []

            for item in items:

                if "text" in item:

                    comments.append(
                        item["text"]
                    )

            df_scraping = pd.DataFrame({

                "text":comments

            })

        # simpan hasil scraping ke session_state supaya tidak
        # hilang saat halaman rerun (misalnya saat tombol
        # download di bawah ini diklik)
        st.session_state["df_scraping"] = df_scraping

    if "df_scraping" in st.session_state:
        df = st.session_state["df_scraping"]


# =====================================================
# UPLOAD CSV
# =====================================================

if pilihan_data == "Upload Dataset CSV":

    uploaded_file = st.file_uploader(
        "Pilih file CSV",
        type=["csv"]
    )

    if uploaded_file is not None:

        df = pd.read_csv(
            uploaded_file,
            encoding="utf-8",
            sep=";",
            engine="python",
            on_bad_lines="skip"
        )            

# =====================================================
# ANALISIS 1 KOMENTAR
# =====================================================

if pilihan_data == "Analisis 1 Komentar":

    st.markdown("""
    <div class="info-card">
        <div class="info-title">
            Analisis Satu Komentar
        </div>
        <div class="info-text">
            Masukkan satu komentar untuk mengetahui hasil analisis sentimen.
        </div>
    </div>
    """, unsafe_allow_html=True)

    komentar = st.text_area(
        "Masukkan Komentar",
        placeholder="Contoh: Tempatnya bagus banget, adem dan bersih.",
        height=150
    )
    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        analisis = st.button(
            "Analisis Komentar",
            use_container_width=True
        )

    if analisis:

        if komentar.strip() == "":

            st.warning("Komentar tidak boleh kosong.")

            st.stop()

        # dataframe yang nanti dipakai pipeline preprocessing
        df = pd.DataFrame({

            "text":[komentar]

        })    

# =====================================================
# BASE DIRECTORY
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

# =====================================================
# LOAD MODEL
# =====================================================

with open(
    os.path.join(BASE_DIR, 'model', 'naive_bayes_model.pkl'),
    'rb'
) as file:
    model = pickle.load(file)

# =====================================================
# LOAD TF-IDF
# =====================================================

with open(
    os.path.join(BASE_DIR, 'model', 'tfidf_vectorizer.pkl'),
    'rb'
) as file:
    tfidf = pickle.load(file)

# =====================================================
# LOAD NORMALIZATION
# =====================================================

normalization_df = pd.read_csv(
    os.path.join(BASE_DIR, 'dataset', 'kamus_normalisasi.csv'),
    encoding='utf-8'
)

normalization_dict = dict(
    zip(
        normalization_df.iloc[:,0].str.lower(),
        normalization_df.iloc[:,1].str.lower()
    )
)

phrase_df = pd.read_csv(
    os.path.join(BASE_DIR, "dataset", "phrase_normalisasi.csv"),
    encoding="utf-8"
)

phrase_dict = dict(
    zip(
        phrase_df.iloc[:, 0].str.lower(),
        phrase_df.iloc[:, 1].str.lower()
    )
)

# =====================================================
# STOPWORD
# =====================================================

try:
    stopword_df = pd.read_csv(
        os.path.join(
            BASE_DIR,
            'dataset',
            'stopword.txt'
        ),
        header=None
    )

    stopwords = (
        stopword_df[0]
        .astype(str)
        .str.strip()
        .str.lower()
        .tolist()
    )

except:
    stopwords = []

# =====================================================
# STEMMER
# =====================================================

stem_factory = StemmerFactory()
stemmer = stem_factory.create_stemmer()

try:
    exception_df = pd.read_csv(
        os.path.join(
            BASE_DIR,
            "dataset",
            "exception_stemming.txt"
        ),
        header=None
    )

    exception_words = (
        exception_df[0]
        .astype(str)
        .str.strip()
        .str.lower()
        .tolist()
    )

except:
    exception_words = []

# =====================================================
# LOAD LEXICON
# =====================================================

lexicon = {}

with open(
    os.path.join(BASE_DIR, 'dataset', 'sentiwords_id.txt'),
    'r',
    encoding='utf-8'
) as file:
    for line in file:
        data = line.strip().split(':')
        if len(data) == 2:
            word = data[0]
            score = int(data[1])
            lexicon[word] = score
            negation_words = [
                            'tidak',
                            'ga',
                            'gak',
                            'nggak',
                            'tak',
                        ]

# =====================================================
# FUNGSI PREPROCESSING
# =====================================================

def cleaning_text(text):
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#\w+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.strip()
    return text

def remove_repeated_char(text):
    words = text.split()
    cleaned_words = []
    for word in words:
        word = re.sub(r'(.)\1{2,}', r'\1', word)
        cleaned_words.append(word)
    return ' '.join(cleaned_words)

def tokenizing(text):
    return text.split()

def normalize_text(text):
    text = remove_repeated_char(text)
    for key, value in phrase_dict.items():
        text = text.replace(key, value)
    words = text.split()
    normalized_words = [
        normalization_dict[word] if word in normalization_dict else word
        for word in words
    ]
    return ' '.join(normalized_words)

def remove_stopwords(text):
    words = text.split()
    filtered_words = [word for word in words if word not in stopwords]
    return ' '.join(filtered_words)

def stemming_text(text):
    words = text.split()
    stemmed_words = []
    for word in words:
        if word in exception_words:
            stemmed_words.append(word)
        else:
            stemmed_words.append(stemmer.stem(word))
    return ' '.join(stemmed_words)

def sentiment_score(text):

    words = text.split()
    score = 0

    for i, word in enumerate(words):

        if word in lexicon:

            current_score = lexicon[word]

            # cek apakah kata sebelumnya adalah negasi
            if i > 0 and words[i - 1] in negation_words:
                current_score = current_score * -1

            score += current_score

    return score

def sentiment_label(score):
    if score > 0:
        return 'positif'
    elif score < 0:
        return 'negatif'
    else:
        return 'netral'

def preprocessing_pipeline(text):
    case_folding = str(text).lower()
    cleaned = cleaning_text(case_folding)
    normalized = normalize_text(cleaned)
    tokens = tokenizing(normalized)
    tokenized = ' | '.join(tokens)
    stopword_removed = remove_stopwords(normalized)
    stopword_display = " | ".join(stopword_removed.split())
    stemmed = stemming_text(stopword_removed)
    
    return {
        'case_folding': case_folding,
        'cleaning': cleaned,
        'normalization': normalized,
        'tokenizing': tokenized,
        'stopword': stopword_display,
        'stemming': stemmed,
        'final_text': stemmed
    }

# =====================================================
# PROSES ANALISIS
# =====================================================

if df is not None:
    
    try:
        if "text" not in df.columns:

            st.error(
                "Dataset harus memiliki kolom text."
            )

            st.stop()

        # ===========================
        # Pembersihan Dataset
        # ===========================

        df = df.dropna(subset=["text"])

        df["text"] = df["text"].astype(str).str.strip()

        df = df[df["text"] != ""]

        df = df.drop_duplicates(subset=["text"]).reset_index(drop=True)    

        is_single = (pilihan_data == "Analisis 1 Komentar")

        # =============================================
        # DATASET AWAL
        # =============================================

        if is_single:

            st.markdown(f"""
            <div class="comment-card">
                <div class="comment-card-label">Teks Komentar</div>
                <div class="comment-card-text">{df['text'].iloc[0]}</div>
            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown("""
            <div class="info-card">
                <div class="info-title">Dataset Awal</div>
                <div class="info-text">
                    Menampilkan komentar dari dataset.
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.dataframe(
                df[['text']],
                use_container_width=True,
                height=400
            )

            if pilihan_data == "Scraping TikTok":

                csv_scraping = df[['text']].to_csv(index=False).encode('utf-8')

                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.download_button(
                        label="Download Hasil Scraping",
                        data=csv_scraping,
                        file_name='hasil_scraping_tiktok.csv',
                        mime='text/csv',
                        use_container_width=True
                    )

        # =============================================
        # PREPROCESSING
        # =============================================

        with st.spinner("Sedang memproses data..."):
            preprocessing_results = df['text'].apply(preprocessing_pipeline)

            df['case_folding'] = preprocessing_results.apply(lambda x: x['case_folding'])
            df['cleaning'] = preprocessing_results.apply(lambda x: x['cleaning'])
            df['normalization'] = preprocessing_results.apply(lambda x: x['normalization'])
            df['tokenizing'] = preprocessing_results.apply(lambda x: x['tokenizing'])
            df['stopword'] = preprocessing_results.apply(lambda x: x['stopword'])
            df['stemming'] = preprocessing_results.apply(lambda x: x['stemming'])
            df['final_text'] = preprocessing_results.apply(lambda x: x['final_text'])

            # LABEL AKTUAL
            df['final_score'] = df['final_text'].apply(sentiment_score)
            df['label_aktual'] = df['final_score'].apply(sentiment_label)

            # TF-IDF DAN PREDIKSI
            X_tfidf = tfidf.transform(df['final_text'])
            predictions = model.predict(X_tfidf)
            log_prob = model.predict_log_proba(X_tfidf)
            df["Log Posterior Positif"] = log_prob[:, 2]
            df["Log Posterior Negatif"] = log_prob[:, 0]
            df["Log Posterior Netral"] = log_prob[:, 1]
            df["prediksi_sentimen"] = predictions

            # EVALUASI
            accuracy = accuracy_score(df['label_aktual'], df['prediksi_sentimen'])
            precision = precision_score(df['label_aktual'], df['prediksi_sentimen'], average='weighted', zero_division=0)
            recall = recall_score(df['label_aktual'], df['prediksi_sentimen'], average='weighted', zero_division=0)
            f1 = f1_score(df['label_aktual'], df['prediksi_sentimen'], average='weighted', zero_division=0)

        # =============================================
        # HASIL PREPROCESSING
        # =============================================

        st.markdown("""
        <div class="info-card">
            <div class="info-title">Hasil Preprocessing</div>
            <div class="info-text">
                Case Folding, Cleaning, Normalisasi, Tokenisasi, Stopword Removal, Stemming.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if is_single:

            steps = [
                ("Case Folding", df['case_folding'].iloc[0]),
                ("Cleaning", df['cleaning'].iloc[0]),
                ("Normalisasi", df['normalization'].iloc[0]),
                ("Tokenisasi", df['tokenizing'].iloc[0]),
                ("Stopword Removal", df['stopword'].iloc[0]),
                ("Stemming", df['stemming'].iloc[0]),
            ]

            rows_html = ""

            for i, (label, value) in enumerate(steps, start=1):

                value_display = value if str(value).strip() != "" else "-"

                rows_html += (
                    '<div class="step-row">'
                    f'<div class="step-number">{i}</div>'
                    '<div class="step-content">'
                    f'<div class="step-label">{label}</div>'
                    f'<div class="step-value">{value_display}</div>'
                    '</div>'
                    '</div>'
                )

            st.markdown(
                f'<div class="step-card">{rows_html}</div>',
                unsafe_allow_html=True
            )

        else:

            st.dataframe(
                df[['case_folding','cleaning','normalization','tokenizing','stopword','stemming']],
                use_container_width=True,
                height=400
            )

            preprocessing_csv = df[
                [
                    'text',
                    'case_folding',
                    'cleaning',
                    'normalization',
                    'tokenizing',
                    'stopword',
                    'stemming'
                ]
            ].to_csv(index=False).encode('utf-8')

            col1, col2, col3 = st.columns([1,2,1])

            with col2:

                st.download_button(
                    label="Download Hasil Preprocessing",
                    data=preprocessing_csv,
                    file_name="hasil_preprocessing.csv",
                    mime="text/csv",
                    use_container_width=True
            )

        # =============================================
        # HASIL PREDIKSI
        # =============================================

        st.markdown("""
        <div class="info-card">
            <div class="info-title">Hasil Prediksi</div>
            <div class="info-text">
                Menggunakan Algoritma Naive Bayes.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # =============================================
        # JIKA ANALISIS 1 KOMENTAR
        # =============================================

        if pilihan_data == "Analisis 1 Komentar":

            colors = {
                "positif": ("#DCFCE7", "#16A34A"),
                "negatif": ("#FEE2E2", "#DC2626"),
                "netral":  ("#FEF9C3", "#CA8A04"),
            }

            col1, col2 = st.columns(2)

            with col1:
                label_aktual = df["label_aktual"].iloc[0]
                bg, text_color = colors[label_aktual]

                st.markdown(f"""
                <div class="comment-card" style="
                    text-align:center;
                    background:{bg};
                    border-radius:16px;
                    box-shadow:0 2px 6px rgba(0,0,0,0.1);
                ">
                    <div class="comment-card-label" style="color:#587ba8;">
                        Label Aktual (Lexicon)
                    </div>
                    <div style="font-size:20px; font-weight:700; color:{text_color}; margin-top:6px;">
                        {label_aktual.capitalize()}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                prediksi = df["prediksi_sentimen"].iloc[0]
                bg, text_color = colors[prediksi]

                st.markdown(f"""
                <div class="comment-card" style="
                    text-align:center;
                    background:{bg};
                    border-radius:16px;
                    box-shadow:0 2px 6px rgba(0,0,0,0.1);
                ">
                    <div class="comment-card-label" style="color:#587ba8;">
                        Prediksi Naive Bayes
                    </div>
                    <div style="font-size:20px; font-weight:700; color:{text_color}; margin-top:6px;">
                        {prediksi.capitalize()}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("""
            <div class="info-card">
                <div class="info-title">Log Posterior</div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Positif</div>
                    <div class="metric-value">{df['Log Posterior Positif'].iloc[0]:.4f}</div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Negatif</div>
                    <div class="metric-value">{df['Log Posterior Negatif'].iloc[0]:.4f}</div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Netral</div>
                    <div class="metric-value">{df['Log Posterior Netral'].iloc[0]:.4f}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

        # =============================================
        # JIKA DATASET
        # =============================================

        else:

            st.dataframe(
                df[
                    [
                        'final_text',
                        'label_aktual',
                        'prediksi_sentimen',
                        'Log Posterior Positif',
                        'Log Posterior Negatif',
                        'Log Posterior Netral'
                    ]
                ],
                use_container_width=True,
                height=400
            )

            prediction_csv = df[
                [
                    'text',
                    'final_text',
                    'label_aktual',
                    'prediksi_sentimen',
                    'Log Posterior Positif',
                    'Log Posterior Negatif',
                    'Log Posterior Netral'
                ]
            ].to_csv(index=False).encode("utf-8")

            col1, col2, col3 = st.columns([1,2,1])

            with col2:

                st.download_button(
                    label="Download Hasil Prediksi",
                    data=prediction_csv,
                    file_name="hasil_prediksi.csv",
                    mime="text/csv",
                    use_container_width=True
                )

        if pilihan_data != "Analisis 1 Komentar":
                # =============================================
                # DISTRIBUSI SENTIMEN
                # =============================================

                st.markdown("""
                <div class="info-card">
                    <div class="info-title">Pie Chart</div>
                    <div class="info-text">
                        Visualisasi distribusi sentimen berdasarkan hasil prediksi klasifikasi.
                    </div>
                </div>
                """, unsafe_allow_html=True)

                col1, col2, col3 = st.columns([1, 2, 1])

                # PIE CHART
                with col2:
                    sentiment_counts = df['prediksi_sentimen'].value_counts()
                    fig, ax = plt.subplots(figsize=(5,5))
                    colors = ['#93C5FD', '#EF4444', '#F59E0B']
                    ax.pie(
                        sentiment_counts,
                        labels=sentiment_counts.index,
                        autopct='%1.1f%%',
                        colors=colors
                    )
                    st.pyplot(fig)

                # =============================================
                # Word Cloud
                # =============================================

                st.markdown("""
                <div class="info-card">
                    <div class="info-title">Word Cloud</div>
                    <div class="info-text">
                        Visualisasi kata yang paling sering muncul berdasarkan hasil prediksi sentimen.
                    </div>
                </div>
                """, unsafe_allow_html=True)

                col1, col2, col3 = st.columns(3)

                # =====================================================
                # WORD CLOUD POSITIF
                # =====================================================

                with col1:

                    st.markdown("""
                    <div style="
                        background: rgba(255,255,255,0.92);
                        color: #587ba8;
                        text-align: center;
                        font-weight: 700;
                        font-size: 18px;
                        border-radius: 10px;
                        margin-bottom: 8px;
                        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                    ">
                        Positif
                    </div>
                    """, unsafe_allow_html=True)

                    text_positive = " ".join(
                        df[df["prediksi_sentimen"] == "positif"]["final_text"].astype(str)
                    )

                    if text_positive.strip():

                        wordcloud = WordCloud(
                            width=800,
                            height=800,
                            background_color="white",
                            colormap="Greens"
                        ).generate(text_positive)

                        fig, ax = plt.subplots(figsize=(4, 4))
                        ax.imshow(wordcloud)
                        ax.axis("off")
                        st.pyplot(fig)

                    else:
                        st.info("Tidak ada data positif.")

                # =====================================================
                # WORD CLOUD NEGATIF
                # =====================================================

                with col2:

                    st.markdown("""
                    <div style="
                        background: rgba(255,255,255,0.92);
                        color: #587ba8;
                        text-align: center;
                        font-weight: 700;
                        font-size: 18px;
                        border-radius: 10px;
                        margin-bottom: 8px;
                        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                    ">
                        Negatif
                    </div>
                    """, unsafe_allow_html=True)

                    text_negative = " ".join(
                        df[df["prediksi_sentimen"] == "negatif"]["final_text"].astype(str)
                    )

                    if text_negative.strip():

                        wordcloud = WordCloud(
                            width=800,
                            height=800,
                            background_color="white",
                            colormap="Reds"
                        ).generate(text_negative)

                        fig, ax = plt.subplots(figsize=(4, 4))
                        ax.imshow(wordcloud)
                        ax.axis("off")
                        st.pyplot(fig)

                    else:
                        st.info("Tidak ada data negatif.")

                # =====================================================
                # WORD CLOUD NETRAL
                # =====================================================

                with col3:

                    st.markdown("""
                    <div style="
                        background: rgba(255,255,255,0.92);
                        color: #587ba8;
                        text-align: center;
                        font-weight: 700;
                        font-size: 18px;
                        border-radius: 10px;
                        margin-bottom: 8px;
                        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                    ">
                        Netral
                    </div>
                    """, unsafe_allow_html=True)

                    text_netral = " ".join(
                        df[df["prediksi_sentimen"] == "netral"]["final_text"].astype(str)
                    )

                    if text_netral.strip():

                        wordcloud = WordCloud(
                            width=800,
                            height=800,
                            background_color="white",
                            colormap="Blues"
                        ).generate(text_netral)

                        fig, ax = plt.subplots(figsize=(4, 4))
                        ax.imshow(wordcloud)
                        ax.axis("off")
                        st.pyplot(fig)

                    else:
                        st.info("Tidak ada data netral.")

                # =============================================
                # METRIK EVALUASI
                # =============================================

                st.markdown("""
                <div class="info-card">
                    <div class="info-title">Evaluasi Model</div>
                    <div class="info-text">
                        Hasil evaluasi performa model menggunakan data uji.
                    </div>
                </div>
                """, unsafe_allow_html=True)

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Accuracy</div>
                        <div class="metric-value">{accuracy:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Precision</div>
                        <div class="metric-value">{precision:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Recall</div>
                        <div class="metric-value">{recall:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col4:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">F1-Score</div>
                        <div class="metric-value">{f1:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)

                # =============================================
                # CONFUSION MATRIX
                # =============================================

                st.markdown("""
                <div class="info-card">
                    <div class="info-title">Confusion Matrix</div>
                    <div class="info-text">
                        Confusion Matrix untuk evaluasi model.
                    </div>
                </div>
                """, unsafe_allow_html=True)

                labels = ['negatif', 'netral', 'positif']
                cm = confusion_matrix(df['label_aktual'], df['prediksi_sentimen'], labels=labels)

                fig_cm, ax_cm = plt.subplots(figsize=(3.5,3))
                im = ax_cm.imshow(cm, cmap='Blues')
                ax_cm.set_xticks(range(len(labels)))
                ax_cm.set_yticks(range(len(labels)))
                ax_cm.set_xticklabels(labels)
                ax_cm.set_yticklabels(labels)
                ax_cm.set_xlabel('Prediksi')
                ax_cm.set_ylabel('Aktual')

                for i in range(len(cm)):
                    for j in range(len(cm[0])):
                        ax_cm.text(j, i, cm[i, j], ha='center', va='center')

                plt.tight_layout()

                col1, col2, col3 = st.columns([1, 2, 1])

                with col2:
                    st.pyplot(fig_cm)

    except Exception as e:
        st.error(f"Terjadi kesalahan: {str(e)}")