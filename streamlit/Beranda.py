import streamlit as st
import base64

st.set_page_config(
    page_title="Beranda",
    layout="wide",
)

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
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
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
        padding-bottom: 1rem;
        max-width: 1000px;
        margin: 0 auto;
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
        letter-spacing: -0.02em;
    }}

    .hero-subtitle {{
        color: white;
        font-size: 14px;
        font-weight: 500;
        opacity: 0.95;
        line-height: 1.4;
    }}

    .info-card {{
        background: rgba(255,255,255,0.92);
        backdrop-filter: blur(8px);
        padding: 20px 22px;
        border-radius: 18px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border: 1px solid #DBEAFE;
        transition: all 0.2s ease;
    }}

    .info-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    }}

    .info-title {{
        font-size: 20px;
        font-weight: 700;
        color: #587ba8;
        margin-bottom: 12px;
        border-left: 4px solid #60A5FA;
        padding-left: 14px;
    }}

    .info-text {{
        font-size: 14px;
        font-weight: 400;
        color: #334155;
        line-height: 1.6;
        text-align: justify;
    }}

    .custom-image {{
        border-radius: 18px;
        overflow: hidden;
        box-shadow: 0 6px 16px rgba(0,0,0,0.08);
        border: 2px solid #BFDBFE;
        background-color: rgba(239,246,255,0.9);
        height: 420px;
        transition: all 0.2s ease;
    }}

    .custom-image img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }}

    .custom-image:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    }}

    .row-widget.stColumns {{
        gap: 1.5rem;
    }}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HERO
# =====================================================

st.markdown("""
<div class="hero-box">
    <div class="hero-title">
        Analisis Sentimen
    </div>
    <div class="hero-subtitle">
        Wisata Air Terjun Lau Berte Menggunakan Algoritma Naive Bayes
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# CONTENT
# =====================================================

col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    try:
        with open("assets/lauberte1.jpeg", "rb") as f:
            img_data = f.read()

        st.markdown(
            f'''
            <div class="custom-image">
                <img src="data:image/jpeg;base64,{base64.b64encode(img_data).decode()}">
            </div>
            ''',
            unsafe_allow_html=True
        )
    except:
        st.markdown("""
        <div class="info-card">
            <div class="info-title">Informasi Gambar</div>
            <div class="info-text">Gambar tidak ditemukan. Pastikan file tersedia di folder assets.</div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <div class="info-title">Air Terjun Lau Berte</div>
        <div class="info-text">
            Wisata alam yang terletak di Kabupaten Langkat,
            Sumatera Utara. Wisata ini dikenal memiliki panorama alam yang indah,
            suasana yang sejuk, serta daya tarik alam yang banyak mendapat perhatian
            dan ulasan dari pengunjung di media sosial.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        <div class="info-title">Tentang Sistem</div>
        <div class="info-text">
        Sistem ini digunakan untuk menganalisis sentimen terhadap Wisata Air Terjun Lau Berte berdasarkan komentar di media sosial menggunakan algoritma Naïve Bayes. Hasil analisis diklasifikasikan ke dalam sentimen positif, negatif, dan netral secara otomatis.
        </div>
    </div>
    """, unsafe_allow_html=True)