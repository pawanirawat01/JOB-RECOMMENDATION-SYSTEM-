import html

import streamlit as st

from recommender import load_jobs, recommend

st.set_page_config(page_title="JobMatch", page_icon="💼", layout="wide")

CSS = """
<style>
#MainMenu, footer, header [data-testid="stToolbar"] {visibility: hidden;}
.block-container {padding-top: 2rem; max-width: 1100px;}
[data-testid="stSidebar"] {background: #0F1524; border-right: 1px solid #1F2937;}
.hero {padding: 28px 30px; border-radius: 18px; margin-bottom: 22px;
  background: radial-gradient(1200px 300px at 0% 0%, rgba(99,102,241,.25), transparent),
              radial-gradient(800px 300px at 100% 100%, rgba(34,211,238,.18), transparent), #111827;
  border: 1px solid #1F2937;}
.hero h1 {margin: 0; font-size: 2.1rem; font-weight: 800;
  background: linear-gradient(90deg, #A5B4FC, #67E8F9); -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;}
.hero p {margin: 8px 0 0; color: #9CA3AF; font-size: 1rem;}
.stats {display: flex; gap: 14px; margin: 6px 0 22px; flex-wrap: wrap;}
.stat {flex: 1; min-width: 150px; background: #111827; border: 1px solid #1F2937;
  border-radius: 14px; padding: 14px 18px;}
.stat .v {font-size: 1.6rem; font-weight: 800; color: #F3F4F6;}
.stat .l {font-size: .8rem; color: #9CA3AF; text-transform: uppercase; letter-spacing: .06em;}
.card {background: #111827; border: 1px solid #1F2937; border-radius: 16px;
  padding: 20px 22px; margin-bottom: 6px; transition: all .2s ease;}
.card:hover {border-color: #6366F1; box-shadow: 0 0 0 1px #6366F1, 0 10px 30px rgba(99,102,241,.15);
  transform: translateY(-2px);}
.top {display: flex; justify-content: space-between; align-items: flex-start; gap: 16px;}
.rank {color: #6366F1; font-weight: 700; font-size: .85rem; letter-spacing: .08em;}
.title {font-size: 1.25rem; font-weight: 700; color: #F9FAFB; margin: 2px 0 4px;}
.meta {color: #9CA3AF; font-size: .9rem;}
.meta b {color: #D1D5DB;}
.badge {min-width: 86px; text-align: center; padding: 8px 12px; border-radius: 12px;
  font-weight: 800; font-size: 1.2rem; color: #0B0F19;
  background: linear-gradient(135deg, #A5B4FC, #67E8F9);}
.badge small {display: block; font-size: .65rem; font-weight: 700; letter-spacing: .08em; opacity: .75;}
.bar {height: 6px; background: #1F2937; border-radius: 99px; margin: 14px 0 12px; overflow: hidden;}
.bar > div {height: 100%; border-radius: 99px; background: linear-gradient(90deg, #6366F1, #22D3EE);}
.lbl {font-size: .72rem; color: #6B7280; text-transform: uppercase; letter-spacing: .08em; margin: 8px 0 4px;}
.pill {display: inline-block; padding: 3px 11px; margin: 0 6px 6px 0; border-radius: 99px;
  font-size: .8rem; font-weight: 600;}
.have {background: rgba(52,211,153,.12); color: #6EE7B7; border: 1px solid rgba(52,211,153,.35);}
.need {background: rgba(251,191,36,.10); color: #FCD34D; border: 1px solid rgba(251,191,36,.30);}
.tag {background: #1F2937; color: #C7D2FE; border: 1px solid #374151;}
.steps {display: flex; gap: 14px; flex-wrap: wrap;}
.step {flex: 1; min-width: 220px; background: #111827; border: 1px solid #1F2937;
  border-radius: 14px; padding: 18px;}
.step h4 {margin: 0 0 6px; color: #F3F4F6;}
.step p {margin: 0; color: #9CA3AF; font-size: .9rem;}
.stButton > button, .stFormSubmitButton > button {border-radius: 12px; font-weight: 700; border: 0;
  background: linear-gradient(90deg, #6366F1, #22D3EE); color: #0B0F19;}
.stButton > button:hover, .stFormSubmitButton > button:hover {filter: brightness(1.1); color: #0B0F19;}
details {border-radius: 12px !important; border-color: #1F2937 !important;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


@st.cache_data
def get_jobs():
    return load_jobs("jobs.csv")


def esc(x):
    return html.escape(str(x))


def pills(items, cls):
    return "".join(f'<span class="pill {cls}">{esc(i)}</span>' for i in items) or \
        '<span class="pill tag">None 🎉</span>'


def job_card(rank, r):
    score = float(r["match_score"])
    width = max(4, min(int(score), 100))
    return (
        '<div class="card">'
        '<div class="top"><div>'
        f'<div class="rank">#{rank} MATCH</div>'
        f'<div class="title">{esc(r["title"])}</div>'
        f'<div class="meta"><b>{esc(r["company"])}</b> &nbsp;·&nbsp; 📍 {esc(r["location"])}'
        f' &nbsp;·&nbsp; 🎓 {esc(r["experience"])}</div>'
        f'</div><div class="badge">{score:.0f}%<small>MATCH</small></div></div>'
        f'<div class="bar"><div style="width:{width}%"></div></div>'
        f'<div class="lbl">✅ Skills you have</div>{pills(r["matched_skills"], "have")}'
        f'<div class="lbl">📘 Skills to learn</div>{pills(r["missing_skills"], "need")}'
        '</div>'
    )


jobs = get_jobs()

# ------------------------------------------------------------------ sidebar form
with st.sidebar:
    st.markdown("### 👤 Your profile")
    with st.form("profile"):
        skills = st.text_area("Skills (comma separated)",
                              "Python, SQL, Machine Learning", height=100)
        role = st.text_input("Preferred job role", "Data Analyst")
        education = st.selectbox("Education", ["BCA", "B.Tech", "MCA", "BSc", "M.Tech", "Other"])
        experience = st.selectbox("Experience", ["Fresher", "1-2 years", "3+ years"])
        location = st.selectbox("Preferred location", ["Any"] + sorted(jobs["location"].unique()))
        top_n = st.slider("Results", 3, 15, 6)
        go = st.form_submit_button("🔍  Find my jobs", use_container_width=True)
    st.caption("Suggestions are guidance only and do not guarantee a job.")

# -------------------------------------------------------------------------- hero
st.markdown(
    '<div class="hero"><h1>💼 JobMatch</h1>'
    '<p>AI powered job recommendations using TF-IDF and cosine similarity. '
    'Tell us your skills, we find your best fit.</p></div>', unsafe_allow_html=True)

if go:
    if not skills.strip():
        st.warning("Please enter at least one skill.")
    else:
        recs = recommend(jobs, skills, education, experience, role,
                         "" if location == "Any" else location, top_n)
        if recs.empty:
            st.info("No matching jobs found. Try adding more skills.")
        else:
            st.markdown(
                '<div class="stats">'
                f'<div class="stat"><div class="v">{len(jobs)}</div><div class="l">Jobs searched</div></div>'
                f'<div class="stat"><div class="v">{recs["match_score"].max():.0f}%</div><div class="l">Best match</div></div>'
                f'<div class="stat"><div class="v">{recs["match_score"].mean():.0f}%</div><div class="l">Average of top {len(recs)}</div></div>'
                '</div>', unsafe_allow_html=True)
            for i, r in recs.iterrows():
                st.markdown(job_card(i + 1, r), unsafe_allow_html=True)
                with st.expander("View job description"):
                    st.write(r["description"])
                    st.markdown('<div class="lbl">Required skills</div>' +
                                pills(r["skills"].split(";"), "tag"), unsafe_allow_html=True)
else:
    st.markdown(
        '<div class="steps">'
        '<div class="step"><h4>1 · Enter profile</h4><p>Add your skills, education, experience and preferred role in the sidebar.</p></div>'
        '<div class="step"><h4>2 · We compare</h4><p>Your profile is matched with every job using TF-IDF and cosine similarity.</p></div>'
        '<div class="step"><h4>3 · Get ranked jobs</h4><p>See match scores, skills you have and skills you still need to learn.</p></div>'
        '</div>', unsafe_allow_html=True)
