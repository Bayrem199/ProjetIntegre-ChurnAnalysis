import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import base64
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.model import load_clients_a_risque

st.set_page_config(
    page_title="Clients à Risque — ChurnGuard",
    page_icon="⚠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── HELPERS ────────────────────────────────────────────
def img_to_b64(path):
    p = Path(__file__).resolve().parents[1] / path
    if p.exists():
        return base64.b64encode(p.read_bytes()).decode()
    return None

def img_tag(path, style=""):
    b64 = img_to_b64(path)
    if b64:
        ext = Path(path).suffix.lstrip(".")
        return f'<img src="data:image/{ext};base64,{b64}" style="{style}">'
    return ""

# ─── TRANSLATIONS ─────────────────────────────────────
T = {
    "fr": {
        "brand": "ChurnGuard", "brand_sub": "Intelligence de Rétention Client",
        "nav_home": "Tableau de Bord", "nav_pred": "Prédiction", "nav_risk": "Clients à Risque",
        "model_label": "Modèle Actif", "powered": "Propulsé par Machine Learning",
        "version": "Version 1.0 · 2025", "theme_dark": "Sombre", "theme_light": "Clair",
        "lang_label": "Langue", "theme_label": "Apparence",
        "page_title": "Clients Actifs à Risque",
        "page_sub": "Portefeuille des comptes identifiés à probabilité de churn élevée",
        "kpi_total": "Clients à Risque",
        "kpi_avg": "Probabilité Moyenne",
        "kpi_critical": "Risque Critique (>90%)",
        "kpi_high": "Risque Élevé (>75%)",
        "filter_nature": "Nature Client",
        "filter_kyc": "Score KYC",
        "filter_seuil": "Seuil de probabilité minimum",
        "table_title": "clients identifiés",
        "col_client": "N° Client",
        "col_account": "N° Compte",
        "col_nature": "Nature",
        "col_kyc": "KYC",
        "col_balance": "Solde (TND)",
        "col_proba": "Prob. Churn",
        "col_risque": "Risque",
        "chart1": "Probabilité moy. par Nature Client",
        "chart2": "Probabilité moy. par Score KYC",
        "chart3": "Distribution des Probabilités",
        "chart4": "Risque par Segment",
        "export": "📥 Télécharger CSV complet",
        "export_filtered": "📥 Télécharger sélection",
        "no_data": "Aucun client trouvé avec ces critères.",
        "loading": "Chargement des données...",
        "error_no_file": "Fichier clients_a_risque.csv introuvable.",
        "footer": "© 2025 ESPRIT School of Business · Master 1 Business Analytics · ChurnGuard",
        "print": "🖨️ Imprimer",
        "all": "Tous",
        "search": "Rechercher un client (N° ou compte)...",
    },
    "en": {
        "brand": "ChurnGuard", "brand_sub": "Client Retention Intelligence",
        "nav_home": "Dashboard", "nav_pred": "Prediction", "nav_risk": "At-Risk Clients",
        "model_label": "Active Model", "powered": "Powered by Machine Learning",
        "version": "Version 1.0 · 2025", "theme_dark": "Dark", "theme_light": "Light",
        "lang_label": "Language", "theme_label": "Appearance",
        "page_title": "At-Risk Active Clients",
        "page_sub": "Portfolio of accounts identified with high churn probability",
        "kpi_total": "At-Risk Clients",
        "kpi_avg": "Average Probability",
        "kpi_critical": "Critical Risk (>90%)",
        "kpi_high": "High Risk (>75%)",
        "filter_nature": "Client Type",
        "filter_kyc": "KYC Score",
        "filter_seuil": "Minimum probability threshold",
        "table_title": "clients identified",
        "col_client": "Client No.",
        "col_account": "Account No.",
        "col_nature": "Type",
        "col_kyc": "KYC",
        "col_balance": "Balance (TND)",
        "col_proba": "Churn Prob.",
        "col_risque": "Risk",
        "chart1": "Avg. Probability by Client Type",
        "chart2": "Avg. Probability by KYC Score",
        "chart3": "Probability Distribution",
        "chart4": "Risk by Segment",
        "export": "📥 Download full CSV",
        "export_filtered": "📥 Download selection",
        "no_data": "No clients found with these criteria.",
        "loading": "Loading data...",
        "error_no_file": "File clients_a_risque.csv not found.",
        "footer": "© 2025 ESPRIT School of Business · Master 1 Business Analytics · ChurnGuard",
        "print": "🖨️ Print",
        "all": "All",
        "search": "Search a client (No. or account)...",
    },
    "ar": {
        "brand": "ChurnGuard", "brand_sub": "منصة الاحتفاظ بالعملاء",
        "nav_home": "لوحة التحكم", "nav_pred": "التنبؤ", "nav_risk": "العملاء المعرضون للخطر",
        "model_label": "النموذج النشط", "powered": "مدعوم بالذكاء الاصطناعي",
        "version": "الإصدار 1.0 · 2025", "theme_dark": "داكن", "theme_light": "فاتح",
        "lang_label": "اللغة", "theme_label": "المظهر",
        "page_title": "العملاء النشطون المعرضون للخطر",
        "page_sub": "محفظة الحسابات ذات احتمالية مغادرة عالية",
        "kpi_total": "عملاء معرضون للخطر",
        "kpi_avg": "متوسط الاحتمالية",
        "kpi_critical": "خطر حرج (>90%)",
        "kpi_high": "خطر مرتفع (>75%)",
        "filter_nature": "نوع العميل",
        "filter_kyc": "تقييم KYC",
        "filter_seuil": "الحد الأدنى للاحتمالية",
        "table_title": "عميل محدد",
        "col_client": "رقم العميل",
        "col_account": "رقم الحساب",
        "col_nature": "النوع",
        "col_kyc": "KYC",
        "col_balance": "الرصيد",
        "col_proba": "احتمالية المغادرة",
        "col_risque": "الخطر",
        "chart1": "متوسط الاحتمالية حسب النوع",
        "chart2": "متوسط الاحتمالية حسب KYC",
        "chart3": "توزيع الاحتمالية",
        "chart4": "الخطر حسب الفئة",
        "export": "📥 تحميل CSV الكامل",
        "export_filtered": "📥 تحميل الاختيار",
        "no_data": "لا يوجد عملاء بهذه المعايير.",
        "loading": "جارٍ تحميل البيانات...",
        "error_no_file": "ملف clients_a_risque.csv غير موجود.",
        "footer": "© 2025 ESPRIT School of Business · ChurnGuard",
        "print": "🖨️ طباعة",
        "all": "الكل",
        "search": "البحث عن عميل...",
    },
}

# ─── SESSION STATE ────────────────────────────────────
if "lang"  not in st.session_state: st.session_state.lang  = "fr"
if "theme" not in st.session_state: st.session_state.theme = "dark"

lang  = st.session_state.lang
t     = T[lang]
dark  = st.session_state.theme == "dark"
rtl   = lang == "ar"
dir_  = "rtl" if rtl else "ltr"

# ─── THEME TOKENS ─────────────────────────────────────
if dark:
    BG       = "#020817"
    CARD     = "rgba(255,255,255,0.03)"
    CARD_BOR = "rgba(255,255,255,0.08)"
    TXT      = "#f1f5f9"
    TXT2     = "rgba(241,245,249,0.5)"
    SIDEBAR  = "linear-gradient(180deg,#061953 0%,#040f33 100%)"
    INP_BG   = "rgba(255,255,255,0.05)"
    INP_BOR  = "rgba(255,255,255,0.12)"
    PLOT_BG  = "rgba(0,0,0,0)"
    PLOT_PAPER = "rgba(0,0,0,0)"
    GRID_C   = "rgba(255,255,255,0.05)"
    TICK_C   = "rgba(255,255,255,0.4)"
else:
    BG       = "#f8faff"
    CARD     = "rgba(255,255,255,0.95)"
    CARD_BOR = "rgba(13,43,78,0.12)"
    TXT      = "#0D2B4E"
    TXT2     = "rgba(13,43,78,0.55)"
    SIDEBAR  = "linear-gradient(180deg,#0D2B4E 0%,#1a4a7a 100%)"
    INP_BG   = "rgba(13,43,78,0.04)"
    INP_BOR  = "rgba(13,43,78,0.15)"
    PLOT_BG  = "rgba(0,0,0,0)"
    PLOT_PAPER = "rgba(0,0,0,0)"
    GRID_C   = "rgba(13,43,78,0.06)"
    TICK_C   = "rgba(13,43,78,0.5)"

GOLD  = "#C9982A"
GREEN = "#10b981"
RED   = "#ef4444"
AMBER = "#f59e0b"
ORANGE = "#f97316"

logo_b64 = img_to_b64("assets/logo.png")
logo_html = (
    f'<img src="data:image/png;base64,{logo_b64}" '
    f'style="width:60px;height:60px;border-radius:16px;object-fit:cover;">'
    if logo_b64 else
    '<div style="width:60px;height:60px;background:linear-gradient(135deg,'
    'rgba(201,152,42,0.3),rgba(201,152,42,0.1));border:2px solid rgba(201,152,42,0.5);'
    'border-radius:16px;display:flex;align-items:center;justify-content:center;'
    'font-size:1.8rem;">🏦</div>'
)

# ─── GLOBAL CSS ───────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Cairo:wght@400;600;700;800&display=swap');

*, *::before, *::after {{
    font-family: {'Cairo' if rtl else 'Inter'}, sans-serif;
    box-sizing: border-box;
}}
#MainMenu, header[data-testid="stHeader"], footer, .stDeployButton {{
    visibility: hidden !important; display: none !important;
}}
.stApp {{ background: {BG} !important; direction: {dir_}; }}

::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: {BG}; }}
::-webkit-scrollbar-thumb {{ background: {GOLD}44; border-radius: 10px; }}
::-webkit-scrollbar-thumb:hover {{ background: {GOLD}; }}

/* ── SIDEBAR ─────────────────────────────────── */
section[data-testid="stSidebar"] {{
    background: {SIDEBAR} !important;
    border-right: 1px solid {GOLD}30 !important;
    box-shadow: 6px 0 40px rgba(0,0,0,0.4) !important;
}}
section[data-testid="stSidebar"] > div:first-child {{ padding: 0 !important; }}
section[data-testid="stSidebar"] * {{ color: white !important; }}
section[data-testid="stSidebar"] a[data-testid="stPageLink"] {{
    display: flex !important; align-items: center !important; gap: 10px !important;
    padding: 11px 14px !important; border-radius: 12px !important; margin-bottom: 4px !important;
    font-size: 0.88rem !important; font-weight: 500 !important;
    color: rgba(255,255,255,0.65) !important; border: 1px solid transparent !important;
    background: transparent !important; transition: all 0.25s ease !important; text-decoration: none !important;
}}
section[data-testid="stSidebar"] a[data-testid="stPageLink"]:hover {{
    background: rgba(255,255,255,0.07) !important; color: white !important;
    border-color: rgba(255,255,255,0.1) !important; padding-left: 18px !important;
}}
section[data-testid="stSidebar"] a[data-testid="stPageLink-active"] {{
    background: linear-gradient(135deg,{GOLD}20,{GOLD}08) !important;
    color: {GOLD} !important; border-color: {GOLD}40 !important; font-weight: 600 !important;
}}
section[data-testid="stSidebar"] .stButton button {{
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: rgba(255,255,255,0.7) !important; border-radius: 10px !important;
    font-size: 0.78rem !important; padding: 6px 4px !important; transition: all 0.2s ease !important;
}}
section[data-testid="stSidebar"] .stButton button:hover {{
    background: rgba(255,255,255,0.12) !important; color: white !important;
}}
section[data-testid="stSidebar"] button[kind="primary"] {{
    background: linear-gradient(135deg,{GOLD},{GOLD}aa) !important;
    border-color: {GOLD} !important; color: white !important; font-weight: 700 !important;
}}
hr {{ border-color: rgba(255,255,255,0.07) !important; margin: 14px 0 !important; }}

/* ── PAGE HEADER ─────────────────────────────── */
.page-header {{
    background: linear-gradient(135deg,{CARD},transparent);
    border: 1px solid {CARD_BOR}; border-radius: 20px;
    padding: 32px 40px; margin-bottom: 28px;
    display: flex; align-items: center; gap: 24px;
    animation: fadeSlide 0.6s ease;
}}
@keyframes fadeSlide {{
    from {{ opacity:0; transform:translateY(-14px); }}
    to   {{ opacity:1; transform:translateY(0); }}
}}
.ph-icon {{
    width: 64px; height: 64px; border-radius: 18px; flex-shrink: 0;
    background: linear-gradient(135deg,{RED}25,{RED}08);
    border: 1px solid {RED}40;
    display: flex; align-items: center; justify-content: center; font-size: 2rem;
}}
.ph-title {{ font-size: 1.8rem; font-weight: 800; color: {TXT}; margin-bottom: 6px; }}
.ph-sub   {{ font-size: 0.88rem; color: {TXT2}; font-weight: 400; }}

/* ── KPI CARDS ───────────────────────────────── */
.kpi-grid {{
    display: grid; grid-template-columns: repeat(4,1fr);
    gap: 14px; margin-bottom: 28px;
}}
.kpi-card {{
    background: {CARD}; border: 1px solid {CARD_BOR};
    border-radius: 18px; padding: 22px 18px; text-align: center;
    transition: all 0.35s cubic-bezier(0.34,1.56,0.64,1);
    animation: cardRise 0.5s ease forwards; opacity: 0;
    position: relative; overflow: hidden;
}}
.kpi-card::after {{
    content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 3px;
    transform: scaleX(0); transition: transform 0.3s ease;
    background: var(--accent, {GOLD});
}}
.kpi-card:hover::after {{ transform: scaleX(1); }}
.kpi-card:nth-child(1) {{ animation-delay:.05s; --accent:{RED}; }}
.kpi-card:nth-child(2) {{ animation-delay:.10s; --accent:{AMBER}; }}
.kpi-card:nth-child(3) {{ animation-delay:.15s; --accent:{RED}; }}
.kpi-card:nth-child(4) {{ animation-delay:.20s; --accent:{ORANGE}; }}
@keyframes cardRise {{
    from{{ opacity:0; transform:translateY(20px) scale(0.97); }}
    to  {{ opacity:1; transform:translateY(0)    scale(1); }}
}}
.kpi-card:hover {{
    transform: translateY(-5px) scale(1.02);
    border-color: {GOLD}55;
    box-shadow: 0 14px 36px {GOLD}15;
}}
.kpi-val {{ font-size: 2rem; font-weight: 800; line-height: 1; margin-bottom: 8px; }}
.kpi-lbl {{
    font-size: 0.68rem; color: {TXT2};
    text-transform: uppercase; letter-spacing: 1.5px; font-weight: 500;
}}

/* ── FILTER CARD ─────────────────────────────── */
.filter-card {{
    background: {CARD}; border: 1px solid {CARD_BOR};
    border-radius: 16px; padding: 24px 24px 8px;
    margin-bottom: 20px;
    animation: cardRise 0.5s 0.2s ease forwards; opacity: 0;
}}
.filter-title {{
    font-size: 0.7rem; font-weight: 700; color: {GOLD};
    text-transform: uppercase; letter-spacing: 2.5px;
    margin-bottom: 16px; display: flex; align-items: center; gap: 8px;
}}

/* ── TABLE CARD ──────────────────────────────── */
.table-card {{
    background: {CARD}; border: 1px solid {CARD_BOR};
    border-radius: 16px; padding: 24px;
    margin-bottom: 20px;
    animation: cardRise 0.5s 0.3s ease forwards; opacity: 0;
}}
.table-header {{
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 16px; flex-wrap: wrap; gap: 12px;
}}
.table-count {{
    font-size: 0.9rem; font-weight: 700; color: {TXT};
}}
.table-count span {{ color: {GOLD}; font-size: 1.1rem; }}

/* ── CHART CARD ──────────────────────────────── */
.chart-card {{
    background: {CARD}; border: 1px solid {CARD_BOR};
    border-radius: 16px; padding: 24px;
    animation: cardRise 0.5s 0.35s ease forwards; opacity: 0;
}}
.chart-title {{
    font-size: 0.78rem; font-weight: 700; color: {TXT};
    text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 16px;
}}

/* ── RISK PILL ───────────────────────────────── */
.pill {{
    display: inline-block; padding: 3px 10px;
    border-radius: 20px; font-size: 0.72rem; font-weight: 700;
}}
.pill-critical {{ background:{RED}22;   color:{RED};    border:1px solid {RED}44; }}
.pill-high     {{ background:{ORANGE}22; color:{ORANGE}; border:1px solid {ORANGE}44; }}
.pill-medium   {{ background:{AMBER}22;  color:{AMBER};  border:1px solid {AMBER}44; }}
.pill-low      {{ background:{GREEN}22;  color:{GREEN};  border:1px solid {GREEN}44; }}

/* ── SECTION HEADER ──────────────────────────── */
.sec-head {{ display:flex; align-items:center; gap:16px; margin:0 0 20px; }}
.sec-label {{
    font-size:0.72rem; font-weight:700; color:{GOLD};
    text-transform:uppercase; letter-spacing:3px; white-space:nowrap;
}}
.sec-rule {{ flex:1; height:1px; background:linear-gradient(90deg,{GOLD}50,transparent); }}

/* ── STREAMLIT WIDGETS ───────────────────────── */
.stMultiSelect [data-baseweb="select"] {{
    background: {INP_BG} !important; border-color: {INP_BOR} !important;
    border-radius: 10px !important;
}}
.stSlider [data-baseweb="slider"] {{ margin-top: 8px; }}
label {{ color: {TXT2} !important; font-size: 0.82rem !important; font-weight: 500 !important; }}
.stTextInput input {{
    background: {INP_BG} !important; border-color: {INP_BOR} !important;
    color: {TXT} !important; border-radius: 10px !important;
}}
.stTextInput input:focus {{
    border-color: {GOLD} !important;
    box-shadow: 0 0 0 3px {GOLD}22 !important;
}}

/* ── DOWNLOAD BUTTON ─────────────────────────── */
.stDownloadButton button {{
    background: linear-gradient(135deg,{GOLD},{GOLD}bb) !important;
    color: white !important; font-weight: 700 !important;
    border: none !important; border-radius: 12px !important;
    padding: 12px 24px !important;
    box-shadow: 0 4px 18px {GOLD}33 !important;
    transition: all 0.3s ease !important;
}}
.stDownloadButton button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 30px {GOLD}55 !important;
}}

/* ── DATAFRAME ───────────────────────────────── */
[data-testid="stDataFrame"] {{
    border-radius: 12px !important;
    overflow: hidden !important;
}}

/* ── SIDEBAR HELPERS ─────────────────────────── */
.sb-label {{
    font-size:0.6rem; color:rgba(255,255,255,0.25); text-transform:uppercase;
    letter-spacing:2px; padding:0 4px; margin:12px 0 6px; display:block;
}}
.sb-model {{
    background:{GOLD}10; border:1px solid {GOLD}25;
    border-radius:12px; padding:14px; margin:8px 0;
}}
.sb-model-row {{ display:flex; justify-content:space-between; margin-bottom:5px; }}
.sb-mk {{ font-size:0.68rem; color:rgba(255,255,255,0.35); }}
.sb-mv {{ font-size:0.68rem; color:white; font-weight:600; }}
.sb-dot {{
    width:7px; height:7px; background:{GREEN}; border-radius:50%;
    display:inline-block; box-shadow:0 0 8px {GREEN}; animation:blink 2s infinite;
}}
@keyframes blink {{ 0%,100%{{opacity:1}} 50%{{opacity:0.3}} }}
.sb-footer {{
    text-align:center; padding:12px 0 4px;
    border-top:1px solid rgba(255,255,255,0.06); margin-top:12px;
}}
.sb-fp {{ font-size:0.6rem; color:rgba(255,255,255,0.2); letter-spacing:1.5px; text-transform:uppercase; }}
.sb-fv {{ font-size:0.58rem; color:{GOLD}55; letter-spacing:1px; margin-top:3px; }}

/* ── FOOTER ──────────────────────────────────── */
.main-footer {{
    text-align:center; padding:28px 16px;
    font-size:0.72rem; color:{TXT2};
    border-top:1px solid {CARD_BOR};
    letter-spacing:1.5px; text-transform:uppercase; margin-top:40px;
}}

/* ── PRINT ───────────────────────────────────── */
@media print {{
    section[data-testid="stSidebar"], .stDownloadButton, .filter-card {{ display:none!important; }}
    .stApp {{ background:white!important; }}
    .kpi-card, .chart-card, .table-card {{
        border:1px solid #ddd!important;
        background:white!important;
        box-shadow:none!important;
    }}
    .kpi-val, .kpi-lbl, .ph-title, .ph-sub, .chart-title, .table-count {{ color:#0D2B4E!important; }}
}}
</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR ──────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:28px 20px 20px;text-align:center;
        border-bottom:1px solid rgba(201,152,42,0.15);">
        {logo_html}
        <div style="margin-top:12px;font-size:1.05rem;font-weight:800;
            color:{GOLD};letter-spacing:2px;text-transform:uppercase;">{t['brand']}</div>
        <div style="font-size:0.62rem;color:rgba(255,255,255,0.35);
            letter-spacing:1px;text-transform:uppercase;margin-top:4px;line-height:1.5;">
            {t['brand_sub']}</div>
    </div><br>
    """, unsafe_allow_html=True)

    st.page_link("app.py",                     label=f"  {t['nav_home']}")
    st.page_link("pages/1_Prediction.py",      label=f"  {t['nav_pred']}")
    st.page_link("pages/2_Clients_Risque.py",  label=f"  {t['nav_risk']}")

    st.markdown(f"""
    <hr>
    <span class="sb-label">{t['model_label'].upper()}</span>
    <div class="sb-model">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
            <span class="sb-dot"></span>
            <span style="font-size:0.9rem;font-weight:700;color:{GOLD};">XGBoost</span>
        </div>
        <div class="sb-model-row"><span class="sb-mk">ROC-AUC</span><span class="sb-mv">0.9496</span></div>
        <div class="sb-model-row"><span class="sb-mk">F1-Score</span><span class="sb-mv">0.8805</span></div>
        <div class="sb-model-row"><span class="sb-mk">PR-AUC</span><span class="sb-mv">0.9562</span></div>
    </div>
    <hr>
    <span class="sb-label">{t['lang_label'].upper()}</span>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("FR", use_container_width=True, type="primary" if lang=="fr" else "secondary"):
            st.session_state.lang = "fr"; st.rerun()
    with c2:
        if st.button("EN", use_container_width=True, type="primary" if lang=="en" else "secondary"):
            st.session_state.lang = "en"; st.rerun()
    with c3:
        if st.button("AR", use_container_width=True, type="primary" if lang=="ar" else "secondary"):
            st.session_state.lang = "ar"; st.rerun()

    st.markdown(f'<span class="sb-label" style="margin-top:12px;">{t["theme_label"].upper()}</span>',
                unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button(f"🌙 {t['theme_dark']}", use_container_width=True,
                     type="primary" if dark else "secondary"):
            st.session_state.theme = "dark"; st.rerun()
    with c2:
        if st.button(f"☀️ {t['theme_light']}", use_container_width=True,
                     type="primary" if not dark else "secondary"):
            st.session_state.theme = "light"; st.rerun()

    st.markdown(f"""
    <hr>
    <div style="padding:8px 4px;text-align:center;">
        <div style="font-size:0.62rem;color:rgba(255,255,255,0.25);
            letter-spacing:1.5px;text-transform:uppercase;margin-bottom:10px;">
            Actions
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button(t["print"], use_container_width=True):
        st.components.v1.html(
            "<script>window.print();</script>", height=0
        )

    st.markdown(f"""
    <div class="sb-footer">
        <div class="sb-fp">{t['powered']}</div>
        <div class="sb-fv">{t['version']}</div>
    </div>
    """, unsafe_allow_html=True)

# ─── PAGE HEADER ──────────────────────────────────────
st.markdown(f"""
<div class="page-header">
    <div class="ph-icon">⚠️</div>
    <div>
        <div class="ph-title">{t['page_title']}</div>
        <div class="ph-sub">{t['page_sub']}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── LOAD DATA ────────────────────────────────────────
try:
    df_raw = load_clients_a_risque()

    if df_raw is None or df_raw.empty:
        st.warning(t["error_no_file"])
        st.stop()

    # Ensure numeric probability
    if "PROBA_CHURN" in df_raw.columns:
        df_raw["PROBA_CHURN"] = pd.to_numeric(df_raw["PROBA_CHURN"], errors="coerce").fillna(0)

    # ── KPI CARDS ────────────────────────────────────
    n_total    = len(df_raw)
    avg_proba  = df_raw["PROBA_CHURN"].mean() * 100
    n_critical = len(df_raw[df_raw["PROBA_CHURN"] >= 0.90])
    n_high     = len(df_raw[df_raw["PROBA_CHURN"] >= 0.75])

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-val" style="color:{RED}">{n_total:,}</div>
            <div class="kpi-lbl">{t['kpi_total']}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-val" style="color:{AMBER}">{avg_proba:.1f}%</div>
            <div class="kpi-lbl">{t['kpi_avg']}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-val" style="color:{RED}">{n_critical:,}</div>
            <div class="kpi-lbl">{t['kpi_critical']}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-val" style="color:{ORANGE}">{n_high:,}</div>
            <div class="kpi-lbl">{t['kpi_high']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── FILTER SECTION ────────────────────────────────
    st.markdown(f"""
    <div class="filter-card">
        <div class="filter-title">🔍 Filtres & Recherche</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        r1c1, r1c2, r1c3 = st.columns([1, 1, 1])

        with r1c1:
            nature_opts = sorted(df_raw["NATURE_CLIENT"].dropna().unique().tolist()) \
                if "NATURE_CLIENT" in df_raw.columns else []
            nature_sel = st.multiselect(
                t["filter_nature"],
                options=nature_opts,
                default=nature_opts,
                key="nature_filter"
            )

        with r1c2:
            kyc_opts = sorted(df_raw["SCORE_KYC"].dropna().unique().tolist()) \
                if "SCORE_KYC" in df_raw.columns else []
            kyc_sel = st.multiselect(
                t["filter_kyc"],
                options=kyc_opts,
                default=kyc_opts,
                key="kyc_filter"
            )

        with r1c3:
            seuil = st.slider(t["filter_seuil"], 50, 99, 70, key="seuil_slider")

        search = st.text_input(t["search"], placeholder="ex: C304607", key="search_input")

    # ── APPLY FILTERS ─────────────────────────────────
    df_f = df_raw.copy()

    if nature_sel and "NATURE_CLIENT" in df_f.columns:
        df_f = df_f[df_f["NATURE_CLIENT"].isin(nature_sel)]

    if kyc_sel and "SCORE_KYC" in df_f.columns:
        df_f = df_f[df_f["SCORE_KYC"].isin(kyc_sel)]

    df_f = df_f[df_f["PROBA_CHURN"] >= seuil / 100]

    if search.strip():
        mask = (
            df_f["CUSTOMER_NO"].astype(str).str.contains(search.strip(), case=False, na=False)
            | df_f["ACCOUNT_NO"].astype(str).str.contains(search.strip(), case=False, na=False)
        )
        df_f = df_f[mask]

    df_display = df_f.copy()
    df_display["PROBA_%"] = (df_display["PROBA_CHURN"] * 100).round(1)

    # ── TABLE CARD ────────────────────────────────────
    st.markdown(f"""
    <div class="table-card">
        <div class="table-header">
            <div class="table-count">
                <span>{len(df_display):,}</span> {t['table_title']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if df_display.empty:
        st.info(t["no_data"])
    else:
        # Build display columns
        show_cols = []
        col_rename = {}
        for col_key, col_name in [
            ("CUSTOMER_NO", t["col_client"]),
            ("ACCOUNT_NO",  t["col_account"]),
            ("NATURE_CLIENT", t["col_nature"]),
            ("SCORE_KYC",   t["col_kyc"]),
            ("ACCT_BALANCE", t["col_balance"]),
            ("PROBA_%",     t["col_proba"]),
            ("RISQUE",      t["col_risque"]),
        ]:
            if col_key in df_display.columns:
                show_cols.append(col_key)
                col_rename[col_key] = col_name

        df_show = df_display[show_cols].rename(columns=col_rename)
        df_show = df_show.sort_values(t["col_proba"], ascending=False).reset_index(drop=True)

        st.dataframe(
            df_show,
            use_container_width=True,
            hide_index=True,
            height=420,
            column_config={
                t["col_proba"]: st.column_config.ProgressColumn(
                    t["col_proba"],
                    min_value=0, max_value=100,
                    format="%.1f%%",
                ),
                t["col_balance"]: st.column_config.NumberColumn(
                    t["col_balance"],
                    format="%.0f TND",
                ),
            }
        )

    # ── CHARTS ───────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="sec-head">
        <span class="sec-label">📊 Analyses Graphiques</span>
        <div class="sec-rule"></div>
    </div>
    """, unsafe_allow_html=True)

    def style_fig(fig):
        fig.update_layout(
            paper_bgcolor=PLOT_PAPER,
            plot_bgcolor=PLOT_BG,
            font=dict(color=TICK_C, family="Inter, sans-serif", size=11),
            margin=dict(l=16, r=16, t=40, b=16),
            xaxis=dict(gridcolor=GRID_C, linecolor=GRID_C, tickfont=dict(color=TICK_C)),
            yaxis=dict(gridcolor=GRID_C, linecolor=GRID_C, tickfont=dict(color=TICK_C)),
            showlegend=False,
            coloraxis_showscale=False,
        )
        return fig

    ch1, ch2 = st.columns(2)

    with ch1:
        st.markdown(f'<div class="chart-card"><div class="chart-title">{t["chart1"]}</div>', unsafe_allow_html=True)
        if "NATURE_CLIENT" in df_raw.columns:
            grp1 = (
                df_raw.groupby("NATURE_CLIENT")["PROBA_CHURN"]
                .mean()
                .reset_index()
                .sort_values("PROBA_CHURN", ascending=False)
            )
            grp1["PROBA_%"] = (grp1["PROBA_CHURN"] * 100).round(1)
            fig1 = px.bar(
                grp1, x="NATURE_CLIENT", y="PROBA_%",
                color="PROBA_%",
                color_continuous_scale=[[0, GREEN], [0.5, AMBER], [1, RED]],
                text="PROBA_%",
            )
            fig1.update_traces(
                texttemplate="%{text:.1f}%", textposition="outside",
                marker_line_width=0,
                selector=dict(type="bar"),
            )
            fig1 = style_fig(fig1)
            fig1.update_layout(yaxis_title="Probabilité (%)", xaxis_title="")
            st.plotly_chart(fig1, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with ch2:
        st.markdown(f'<div class="chart-card"><div class="chart-title">{t["chart2"]}</div>', unsafe_allow_html=True)
        if "SCORE_KYC" in df_raw.columns:
            grp2 = (
                df_raw.groupby("SCORE_KYC")["PROBA_CHURN"]
                .mean()
                .reset_index()
                .sort_values("PROBA_CHURN", ascending=False)
            )
            grp2["PROBA_%"] = (grp2["PROBA_CHURN"] * 100).round(1)
            fig2 = px.bar(
                grp2, x="SCORE_KYC", y="PROBA_%",
                color="PROBA_%",
                color_continuous_scale=[[0, GREEN], [0.5, AMBER], [1, RED]],
                text="PROBA_%",
            )
            fig2.update_traces(
                texttemplate="%{text:.1f}%", textposition="outside",
                marker_line_width=0,
            )
            fig2 = style_fig(fig2)
            fig2.update_layout(yaxis_title="Probabilité (%)", xaxis_title="")
            st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    ch3, ch4 = st.columns(2)

    with ch3:
        st.markdown(f'<div class="chart-card"><div class="chart-title">{t["chart3"]}</div>', unsafe_allow_html=True)
        fig3 = px.histogram(
            df_raw,
            x="PROBA_CHURN",
            nbins=30,
            color_discrete_sequence=[GOLD],
        )
        fig3.update_traces(opacity=0.85, marker_line_width=0)
        fig3 = style_fig(fig3)
        fig3.update_layout(
            xaxis_title="Probabilité de Churn",
            yaxis_title="Nombre de Clients",
            bargap=0.05,
        )
        fig3.add_vrect(x0=0.75, x1=1.0, fillcolor=RED, opacity=0.07, line_width=0)
        fig3.add_vrect(x0=0.50, x1=0.75, fillcolor=AMBER, opacity=0.05, line_width=0)
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with ch4:
        st.markdown(f'<div class="chart-card"><div class="chart-title">{t["chart4"]}</div>', unsafe_allow_html=True)
        if "RISQUE" in df_raw.columns:
            risk_counts = df_raw["RISQUE"].value_counts().reset_index()
            risk_counts.columns = ["Risque", "Clients"]
            color_map = {
                "🔴 Critique":  RED,
                "🟠 Élevé":     ORANGE,
                "🟡 Modéré":    AMBER,
                "🟢 Faible":    GREEN,
            }
            # Fallback colors
            colors_list = [
                color_map.get(r, GOLD)
                for r in risk_counts["Risque"]
            ]
            fig4 = go.Figure(data=[go.Pie(
                labels=risk_counts["Risque"],
                values=risk_counts["Clients"],
                hole=0.55,
                marker=dict(colors=colors_list, line=dict(color=BG, width=2)),
                textinfo="label+percent",
                textfont=dict(size=11, color=TICK_C),
            )])
            fig4 = style_fig(fig4)
            fig4.update_layout(
                showlegend=True,
                legend=dict(
                    font=dict(color=TICK_C, size=10),
                    orientation="v",
                    x=1.02,
                )
            )
            st.plotly_chart(fig4, use_container_width=True)
        else:
            # Donut by probability bands
            bands = pd.cut(
                df_raw["PROBA_CHURN"],
                bins=[0, 0.35, 0.55, 0.75, 1.0],
                labels=["🟢 Faible", "🟡 Modéré", "🟠 Élevé", "🔴 Critique"]
            ).value_counts().reset_index()
            bands.columns = ["Risque", "Clients"]
            fig4 = px.pie(bands, names="Risque", values="Clients", hole=0.55,
                          color_discrete_sequence=[GREEN, AMBER, ORANGE, RED])
            fig4 = style_fig(fig4)
            st.plotly_chart(fig4, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── EXPORT ───────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    ec1, ec2 = st.columns(2)

    with ec1:
        csv_full = df_raw.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label=t["export"],
            data=csv_full,
            file_name="clients_a_risque_complet.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with ec2:
        if not df_display.empty:
            csv_sel = df_display[show_cols].rename(columns=col_rename).to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                label=t["export_filtered"],
                data=csv_sel,
                file_name="clients_a_risque_selection.csv",
                mime="text/csv",
                use_container_width=True,
            )

except Exception as e:
    st.error(f"❌ Erreur : {e}")
    st.exception(e)

# ─── FOOTER ───────────────────────────────────────────
st.markdown(f'<div class="main-footer">{t["footer"]}</div>', unsafe_allow_html=True)