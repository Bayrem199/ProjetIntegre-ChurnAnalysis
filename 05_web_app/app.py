import streamlit as st
import sys
import base64
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils.preprocessing import load_kpis

st.set_page_config(
    page_title="ChurnGuard — Intelligence Bancaire",
    page_icon="assets/logo.png" if Path("assets/logo.png").exists() else "🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── HELPERS ────────────────────────────────────────────
def img_to_b64(path):
    p = Path(__file__).resolve().parent / path
    if p.exists():
        return base64.b64encode(p.read_bytes()).decode()
    return None

def img_tag(path, style=""):
    b64 = img_to_b64(path)
    if b64:
        ext = Path(path).suffix.lstrip(".")
        return f'<img src="data:image/{ext};base64,{b64}" style="{style}">'
    return ""

# ─── TRANSLATIONS ────────────────────────────────────────
T = {
    "fr": {
        "brand"       : "ChurnGuard",
        "brand_sub"   : "Intelligence de Rétention Client",
        "nav_home"    : "Tableau de Bord",
        "nav_pred"    : "Prédiction",
        "nav_risk"    : "Clients à Risque",
        "nav_settings": "Paramètres",
        "model_label" : "Modèle Actif",
        "powered"     : "Propulsé par Machine Learning",
        "version"     : "Version 1.0 · 2025",
        "theme_dark"  : "Sombre",
        "theme_light" : "Clair",
        "lang_label"  : "Langue",
        "theme_label" : "Apparence",
        "hero_eyebrow": "Plateforme Analytique Bancaire",
        "hero_h1"     : "Anticipez le Churn,\nProtégez vos Clients",
        "hero_sub"    : "Modèle XGBoost entraîné sur 484 443 clients réels — ROC-AUC 0.9496",
        "hero_cta1"   : "Lancer une Prédiction",
        "hero_cta2"   : "Voir les Clients à Risque",
        "kpi_section" : "Indicateurs en Temps Réel",
        "kpi_total"   : "Clients Analysés",
        "kpi_churn"   : "Taux de Churn",
        "kpi_churners": "Comptes Clôturés",
        "kpi_actifs"  : "Clients Actifs",
        "kpi_senio"   : "Ancienneté Moy.",
        "mod_section" : "Modules de la Plateforme",
        "mod1_title"  : "Prédiction Individuelle",
        "mod1_desc"   : "Saisissez le profil d'un client et obtenez en temps réel sa probabilité de churn avec niveau de risque et recommandations d'action.",
        "mod1_cta"    : "Accéder →",
        "mod2_title"  : "Clients à Risque",
        "mod2_desc"   : "Explorez et filtrez les 12 765 clients actifs identifiés à risque élevé. Export CSV, graphiques analytiques, seuils personnalisables.",
        "mod2_cta"    : "Accéder →",
        "footer"      : "© 2025 ESPRIT School of Business · Master 1 Business Analytics · ChurnGuard Platform",
    },
    "en": {
        "brand"       : "ChurnGuard",
        "brand_sub"   : "Client Retention Intelligence",
        "nav_home"    : "Dashboard",
        "nav_pred"    : "Prediction",
        "nav_risk"    : "At-Risk Clients",
        "nav_settings": "Settings",
        "model_label" : "Active Model",
        "powered"     : "Powered by Machine Learning",
        "version"     : "Version 1.0 · 2025",
        "theme_dark"  : "Dark",
        "theme_light" : "Light",
        "lang_label"  : "Language",
        "theme_label" : "Appearance",
        "hero_eyebrow": "Banking Analytics Platform",
        "hero_h1"     : "Predict Churn,\nRetain Clients",
        "hero_sub"    : "XGBoost model trained on 484,443 real clients — ROC-AUC 0.9496",
        "hero_cta1"   : "Run a Prediction",
        "hero_cta2"   : "View At-Risk Clients",
        "kpi_section" : "Real-Time Indicators",
        "kpi_total"   : "Clients Analyzed",
        "kpi_churn"   : "Churn Rate",
        "kpi_churners": "Closed Accounts",
        "kpi_actifs"  : "Active Clients",
        "kpi_senio"   : "Avg. Seniority",
        "mod_section" : "Platform Modules",
        "mod1_title"  : "Individual Prediction",
        "mod1_desc"   : "Enter a client profile and get real-time churn probability with risk level and action recommendations.",
        "mod1_cta"    : "Access →",
        "mod2_title"  : "At-Risk Clients",
        "mod2_desc"   : "Explore and filter 12,765 active clients identified as high risk. CSV export, analytics charts, custom thresholds.",
        "mod2_cta"    : "Access →",
        "footer"      : "© 2025 ESPRIT School of Business · Master 1 Business Analytics · ChurnGuard Platform",
    },
    "ar": {
        "brand"       : "ChurnGuard",
        "brand_sub"   : "منصة الاحتفاظ بالعملاء",
        "nav_home"    : "لوحة التحكم",
        "nav_pred"    : "التنبؤ",
        "nav_risk"    : "العملاء المعرضون للخطر",
        "nav_settings": "الإعدادات",
        "model_label" : "النموذج النشط",
        "powered"     : "مدعوم بالذكاء الاصطناعي",
        "version"     : "الإصدار 1.0 · 2025",
        "theme_dark"  : "داكن",
        "theme_light" : "فاتح",
        "lang_label"  : "اللغة",
        "theme_label" : "المظهر",
        "hero_eyebrow": "منصة التحليلات البنكية",
        "hero_h1"     : "توقع المغادرة،\nاحتفظ بعملائك",
        "hero_sub"    : "نموذج XGBoost مدرب على 484,443 عميل حقيقي — ROC-AUC 0.9496",
        "hero_cta1"   : "إجراء تنبؤ",
        "hero_cta2"   : "عرض العملاء المعرضين للخطر",
        "kpi_section" : "المؤشرات الرئيسية",
        "kpi_total"   : "العملاء المحللون",
        "kpi_churn"   : "معدل المغادرة",
        "kpi_churners": "الحسابات المغلقة",
        "kpi_actifs"  : "العملاء النشطون",
        "kpi_senio"   : "متوسط الأقدمية",
        "mod_section" : "وحدات المنصة",
        "mod1_title"  : "التنبؤ الفردي",
        "mod1_desc"   : "أدخل ملف العميل واحصل على احتمالية المغادرة في الوقت الفعلي مع مستوى الخطر وتوصيات الإجراءات.",
        "mod1_cta"    : "الوصول ←",
        "mod2_title"  : "العملاء المعرضون للخطر",
        "mod2_desc"   : "استكشف وفلتر 12,765 عميلاً نشطاً تم تحديده على أنه عالي الخطر. تصدير CSV ورسوم بيانية.",
        "mod2_cta"    : "الوصول ←",
        "footer"      : "© 2025 ESPRIT School of Business · ماجستير 1 تحليلات الأعمال · ChurnGuard",
    },
}

# ─── SESSION STATE ───────────────────────────────────────
if "lang"  not in st.session_state: st.session_state.lang  = "fr"
if "theme" not in st.session_state: st.session_state.theme = "dark"

lang  = st.session_state.lang
t     = T[lang]
dark  = st.session_state.theme == "dark"
rtl   = lang == "ar"
dir_  = "rtl" if rtl else "ltr"

# ─── THEME TOKENS ────────────────────────────────────────
if dark:
    BG        = "#020817"
    BG2       = "#0a1628"
    CARD      = "rgba(255,255,255,0.03)"
    CARD_BOR  = "rgba(255,255,255,0.08)"
    TXT       = "#f1f5f9"
    TXT2      = "rgba(241,245,249,0.5)"
    SIDEBAR   = "linear-gradient(180deg,#061953 0%,#040f33 100%)"
    HERO_OVER = "rgba(2,8,23,0.55)"
else:
    BG        = "#f8faff"
    BG2       = "#eef2ff"
    CARD      = "rgba(255,255,255,0.95)"
    CARD_BOR  = "rgba(13,43,78,0.12)"
    TXT       = "#0D2B4E"
    TXT2      = "rgba(13,43,78,0.55)"
    SIDEBAR   = "linear-gradient(180deg,#0D2B4E 0%,#1a4a7a 100%)"
    HERO_OVER = "rgba(13,43,78,0.45)"

GOLD  = "#C9982A"
GREEN = "#10b981"
RED   = "#ef4444"

banner_b64 = img_to_b64("assets/banner.png")
logo_b64   = img_to_b64("assets/logo.png")

banner_css = f'url("data:image/png;base64,{banner_b64}")' if banner_b64 else \
    f'linear-gradient(135deg, #0D2B4E 0%, #1a4a7a 40%, #C9982A 100%)'

logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="width:60px;height:60px;border-radius:16px;object-fit:cover;">' \
    if logo_b64 else \
    '<div style="width:60px;height:60px;background:linear-gradient(135deg,rgba(201,152,42,0.3),rgba(201,152,42,0.1));border:2px solid rgba(201,152,42,0.5);border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:1.8rem;">🏦</div>'

# ─── GLOBAL CSS ─────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Cairo:wght@400;600;700;800&display=swap');

*, *::before, *::after {{
    font-family: {'Cairo' if rtl else 'Inter'}, sans-serif;
    box-sizing: border-box;
}}

#MainMenu, header[data-testid="stHeader"], footer, .stDeployButton {{
    visibility: hidden !important;
    display: none !important;
}}

.stApp {{
    background: {BG} !important;
    direction: {dir_};
}}

/* SCROLLBAR */
::-webkit-scrollbar {{ width: 5px; }}
::-webkit-scrollbar-track {{ background: {BG}; }}
::-webkit-scrollbar-thumb {{ background: {GOLD}44; border-radius: 10px; }}
::-webkit-scrollbar-thumb:hover {{ background: {GOLD}; }}

/* SIDEBAR */
section[data-testid="stSidebar"] {{
    background: {SIDEBAR} !important;
    border-right: 1px solid {GOLD}30 !important;
    box-shadow: 6px 0 40px rgba(0,0,0,0.4) !important;
}}
section[data-testid="stSidebar"] > div:first-child {{
    padding: 0 !important;
}}
section[data-testid="stSidebar"] * {{
    color: white !important;
}}
section[data-testid="stSidebar"] a[data-testid="stPageLink"] {{
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
    padding: 11px 14px !important;
    border-radius: 12px !important;
    margin-bottom: 4px !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    color: rgba(255,255,255,0.65) !important;
    border: 1px solid transparent !important;
    background: transparent !important;
    transition: all 0.25s ease !important;
    text-decoration: none !important;
}}
section[data-testid="stSidebar"] a[data-testid="stPageLink"]:hover {{
    background: rgba(255,255,255,0.07) !important;
    color: white !important;
    border-color: rgba(255,255,255,0.1) !important;
    padding-left: 18px !important;
}}
section[data-testid="stSidebar"] a[data-testid="stPageLink-active"] {{
    background: linear-gradient(135deg,{GOLD}20,{GOLD}08) !important;
    color: {GOLD} !important;
    border-color: {GOLD}40 !important;
    font-weight: 600 !important;
}}

/* SIDEBAR BUTTONS */
section[data-testid="stSidebar"] .stButton button {{
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: rgba(255,255,255,0.7) !important;
    border-radius: 10px !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    padding: 6px 4px !important;
    transition: all 0.2s ease !important;
}}
section[data-testid="stSidebar"] .stButton button:hover {{
    background: rgba(255,255,255,0.12) !important;
    color: white !important;
    border-color: rgba(255,255,255,0.2) !important;
}}
section[data-testid="stSidebar"] button[kind="primary"] {{
    background: linear-gradient(135deg,{GOLD},{GOLD}aa) !important;
    border-color: {GOLD} !important;
    color: white !important;
    font-weight: 700 !important;
}}

/* DIVIDER */
hr {{ border-color: rgba(255,255,255,0.07) !important; margin: 14px 0 !important; }}

/* HERO */
.hero-wrap {{
    position: relative;
    border-radius: 24px;
    overflow: hidden;
    margin-bottom: 48px;
    min-height: 380px;
    display: flex;
    align-items: center;
    background-image: {banner_css};
    background-size: cover;
    background-position: center;
    animation: heroIn 1s ease;
}}
@keyframes heroIn {{
    from {{ opacity:0; transform:translateY(-16px); }}
    to   {{ opacity:1; transform:translateY(0); }}
}}
.hero-overlay {{
    position: absolute; inset: 0;
    background: {HERO_OVER};
    backdrop-filter: blur(2px);
}}
.hero-content {{
    position: relative; z-index: 2;
    padding: 60px 56px;
    max-width: 680px;
    direction: {dir_};
}}
.hero-eyebrow {{
    display: inline-flex; align-items: center; gap: 8px;
    background: {GOLD}22;
    border: 1px solid {GOLD}55;
    color: {GOLD};
    padding: 5px 16px;
    border-radius: 50px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 20px;
}}
.hero-eyebrow::before {{
    content: '';
    width: 6px; height: 6px;
    background: {GOLD};
    border-radius: 50%;
    box-shadow: 0 0 8px {GOLD};
    animation: blink 2s infinite;
}}
@keyframes blink {{ 0%,100%{{opacity:1}} 50%{{opacity:0.3}} }}
.hero-h1 {{
    font-size: 3rem;
    font-weight: 900;
    color: white;
    line-height: 1.15;
    margin-bottom: 16px;
    white-space: pre-line;
}}
.hero-h1 span {{ color: {GOLD}; }}
.hero-sub {{
    font-size: 0.95rem;
    color: rgba(255,255,255,0.7);
    font-weight: 400;
    line-height: 1.6;
    margin-bottom: 32px;
}}
.hero-ctas {{ display: flex; gap: 14px; flex-wrap: wrap; }}
.cta-primary {{
    background: linear-gradient(135deg,{GOLD},{GOLD}bb);
    color: white; font-weight: 700; font-size: 0.88rem;
    padding: 12px 26px; border-radius: 12px; border: none;
    cursor: pointer; transition: all 0.3s ease; text-decoration: none;
    display: inline-block;
}}
.cta-primary:hover {{
    transform: translateY(-2px);
    box-shadow: 0 12px 30px {GOLD}55;
}}
.cta-secondary {{
    background: rgba(255,255,255,0.1);
    color: white; font-weight: 600; font-size: 0.88rem;
    padding: 12px 26px; border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.25);
    cursor: pointer; transition: all 0.3s ease; text-decoration: none;
    display: inline-block; backdrop-filter: blur(8px);
}}
.cta-secondary:hover {{
    background: rgba(255,255,255,0.18);
    transform: translateY(-2px);
}}

/* SECTION HEADER */
.sec-head {{
    display: flex; align-items: center; gap: 16px;
    margin: 0 0 28px;
}}
.sec-label {{
    font-size: 0.72rem; font-weight: 700; color: {GOLD};
    text-transform: uppercase; letter-spacing: 3px; white-space: nowrap;
}}
.sec-rule {{
    flex: 1; height: 1px;
    background: linear-gradient(90deg,{GOLD}50,transparent);
}}

/* KPI GRID */
.kpi-grid {{
    display: grid; grid-template-columns: repeat(5,1fr);
    gap: 14px; margin-bottom: 48px;
}}
.kpi-card {{
    background: {CARD};
    border: 1px solid {CARD_BOR};
    border-radius: 18px; padding: 24px 16px; text-align: center;
    transition: all 0.35s cubic-bezier(0.34,1.56,0.64,1);
    animation: cardRise 0.6s ease forwards; opacity: 0;
    position: relative; overflow: hidden;
}}
.kpi-card::before {{
    content: '';
    position: absolute; bottom: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg,transparent,{GOLD},transparent);
    transform: scaleX(0); transition: transform 0.3s ease;
}}
.kpi-card:hover::before {{ transform: scaleX(1); }}
.kpi-card:nth-child(1){{animation-delay:.05s}}
.kpi-card:nth-child(2){{animation-delay:.1s}}
.kpi-card:nth-child(3){{animation-delay:.15s}}
.kpi-card:nth-child(4){{animation-delay:.2s}}
.kpi-card:nth-child(5){{animation-delay:.25s}}
@keyframes cardRise {{
    from{{opacity:0;transform:translateY(24px) scale(0.96)}}
    to{{opacity:1;transform:translateY(0) scale(1)}}
}}
.kpi-card:hover {{
    transform: translateY(-6px) scale(1.02);
    border-color: {GOLD}55;
    box-shadow: 0 16px 40px {GOLD}18;
}}
.kpi-val {{
    font-size: 2rem; font-weight: 800; color: {GOLD};
    line-height: 1; margin-bottom: 8px;
}}
.kpi-lbl {{
    font-size: 0.68rem; color: {TXT2};
    text-transform: uppercase; letter-spacing: 1.5px; font-weight: 500;
}}

/* MODULE CARDS */
.mod-grid {{
    display: grid; grid-template-columns: 1fr 1fr; gap: 20px;
    margin-bottom: 48px;
}}
.mod-card {{
    border-radius: 22px; padding: 36px 32px; position: relative;
    overflow: hidden; transition: all 0.4s ease;
}}
.mod-card::after {{
    content:''; position:absolute; inset:0;
    opacity:0; transition: opacity 0.3s;
    background: radial-gradient(circle at 30% 50%, {GOLD}12, transparent 60%);
}}
.mod-card:hover::after {{ opacity:1; }}
.mod-card:hover {{ transform: translateY(-8px); }}
.mod-card.green-card {{
    background: {'rgba(16,185,129,0.06)' if dark else 'rgba(16,185,129,0.05)'};
    border: 1px solid {GREEN}30;
}}
.mod-card.green-card:hover {{
    border-color: {GREEN}80;
    box-shadow: 0 24px 60px {GREEN}18;
}}
.mod-card.red-card {{
    background: {'rgba(239,68,68,0.06)' if dark else 'rgba(239,68,68,0.05)'};
    border: 1px solid {RED}30;
}}
.mod-card.red-card:hover {{
    border-color: {RED}80;
    box-shadow: 0 24px 60px {RED}18;
}}
.mod-img {{
    width: 56px; height: 56px; border-radius: 16px; margin-bottom: 20px;
    object-fit: cover;
}}
.mod-img-fallback {{
    width: 56px; height: 56px; border-radius: 16px; margin-bottom: 20px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.8rem;
}}
.mod-title {{
    font-size: 1.3rem; font-weight: 700; color: {TXT}; margin-bottom: 10px;
}}
.mod-desc {{
    font-size: 0.85rem; color: {TXT2}; line-height: 1.7;
    margin-bottom: 24px;
}}
.mod-cta {{
    display: inline-block; font-size: 0.85rem; font-weight: 700;
    color: {GOLD}; letter-spacing: 0.5px; transition: gap 0.2s;
}}
.mod-card:hover .mod-cta {{ letter-spacing: 2px; }}

/* FOOTER */
.main-footer {{
    text-align: center; padding: 32px 16px;
    font-size: 0.72rem; color: {TXT2};
    border-top: 1px solid {CARD_BOR};
    letter-spacing: 1.5px; text-transform: uppercase; margin-top: 48px;
}}

/* SIDEBAR LABELS */
.sb-label {{
    font-size: 0.6rem; color: rgba(255,255,255,0.25);
    text-transform: uppercase; letter-spacing: 2px;
    padding: 0 4px; margin: 12px 0 6px; display: block;
}}
.sb-model {{
    background: {GOLD}10; border: 1px solid {GOLD}25;
    border-radius: 12px; padding: 14px; margin: 8px 0;
}}
.sb-model-row {{
    display: flex; justify-content: space-between;
    margin-bottom: 5px;
}}
.sb-mk {{ font-size: 0.68rem; color: rgba(255,255,255,0.35); }}
.sb-mv {{ font-size: 0.68rem; color: white; font-weight: 600; }}
.sb-dot {{
    width:7px;height:7px;background:{GREEN};border-radius:50%;
    display:inline-block;box-shadow:0 0 8px {GREEN};
    animation: blink 2s infinite;
}}
.sb-footer {{
    text-align:center; padding:12px 0 4px;
    border-top:1px solid rgba(255,255,255,0.06); margin-top:12px;
}}
.sb-fp {{ font-size:0.6rem; color:rgba(255,255,255,0.2); letter-spacing:1.5px; text-transform:uppercase; }}
.sb-fv {{ font-size:0.58rem; color:{GOLD}55; letter-spacing:1px; margin-top:3px; }}
</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR ────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:28px 20px 20px;text-align:center;
        border-bottom:1px solid rgba(201,152,42,0.15);">
        {logo_html}
        <div style="margin-top:12px;font-size:1.05rem;font-weight:800;
            color:{GOLD};letter-spacing:2px;text-transform:uppercase;">
            {t['brand']}
        </div>
        <div style="font-size:0.62rem;color:rgba(255,255,255,0.35);
            letter-spacing:1px;text-transform:uppercase;margin-top:4px;
            line-height:1.5;">
            {t['brand_sub']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<span class="sb-label">{t["nav_home"][:3].upper()} · NAVIGATION</span>', unsafe_allow_html=True)

    st.page_link("app.py",                    label=f"  {t['nav_home']}")
    st.page_link("pages/1_Prediction.py",     label=f"  {t['nav_pred']}")
    st.page_link("pages/2_Clients_Risque.py", label=f"  {t['nav_risk']}")

    st.markdown(f"""
    <hr>
    <span class="sb-label">{t['model_label'].upper()}</span>
    <div class="sb-model">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
            <span class="sb-dot"></span>
            <span style="font-size:0.9rem;font-weight:700;color:{GOLD};">XGBoost</span>
        </div>
        <div class="sb-model-row">
            <span class="sb-mk">ROC-AUC</span><span class="sb-mv">0.9496</span>
        </div>
        <div class="sb-model-row">
            <span class="sb-mk">F1-Score</span><span class="sb-mv">0.8805</span>
        </div>
        <div class="sb-model-row">
            <span class="sb-mk">PR-AUC</span><span class="sb-mv">0.9562</span>
        </div>
    </div>
    <hr>
    <span class="sb-label">{t['lang_label'].upper()}</span>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("FR", use_container_width=True,
            type="primary" if lang=="fr" else "secondary"):
            st.session_state.lang="fr"; st.rerun()
    with c2:
        if st.button("EN", use_container_width=True,
            type="primary" if lang=="en" else "secondary"):
            st.session_state.lang="en"; st.rerun()
    with c3:
        if st.button("AR", use_container_width=True,
            type="primary" if lang=="ar" else "secondary"):
            st.session_state.lang="ar"; st.rerun()

    st.markdown(f'<span class="sb-label" style="margin-top:12px;">{t["theme_label"].upper()}</span>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button(f"🌙 {t['theme_dark']}", use_container_width=True,
            type="primary" if dark else "secondary"):
            st.session_state.theme="dark"; st.rerun()
    with c2:
        if st.button(f"☀️ {t['theme_light']}", use_container_width=True,
            type="primary" if not dark else "secondary"):
            st.session_state.theme="light"; st.rerun()

    st.markdown(f"""
    <div class="sb-footer">
        <div class="sb-fp">{t['powered']}</div>
        <div class="sb-fv">{t['version']}</div>
    </div>
    """, unsafe_allow_html=True)

# ─── HERO ───────────────────────────────────────────────
h1_parts = t["hero_h1"].split("\n")
h1_html  = h1_parts[0] + (f'<br><span>{h1_parts[1]}</span>' if len(h1_parts)>1 else "")

st.markdown(f"""
<div class="hero-wrap">
    <div class="hero-overlay"></div>
    <div class="hero-content">
        <div class="hero-eyebrow">{t['hero_eyebrow']}</div>
        <div class="hero-h1">{h1_html}</div>
        <div class="hero-sub">{t['hero_sub']}</div>
        <div class="hero-ctas">
            <a class="cta-primary"  href="/Prediction"     target="_self">{t['hero_cta1']}</a>
            <a class="cta-secondary" href="/Clients_Risque" target="_self">{t['hero_cta2']}</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── KPIs ───────────────────────────────────────────────
st.markdown(f"""
<div class="sec-head">
    <span class="sec-label">{t['kpi_section']}</span>
    <div class="sec-rule"></div>
</div>
""", unsafe_allow_html=True)

try:
    kpis = load_kpis()
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-val">{kpis['total']:,}</div>
            <div class="kpi-lbl">{t['kpi_total']}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-val" style="color:{RED}">{kpis['taux_churn']}%</div>
            <div class="kpi-lbl">{t['kpi_churn']}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-val" style="color:{RED}">{kpis['churners']:,}</div>
            <div class="kpi-lbl">{t['kpi_churners']}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-val" style="color:{GREEN}">{kpis['actifs']:,}</div>
            <div class="kpi-lbl">{t['kpi_actifs']}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-val">{kpis['anciennete']} ans</div>
            <div class="kpi-lbl">{t['kpi_senio']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
except Exception as e:
    st.error(f"Erreur KPIs : {e}")

# ─── MODULE CARDS ────────────────────────────────────────
pred_img  = img_tag("assets/pred_icon.png",  "width:56px;height:56px;border-radius:16px;object-fit:cover;")
risk_img  = img_tag("assets/risk_icon.png",  "width:56px;height:56px;border-radius:16px;object-fit:cover;")
pred_icon = pred_img  if pred_img  else '<div class="mod-img-fallback" style="background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.3);">📊</div>'
risk_icon = risk_img  if risk_img  else '<div class="mod-img-fallback" style="background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);">📋</div>'

st.markdown(f"""
<div class="sec-head">
    <span class="sec-label">{t['mod_section']}</span>
    <div class="sec-rule"></div>
</div>
<div class="mod-grid">
    <div class="mod-card green-card">
        {pred_icon}
        <div class="mod-title">{t['mod1_title']}</div>
        <div class="mod-desc">{t['mod1_desc']}</div>
        <span class="mod-cta">{t['mod1_cta']}</span>
    </div>
    <div class="mod-card red-card">
        {risk_icon}
        <div class="mod-title">{t['mod2_title']}</div>
        <div class="mod-desc">{t['mod2_desc']}</div>
        <span class="mod-cta">{t['mod2_cta']}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── FOOTER ─────────────────────────────────────────────
st.markdown(f'<div class="main-footer">{t["footer"]}</div>', unsafe_allow_html=True)