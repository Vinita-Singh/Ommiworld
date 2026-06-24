# 👶 Ommiworld AI Assistant | Track B Submission



---

## 📝 One-Paragraph Summary

**Ommi World AI Assistant** is a bilingual AI-powered recommendation engine that solves a real problem for first-time and busy mothers in the GCC: the overwhelm of choosing the right baby products. When a mom can't figure out what to buy (whether it's equipment for a 6-month-old starting solids or symptom management for a feverish infant), she describes her situation in natural language, and the AI returns curated product recommendations with relevant health advice—in both English and Arabic. The app is built with Streamlit, Llama 3.3 70B via Groq's free API, and includes a language toggle for a fully native bilingual experience.

---

## 🔍 Discovery

### The Persona: Yatima
- **Name**: Yatima Al-Mansouri
- **Age**: 28, first-time mother in Dubai
- **Situation**: Has a 6-month-old son (Zain) and a 2-year-old daughter (Nora)
- **Goals**: Find the right products to keep her kids healthy, happy, and developmentally on track without overwhelming herself with options
- **Pain Points**:
  - Doesn't know what specific equipment or products she needs for each developmental stage
  - Worried about giving wrong medicines or products without professional guidance
  - Reads conflicting advice online (Arabic forums, English mom blogs, Instagram)
  - Doesn't have time to scroll through hundreds of Ommi World products to find the right ones
  - Prefers information in Arabic but some products only have English descriptions

### Problems I Identified on Ommi World

1. **Search Overwhelm** - Searching "6-month-old" returns 300+ products with no curation
2. **Lack of Context** - A product listing doesn't explain *when* or *why* to buy it
3. **No Health Integration** - If a baby has symptoms, mom has to juggle health advice + shopping separately
4. **Language Gap** - Key parenting advice is often English-only, but moms in UAE prefer Arabic
5. **Decision Fatigue** - Even with filters, moms don't know if they're making the right choice
6. **Trust Gap** - Generic product descriptions don't build confidence in non-obvious purchases

### Why This Problem Matters Most

**Conversion Blocker**: Moms abandon carts or don't purchase at all because they're unsure. An AI that says "for your situation, here are the 5 products you actually need" removes friction and increases AOV.

---

## 🤖 Why AI

### Why AI vs. Other Solutions

| Solution | Why It Fails | Why AI Wins |
|----------|-------------|-----------|
| **UX Fix (Better Menu)** | Doesn't solve knowledge problem; mom still doesn't know what she needs | Understands context ("6-month-old starting solids" → specific needs) |
| **Curated Collections** | Static; can't handle health concerns (fever, constipation, reflux) | Handles free-text queries; adapts to infinite situations |
| **Customer Support** | Doesn't scale; costs per inquiry | Infinite scalability; same cost per 1000 queries |
| **Filters & Categories** | Still requires mom to choose; builds no confidence | Recommends specific categories + explains WHY |

### The AI-Native Insight

This isn't a chatbot wrapper. It's using AI as a **product discovery layer**—turning unstructured parenting concerns into structured Ommi World shopping lists. The LLM does semantic work: understanding developmental stages, symptom triage, product category mapping, and confidence scoring.

---

## 🛠️ Show Your Work

### Tools Used

| Tool | Role |
|------|------|
| **Groq API** (free tier) | Model gateway; free access to Llama 3.3 70B without rate limits |
| **Llama 3.3 70B Versatile** | LLM backbone; multilingual, instruction-tuned, excellent for parenting reasoning |
| **Streamlit** | UI framework; fast iteration, built-in session management |
| **Python (dotenv, time, random)** | Environment management, session utilities |
| **GitHub Copilot** | Pair-coding for prompt refinement, CSS debugging, error handling |
| **CSS + HTML** | Pink theme, animations, RTL support for Arabic |
| **Git + GitHub Actions** | CI/CD pipeline, deployment automation |

### Timeline Log (30-min increments)

**Session 1: Problem Scoping & MVP (90 min)**
- *0:00-0:30* - Sketched persona (Fatima), pain points, validated "AI is the right tool"
- *0:30-1:00* - Designed app flow: input → AI → bilingual output
- *1:00-1:30* - Set up Streamlit project, pink UI shell

**Session 2: AI Integration & Health Safety (90 min)**
- *0:00-0:30* - Integrated Groq API, tested Llama model with baby scenarios
- *0:30-1:00* - Iterated on prompt for medicine recommendations
- *1:00-1:30* - Fixed: Model was too aggressive with medicines → added pediatrician disclaimers

**Session 3: Multilingual & UI Polish (120 min)**
- *0:00-0:45* - Created EN/AR content dictionaries, language selector
- *0:45-1:15* - Fixed: Translation button breaking on reruns → moved to session_state
- *1:15-1:45* - CSS animations, pink gradient buttons, RTL formatting
- *1:45-2:00* - Tested on mobile, edge cases

**Session 4: Deployment & Docs (60 min)**
- *0:00-0:30* - GitHub Actions CI/CD pipeline, syntax validation
- *0:30-1:00* - README, DOCUMENTATION.md, DEPLOYMENT.md

**Total**: 5.5 hours (30 min over estimate, documented honestly)

### Prompts That Mattered

**Prompt 1: Initial Version (Failed)**
```
You are a parenting advisor. The user has a baby situation. 
Recommend products from Ommi World and any helpful advice.
```
❌ Model recommended specific medicines without disclaimers

**Prompt 2: Iteration (Better)**
```
You are a warm parenting advisor for Ommi World.
1. Acknowledge their concern
2. Suggest 3-5 product categories
3. If health-related: ALWAYS say "Consult your pediatrician"
```
⚠️ Still inventing product names

**Prompt 3: Production (Current)**
```
A parent has come to you with this situation: "{user_input}"

Provide a warm, empathetic response. Then, list 3 to 5 specific product categories they should look for on Ommi World to solve this situation. 
Briefly explain why they need each item.

IMPORTANT: If the baby's situation involves illness, fever, pain, or discomfort, please include:
1. Recommended baby medicines/supplements that can help (e.g., paracetamol, ibuprofen for babies, saline drops, etc.)
2. Dosage guidelines (always recommend consulting a pediatrician)
3. Safe medical products available on Ommi World

Always emphasize consulting with a pediatrician before giving any medication. Keep the tone helpful and reassuring.
```
✅ Works well. Balances recommendations with safety.

### Dead Ends

1. **Price Recommendations** - Tried to include "products under 500 AED"
   - ❌ Model doesn't have real-time pricing; made up prices
   - **Lesson**: AI needs grounding in real data; without RAG/database, prices aren't trustworthy
   - ✅ **Decision**: Removed; focus on categories only

2. **Automatic Language Detection** - Used LLM to detect input language, auto-respond
   - ❌ Added latency; inconsistent; complex state
   - **Lesson**: Explicit user choice beats unreliable auto-detection
   - ✅ **Decision**: Radio button selector

3. **Translation Button Rerun Loop** - `if st.button("Show Arabic"): translate()`
   - ❌ Streamlit reruns; state lost on every interaction
   - **Lesson**: Session state is your friend; rerun logic is a trap
   - ✅ **Decision**: Moved to session_state + checkbox

4. **Arabic-Only Button Text** - Tried full Arabic phrases on buttons
   - ❌ Mobile browsers cut off text; alignment broke
   - **Lesson**: Short labels (emoji) > long text on buttons
   - ✅ **Decision**: Emoji labels + conditional EN/AR text

5. **Storing All Responses in Session** - Cache every response
   - ❌ Old responses confused users if input changed
   - **Lesson**: Session state needs lifecycle management
   - ✅ **Decision**: Clear on new input; only store latest

### Cuts from Scope

1. **Symptom Severity Scoring** - Wanted green/yellow/red urgency indicator
   - ❌ Adds liability; mom needs doctor, not traffic light
   - 🔄 **Reconsider if**: Legal review + pediatrician validation

2. **Product Database Integration (RAG)** - Real SKU recommendations
   - ❌ Need access to catalog; adds 3+ hours
   - 🔄 **Reconsider if**: Given real data + 8 hours

3. **User Feedback Loop** - "Was this helpful?" buttons
   - ❌ Needs backend (database, auth); 5-hour scope
   - 🔄 **Reconsider if**: Shipping to production

4. **Voice Input** - Record voice memos
   - ❌ Speech-to-text dependency; mobile testing nightmare
   - 🔄 **Reconsider if**: Native iOS/Android app

5. **Video Content** - Surface how-to videos
   - ❌ Requires curated video DB; licensing; out of scope
   - 🔄 **Reconsider if**: Ommi World has internal library

---

## 📊 Measurement

### Week 1 Leading Indicator

**Metric**: **Query Completion Rate**
- **Definition**: % of sessions with ≥1 completed query
- **Target**: >70%
- **Why it matters**: Completion = product is solving the problem
- **How to track**: Streamlit Cloud analytics + simple logging

**Secondary**: **Arabic Usage %**
- **Target**: >40% (bilingual market)
- **Why it matters**: Validates Arabic experience is valued

---

### 5% A/B Experiment (Week 2)

**Hypothesis**: Confidence scores increase product CTR

**Design**:
- **Control (50%)**: Current (recommendations only)
- **Test (50%)**: Same + confidence % ("87% match for your situation")

**Success Metrics**:
- ✅ **Works**: 25%+ lift in Ommi World CTR
- ❌ **Flat**: <10% difference
- 🚩 **Fails**: Test underperforms 15%+ (moms trust reviews more?)

**Decision Rule**:
- Works → ship scores
- Flat → test other signals (ratings, reviews)
- Fails → debug (unclear wording? too clinical?)

---

## 🛠️ AI Usage Note

**Groq API + Llama 3.3 70B**: All recommendation generation, multilingual responses
**GitHub Copilot**: Prompt iteration, CSS debugging, session logic (overrode on error handling)
**Claude (via Copilot Chat)**: Brainstorming, persona development, dead-end analysis

---

## ⏱️ Time Log

| Phase | Time | Notes |
|-------|------|-------|
| Discovery + persona | 45 min | Fatima, pain points, AI vs alternatives |
| MVP + Groq integration | 90 min | Streamlit, Llama, prompt testing |
| Health/safety features | 60 min | Prompt refinement, disclaimers, edge cases |
| Multilingual + animations | 75 min | EN/AR, RTL, session state, CSS |
| Deployment + docs | 60 min | GitHub Actions, README, DOCUMENTATION.md |
| **Total** | **330 min (5.5 hrs)** | ~30 min over; prioritized quality + transparency |

---

## 🚀 Prototype Access

**GitHub Repo**: https://github.com/paulamartya25/Ommi World.in

**Setup (Under 5 Min)**:
```bash
git clone https://github.com/vinitasingh57/Ommi World.in.git
cd Ommi World-ai
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "GROQ_API_KEY=your_free_key_here" > .env
streamlit run app.py
```

---

## Features ✨

- **AI-Powered Recommendations** - Llama 3.3 70B via Groq (free tier)
- **Multilingual** - English & Arabic with native output (not translations)
- **Baby Health Advice** - Medicine recommendations with pediatrician disclaimers
- **Beautiful UI** - Pink-themed, animated, responsive design
- **Free & Fast** - No paid APIs; <5 min setup

---

## Tech Stack 🛠️

- **Frontend**: Streamlit
- **AI Model**: Llama 3.3 70B (Groq)
- **Language**: Python 3.x
- **Styling**: CSS + HTML
- **Deployment**: Streamlit Cloud + GitHub Actions

---

## Project Structure 📁

```
Ommi World-ai/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env                   # API keys (not in repo)
├── .gitignore            # Git ignore rules
├── README.md             # This file (Track B submission)
├── DOCUMENTATION.md      # Technical deep-dive
├── DEPLOYMENT.md         # Streamlit Cloud setup
├── SUBMISSION_ASSESSMENT.md  # Track alignment analysis
└── .github/workflows/deploy.yml  # GitHub Actions CI/CD
```

---

## Troubleshooting 🔧

**"GROQ_API_KEY not set"** → Create `.env` with your key from https://console.groq.com

**"Module not found"** → Run `pip install -r requirements.txt` in virtual environment

**Arabic not displaying** → Clear browser cache (`Ctrl+Shift+R`)

**Translation button not working** → Ensure session is initialized; refresh page

---

## What's Next 🔮

1. **Product Database Integration** - Connect to real Ommi World catalog for SKU recommendations
2. **Feedback Loop** - "Was this helpful?" ratings for continuous improvement
3. **Symptom Severity Triage** - Enhanced pediatric decision-making
4. **Personalization** - Remember previous queries; segment by baby age
5. **Native Mobile App** - iOS/Android with voice input

---

**Submitted**: April 29, 2026 | Track B | Ommi World AI-Native Product Intern Assessment

## Security & Privacy 🔐

- API keys stored in `.env` (never committed to repo)
- User queries sent only to Groq API
- No data persistence or tracking
- Stateless conversation model

## License 📝

MIT License - feel free to use and modify

## Support & Contact 💬

For issues, questions, or feature requests:
1. Open an issue on GitHub
2. Check DOCUMENTATION.md for technical details
3. Review Groq API docs: https://console.groq.com

## Credits 👏

- **AI Model**: Meta's Llama 3.3 70B
- **API Provider**: Groq
- **Framework**: Streamlit
- **Design**: Custom CSS/HTML

---

**Made with ❤️ for parents and babies everywhere** 👶💕

*"Every baby deserves the best, and every parent deserves support!"*
