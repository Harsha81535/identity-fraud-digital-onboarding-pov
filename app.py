from pathlib import Path
import math
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Reducing Identity Fraud Without Losing Good Customers",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Theme-independent palette: the app always uses its own light canvas and explicit text colours.
NAVY = "#14263D"
NAVY2 = "#203F5D"
BLUE = "#2E6F95"
TEAL = "#237C78"
GOLD = "#B77A12"
PALE = "#F2F6F8"
MUTED = "#526577"
BORDER = "#D8E2E9"
WHITE = "#FFFFFF"

st.markdown(
    f"""
    <style>
    :root {{ color-scheme: light; }}
    html, body, [data-testid="stAppViewContainer"], .stApp {{
        background: #F5F8FA !important;
        color: {NAVY} !important;
    }}
    [data-testid="stHeader"] {{ background: #F5F8FA !important; }}
    [data-testid="stMain"], [data-testid="stMainBlockContainer"] {{
        background: #F5F8FA !important; color: {NAVY} !important;
    }}
    .block-container {{ padding-top: 1.1rem; padding-bottom: 3rem; max-width: 1440px; }}
    h1, h2, h3, h4, p, li, label, .stMarkdown, [data-testid="stCaptionContainer"] {{
        color: {NAVY} !important;
    }}
    h1 {{ font-size: 2rem !important; }}
    h2 {{ font-size: 1.65rem !important; }}
    h3 {{ font-size: 1.28rem !important; }}
    p, li {{ font-size: 1rem !important; line-height: 1.58 !important; }}
    [data-testid="stRadio"] label p {{ font-size: 1rem !important; }}
    [data-testid="stCaptionContainer"] p {{ font-size: .94rem !important; color: {MUTED} !important; }}

    .project-header {{ display:flex; justify-content:space-between; align-items:flex-start; gap:2rem; width:100%; }}
    .project-header-left {{ flex:1 1 auto; min-width:0; }}
    .project-header-right {{ flex:0 0 340px; max-width:340px; text-align:right; color:{NAVY} !important; font-size:1rem !important; line-height:1.55 !important; }}
    .project-header-right .author-name {{ font-weight:800 !important; color:{NAVY} !important; }}
    @media (max-width: 900px) {{
      .project-header {{ flex-direction:column; gap:.5rem; }}
      .project-header-right {{ flex:1 1 auto; max-width:100%; text-align:left; }}
    }}

    .author {{ display:block !important; visibility:visible !important; opacity:1 !important;
               text-align:right; color:{NAVY} !important; font-size:1rem; line-height:1.55;
               min-width:330px; max-width:430px; flex:0 0 auto; overflow:visible !important; }}
    .author div {{ display:block !important; visibility:visible !important; color:{NAVY} !important; }}
    .author .author-name {{ font-size:1.08rem !important; font-weight:900 !important;
                            color:{NAVY} !important; margin-bottom:.1rem; }}
    .navwrap {{ background:{NAVY}; padding:.7rem 1rem; border-radius:12px; margin-bottom:1.2rem; }}
    .navwrap span {{ color:#FFFFFF !important; font-size:1rem !important; line-height:1.55; }}
    .hero {{ background:linear-gradient(120deg,{NAVY},{NAVY2}); color:white; padding:2rem 2.2rem;
             border-radius:16px; margin-bottom:1.2rem; }}
    .hero h1 {{ color:white !important; font-size:2.05rem !important; line-height:1.25; margin:.35rem 0 .7rem; }}
    .hero p {{ color:#F4F7FA !important; font-size:1.06rem !important; line-height:1.65 !important; margin-bottom:.25rem; }}
    .eyebrow {{ text-transform:uppercase; letter-spacing:.12em; font-size:.84rem;
                line-height:1.4; font-weight:850; color:{TEAL} !important; }}
    .purpose-panel {{ background:linear-gradient(135deg,#14263D,#203F5D) !important;
                      border-radius:15px; padding:1.2rem 1.35rem; margin:.4rem 0 1rem;
                      border:1px solid #2E5976; color:#FFFFFF !important; }}
    .purpose-panel * {{ color:#FFFFFF !important; }}
    .purpose-panel .purpose-title {{ font-size:1.12rem !important; font-weight:850;
                                     letter-spacing:.04em; margin-bottom:.75rem; }}
    .purpose-grid {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:.8rem; }}
    .purpose-item {{ background:rgba(255,255,255,.09) !important; border:1px solid rgba(255,255,255,.22);
                     border-radius:10px; padding:.9rem 1rem; min-height:120px; }}
    .purpose-item .purpose-label {{ color:#A8D8D4 !important; font-size:.9rem !important;
                                    font-weight:850; margin-bottom:.35rem; }}
    .purpose-item p {{ color:#FFFFFF !important; font-size:1rem !important; line-height:1.55 !important; margin:0; }}
    .buyer-card {{ background:#FFFFFF !important; border:1px solid {BORDER}; border-radius:14px;
                   overflow:hidden; margin:.35rem 0 .85rem; color:{NAVY} !important; }}
    .buyer-card .buyer-band {{ background:{NAVY}; color:#FFFFFF !important; padding:.8rem 1rem;
                               font-size:.9rem; font-weight:850; letter-spacing:.07em; }}
    .buyer-card .buyer-body {{ padding:1.1rem 1.2rem; }}
    .buyer-card h3 {{ font-size:1.3rem !important; color:{NAVY} !important; margin:.1rem 0 .65rem; }}
    .buyer-card .buyer-lead {{ font-size:1.04rem !important; color:{BLUE} !important;
                               font-weight:750; line-height:1.5; margin-bottom:.7rem; }}
    .buyer-card .buyer-detail {{ font-size:.97rem !important; color:{MUTED} !important; line-height:1.55; }}
    .approach-card {{ background:#FFFFFF !important; border:1px solid {BORDER}; border-left:5px solid {TEAL};
                      border-radius:13px; padding:1.15rem 1.25rem; min-height:245px; margin:.3rem 0 .8rem;
                      box-shadow:0 3px 12px rgba(20,38,61,.06); color:{NAVY} !important; }}
    .approach-card h3 {{ font-size:1.3rem !important; color:{NAVY} !important; margin:.55rem 0 .65rem;
                         line-height:1.3 !important; }}
    .approach-card .approach-number {{ display:inline-block; background:#E4F2F0 !important;
                                       border-radius:6px; padding:.28rem .5rem; font-size:.82rem !important;
                                       font-weight:900; color:#17645F !important; letter-spacing:.07em; }}
    .approach-card .approach-summary {{ font-size:1.04rem !important; line-height:1.55 !important;
                                        color:{BLUE} !important; font-weight:700; margin:.35rem 0 .7rem; }}
    .approach-card .approach-question {{ background:#F2F6F8 !important; border-radius:8px;
                                         padding:.65rem .75rem; margin-top:.7rem; font-size:.95rem !important;
                                         line-height:1.5 !important; color:{NAVY} !important; }}
    .approach-card p {{ font-size:.97rem !important; line-height:1.5 !important; color:{NAVY} !important; }}
    .vendor-card {{ background:#FFFFFF !important; border:1px solid {BORDER}; border-top:4px solid {TEAL};
                    border-radius:12px; padding:1rem 1.1rem; min-height:195px; margin:.3rem 0 .8rem; }}
    .vendor-card h3 {{ font-size:1.18rem !important; color:{NAVY} !important; margin:.2rem 0 .6rem; }}
    .vendor-card .vendor-focus {{ font-size:1rem !important; color:{BLUE} !important; font-weight:750; line-height:1.5; }}
    .vendor-card p {{ font-size:.95rem !important; color:{MUTED} !important; line-height:1.5 !important; }}
    .cost-method {{ color:{NAVY} !important; background:#FFFFFF !important; border:1px solid {BORDER};
                    border-radius:12px; padding:1rem 1.1rem; }}
    .cost-method-title {{ color:{NAVY} !important; font-size:1.05rem !important; font-weight:850;
                          margin-bottom:.7rem; }}
    .cost-step {{ display:flex; justify-content:space-between; gap:1rem; padding:.55rem .2rem;
                  border-bottom:1px solid {BORDER}; color:{NAVY} !important; font-size:1rem !important; }}
    .cost-step span {{ color:{MUTED} !important; }}
    .cost-step strong {{ color:{NAVY} !important; white-space:nowrap; }}
    .cost-result {{ display:flex; justify-content:space-between; gap:1rem; margin-top:.65rem;
                    padding:.8rem; background:#E4F2F0 !important; border-radius:9px;
                    color:#124F4B !important; font-size:1.05rem !important; }}
    .cost-result * {{ color:#124F4B !important; }}
    .cost-method p {{ color:{MUTED} !important; font-size:.95rem !important; line-height:1.55 !important;
                      margin:.8rem 0 .1rem; }}
    .section-card {{ background:{WHITE} !important; border:1px solid {BORDER}; border-radius:13px;
                     padding:1.25rem 1.35rem; margin:.35rem 0 .8rem; color:{NAVY} !important; }}
    .section-card * {{ color:{NAVY} !important; }}
    .section-card p {{ margin:.45rem 0 .9rem; }}
    .section-card p:last-child {{ margin-bottom:.1rem; }}
    .purpose-grid {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:.85rem; }}
    .purpose-item {{ background:#FFFFFF !important; border:1px solid {BORDER}; border-radius:12px;
                     padding:1rem 1.1rem; color:{NAVY} !important; }}
    .purpose-item h3 {{ color:{NAVY} !important; font-size:1.12rem !important; margin:.3rem 0 .45rem; }}
    .purpose-item p {{ color:{NAVY} !important; font-size:1rem !important; margin:0; }}
    .callout {{ background:#E8F1F6 !important; border-left:5px solid {BLUE}; padding:1rem 1.1rem;
                border-radius:8px; margin:.7rem 0 1rem; line-height:1.65; color:{NAVY} !important; }}
    .callout * {{ color:{NAVY} !important; }}
    .caveat {{ background:#FFF4DF !important; border-left:5px solid {GOLD}; padding:1rem 1.1rem;
               border-radius:8px; margin:.7rem 0 1rem; line-height:1.65; color:{NAVY} !important; }}
    .caveat * {{ color:{NAVY} !important; }}
    .metric-card {{ background:#FFFFFF !important; border:1px solid {BORDER}; border-radius:14px;
                    padding:1.2rem 1.25rem; min-height:158px; color:{NAVY} !important; }}
    .metric-number {{ color:{BLUE} !important; font-size:2.15rem; font-weight:900; line-height:1.2;
                      overflow-wrap:anywhere; margin:.3rem 0 .5rem; }}
    .metric-label {{ color:{NAVY} !important; font-size:1.08rem; font-weight:800; line-height:1.4; }}
    .metric-note {{ color:{MUTED} !important; font-size:.94rem; line-height:1.5; margin-top:.5rem; }}
    .journey-step {{ background:#FFFFFF !important; border:1px solid {BORDER}; border-radius:12px;
                     padding:1rem; min-height:225px; height:100%; color:{NAVY} !important; }}
    .step-number {{ display:inline-flex; background:{NAVY}; color:#FFFFFF !important; border-radius:50%;
                    width:36px; height:36px; align-items:center; justify-content:center;
                    font-size:1rem; font-weight:850; margin-bottom:.7rem; }}
    .journey-step h3 {{ font-size:1.1rem !important; margin:.1rem 0 .5rem; color:{NAVY} !important; }}
    .journey-step p {{ font-size:.96rem !important; line-height:1.5 !important; margin:0; color:{NAVY} !important; }}
    .recommendation {{ background:linear-gradient(120deg,#14263D,#245B69) !important; color:#FFFFFF !important;
                       border-radius:16px; padding:1.5rem 1.65rem; margin:.6rem 0 1.1rem; }}
    .recommendation h2 {{ color:#FFFFFF !important; margin:.35rem 0 .5rem; font-size:1.65rem !important; }}
    .recommendation p {{ color:#F0F5F7 !important; line-height:1.65 !important; margin-bottom:.2rem; }}
    .subhead {{ font-size:1.55rem; font-weight:850; color:{NAVY} !important; margin:1rem 0 .55rem; }}
    div[data-testid="stMetric"] {{ background:#FFFFFF !important; border:1px solid {BORDER};
                                   padding:1rem; border-radius:12px; }}
    div[data-testid="stMetric"] * {{ color:{NAVY} !important; }}
    div[data-testid="stMetric"] label {{ font-size:1rem !important; }}
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {{ font-size:1.9rem !important; }}
    [data-testid="stDataFrame"], [data-testid="stTable"] {{ background:#FFFFFF !important; }}
    [data-testid="stExpander"] {{ background:#FFFFFF !important; border:1px solid {BORDER}; border-radius:10px; }}
    [data-testid="stExpander"] summary {{ background:#E8EEF3 !important; color:{NAVY} !important; }}
    [data-testid="stExpander"] summary * {{ color:{NAVY} !important; }}
    [data-testid="stExpander"] details, [data-testid="stExpander"] details > div {{
        background:#FFFFFF !important; color:{NAVY} !important;
    }}
    [data-testid="stRadio"] > label {{ font-size:1rem !important; }}
    [data-testid="stRadio"] div[role="radiogroup"] label {{
        background:#FFFFFF !important; border:1px solid {BORDER}; border-radius:9px;
        padding:.35rem .7rem; margin-right:.25rem;
    }}
    [data-testid="stRadio"] div[role="radiogroup"] label * {{ color:{NAVY} !important; }}
    [data-baseweb="popover"], [data-baseweb="menu"], [role="listbox"], [role="option"] {{
        background:#FFFFFF !important; color:{NAVY} !important;
    }}
    [data-baseweb="popover"] *, [data-baseweb="menu"] *, [role="listbox"] *, [role="option"] * {{
        color:{NAVY} !important;
    }}
    [data-baseweb="select"] > div {{ background:#FFFFFF !important; color:{NAVY} !important; }}
    [data-testid="stNumberInput"] input, [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea, [data-testid="stDateInput"] input {{
        background:#FFFFFF !important; color:{NAVY} !important; -webkit-text-fill-color:{NAVY} !important;
        border:1px solid #AABAC8 !important; caret-color:{NAVY} !important;
    }}
    [data-testid="stNumberInput"] button {{
        background:#E8EEF3 !important; color:{NAVY} !important; border-color:#AABAC8 !important;
    }}
    [data-testid="stSlider"] [data-baseweb="slider"] {{ color:{TEAL} !important; }}
    [data-testid="stSlider"] * {{ color:{NAVY} !important; }}
    [data-testid="stDataFrame"], [data-testid="stTable"] {{
        background:#FFFFFF !important; color:{NAVY} !important;
    }}


    [data-testid="stExpander"] * {{ color:{NAVY} !important; }}
    [data-baseweb="select"] *, [data-baseweb="input"] *, [data-baseweb="slider"] * {{ color:{NAVY} !important; }}
    .stAlert * {{ color:{NAVY} !important; }}
    @media (max-width: 850px) {{

        .author {{ text-align:left; }}
        .purpose-grid {{ grid-template-columns:1fr; }}

    }}
    </style>
    """,
    unsafe_allow_html=True,
)

ROOT = Path(__file__).resolve().parent
CFPB_CANDIDATES = [ROOT / "cfpb_combined_sorted.csv", ROOT / "cfpb_combined_sorted(1).csv"]


@st.cache_data(show_spinner=False)
def load_cfpb(path_text):
    frame = pd.read_csv(path_text, low_memory=False)
    frame["Date received"] = pd.to_datetime(frame["Date received"], errors="coerce", utc=True)
    for col in ["Product", "Issue", "Sub-issue", "Company", "State"]:
        if col in frame.columns:
            frame[col] = frame[col].fillna("Not specified").astype(str)
    return frame


def find_cfpb():
    for path in CFPB_CANDIDATES:
        if path.exists():
            try:
                return load_cfpb(str(path)), path.name
            except Exception as exc:
                st.warning(f"Could not load {path.name}: {exc}")
    return None, None


def money(value):
    return "—" if value is None or (isinstance(value, float) and math.isnan(value)) else f"${value:,.0f}"


def metric_card(number, label, note=""):
    st.markdown(
        f'<div class="metric-card"><div class="metric-number">{number}</div>'
        f'<div class="metric-label">{label}</div><div class="metric-note">{note}</div></div>',
        unsafe_allow_html=True,
    )


def page_intro(question, completed, takeaway, caveat=None):
    st.markdown(
        f'<div class="purpose-panel"><div class="purpose-title">PURPOSE OF THIS ANALYSIS</div>'
        f'<div class="purpose-grid">'
        f'<div class="purpose-item"><div class="purpose-label">01 · QUESTION</div><p>{question}</p></div>'
        f'<div class="purpose-item"><div class="purpose-label">02 · WORK COMPLETED</div><p>{completed}</p></div>'
        f'<div class="purpose-item"><div class="purpose-label">03 · CURRENT TAKEAWAY</div><p>{takeaway}</p></div>'
        f'</div></div>',
        unsafe_allow_html=True,
    )
    if caveat:
        st.markdown(
            f'<div class="caveat"><div style="font-size:1.08rem;font-weight:850;color:#744B00 !important">'
            f'IMPORTANT LIMITATION</div><div style="font-size:1rem;line-height:1.65;margin-top:.35rem;color:{NAVY} !important">{caveat}</div></div>',
            unsafe_allow_html=True,
        )


df, cfpb_filename = find_cfpb()

st.title("Reducing Identity Fraud Without Losing Good Customers")
st.markdown(
    """
    <div style="display:flex;justify-content:space-between;align-items:center;gap:18px;flex-wrap:wrap;margin-top:-4px;margin-bottom:18px;">
      <div style="color:#168A8A;font-size:.92rem;font-weight:800;letter-spacing:.08em;">
        EVIDENCE-LED ANALYSIS POINT OF VIEW · RESEARCH SCOPE: UNITED STATES
      </div>
      <div style="text-align:right;color:#172D43;font-size:.9rem;line-height:1.5;margin-left:auto;">
        <strong style="color:#172D43;">Prepared by: Harshana</strong><br>
        MBA Finance, IMT Ghaziabad
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

page = st.radio(
    "Navigate the research",
    ["Start Here", "Fraud Landscape", "Buyer & Alternatives", "Buyer Economics", "Evidence & Recommendation"],
    horizontal=True,
    label_visibility="collapsed",
)

st.markdown(
    '<div class="navwrap"><span><b>Scope:</b> US digital onboarding &nbsp;·&nbsp; '
    '<b>Stage:</b> Research and hypothesis validation &nbsp;·&nbsp; '
    '<b>Purpose:</b> Build an evidence-led point of view, not a product pitch</span></div>',
    unsafe_allow_html=True,
)

if page == "Start Here":
    st.markdown(
        """
        <div class="hero">
          <div class="eyebrow" style="color:#A8D8D4 !important">THE CENTRAL QUESTION</div>
          <h1>Can financial institutions make digital onboarding safer without making it harder for good customers?</h1>
          <p>Identity checks help lenders manage fraud risk. But checks can also create delays, manual work or uncertainty for legitimate applicants. This project investigates that trade-off before recommending any solution.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="subhead">The question is not “Which vendor should we buy?”</div>', unsafe_allow_html=True)
    st.markdown(
        "It is **whether a material, unresolved problem exists and whether a better outcome can justify its cost.** "
        "This advisory exercise starts with public evidence, compares existing approaches and tests illustrative economics. "
        "It does not assume a market gap exists."
    )
    st.markdown('<div class="subhead">The research journey</div>', unsafe_allow_html=True)
    st.caption("Each step answers a different question. The sequence matters: understand the problem before testing a solution.")
    journey = [
        ("01", "Establish the context", "Reviewed FTC fraud and identity-theft reports to understand the reported scale of the issue."),
        ("02", "Audit the evidence", "Examined CFPB complaint categories, trends and coverage limits to avoid treating complaints as verified fraud."),
        ("03", "Map the current landscape", "Compared likely buyer segments, existing identity checks and broad vendor positioning."),
        ("04", "Test buyer economics", "Built an editable model for review workload, cost and break-even under explicit assumptions."),
        ("05", "Identify what is missing", "Separated supported findings from hypotheses and set out the buyer evidence needed next."),
    ]
    cols = st.columns(5)
    for col, (num, title, desc) in zip(cols, journey):
        with col:
            st.markdown(
                f'<div class="journey-step"><div class="step-number">{num}</div>'
                f'<h3>{title}</h3><p>{desc}</p></div>',
                unsafe_allow_html=True,
            )
    st.markdown('<div class="subhead">What the research currently says</div>', unsafe_allow_html=True)
    st.caption("These figures establish context. They do not, on their own, prove an unmet need for another product.")
    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("406,110", "Reports involving new credit-card accounts", "FTC identity-theft category count for 2024.")
    with c2:
        metric_card("$12.54B", "Reported fraud losses", "FTC Consumer Sentinel Network total reported for 2024.")
    with c3:
        metric_card("Not established", "An unresolved market gap", "Institution-level pain, incremental value and willingness to pay remain unvalidated.")
    st.markdown(
        '<div class="callout"><b>Current posture: investigate further before recommending a launch.</b><br>'
        'The public data show that fraud and identity theft matter. They do not establish that existing solutions fail broadly, '
        'or that an additional vendor would improve outcomes economically.</div>',
        unsafe_allow_html=True,
    )
    with st.expander("How to read this advisory point of view"):
        st.markdown(
            "- **Evidence:** what a dataset or source directly reports.\n"
            "- **Interpretation:** what the evidence may suggest.\n"
            "- **Hypothesis:** a possible buyer problem that still needs testing.\n"
            "- **Scenario:** an illustrative calculation using assumptions, not a forecast."
        )

elif page == "Fraud Landscape":
    page_intro(
        "What do public US data sources tell us about fraud and identity-theft signals?",
        "Reviewed selected CFPB complaint categories and FTC 2024 reported-fraud and identity-theft tables.",
        "The sources show meaningful reported activity, but they measure different things and cannot by themselves prove a lender-specific onboarding gap.",
        "CFPB complaints are consumer-submitted complaints, not verified fraud events or a representative estimate of prevalence. FTC reports are also reports, not necessarily unique victims."
    )
    st.markdown('<div class="subhead">FTC 2024: reported fraud and identity theft</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("2.60M", "Fraud reports", "Reports submitted to the FTC Consumer Sentinel Network.")
    with c2:
        metric_card("$12.54B", "Reported fraud losses", "Aggregate reported losses across the network.")
    with c3:
        metric_card("1.135M", "Identity-theft reports", "Reports of identity theft; not necessarily unique people.")
    st.caption("Source: FTC Consumer Sentinel Network Data Book 2024. Figures depend on consumer reporting.")
    st.divider()
    st.markdown('<div class="subhead">Which identity-theft categories are reported most often?</div>', unsafe_allow_html=True)
    identity = pd.DataFrame({
        "Identity-theft category": ["Credit card", "Other identity theft", "Loan or lease", "Bank account", "Employment or tax", "Phone or utilities", "Government documents or benefits"],
        "Reports": [458538, 379615, 202390, 122668, 92281, 91048, 76840],
    })
    fig = px.bar(identity.sort_values("Reports"), x="Reports", y="Identity-theft category", orientation="h", text="Reports", color_discrete_sequence=[BLUE])
    fig.update_layout(height=430, margin=dict(l=10,r=35,t=20,b=10), xaxis_title="Reports", yaxis_title="", showlegend=False, font=dict(size=13))
    fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside", cliponaxis=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        '<div class="callout"><b>How to interpret the credit-card figure</b><br>'
        'The 458,538 credit-card identity-theft reports cover multiple card-related categories. '
        'The research separately identifies 406,110 reports involving new credit-card accounts. '
        'These are category counts, not necessarily unique people.</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="subhead">Explore the selected CFPB complaint extract</div>', unsafe_allow_html=True)
    if df is None:
        st.warning("The CFPB CSV was not found beside app.py. Place cfpb_combined_sorted.csv in the same folder as this app.")
    else:
        st.caption(f"Loaded {cfpb_filename}: {len(df):,} rows, from {df['Date received'].min().date()} to {df['Date received'].max().date()}.")
        focus_issues = ["Fraud or scam", "Unauthorized transactions or other transaction problem", "Attempts to collect debt not owed", "Getting a credit card"]
        available_issues = sorted(df["Issue"].dropna().unique().tolist())
        defaults = [x for x in focus_issues if x in available_issues]
        selected_issues = st.multiselect("Choose complaint issues", available_issues, default=defaults)
        years = sorted(df["Date received"].dropna().dt.year.unique().tolist())
        if years:
            selected_years = st.slider("Choose a year range", int(min(years)), int(max(years)), (int(min(years)), int(max(years))))
            subset = df[df["Issue"].isin(selected_issues)].copy()
            subset = subset[subset["Date received"].dt.year.between(selected_years[0], selected_years[1])]
            if not subset.empty:
                subset["Year"] = subset["Date received"].dt.year
                annual = subset.groupby(["Year", "Issue"]).size().reset_index(name="Complaints")
                fig2 = px.line(annual, x="Year", y="Complaints", color="Issue", markers=True, color_discrete_sequence=[BLUE, TEAL, GOLD, "#6D78A8"])
                fig2.update_layout(height=400, margin=dict(l=10,r=10,t=25,b=10), legend_title_text="", xaxis_title="", yaxis_title="Complaints", font=dict(size=12))
                st.plotly_chart(fig2, use_container_width=True)
                st.metric("Complaints in this selection", f"{len(subset):,}")
                with st.expander("View the 20 companies with the most complaints in this selection"):
                    counts = subset.groupby("Company").size().sort_values(ascending=False).head(20).rename("Complaints").reset_index()
                    st.dataframe(counts, use_container_width=True, hide_index=True)
            else:
                st.info("No rows match the selected filters.")
        st.markdown(
            '<div class="caveat">The extract has uneven category coverage over time; credit-card complaint coverage is mainly through 2023. '
            'Changes and spikes are signals to investigate, not proof of changing fraud incidence or company performance.</div>',
            unsafe_allow_html=True,
        )
    with st.expander("Notebook work reflected on this page"):
        st.markdown(
            "- Combined and sorted the CFPB exports.\n"
            "- Checked product, issue and sub-issue combinations.\n"
            "- Examined annual and monthly trends, including the January 2025 spike.\n"
            "- Checked company concentration and complaint metadata around the spike.\n"
            "- Reviewed FTC state, payment-method and identity-theft tables while keeping each table's scope separate."
        )

elif page == "Buyer & Alternatives":
    page_intro(
        "Who might have this problem, and what can they already use?",
        "Compared digital lenders with card issuers; reviewed existing identity-control approaches and broad vendor positioning.",
        "Digital lenders are the provisional primary segment for further investigation, with card issuers as a comparison, not a validated market selection.",
        "Public vendor descriptions do not prove superiority, customer outcomes or an unmet buyer need."
    )
    st.markdown('<div class="subhead">Two buyer segments to investigate</div>', unsafe_allow_html=True)
    a, b = st.columns(2)
    with a:
        st.markdown(
            '<div class="buyer-card"><div class="buyer-band">PRIMARY RESEARCH FOCUS</div><div class="buyer-body">'
            '<h3>US digital lenders</h3><div class="buyer-lead">Balance fast application decisions with fraud and lending risk.</div>'
            '<p class="buyer-detail"><b>Potential buyer:</b> Head of Fraud, Identity Risk or onboarding operations.</p>'
            '<p class="buyer-detail"><b>What we need to learn:</b> where applicants are delayed, why cases are escalated, and whether current controls leave a measurable gap.</p></div></div>',
            unsafe_allow_html=True,
        )
    with b:
        st.markdown(
            '<div class="buyer-card"><div class="buyer-band">COMPARISON SEGMENT</div><div class="buyer-body">'
            '<h3>US credit-card issuers</h3><div class="buyer-lead">Acquire good customers while controlling new-account fraud.</div>'
            '<p class="buyer-detail"><b>Potential buyer:</b> Fraud strategy, identity risk or card acquisition leadership.</p>'
            '<p class="buyer-detail"><b>What we need to learn:</b> the balance between fraud prevention, approval quality and application completion.</p></div></div>',
            unsafe_allow_html=True,
        )
    st.markdown('<div class="subhead">Existing approaches are part of the answer</div>', unsafe_allow_html=True)
    approaches = [
        ("Government identity check (eCBSV)", "Compare applicant information with Social Security Administration records and return match details.", "A mismatch does not, by itself, establish fraud or credit risk."),
        ("Credit bureau and other data checks", "Add identity, file and account-history signals.", "Coverage, freshness and interpretation differ by applicant and provider."),
        ("Identity-risk scoring and orchestration", "Combine signals and route decisions or workflows.", "Incremental performance, explainability, cost and overlap need validation."),
        ("Document or biometric verification", "Add evidence when uncertainty or risk warrants it.", "Can add friction; suitability depends on applicant, channel and threat."),
        ("Step-up checks and manual review", "Investigate selected uncertain applications.", "Consumes time and may delay or lose legitimate applicants; actual costs need measurement."),
    ]
    for i in range(0, len(approaches), 2):
        row = st.columns(2)
        for col, item in zip(row, approaches[i:i+2]):
            title, description, limitation = item
            with col:
                st.markdown(
                    f'<div class="approach-card"><div class="approach-number">EXISTING APPROACH</div><h3>{title}</h3>'
                    f'<p>{description}</p><p><b>Question to validate:</b> {limitation}</p></div>',
                    unsafe_allow_html=True,
                )
    st.markdown('<div class="subhead">Vendor landscape: orientation, not a ranking</div>', unsafe_allow_html=True)
    vendors = [
        ("Socure", "Identity data and predictive machine learning", "Validate outcomes, pricing, applicant fit and operational impact."),
        ("Alloy", "Identity and fraud workflow orchestration", "Validate stack overlap, workflow fit and implementation effort."),
        ("LexisNexis Risk Solutions", "Identity data and digital identity network", "Validate coverage, data fit, outcomes and total cost."),
        ("Mitek Systems", "Document verification and biometrics", "Validate applicant friction, fraud outcomes and performance by applicant type."),
    ]
    for i in range(0, 4, 2):
        row = st.columns(2)
        for col, item in zip(row, vendors[i:i+2]):
            name, positioning, validation = item
            with col:
                st.markdown(
                    f'<div class="vendor-card"><h3>{name}</h3><div class="vendor-focus">{positioning}</div>'
                    f'<p><b>Evidence still needed</b><br>{validation}</p></div>',
                    unsafe_allow_html=True,
                )
    st.caption("Positioning summaries are based on the research completed so far. This is not a verified feature-by-feature comparison.")
    st.markdown('<div class="subhead">What would validate the buyer pain?</div>', unsafe_allow_html=True)
    st.markdown(
        "1. Actual application-funnel data: approval, decline, step-up and manual-review rates.\n"
        "2. Reason-coded review and decline samples, with known outcomes where available.\n"
        "3. Review time and loaded cost, separated from software and data fees.\n"
        "4. The current vendor stack, overlap, operational constraints and measurable gaps.\n"
        "5. Evidence that a proposed change improves outcomes without shifting cost or risk elsewhere."
    )

elif page == "Buyer Economics":
    page_intro(
        "Could reducing manual-review workload justify the cost of an additional solution?",
        "Built a transparent model, tested input validation, calculated recurring and first-year break-even, and ran sensitivity scenarios.",
        "At the original illustrative base case, recurring net benefit is $37,750 and first-year net benefit is $7,750. Neither is validated cash savings.",
        "All operating inputs are editable scenarios. Replace them with institution-specific data before using the result for a purchasing decision."
    )
    st.markdown('<div class="subhead">Adjust the assumptions</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        annual_reviews = st.number_input("Manual reviews per year", min_value=0, max_value=10000000, value=50000, step=5000)
        reduction_pct = st.slider("Reduction in manual reviews", min_value=0, max_value=100, value=25, step=5)
    with c2:
        cost_per_review = st.number_input("Loaded labour cost per review ($)", min_value=0.0, max_value=10000.0, value=7.02, step=0.25, format="%.2f")
        annual_vendor_fee = st.number_input("Annual vendor fee ($)", min_value=0, max_value=100000000, value=50000, step=5000)
    with c3:
        implementation_cost = st.number_input("One-time implementation cost ($)", min_value=0, max_value=100000000, value=30000, step=5000)
        st.caption("Starting values are illustrative assumptions from the notebook, not industry benchmarks.")
    reduction = reduction_pct / 100
    avoided = annual_reviews * reduction
    gross_savings = avoided * cost_per_review
    annual_net = gross_savings - annual_vendor_fee
    first_year_net = annual_net - implementation_cost
    recurring_be = annual_vendor_fee / (annual_reviews * cost_per_review) * 100 if annual_reviews > 0 and cost_per_review > 0 else None
    first_year_be = (annual_vendor_fee + implementation_cost) / (annual_reviews * cost_per_review) * 100 if annual_reviews > 0 and cost_per_review > 0 else None
    st.markdown('<div class="subhead">What the model estimates</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card(f"{avoided:,.0f}", "Reviews avoided", "Annual workload reduction under the selected scenario.")
    with c2:
        metric_card(money(gross_savings), "Gross labour savings", "Before vendor fees and implementation costs.")
    with c3:
        metric_card(money(annual_net), "Annual net benefit", "After recurring vendor fee; before one-time implementation.")
    with c4:
        metric_card(money(first_year_net), "First-year net benefit", "After recurring fee and one-time implementation cost.")
    if annual_net >= 0 and first_year_net >= 0:
        st.success("The scenario is positive in recurring and first-year terms. It is not validated cash savings.")
    elif annual_net >= 0:
        st.warning("Recurring economics are positive, but the one-time implementation cost makes the first year negative.")
    else:
        st.warning("Under these assumptions, estimated labour savings do not cover the recurring vendor fee.")
    b1, b2 = st.columns(2)
    with b1:
        metric_card(f"{recurring_be:.1f}%" if recurring_be is not None else "Not calculable", "Recurring break-even reduction", "Reduction required for gross labour savings to cover the annual vendor fee.")
    with b2:
        metric_card(f"{first_year_be:.1f}%" if first_year_be is not None else "Not calculable", "First-year break-even reduction", "Reduction required to cover the annual fee plus implementation.")
    if recurring_be is not None and recurring_be > 100:
        st.caption("Break-even exceeds 100% of reviews under these assumptions; review reduction alone cannot cover the annual fee.")
    st.markdown('<div class="subhead">Sensitivity: what if review reduction is lower or higher?</div>', unsafe_allow_html=True)
    rates = [5, 10, 15, 25, 40, 60]
    sens = pd.DataFrame({
        "Reduction in reviews": [f"{x}%" for x in rates],
        "Gross labour savings ($)": [annual_reviews * x / 100 * cost_per_review for x in rates],
        "Annual net benefit ($)": [annual_reviews * x / 100 * cost_per_review - annual_vendor_fee for x in rates],
        "First-year net benefit ($)": [annual_reviews * x / 100 * cost_per_review - annual_vendor_fee - implementation_cost for x in rates],
    })
    fig = px.bar(sens, x="Reduction in reviews", y="First-year net benefit ($)", color_discrete_sequence=[TEAL])
    fig.add_hline(y=0, line_dash="dash", line_color=GOLD)
    fig.update_layout(
        height=360, margin=dict(l=10,r=15,t=20,b=10),
        xaxis_title="Assumed reduction in manual reviews",
        yaxis_title="First-year net benefit ($)",
        font=dict(size=14, color=NAVY),
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        xaxis=dict(color=NAVY, gridcolor="#E2E8EE", zerolinecolor="#AABAC8"),
        yaxis=dict(color=NAVY, gridcolor="#E2E8EE", zerolinecolor="#AABAC8"),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(sens.style.format({
        "Gross labour savings ($)": "${:,.0f}",
        "Annual net benefit ($)": "${:,.0f}",
        "First-year net benefit ($)": "${:,.0f}",
    }), use_container_width=True, hide_index=True)
    with st.expander("How was the $7.02 cost per review estimated?"):
        st.markdown(
            '<div class="cost-method">'
            '<div class="cost-method-title">Illustrative calculation, not an industry benchmark</div>'
            '<div class="cost-step"><span>Hourly wage proxy</span><strong>&#36;38.99 / hour</strong></div>'
            '<div class="cost-step"><span>Assumed review time</span><strong>8 minutes</strong></div>'
            '<div class="cost-step"><span>Direct labour cost</span><strong>&#36;5.20 per review</strong></div>'
            '<div class="cost-step"><span>Illustrative loading factor</span><strong>1.35×</strong></div>'
            '<div class="cost-result"><span>Estimated loaded labour cost</span><strong>&#36;7.02 per review</strong></div>'
            '<p>The wage proxy comes from a broad O*NET / BLS financial-specialist occupation, not a direct fraud-reviewer wage. The assumed review time and loading factor are scenarios, not benchmarks. This estimate excludes verification fees, software, fraud losses and other operating costs.</p>'
            '</div>',
            unsafe_allow_html=True,
        )
    st.markdown(
        '<div class="caveat"><b>Capacity is not automatically cash savings.</b><br>'
        'Released staff time creates cash savings only if the institution can reduce spend or avoid incremental hiring. '
        'This model does not yet include incremental legitimate approvals or net fraud-loss reduction; adding them without evidence could overstate the case.</div>',
        unsafe_allow_html=True,
    )

elif page == "Evidence & Recommendation":
    page_intro(
        "What can we responsibly conclude today, and what evidence is still missing?",
        "Reviewed key numerical claims, checked source scope, compared alternatives, and separated public evidence from commercial hypotheses.",
        "Continue validation before selecting a vendor, claiming a market gap, or recommending a launch.",
        "This is a research-based advisory point of view, not a validated business case or final client recommendation."
    )
    st.markdown('<div class="subhead">Recommended next steps</div>', unsafe_allow_html=True)
    st.caption("These are the actions that would turn the current public-data investigation into a buyer-validated advisory recommendation.")
    steps = [
        ("01", "Interview target buyers", "Speak with fraud, identity-risk and onboarding leaders at a small set of US digital lenders."),
        ("02", "Obtain baseline data", "Request anonymised application outcomes, step-up checks, manual reviews and known outcomes."),
        ("03", "Map current controls", "Identify where existing tools are insufficient, if any, and what a new approach would need to improve."),
        ("04", "Define a controlled pilot", "Measure confirmed fraud, legitimate-applicant completion, review workload, latency and total cost."),
        ("05", "Re-test the business case", "Use buyer data to compare build, buy, optimise existing tools or take no action."),
    ]
    cols = st.columns(5)
    for col, (num, title, desc) in zip(cols, steps):
        with col:
            st.markdown(
                f'<div class="journey-step"><div class="step-number">{num}</div><h3>{title}</h3><p>{desc}</p></div>',
                unsafe_allow_html=True,
            )
    st.markdown(
        '<div class="recommendation"><div class="eyebrow" style="color:#A8D8D4 !important">PRELIMINARY ADVISORY RECOMMENDATION</div>'
        '<h2>Validate the problem before selecting a solution.</h2>'
        '<p>Public evidence establishes the relevance of fraud and identity theft. It does not yet establish a material, addressable residual problem for the target buyer, '
        'nor prove that an additional solution creates positive incremental value. The next decision should be driven by buyer data and controlled testing, not market-level headline figures alone.</p></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="subhead">Evidence register: claims and how to use them</div>', unsafe_allow_html=True)
    evidence = pd.DataFrame([
        ["FTC: 406,110 new credit-card account identity-theft reports in 2024", "Official reported category count", "Supports the relevance of new-account identity theft; not a count of unique victims or lender-specific losses."],
        ["FTC: $12.54B reported fraud losses in 2024", "Official reported aggregate", "Shows scale of reported fraud; not the addressable market or losses preventable by identity checks."],
        ["CFPB complaint increases / January 2025 spike", "Consumer complaint signal", "Useful for investigation; cause and fraud incidence cannot be inferred from counts alone."],
        ["FinRegLab report: some institutions reject high shares of online applications", "Interview-based evidence cited in report", "Potential signal of verification difficulty; not a market-wide false-rejection rate."],
        ["Vendor case studies report review reductions", "Vendor-reported outcomes", "Can inform buyer questions; outcomes may not generalise and require independent validation."],
        ["$7.02 review cost and 25% reduction", "Illustrative model assumptions", "Useful for break-even testing; not validated buyer inputs or industry benchmarks."],
    ], columns=["Claim / evidence", "Evidence type", "What it supports and what it does not"])
    st.dataframe(evidence, use_container_width=True, hide_index=True)
    st.markdown('<div class="subhead">Key hypotheses still to test</div>', unsafe_allow_html=True)
    hypotheses = [
        ("Residual applicant friction", "Are legitimate applicants delayed or declined because identity evidence is hard to resolve?", "Application-funnel data, reason codes, known outcomes and applicant-level review samples."),
        ("Manual-review economics", "Is manual review costly enough, and can workload actually be reduced?", "Review volume, minutes per case, loaded cost, disposition and avoidable spend."),
        ("Incremental value over current vendors", "Does any proposed approach improve outcomes beyond the existing stack?", "Controlled pilot, matched cohorts, baseline metrics and independent outcome validation."),
        ("Buyer willingness to pay", "Would the economic and risk benefit justify incremental cost?", "Buyer interviews, procurement constraints, pricing and implementation estimates."),
    ]
    for title, question, needed in hypotheses:
        with st.expander(title):
            st.markdown(f"**Question to test:** {question}")
            st.markdown(f"**Evidence needed:** {needed}")
    st.markdown('<div class="subhead">Sources used in the current research</div>', unsafe_allow_html=True)
    st.markdown(
        "- Consumer Financial Protection Bureau (CFPB), selected consumer complaint extracts, 2020–2025.\n"
        "- Federal Trade Commission (FTC), *Consumer Sentinel Network Data Book 2024* and associated tables.\n"
        "- FinRegLab, *Market Context Report: Innovations for Identity Proofing and Transaction Monitoring* (2024).\n"
        "- Social Security Administration, eCBSV technical information: https://www.ssa.gov/dataexchange/eCBSV/\n"
        "- SentiLink, *An Analysis of eCBSV Mismatches* (vendor-authored research): https://resources.sentilink.com/blog/an-analysis-of-ecbsv-mismatches\n"
        "- O*NET Online wage data used as a broad wage proxy: https://www.onetonline.org/link/localwages/13-2099.04"
    )
    st.caption("Retain the full source register, dates accessed and claim-to-source mapping with the final portfolio deliverable.")

st.markdown("---")

