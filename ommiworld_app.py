import streamlit as st
import streamlit.components.v1 as components
from groq import Groq
import os, re, random, base64
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
if API_KEY:
    client = Groq(api_key=API_KEY)

st.set_page_config(
    page_title="Ommi world AI Assistant",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "prefill" not in st.session_state:
    st.session_state.prefill = ""

# ── Hero video assets ─────────────────────────────────────────────────────────
# The video is embedded directly into the page (no "static" folder or server
# config needed). Drop hero_video.mp4 / hero_poster.jpg in ANY of these spots:
#   - the same folder as this script
#   - a "media", "static", or "assets" subfolder next to this script
HERO_VIDEO_FILE  = "hero_video.mp4"    # swap to "hero_video_alt.mp4" for the other clip
HERO_POSTER_FILE = "hero_poster.jpg"   # swap to "hero_poster_alt.jpg" to match

_SCRIPT_DIR   = Path(__file__).parent
_SEARCH_DIRS  = [_SCRIPT_DIR, _SCRIPT_DIR / "media", _SCRIPT_DIR / "static", _SCRIPT_DIR / "assets"]


def find_asset(filename: str):
    """Return the first existing path for `filename` across the search folders, else None."""
    for folder in _SEARCH_DIRS:
        p = folder / filename
        if p.exists():
            return p
    return None


@st.cache_data(show_spinner=False)
def b64_of(path_str: str) -> str:
    """Base64-encode a file (cached so it only happens once per file)."""
    return base64.b64encode(Path(path_str).read_bytes()).decode()


def md_to_html(text: str) -> str:
    text = re.sub(r"^### (.+)$", r'<h4 style="color:#6E5A8E;margin:16px 0 6px 0;">\1</h4>', text, flags=re.MULTILINE)
    text = re.sub(r"^## (.+)$",  r'<h3 style="color:#A85574;margin:18px 0 8px 0;">\1</h3>',  text, flags=re.MULTILINE)
    text = re.sub(r"^# (.+)$",   r'<h2 style="color:#A85574;margin:20px 0 10px 0;">\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r"\*\*(.*?)\*\*", r'<strong style="color:#A85574;">\1</strong>', text)
    text = re.sub(r"\*(.*?)\*",     r"<em>\1</em>", text)

    def make_ul(m):
        items = re.findall(r"^[ \t]*[•\-\*][ \t]+(.+)$", m.group(0), re.MULTILINE)
        lis = "".join(f'<li style="margin-bottom:6px;">{i}</li>' for i in items)
        return f'<ul style="padding-left:22px;margin:10px 0;">{lis}</ul>'

    def make_ol(m):
        items = re.findall(r"^\d+[.)]\s+(.+)$", m.group(0), re.MULTILINE)
        lis = "".join(f'<li style="margin-bottom:6px;">{i}</li>' for i in items)
        return f'<ol style="padding-left:22px;margin:10px 0;">{lis}</ol>'

    text = re.sub(r"(?m)(^[ \t]*[•\-\*][ \t]+.+$\n?)+", make_ul, text)
    text = re.sub(r"(?m)(^\d+[.)]\s+.+$\n?)+",          make_ol, text)

    out = []
    for p in text.split("\n\n"):
        p = p.strip()
        if not p:
            continue
        out.append(p if p.startswith("<") else
                   f'<p style="line-height:1.78;margin:8px 0;color:#3E3140;">{p.replace(chr(10),"<br>")}</p>')
    return "\n".join(out)


# ── CSS ───────────────────────────────────────────────────────────────────────
# Soft palette:
#   cream  #FBF6F3  | blush #F8E4EC | lilac #ECE4FA
#   rose   #C2718C  (primary accent)   rose-deep #A85574 (text on light)
#   plum   #8E76B0 / #6E5A8E (secondary)   ink #3E3140 (body)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Nunito:wght@400;600;700;800;900&display=swap');

* { font-family: 'Nunito', sans-serif !important; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, .stDeployButton,
[data-testid="stDecoration"],
[data-testid="stToolbar"] { visibility: hidden !important; display: none !important; }
header[data-testid="stHeader"] { background: transparent !important; }

/* ── Soft animated background ── */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(-45deg, #FBF6F3, #F7EAF1, #FBF4F8, #EEE7FA);
    background-size: 400% 400%;
    animation: bgShift 26s ease infinite;
    min-height: 100vh;
}
@keyframes bgShift {
    0%,100% { background-position: 0% 50%; }
    50%      { background-position: 100% 50%; }
}
[data-testid="stAppViewContainer"]::before {
    content: ''; position: fixed;
    width: 620px; height: 620px; border-radius: 50%;
    top: -250px; left: -250px;
    background: radial-gradient(circle, rgba(194,113,140,0.10) 0%, transparent 65%);
    pointer-events: none; z-index: 0;
    animation: blob1 16s ease-in-out infinite;
}
[data-testid="stAppViewContainer"]::after {
    content: ''; position: fixed;
    width: 540px; height: 540px; border-radius: 50%;
    bottom: -200px; right: -200px;
    background: radial-gradient(circle, rgba(142,118,176,0.09) 0%, transparent 65%);
    pointer-events: none; z-index: 0;
    animation: blob2 20s ease-in-out infinite;
}
@keyframes blob1 {
    0%,100% { transform: translate(0,0) scale(1); }
    40%     { transform: translate(80px,65px) scale(1.08); }
    70%     { transform: translate(-35px,95px) scale(0.96); }
}
@keyframes blob2 {
    0%,100% { transform: translate(0,0) scale(1); }
    40%     { transform: translate(-65px,-50px) scale(1.05); }
    70%     { transform: translate(50px,-30px) scale(0.93); }
}
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"] { position: relative; z-index: 1; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FBEAF1 0%, #EFE7FB 100%) !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] label { color: #4A3A52 !important; }

/* Sidebar example buttons */
[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.66) !important;
    color: #4A3A52 !important;
    border: 1.5px solid rgba(194,113,140,0.22) !important;
    border-radius: 12px !important;
    font-size: 0.83em !important; font-weight: 700 !important;
    padding: 7px 12px !important; width: 100% !important;
    box-shadow: none !important; text-align: left !important;
    letter-spacing: 0 !important;
    transition: all 0.18s !important;
    transform: none !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(194,113,140,0.10) !important;
    border-color: rgba(194,113,140,0.42) !important;
    transform: translateX(4px) !important;
    box-shadow: none !important;
}

/* ── Global text ── */
p, li, span { color: #3E3140; }
h1, h2, h3, h4, h5, h6 { color: #3E3140; }
[data-testid="stMarkdownContainer"] p { color: #3E3140 !important; }

/* ── Main buttons (soft gradient) ── */
.stButton > button {
    background: linear-gradient(135deg, #C2718C 0%, #8E76B0 100%) !important;
    color: white !important; border: none !important;
    border-radius: 50px !important; font-weight: 800 !important;
    font-size: 1.05em !important; padding: 13px 28px !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 6px 20px rgba(194,113,140,0.30) !important;
    letter-spacing: 0.3px !important;
}
.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 26px rgba(142,118,176,0.42) !important;
}
.stButton > button:active { transform: scale(0.97) !important; }

/* ── Hero banner with video ── */
.hero {
    position: relative; overflow: hidden;
    border-radius: 26px; min-height: 340px;
    display: flex; align-items: center; justify-content: center;
    text-align: center; margin-bottom: 30px;
    box-shadow: 0 14px 44px rgba(142,118,176,0.22);
}
.hero-vid {
    position: absolute; inset: 0;
    width: 100%; height: 100%;
    object-fit: cover; z-index: 0;
}
.hero-veil {
    position: absolute; inset: 0; z-index: 1;
    background:
        linear-gradient(135deg, rgba(194,113,140,0.70) 0%, rgba(110,90,142,0.66) 100%),
        radial-gradient(circle at 70% 20%, rgba(255,255,255,0.16) 0%, transparent 55%);
}
.hero-content {
    position: relative; z-index: 2;
    padding: 50px 36px;
    animation: slideDown 0.65s ease-out;
}
.hero-eyebrow {
    font-size: 0.74em; font-weight: 800; letter-spacing: 3px;
    color: rgba(255,255,255,0.82) !important; margin: 0 0 14px;
}
.hero-title {
    font-family: 'Fraunces', serif !important;
    font-size: 2.7em; font-weight: 600; color: white !important;
    text-shadow: 0 3px 18px rgba(58,40,58,0.35);
    margin: 0 0 10px; line-height: 1.1;
}
.hero-sub {
    font-size: 1.12em; font-weight: 700;
    color: rgba(255,255,255,0.92) !important; margin: 0 0 6px;
}
.hero-slogan {
    font-size: 0.94em; font-style: italic;
    color: rgba(255,255,255,0.78) !important; margin: 0 0 22px;
}
.pill {
    display: inline-block;
    background: rgba(255,255,255,0.20);
    border: 1px solid rgba(255,255,255,0.34);
    border-radius: 20px; padding: 5px 14px;
    font-size: 0.77em; font-weight: 700;
    color: white !important; margin: 3px;
    backdrop-filter: blur(6px);
}
/* Fallback hero when the video file is missing */
.hero-fallback {
    background: linear-gradient(135deg, #C2718C 0%, #8E76B0 100%);
}

/* ── Input label ── */
.inp-label {
    font-size: 1.08em; font-weight: 800;
    color: #8E76B0 !important; margin: 0 0 10px;
}

/* ── Textarea ── */
.stTextArea textarea {
    border: 2px solid rgba(194,113,140,0.20) !important;
    border-radius: 16px !important; font-size: 0.97em !important;
    font-weight: 500 !important; padding: 14px 16px !important;
    color: #3E3140 !important; resize: none !important;
    background: rgba(255,255,255,0.94) !important;
    box-shadow: 0 2px 10px rgba(194,113,140,0.07) !important;
    transition: border-color 0.22s, box-shadow 0.22s !important;
}
.stTextArea textarea:focus {
    border-color: #C2718C !important;
    box-shadow: 0 0 0 3px rgba(194,113,140,0.13),
                0 2px 10px rgba(194,113,140,0.07) !important;
    outline: none !important;
}
.stTextArea textarea::placeholder { color: rgba(110,90,142,0.42) !important; }
.stTextArea label { display: none !important; }

/* ── Language radio ── */
div[data-testid="stRadio"] > div {
    display: flex !important; gap: 3px !important;
    background: rgba(194,113,140,0.08) !important;
    border-radius: 50px !important; padding: 4px !important;
    border: 1px solid rgba(194,113,140,0.14) !important;
    width: fit-content !important; margin: 0 auto !important;
}
div[data-testid="stRadio"] [data-baseweb="radio"] { display: none !important; }
div[data-testid="stRadio"] label {
    border-radius: 50px !important; padding: 7px 20px !important;
    font-weight: 700 !important; font-size: 0.83em !important;
    cursor: pointer !important; background: transparent !important;
    color: #A85574 !important; border: none !important;
    transition: all 0.2s !important; margin: 0 !important; white-space: nowrap !important;
}
div[data-testid="stRadio"] label:has(input:checked) {
    background: linear-gradient(135deg, #C2718C, #8E76B0) !important;
    color: white !important;
    box-shadow: 0 3px 12px rgba(194,113,140,0.34) !important;
}
div[data-testid="stRadio"] label p,
div[data-testid="stRadio"] label span,
div[data-testid="stRadio"] label div {
    color: inherit !important; font-size: inherit !important;
    font-weight: inherit !important; background: transparent !important;
    margin: 0 !important; padding: 0 !important;
}

/* ── Checkbox ── */
.stCheckbox label { font-weight: 700 !important; font-size: 0.9em !important; }
.stCheckbox label span { color: #6B7280 !important; }

/* ── Response card ── */
.res-card {
    background: rgba(255,255,255,0.94);
    backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(194,113,140,0.12); border-radius: 22px;
    overflow: hidden; margin-top: 24px;
    box-shadow: 0 10px 40px rgba(142,118,176,0.12), 0 1px 4px rgba(194,113,140,0.05);
    animation: cardIn 0.5s cubic-bezier(0.22,1,0.36,1);
}
@keyframes cardIn {
    from { transform: translateY(20px); opacity: 0; }
    to   { transform: translateY(0);    opacity: 1; }
}
.res-head {
    background: linear-gradient(135deg, #C2718C 0%, #8E76B0 100%);
    padding: 16px 26px; display: flex; align-items: center; gap: 10px;
}
.res-head span {
    color: white !important; font-weight: 700; font-size: 1.08em;
    font-family: 'Fraunces', serif !important;
}
.res-body { padding: 26px 30px; }
.res-body p  { color: #3E3140 !important; line-height: 1.8; }
.res-body li { color: #3E3140 !important; }
.res-body strong { color: #A85574 !important; }
.res-body h2, .res-body h3 { color: #A85574 !important; }
.res-body h4 { color: #6E5A8E !important; }
.arabic-wrap { direction: rtl !important; text-align: right !important; }

/* ── Alerts ── */
.stAlert { border-radius: 14px !important; }

/* ── HR ── */
hr { border: none !important; border-top: 1px solid rgba(194,113,140,0.12) !important;
     margin: 20px 0 !important; }

/* ── Animations ── */
@keyframes slideDown {
    from { transform: translateY(-22px); opacity: 0; }
    to   { transform: translateY(0);     opacity: 1; }
}

/* ── Respect reduced-motion preference ── */
@media (prefers-reduced-motion: reduce) {
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"]::before,
    [data-testid="stAppViewContainer"]::after,
    .hero-content, .res-card { animation: none !important; }
}
</style>
""", unsafe_allow_html=True)


# ── CONTENT ───────────────────────────────────────────────────────────────────
content_en = {
    "slogans": [
        "Because every mom deserves a little magic ✨",
        "Your baby, your love, our support 💝",
        "Every milestone matters — we're here for them all 🌟",
        "Shop smarter, parent better 🛍️",
        "Making motherhood moments magical 💕",
        "Where parenting meets possibility 🌈",
    ],
    "input_label": "Describe your baby's situation",
    "placeholder": "e.g., My 6-month-old is starting solids and I need the right feeding equipment...",
    "checkbox":    "Also show response in Arabic",
    "button":      "✨  Get Recommendations",
    "spinner":     "Analyzing your needs...",
    "success":     "Your personalized recommendations are ready!",
    "warning":     "Please describe your baby's situation first.",
    "res_title":   "🛍️  Recommendations for You",
    "ar_title":    "🛍️  التوصيات بالعربية",
}
content_ar = {
    "slogans": [
        "لأن كل أم تستحق قليلاً من السحر ✨",
        "طفلك، حبك، دعمنا 💝",
        "كل مرحلة مهمة — نحن هنا من أجلك 🌟",
        "تسوقي بذكاء، كوني أماً أفضل 🛍️",
        "صنع لحظات الأمومة سحرية 💕",
    ],
    "input_label": "صفي وضع طفلك",
    "placeholder": "مثال: طفلي عمره 6 أشهر يبدأ الأطعمة الصلبة وأحتاج معدات التغذية المناسبة...",
    "checkbox":    "عرض الرد أيضاً باللغة العربية",
    "button":      "✨  احصلي على التوصيات",
    "spinner":     "جاري تحليل احتياجاتك...",
    "success":     "إليك توصياتك الشخصية!",
    "warning":     "يرجى وصف وضع طفلك أولاً.",
    "res_title":   "🛍️  توصياتنا لك",
    "ar_title":    "🛍️  الترجمة العربية",
}


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:10px 0 22px;
                border-bottom:1px solid rgba(194,113,140,0.2); margin-bottom:18px;">
        <div style="font-size:3em; line-height:1.1;">👶</div>
        <div style="font-family:'Fraunces',serif; font-size:1.4em; font-weight:600; color:#A85574 !important;">Ommi world</div>
        <div style="font-size:0.84em; font-weight:700; color:#8E76B0 !important;">
            AI Parenting Assistant
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**🌍 Language**")
    selected_language = st.radio(
        "", ["English 🇬🇧", "العربية 🇸🇦", "Both 🌐"],
        key="language_selector", label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("**💡 Quick Examples**")
    examples = [
        ("🌙  3-month-old not sleeping",   "My 3-month-old isn't sleeping well at night"),
        ("🥣  6-month-old starting solids", "My 6-month-old is ready to start solids"),
        ("🌡️  1-year-old has high fever",  "My 1-year-old has had a high fever for 2 days"),
        ("🧸  Toys for 2-year-old",        "Best developmental toys for a 2-year-old"),
        ("👶  Newborn essentials",         "Complete newborn essentials checklist"),
        ("🤒  Colic / reflux",             "My newborn has colic and won't stop crying"),
    ]
    for label, val in examples:
        if st.button(label, key=f"ex_{hash(val)}", use_container_width=True):
            st.session_state.prefill = val
            st.rerun()

    st.markdown("---")
    st.markdown("""
**📌 Tips for best results**
- Mention your baby's exact age
- Describe symptoms clearly
- Include developmental stage
- Ask specific questions
""")
    st.markdown("""
    <div style="text-align:center; padding:14px 0 4px; margin-top:8px;
                border-top:1px solid rgba(194,113,140,0.15);
                font-size:0.75em; color:rgba(110,90,142,0.6) !important;">
        Powered by Llama 3.3 70B · Groq
    </div>
    """, unsafe_allow_html=True)


# ── LANGUAGE STATE ────────────────────────────────────────────────────────────
is_en = selected_language in ["English 🇬🇧", "Both 🌐"]
is_ar = selected_language in ["العربية 🇸🇦", "Both 🌐"]
c = content_en if is_en else content_ar


# ── HERO ──────────────────────────────────────────────────────────────────────
slogan = random.choice(c["slogans"])
title  = "Welcome to Ommi world" if is_en else "أهلاً بك في مامز وورلد"
sub    = "Your gentle AI companion for every newborn moment" if is_en else "رفيقك الذكي اللطيف في كل لحظة مع مولودك"
eyebrow = "Ommi world · AI COMPANION" if is_en else "مامز وورلد · رفيق ذكي"

video_path  = find_asset(HERO_VIDEO_FILE)
poster_path = find_asset(HERO_POSTER_FILE)

pills = (
    '<span class="pill">🤖 AI-Powered</span>'
    '<span class="pill">🌍 Bilingual</span>'
    '<span class="pill">👶 Baby Expert</span>'
    '<span class="pill">⚡ Free &amp; Fast</span>'
)

# Self-contained CSS for the iframe hero (the iframe is isolated from the page,
# so its styles must live here, not in the global st.markdown block above).
_HERO_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Nunito:wght@700;800&display=swap');
* { margin:0; padding:0; box-sizing:border-box; }
body { background:transparent; font-family:'Nunito',sans-serif; }
.hero { position:relative; height:340px; border-radius:26px; overflow:hidden;
        display:flex; align-items:center; justify-content:center; text-align:center;
        box-shadow:0 14px 44px rgba(142,118,176,0.22); }
.hero video { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; z-index:0; }
.veil { position:absolute; inset:0; z-index:1;
        background:linear-gradient(135deg, rgba(194,113,140,0.70) 0%, rgba(110,90,142,0.66) 100%),
                   radial-gradient(circle at 70% 20%, rgba(255,255,255,0.16) 0%, transparent 55%); }
.content { position:relative; z-index:2; padding:0 36px; animation:rise .65s ease-out; }
.eyebrow { font-size:0.74rem; font-weight:800; letter-spacing:3px; color:rgba(255,255,255,0.82); margin-bottom:14px; }
.title { font-family:'Fraunces',serif; font-size:2.7rem; font-weight:600; color:#fff;
         text-shadow:0 3px 18px rgba(58,40,58,0.35); margin-bottom:10px; line-height:1.1; }
.sub { font-size:1.12rem; font-weight:700; color:rgba(255,255,255,0.92); margin-bottom:6px; }
.slogan { font-size:0.94rem; font-style:italic; color:rgba(255,255,255,0.78); margin-bottom:22px; }
.pill { display:inline-block; background:rgba(255,255,255,0.20); border:1px solid rgba(255,255,255,0.34);
        border-radius:20px; padding:5px 14px; font-size:0.77rem; font-weight:700; color:#fff; margin:3px; }
@keyframes rise { from { transform:translateY(-18px); opacity:0; } to { transform:translateY(0); opacity:1; } }
@media (prefers-reduced-motion: reduce) { .content { animation:none; } }
</style>
"""

if video_path:
    vid_uri = f"data:video/mp4;base64,{b64_of(str(video_path))}"
    poster_attr = f' poster="data:image/jpeg;base64,{b64_of(str(poster_path))}"' if poster_path else ""
    hero_body = (
        '<body><div class="hero">'
        f'<video autoplay loop muted playsinline{poster_attr}>'
        f'<source src="{vid_uri}" type="video/mp4"></video>'
        '<div class="veil"></div>'
        '<div class="content">'
        f'<div class="eyebrow">{eyebrow}</div>'
        f'<div class="title">{title} 👶</div>'
        f'<div class="sub">{sub}</div>'
        f'<div class="slogan">{slogan}</div>'
        f'<div>{pills}</div>'
        '</div></div></body>'
    )
    hero_html = "<!doctype html><html><head><meta charset='utf-8'>" + _HERO_CSS + "</head>" + hero_body + "</html>"
    components.html(hero_html, height=360)
else:
    # No video file found — render the soft gradient hero instead.
    st.markdown(
        f'<div class="hero hero-fallback">'
        f'<div class="hero-content">'
        f'<div class="hero-eyebrow">{eyebrow}</div>'
        f'<div class="hero-title">{title} 👶</div>'
        f'<div class="hero-sub">{sub}</div>'
        f'<div class="hero-slogan">{slogan}</div>'
        f'<div class="hero-pills">{pills}</div>'
        f'</div></div>',
        unsafe_allow_html=True,
    )
    st.caption(
        f"🎬 Hero video not found. Place **{HERO_VIDEO_FILE}** next to the app "
        f"(or in a media/static/assets subfolder). Looked in: "
        + " · ".join(str(d) for d in _SEARCH_DIRS)
    )


# ── INPUT ─────────────────────────────────────────────────────────────────────
_, col, _ = st.columns([1, 10, 1])
with col:
    st.markdown(f'<p class="inp-label">💭 {c["input_label"]}</p>', unsafe_allow_html=True)

    user_input = st.text_area(
        "",
        value=st.session_state.prefill,
        height=125,
        placeholder=c["placeholder"],
        label_visibility="collapsed",
        key="user_input",
    )

    chk_col, btn_col = st.columns([3, 2])
    with chk_col:
        show_arabic = st.checkbox(f"🌍  {c['checkbox']}", value=is_ar)
    with btn_col:
        submit = st.button(c["button"], use_container_width=True)


# ── RESPONSE ──────────────────────────────────────────────────────────────────
    if submit:
        if not API_KEY:
            st.error("⚠️  GROQ_API_KEY not found. Create a `.env` file with `GROQ_API_KEY=your_key`.")
        elif not user_input.strip():
            st.warning(f"⚠️  {c['warning']}")
        else:
            with st.spinner(c["spinner"]):
                prompt = f"""
You are an expert shopping assistant for Ommi world, a leading Middle Eastern e-commerce site for mothers and children.
A parent has come to you with this situation: "{user_input}"

Provide a warm, empathetic opening. Then list 3–5 specific product categories they should look for on Ommi world.
Format each product as a bullet point starting with "- " with the category name in **bold**, followed by a brief explanation.

If the situation involves illness, fever, pain, or discomfort:
1. Gently urge the parent to contact a pediatrician or pharmacist before giving any medicine.
2. Point to general baby-care categories on Ommi world (e.g. thermometers, saline drops, comfort items) WITHOUT specifying medication names or dosages.
3. Make clear you are a shopping guide, not a medical professional.

Keep the tone warm, helpful, and reassuring. Always remind parents to consult a pediatrician before giving any medication.
"""
                if show_arabic:
                    prompt += "\n\nIMPORTANT: After your full English response, add exactly '---ARABIC---' on its own line, then provide the complete Arabic translation."

                try:
                    resp = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "You are a helpful, empathetic shopping assistant for Ommi world. You are not a doctor and never give medication names or dosages; you always defer medical questions to a pediatrician."},
                            {"role": "user",   "content": prompt},
                        ],
                        model="llama-3.3-70b-versatile",
                    )
                    full = resp.choices[0].message.content

                    if show_arabic and "---ARABIC---" in full:
                        en_part, ar_part = full.split("---ARABIC---", 1)
                    else:
                        en_part, ar_part = full, None

                    st.success(f"✅  {c['success']}")

                    # English card
                    st.markdown(f"""
<div class="res-card">
    <div class="res-head"><span>{content_en["res_title"]}</span></div>
    <div class="res-body">{md_to_html(en_part.strip())}</div>
</div>
""", unsafe_allow_html=True)

                    # Arabic card
                    if show_arabic and ar_part:
                        st.markdown(f"""
<div class="res-card" style="margin-top:16px;">
    <div class="res-head"><span>{content_en["ar_title"]}</span></div>
    <div class="res-body arabic-wrap">{md_to_html(ar_part.strip())}</div>
</div>
""", unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"An error occurred: {e}")

st.markdown('<div style="height:40px"></div>', unsafe_allow_html=True)