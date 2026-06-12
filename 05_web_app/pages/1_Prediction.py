import streamlit as st
import sys
import base64
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.model import predict

st.set_page_config(
    page_title="Prédiction — ChurnGuard",
    page_icon="assets/logo.png" if Path("assets/logo.png").exists() else "🏦",
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

# ─── TRANSLATIONS ────────────────────────────────────────
T = {
    "fr": {
        "brand":"ChurnGuard","brand_sub":"Intelligence de Rétention Client",
        "nav_home":"Tableau de Bord","nav_pred":"Prédiction","nav_risk":"Clients à Risque",
        "model_label":"Modèle Actif","powered":"Propulsé par Machine Learning","version":"Version 1.0 · 2025",
        "theme_dark":"Sombre","theme_light":"Clair","lang_label":"Langue","theme_label":"Apparence",
        "page_title":"Prédiction Individuelle",
        "page_sub":"Analysez le profil d'un client et obtenez instantanément sa probabilité de churn",
        "section_profile":"Profil Client",
        "section_finance":"Données Financières",
        "section_compte":"Informations Compte",
        "age":"Âge du client","anciennete":"Ancienneté (années)",
        "marital":"Statut marital","nature":"Type de client",
        "solde":"Solde du compte (TND)","salaire":"Salaire mensuel (TND)",
        "currency":"Devise","kyc":"Score KYC",
        "lob":"Ligne de Business (LOB)","industry":"Secteur d'activité",
        "nationality":"Nationalité","residence":"Pays de résidence",
        "completed":"Dossier complété",
        "btn":"Analyser ce Client",
        "analyzing":"Analyse en cours...",
        "result_title":"Résultat de l'Analyse",
        "proba":"Probabilité de Churn",
        "prediction":"Prédiction",
        "risque":"Niveau de Risque",
        "churner":"Client à Risque",
        "stable":"Client Stable",
        "action_high":"Actions recommandées — Risque Élevé",
        "action_high_items":["Contacter le client dans les 48h", "Proposer une offre de fidélisation personnalisée", "Analyser les motifs potentiels de départ", "Escalader au conseiller principal"],
        "action_low":"Profil stable — Suivi standard recommandé",
        "footer":"© 2025 ESPRIT School of Business · Master 1 Business Analytics · ChurnGuard",
    },
    "en": {
        "brand":"ChurnGuard","brand_sub":"Client Retention Intelligence",
        "nav_home":"Dashboard","nav_pred":"Prediction","nav_risk":"At-Risk Clients",
        "model_label":"Active Model","powered":"Powered by Machine Learning","version":"Version 1.0 · 2025",
        "theme_dark":"Dark","theme_light":"Light","lang_label":"Language","theme_label":"Appearance",
        "page_title":"Individual Prediction",
        "page_sub":"Analyze a client profile and instantly get their churn probability",
        "section_profile":"Client Profile",
        "section_finance":"Financial Data",
        "section_compte":"Account Information",
        "age":"Client age","anciennete":"Seniority (years)",
        "marital":"Marital status","nature":"Client type",
        "solde":"Account balance (TND)","salaire":"Monthly salary (TND)",
        "currency":"Currency","kyc":"KYC Score",
        "lob":"Line of Business (LOB)","industry":"Industry sector",
        "nationality":"Nationality","residence":"Country of residence",
        "completed":"Completed file",
        "btn":"Analyze this Client",
        "analyzing":"Analyzing...",
        "result_title":"Analysis Result",
        "proba":"Churn Probability",
        "prediction":"Prediction",
        "risque":"Risk Level",
        "churner":"At-Risk Client",
        "stable":"Stable Client",
        "action_high":"Recommended Actions — High Risk",
        "action_high_items":["Contact the client within 48h", "Offer a personalized retention offer", "Analyze potential departure motives", "Escalate to senior advisor"],
        "action_low":"Stable profile — Standard follow-up recommended",
        "footer":"© 2025 ESPRIT School of Business · Master 1 Business Analytics · ChurnGuard",
    },
    "ar": {
        "brand":"ChurnGuard","brand_sub":"منصة الاحتفاظ بالعملاء",
        "nav_home":"لوحة التحكم","nav_pred":"التنبؤ","nav_risk":"العملاء المعرضون للخطر",
        "model_label":"النموذج النشط","powered":"مدعوم بالذكاء الاصطناعي","version":"الإصدار 1.0 · 2025",
        "theme_dark":"داكن","theme_light":"فاتح","lang_label":"اللغة","theme_label":"المظهر",
        "page_title":"التنبؤ الفردي",
        "page_sub":"حلل ملف العميل واحصل على احتمالية مغادرته فوراً",
        "section_profile":"ملف العميل",
        "section_finance":"البيانات المالية",
        "section_compte":"معلومات الحساب",
        "age":"عمر العميل","anciennete":"الأقدمية (سنوات)",
        "marital":"الحالة الاجتماعية","nature":"نوع العميل",
        "solde":"رصيد الحساب (دينار)","salaire":"الراتب الشهري (دينار)",
        "currency":"العملة","kyc":"تقييم KYC",
        "lob":"خط الأعمال","industry":"قطاع النشاط",
        "nationality":"الجنسية","residence":"بلد الإقامة",
        "completed":"الملف مكتمل",
        "btn":"تحليل هذا العميل",
        "analyzing":"جارٍ التحليل...",
        "result_title":"نتيجة التحليل",
        "proba":"احتمالية المغادرة",
        "prediction":"التنبؤ",
        "risque":"مستوى الخطر",
        "churner":"عميل معرض للخطر",
        "stable":"عميل مستقر",
        "action_high":"الإجراءات الموصى بها — خطر مرتفع",
        "action_high_items":["التواصل مع العميل خلال 48 ساعة","تقديم عرض احتفاظ مخصص","تحليل أسباب المغادرة المحتملة","إحالة إلى المستشار الرئيسي"],
        "action_low":"ملف مستقر — يُوصى بالمتابعة المعتادة",
        "footer":"© 2025 ESPRIT School of Business · ChurnGuard",
    },
}

if "lang"  not in st.session_state: st.session_state.lang  = "fr"
if "theme" not in st.session_state: st.session_state.theme = "dark"

lang = st.session_state.lang
t    = T[lang]
dark = st.session_state.theme == "dark"
rtl  = lang == "ar"
dir_ = "rtl" if rtl else "ltr"

if dark:
    BG      = "#020817"
    BG2     = "#0a1628"
    CARD    = "rgba(255,255,255,0.03)"
    CARD_BOR= "rgba(255,255,255,0.08)"
    TXT     = "#f1f5f9"
    TXT2    = "rgba(241,245,249,0.5)"
    SIDEBAR = "linear-gradient(180deg,#061953 0%,#040f33 100%)"
    INP_BG  = "rgba(255,255,255,0.05)"
    INP_BOR = "rgba(255,255,255,0.12)"
else:
    BG      = "#f8faff"
    BG2     = "#eef2ff"
    CARD    = "rgba(255,255,255,0.95)"
    CARD_BOR= "rgba(13,43,78,0.12)"
    TXT     = "#0D2B4E"
    TXT2    = "rgba(13,43,78,0.55)"
    SIDEBAR = "linear-gradient(180deg,#0D2B4E 0%,#1a4a7a 100%)"
    INP_BG  = "rgba(13,43,78,0.04)"
    INP_BOR = "rgba(13,43,78,0.15)"

GOLD="#C9982A"; GREEN="#10b981"; RED="#ef4444"
logo_b64 = img_to_b64("assets/logo.png")
logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="width:60px;height:60px;border-radius:16px;object-fit:cover;">' \
    if logo_b64 else '<div style="width:60px;height:60px;background:linear-gradient(135deg,rgba(201,152,42,0.3),rgba(201,152,42,0.1));border:2px solid rgba(201,152,42,0.5);border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:1.8rem;">🏦</div>'

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Cairo:wght@400;600;700;800&display=swap');
*,*::before,*::after{{font-family:{'Cairo' if rtl else 'Inter'},sans-serif;box-sizing:border-box;}}
#MainMenu,header[data-testid="stHeader"],footer,.stDeployButton{{visibility:hidden!important;display:none!important;}}
.stApp{{background:{BG}!important;direction:{dir_};}}
::-webkit-scrollbar{{width:5px;}}
::-webkit-scrollbar-thumb{{background:{GOLD}44;border-radius:10px;}}
::-webkit-scrollbar-thumb:hover{{background:{GOLD};}}

section[data-testid="stSidebar"]{{
    background:{SIDEBAR}!important;
    border-right:1px solid {GOLD}30!important;
    box-shadow:6px 0 40px rgba(0,0,0,0.4)!important;
}}
section[data-testid="stSidebar"]>div:first-child{{padding:0!important;}}
section[data-testid="stSidebar"] *{{color:white!important;}}
section[data-testid="stSidebar"] a[data-testid="stPageLink"]{{
    display:flex!important;align-items:center!important;gap:10px!important;
    padding:11px 14px!important;border-radius:12px!important;margin-bottom:4px!important;
    font-size:0.88rem!important;font-weight:500!important;
    color:rgba(255,255,255,0.65)!important;border:1px solid transparent!important;
    background:transparent!important;transition:all 0.25s ease!important;text-decoration:none!important;
}}
section[data-testid="stSidebar"] a[data-testid="stPageLink"]:hover{{
    background:rgba(255,255,255,0.07)!important;color:white!important;
    border-color:rgba(255,255,255,0.1)!important;padding-left:18px!important;
}}
section[data-testid="stSidebar"] a[data-testid="stPageLink-active"]{{
    background:linear-gradient(135deg,{GOLD}20,{GOLD}08)!important;
    color:{GOLD}!important;border-color:{GOLD}40!important;font-weight:600!important;
}}
section[data-testid="stSidebar"] .stButton button{{
    background:rgba(255,255,255,0.07)!important;border:1px solid rgba(255,255,255,0.12)!important;
    color:rgba(255,255,255,0.7)!important;border-radius:10px!important;
    font-size:0.78rem!important;padding:6px 4px!important;transition:all 0.2s ease!important;
}}
section[data-testid="stSidebar"] .stButton button:hover{{
    background:rgba(255,255,255,0.12)!important;color:white!important;
}}
section[data-testid="stSidebar"] button[kind="primary"]{{
    background:linear-gradient(135deg,{GOLD},{GOLD}aa)!important;
    border-color:{GOLD}!important;color:white!important;font-weight:700!important;
}}
hr{{border-color:rgba(255,255,255,0.07)!important;margin:14px 0!important;}}

/* PAGE HEADER */
.page-header{{
    background:linear-gradient(135deg,{CARD},transparent);
    border:1px solid {CARD_BOR};border-radius:20px;
    padding:36px 40px;margin-bottom:36px;
    display:flex;align-items:center;gap:24px;
    animation:fadeSlide 0.7s ease;
}}
@keyframes fadeSlide{{from{{opacity:0;transform:translateY(-14px)}}to{{opacity:1;transform:translateY(0)}}}}
.page-header-icon{{
    width:64px;height:64px;border-radius:18px;
    background:linear-gradient(135deg,{GOLD}25,{GOLD}08);
    border:1px solid {GOLD}40;
    display:flex;align-items:center;justify-content:center;
    font-size:2rem;flex-shrink:0;
}}
.page-header-title{{font-size:1.8rem;font-weight:800;color:{TXT};margin-bottom:6px;}}
.page-header-sub{{font-size:0.88rem;color:{TXT2};font-weight:400;}}

/* FORM SECTIONS */
.form-section{{
    background:{CARD};border:1px solid {CARD_BOR};
    border-radius:18px;padding:28px;margin-bottom:20px;
    animation:cardRise 0.5s ease forwards;opacity:0;
}}
.form-section:nth-child(1){{animation-delay:0.05s}}
.form-section:nth-child(2){{animation-delay:0.1s}}
.form-section:nth-child(3){{animation-delay:0.15s}}
@keyframes cardRise{{from{{opacity:0;transform:translateY(16px)}}to{{opacity:1;transform:translateY(0)}}}}
.form-sec-title{{
    font-size:0.72rem;font-weight:700;color:{GOLD};
    text-transform:uppercase;letter-spacing:2.5px;
    margin-bottom:20px;padding-bottom:12px;
    border-bottom:1px solid {CARD_BOR};
}}

/* STREAMLIT INPUTS */
.stSlider>div>div>div{{color:{GOLD}!important;}}
.stSelectbox>div>div{{
    background:{INP_BG}!important;border-color:{INP_BOR}!important;
    color:{TXT}!important;border-radius:10px!important;
}}
.stNumberInput>div>div{{
    background:{INP_BG}!important;border-color:{INP_BOR}!important;
    color:{TXT}!important;border-radius:10px!important;
}}
label{{color:{TXT2}!important;font-size:0.82rem!important;font-weight:500!important;}}
.stSlider label{{color:{TXT2}!important;}}

/* PREDICT BUTTON */
div[data-testid="stButton"]>button{{
    background:linear-gradient(135deg,{GOLD},{GOLD}bb)!important;
    color:white!important;font-weight:700!important;font-size:1rem!important;
    border:none!important;border-radius:14px!important;
    padding:16px 32px!important;
    transition:all 0.3s ease!important;
    box-shadow:0 4px 20px {GOLD}33!important;
    width:100%!important;
}}
div[data-testid="stButton"]>button:hover{{
    transform:translateY(-2px)!important;
    box-shadow:0 12px 35px {GOLD}55!important;
}}

/* RESULT */
.result-wrap{{
    animation:resultIn 0.6s cubic-bezier(0.34,1.56,0.64,1);
    margin-top:28px;
}}
@keyframes resultIn{{from{{opacity:0;transform:scale(0.94)}}to{{opacity:1;transform:scale(1)}}}}
.result-card{{
    border-radius:20px;padding:36px;margin-bottom:20px;
    position:relative;overflow:hidden;
}}
.result-card.risk{{
    background:linear-gradient(135deg,rgba(239,68,68,0.08),rgba(239,68,68,0.02));
    border:1px solid {RED}40;
}}
.result-card.safe{{
    background:linear-gradient(135deg,rgba(16,185,129,0.08),rgba(16,185,129,0.02));
    border:1px solid {GREEN}40;
}}
.result-card::before{{
    content:'';position:absolute;top:0;left:0;right:0;height:3px;
}}
.result-card.risk::before{{background:linear-gradient(90deg,{RED},{RED}44,transparent);}}
.result-card.safe::before{{background:linear-gradient(90deg,{GREEN},{GREEN}44,transparent);}}
.result-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:24px;}}
.result-metric{{
    background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
    border-radius:14px;padding:20px;text-align:center;
}}
.result-metric-val{{font-size:2rem;font-weight:800;margin-bottom:6px;line-height:1;}}
.result-metric-lbl{{font-size:0.68rem;color:{TXT2};text-transform:uppercase;letter-spacing:1.5px;}}
.actions-list{{list-style:none;padding:0;margin:0;}}
.actions-list li{{
    display:flex;align-items:center;gap:10px;
    padding:10px 14px;border-radius:10px;
    background:rgba(239,68,68,0.06);border:1px solid rgba(239,68,68,0.15);
    margin-bottom:8px;font-size:0.85rem;color:{TXT};
}}
.actions-list li::before{{
    content:'';width:6px;height:6px;border-radius:50%;
    background:{RED};flex-shrink:0;box-shadow:0 0 6px {RED};
}}

/* SECTION HEADER */
.sec-head{{display:flex;align-items:center;gap:16px;margin:0 0 24px;}}
.sec-label{{font-size:0.72rem;font-weight:700;color:{GOLD};text-transform:uppercase;letter-spacing:3px;white-space:nowrap;}}
.sec-rule{{flex:1;height:1px;background:linear-gradient(90deg,{GOLD}50,transparent);}}

.sb-label{{font-size:0.6rem;color:rgba(255,255,255,0.25);text-transform:uppercase;letter-spacing:2px;padding:0 4px;margin:12px 0 6px;display:block;}}
.sb-model{{background:{GOLD}10;border:1px solid {GOLD}25;border-radius:12px;padding:14px;margin:8px 0;}}
.sb-model-row{{display:flex;justify-content:space-between;margin-bottom:5px;}}
.sb-mk{{font-size:0.68rem;color:rgba(255,255,255,0.35);}}
.sb-mv{{font-size:0.68rem;color:white;font-weight:600;}}
.sb-dot{{width:7px;height:7px;background:{GREEN};border-radius:50%;display:inline-block;box-shadow:0 0 8px {GREEN};animation:blink 2s infinite;}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:0.3}}}}
.sb-footer{{text-align:center;padding:12px 0 4px;border-top:1px solid rgba(255,255,255,0.06);margin-top:12px;}}
.sb-fp{{font-size:0.6rem;color:rgba(255,255,255,0.2);letter-spacing:1.5px;text-transform:uppercase;}}
.sb-fv{{font-size:0.58rem;color:{GOLD}55;letter-spacing:1px;margin-top:3px;}}
.main-footer{{text-align:center;padding:32px 16px;font-size:0.72rem;color:{TXT2};border-top:1px solid {CARD_BOR};letter-spacing:1.5px;text-transform:uppercase;margin-top:48px;}}
</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR ────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:28px 20px 20px;text-align:center;border-bottom:1px solid rgba(201,152,42,0.15);">
        {logo_html}
        <div style="margin-top:12px;font-size:1.05rem;font-weight:800;color:{GOLD};letter-spacing:2px;text-transform:uppercase;">{t['brand']}</div>
        <div style="font-size:0.62rem;color:rgba(255,255,255,0.35);letter-spacing:1px;text-transform:uppercase;margin-top:4px;line-height:1.5;">{t['brand_sub']}</div>
    </div>
    <br>
    """, unsafe_allow_html=True)

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
        <div class="sb-model-row"><span class="sb-mk">ROC-AUC</span><span class="sb-mv">0.9496</span></div>
        <div class="sb-model-row"><span class="sb-mk">F1-Score</span><span class="sb-mv">0.8805</span></div>
        <div class="sb-model-row"><span class="sb-mk">PR-AUC</span><span class="sb-mv">0.9562</span></div>
    </div>
    <hr>
    <span class="sb-label">{t['lang_label'].upper()}</span>
    """, unsafe_allow_html=True)

    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("FR",use_container_width=True,type="primary" if lang=="fr" else "secondary"):
            st.session_state.lang="fr";st.rerun()
    with c2:
        if st.button("EN",use_container_width=True,type="primary" if lang=="en" else "secondary"):
            st.session_state.lang="en";st.rerun()
    with c3:
        if st.button("AR",use_container_width=True,type="primary" if lang=="ar" else "secondary"):
            st.session_state.lang="ar";st.rerun()

    st.markdown(f'<span class="sb-label" style="margin-top:12px;">{t["theme_label"].upper()}</span>',unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        if st.button(f"🌙 {t['theme_dark']}",use_container_width=True,type="primary" if dark else "secondary"):
            st.session_state.theme="dark";st.rerun()
    with c2:
        if st.button(f"☀️ {t['theme_light']}",use_container_width=True,type="primary" if not dark else "secondary"):
            st.session_state.theme="light";st.rerun()

    st.markdown(f"""
    <div class="sb-footer">
        <div class="sb-fp">{t['powered']}</div>
        <div class="sb-fv">{t['version']}</div>
    </div>
    """, unsafe_allow_html=True)

# ─── PAGE HEADER ────────────────────────────────────────
pred_img = img_tag("assets/pred_icon.png","width:64px;height:64px;border-radius:18px;object-fit:cover;")
pred_icon_html = pred_img if pred_img else '<div style="font-size:2rem;">📊</div>'

st.markdown(f"""
<div class="page-header">
    <div class="page-header-icon">{pred_icon_html}</div>
    <div>
        <div class="page-header-title">{t['page_title']}</div>
        <div class="page-header-sub">{t['page_sub']}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── FORM ───────────────────────────────────────────────
col_form, col_result = st.columns([1.1, 0.9], gap="large")

with col_form:
    st.markdown(f"""
    <div class="form-section">
        <div class="form-sec-title">{t['section_profile']}</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            age        = st.slider(t["age"], 18, 80, 35)
            marital    = st.selectbox(t["marital"], ["M","C","D","V","UNKNOWN"])
        with c2:
            anciennete = st.slider(t["anciennete"], 0, 40, 5)
            nature     = st.selectbox(t["nature"], ["PPH","PM","PRO","TRPP","UNKNOWN"])

    st.markdown(f"""
    <div class="form-section" style="margin-top:16px;">
        <div class="form-sec-title">{t['section_finance']}</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            solde    = st.number_input(t["solde"],   -100000, 500000, 1000, step=500)
            currency = st.selectbox(t["currency"], ["TND","EUR","USD","GBP","CAD","UNKNOWN"])
        with c2:
            salaire  = st.number_input(t["salaire"],  0, 50000, 1200, step=100)
            kyc      = st.selectbox(t["kyc"], ["LR","MR","H1","H2","H3","UNKNOWN"])

    st.markdown(f"""
    <div class="form-section" style="margin-top:16px;">
        <div class="form-sec-title">{t['section_compte']}</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            lob         = st.number_input(t["lob"],      1, 20,   4)
            nationality = st.selectbox(t["nationality"], ["TN","FR","US","LY","DZ","UNKNOWN"])
        with c2:
            industry    = st.number_input(t["industry"], 100, 9999, 9000)
            residence   = st.selectbox(t["residence"],   ["TN","FR","US","LY","DZ","UNKNOWN"])

        completed = st.selectbox(t["completed"], ["Y","N","UNKNOWN"])

    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button(t["btn"], type="primary", use_container_width=True)

# ─── RESULT ─────────────────────────────────────────────
with col_result:
    if predict_btn:
        client = {
            "AGE":age,"CUST_SENIORITY_YEARS":anciennete,
            "ACCT_BALANCE":solde,"SALARY":salaire,
            "NATURE_CLIENT":nature,"SCORE_KYC":kyc,
            "MARITAL_STATUS":marital,"CURRENCY":currency,
            "NATIONALITY":nationality,"RESIDENCE":residence,
            "LOB":lob,"INDUSTRY":industry,"COMPLETED_FILE":completed
        }
        with st.spinner(t["analyzing"]):
            result = predict(client)

        p     = result["probabilite"]
        pred  = result["prediction"]
        risk  = result["risque"]
        card_cls = "risk" if pred==1 else "safe"
        val_color = RED if pred==1 else GREEN
        pred_label = t["churner"] if pred==1 else t["stable"]

        st.markdown(f"""
        <div class="result-wrap">
            <div class="sec-head">
                <span class="sec-label">{t['result_title']}</span>
                <div class="sec-rule"></div>
            </div>
            <div class="result-card {card_cls}">
                <div class="result-grid">
                    <div class="result-metric">
                        <div class="result-metric-val" style="color:{val_color}">{p}%</div>
                        <div class="result-metric-lbl">{t['proba']}</div>
                    </div>
                    <div class="result-metric">
                        <div class="result-metric-val" style="color:{val_color};font-size:1.1rem;">{pred_label}</div>
                        <div class="result-metric-lbl">{t['prediction']}</div>
                    </div>
                    <div class="result-metric">
                        <div class="result-metric-val" style="font-size:1.1rem;">{risk}</div>
                        <div class="result-metric-lbl">{t['risque']}</div>
                    </div>
                </div>
        """, unsafe_allow_html=True)

        if pred == 1:
            items_html = "".join([f"<li>{item}</li>" for item in t["action_high_items"]])
            st.markdown(f"""
                <div style="font-size:0.8rem;font-weight:700;color:{RED};
                    text-transform:uppercase;letter-spacing:1.5px;margin-bottom:12px;">
                    {t['action_high']}
                </div>
                <ul class="actions-list">{items_html}</ul>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;
                    padding:14px;background:rgba(16,185,129,0.08);
                    border:1px solid rgba(16,185,129,0.2);border-radius:12px;">
                    <div style="width:8px;height:8px;background:{GREEN};
                        border-radius:50%;box-shadow:0 0 8px {GREEN};flex-shrink:0;"></div>
                    <div style="font-size:0.85rem;color:{TXT};">{t['action_low']}</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="height:400px;display:flex;flex-direction:column;
            align-items:center;justify-content:center;
            background:{CARD};border:1px solid {CARD_BOR};
            border-radius:20px;text-align:center;padding:40px;
            animation:fadeSlide 0.7s ease;">
            <div style="width:80px;height:80px;border-radius:20px;
                background:linear-gradient(135deg,{GOLD}20,{GOLD}05);
                border:1px solid {GOLD}30;display:flex;align-items:center;
                justify-content:center;font-size:2.5rem;margin-bottom:20px;">📊</div>
            <div style="font-size:1.1rem;font-weight:700;color:{TXT};margin-bottom:10px;">
                {t['page_title']}
            </div>
            <div style="font-size:0.85rem;color:{TXT2};line-height:1.6;">
                {t['page_sub']}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown(f'<div class="main-footer">{t["footer"]}</div>', unsafe_allow_html=True)