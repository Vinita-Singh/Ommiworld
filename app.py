import streamlit as st
from groq import Groq
import os, re, random
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
if API_KEY:
    client = Groq(api_key=API_KEY)

st.set_page_config(
    page_title="Mumzworld AI Assistant",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "prefill" not in st.session_state:
    st.session_state.prefill = ""


def md_to_html(text: str) -> str:
    text = re.sub(r"^### (.+)$", r'<h4 style="color:#6A1B9A;margin:16px 0 6px 0;">\1</h4>', text, flags=re.MULTILINE)
    text = re.sub(r"^## (.+)$",  r'<h3 style="color:#AD1457;margin:18px 0 8px 0;">\1</h3>',  text, flags=re.MULTILINE)
    text = re.sub(r"^# (.+)$",   r'<h2 style="color:#AD1457;margin:20px 0 10px 0;">\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r"\*\*(.*?)\*\*", r'<strong style="color:#AD1457;">\1</strong>', text)
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
                   f'<p style="line-height:1.78;margin:8px 0;color:#1a0533;">{p.replace(chr(10),"<br>")}</p>')
    return "\n".join(out)


# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

* { font-family: 'Nunito', sans-serif !important; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, .stDeployButton,
[data-testid="stDecoration"],
[data-testid="stToolbar"] { visibility: hidden !important; display: none !important; }
header[data-testid="stHeader"] { background: transparent !important; }

/* ── Animated background ── */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(-45deg, #FFF0F7, #F3E8FF, #FFF5FA, #EEE8FF);
    background-size: 400% 400%;
    animation: bgShift 20s ease infinite;
    min-height: 100vh;
}
@keyframes bgShift {
    0%,100% { background-position: 0% 50%; }
    50%      { background-position: 100% 50%; }
}
[data-testid="stAppViewContainer"]::before {
    content: ''; position: fixed;
    width: 650px; height: 650px; border-radius: 50%;
    top: -260px; left: -260px;
    background: radial-gradient(circle, rgba(173,20,87,0.13) 0%, transparent 65%);
    pointer-events: none; z-index: 0;
    animation: blob1 14s ease-in-out infinite;
}
[data-testid="stAppViewContainer"]::after {
    content: ''; position: fixed;
    width: 560px; height: 560px; border-radius: 50%;
    bottom: -200px; right: -200px;
    background: radial-gradient(circle, rgba(106,27,154,0.11) 0%, transparent 65%);
    pointer-events: none; z-index: 0;
    animation: blob2 18s ease-in-out infinite;
}
@keyframes blob1 {
    0%,100% { transform: translate(0,0) scale(1); }
    40%     { transform: translate(85px,70px) scale(1.1); }
    70%     { transform: translate(-40px,100px) scale(0.95); }
}
@keyframes blob2 {
    0%,100% { transform: translate(0,0) scale(1); }
    40%     { transform: translate(-70px,-55px) scale(1.06); }
    70%     { transform: translate(55px,-35px) scale(0.92); }
}
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"] { position: relative; z-index: 1; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FFE8F2 0%, #EDE0FF 100%) !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] label { color: #3D0066 !important; }

/* Sidebar example buttons */
[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.62) !important;
    color: #3D0066 !important;
    border: 1.5px solid rgba(173,20,87,0.22) !important;
    border-radius: 10px !important;
    font-size: 0.83em !important; font-weight: 700 !important;
    padding: 7px 12px !important; width: 100% !important;
    box-shadow: none !important; text-align: left !important;
    letter-spacing: 0 !important;
    transition: all 0.18s !important;
    transform: none !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(173,20,87,0.09) !important;
    border-color: rgba(173,20,87,0.45) !important;
    transform: translateX(4px) !important;
    box-shadow: none !important;
}

/* ── Global text ── */
p, li, span { color: #1a0533; }
h1, h2, h3, h4, h5, h6 { color: #1a0533; }
[data-testid="stMarkdownContainer"] p { color: #1a0533 !important; }

/* ── Main buttons (default — gradient) ── */
.stButton > button {
    background: linear-gradient(135deg, #AD1457 0%, #6A1B9A 100%) !important;
    color: white !important; border: none !important;
    border-radius: 50px !important; font-weight: 800 !important;
    font-size: 1.05em !important; padding: 13px 28px !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 6px 22px rgba(173,20,87,0.38) !important;
    letter-spacing: 0.3px !important;
}
.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 28px rgba(173,20,87,0.55) !important;
}
.stButton > button:active { transform: scale(0.97) !important; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #AD1457 0%, #6A1B9A 100%);
    border-radius: 22px; padding: 48px 40px 42px;
    text-align: center; margin-bottom: 30px;
    box-shadow: 0 14px 44px rgba(173,20,87,0.3);
    position: relative; overflow: hidden;
}
.hero::before {
    content: ''; position: absolute;
    width: 360px; height: 360px;
    background: radial-gradient(circle, rgba(255,255,255,0.12) 0%, transparent 65%);
    top: -110px; right: -70px; border-radius: 50%;
}
.hero::after {
    content: ''; position: absolute;
    width: 240px; height: 240px;
    background: radial-gradient(circle, rgba(255,255,255,0.07) 0%, transparent 65%);
    bottom: -70px; left: -50px; border-radius: 50%;
}
.hero-title {
    font-size: 2.6em; font-weight: 900; color: white !important;
    text-shadow: 0 3px 14px rgba(0,0,0,0.2);
    margin: 0 0 9px; position: relative; z-index: 1;
    animation: slideDown 0.65s ease-out;
}
.hero-sub {
    font-size: 1.1em; font-weight: 700;
    color: rgba(255,255,255,0.88) !important;
    margin: 0 0 5px; position: relative; z-index: 1;
}
.hero-slogan {
    font-size: 0.93em; font-style: italic;
    color: rgba(255,255,255,0.7) !important;
    margin: 0 0 20px; position: relative; z-index: 1;
}
.pill {
    display: inline-block;
    background: rgba(255,255,255,0.18);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 20px; padding: 4px 13px;
    font-size: 0.77em; font-weight: 700;
    color: white !important; margin: 3px;
    backdrop-filter: blur(6px);
    position: relative; z-index: 1;
}

/* ── Input label ── */
.inp-label {
    font-size: 1.08em; font-weight: 800;
    color: #7B1FA2 !important; margin: 0 0 10px;
}

/* ── Textarea ── */
.stTextArea textarea {
    border: 2px solid rgba(173,20,87,0.2) !important;
    border-radius: 16px !important; font-size: 0.97em !important;
    font-weight: 500 !important; padding: 14px 16px !important;
    color: #1a0533 !important; resize: none !important;
    background: rgba(255,255,255,0.92) !important;
    box-shadow: 0 2px 10px rgba(173,20,87,0.07) !important;
    transition: border-color 0.22s, box-shadow 0.22s !important;
}
.stTextArea textarea:focus {
    border-color: #AD1457 !important;
    box-shadow: 0 0 0 3px rgba(173,20,87,0.11),
                0 2px 10px rgba(173,20,87,0.07) !important;
    outline: none !important;
}
.stTextArea textarea::placeholder { color: rgba(61,0,102,0.36) !important; }
.stTextArea label { display: none !important; }

/* ── Language radio ── */
div[data-testid="stRadio"] > div {
    display: flex !important; gap: 3px !important;
    background: rgba(173,20,87,0.07) !important;
    border-radius: 50px !important; padding: 4px !important;
    border: 1px solid rgba(173,20,87,0.13) !important;
    width: fit-content !important; margin: 0 auto !important;
}
div[data-testid="stRadio"] [data-baseweb="radio"] { display: none !important; }
div[data-testid="stRadio"] label {
    border-radius: 50px !important; padding: 7px 20px !important;
    font-weight: 700 !important; font-size: 0.83em !important;
    cursor: pointer !important; background: transparent !important;
    color: #AD1457 !important; border: none !important;
    transition: all 0.2s !important; margin: 0 !important; white-space: nowrap !important;
}
div[data-testid="stRadio"] label:has(input:checked) {
    background: linear-gradient(135deg, #AD1457, #6A1B9A) !important;
    color: white !important;
    box-shadow: 0 3px 12px rgba(173,20,87,0.38) !important;
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
    background: rgba(255,255,255,0.92);
    backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(173,20,87,0.12); border-radius: 22px;
    overflow: hidden; margin-top: 24px;
    box-shadow: 0 10px 40px rgba(173,20,87,0.12), 0 1px 4px rgba(173,20,87,0.05);
    animation: cardIn 0.5s cubic-bezier(0.22,1,0.36,1);
}
@keyframes cardIn {
    from { transform: translateY(20px); opacity: 0; }
    to   { transform: translateY(0);    opacity: 1; }
}
.res-head {
    background: linear-gradient(135deg, #AD1457 0%, #6A1B9A 100%);
    padding: 16px 26px; display: flex; align-items: center; gap: 10px;
}
.res-head span { color: white !important; font-weight: 800; font-size: 1.04em; }
.res-body { padding: 26px 30px; }
.res-body p  { color: #374151 !important; line-height: 1.8; }
.res-body li { color: #374151 !important; }
.res-body strong { color: #AD1457 !important; }
.res-body h2, .res-body h3 { color: #AD1457 !important; }
.res-body h4 { color: #6A1B9A !important; }
.arabic-wrap { direction: rtl !important; text-align: right !important; }

/* ── Alerts ── */
.stAlert { border-radius: 14px !important; }

/* ── HR ── */
hr { border: none !important; border-top: 1px solid rgba(173,20,87,0.12) !important;
     margin: 20px 0 !important; }

/* ── Animations ── */
@keyframes slideDown {
    from { transform: translateY(-22px); opacity: 0; }
    to   { transform: translateY(0);     opacity: 1; }
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
                border-bottom:1px solid rgba(173,20,87,0.2); margin-bottom:18px;">
        <div style="font-size:3em; line-height:1.1;">👶</div>
        <div style="font-size:1.35em; font-weight:900; color:#AD1457 !important;">Mumzworld</div>
        <div style="font-size:0.84em; font-weight:700; color:#6A1B9A !important;">
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
                border-top:1px solid rgba(173,20,87,0.15);
                font-size:0.75em; color:rgba(61,0,102,0.5) !important;">
        Powered by Llama 3.3 70B · Groq
    </div>
    """, unsafe_allow_html=True)


# ── LANGUAGE STATE ────────────────────────────────────────────────────────────
is_en = selected_language in ["English 🇬🇧", "Both 🌐"]
is_ar = selected_language in ["العربية 🇸🇦", "Both 🌐"]
c = content_en if is_en else content_ar


# ── HERO ──────────────────────────────────────────────────────────────────────
slogan = random.choice(c["slogans"])
title  = "Welcome to Mumzworld! 👶" if is_en else "أهلاً بك في مامز وورلد! 👶"
sub    = "Your Smart AI Parenting Assistant" if is_en else "مساعدك الذكي لتربية الأطفال"

st.markdown(f"""
<div class="hero">
    <div class="hero-title">{title}</div>
    <div class="hero-sub">{sub}</div>
    <div class="hero-slogan">{slogan}</div>
    <div>
        <span class="pill">🤖 AI-Powered</span>
        <span class="pill">🌍 Bilingual</span>
        <span class="pill">👶 Baby Expert</span>
        <span class="pill">⚡ Free &amp; Fast</span>
    </div>
</div>
""", unsafe_allow_html=True)


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
You are an expert shopping assistant for Mumzworld, a leading Middle Eastern e-commerce site for mothers and children.
A parent has come to you with this situation: "{user_input}"

Provide a warm, empathetic opening. Then list 3–5 specific product categories they should look for on Mumzworld.
Format each product as a bullet point starting with "- " with the category name in **bold**, followed by a brief explanation.

If the situation involves illness, fever, pain, or discomfort:
1. Recommend baby medicines/supplements (e.g., paracetamol, ibuprofen for babies, saline drops)
2. Include dosage guidelines — always recommend consulting a pediatrician first
3. Mention safe medical products available on Mumzworld

Keep the tone warm, helpful, and reassuring. Remind parents to consult a pediatrician before giving any medication.
"""
                if show_arabic:
                    prompt += "\n\nIMPORTANT: After your full English response, add exactly '---ARABIC---' on its own line, then provide the complete Arabic translation."

                try:
                    resp = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "You are a helpful, empathetic shopping assistant for Mumzworld."},
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
