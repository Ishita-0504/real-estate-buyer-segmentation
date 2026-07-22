import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Parcl AI Buyer Intelligence",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# DATA LOADING
# =========================================================
@st.cache_data
def load_data():
    data = pd.read_csv("data/final_data.csv")

    cluster_names = {
        0: "Luxury Investors",
        1: "Established Home Buyers",
        2: "Budget Buyers",
        3: "First-Time Buyers"
    }

    data["Segment"] = data["Cluster"].map(cluster_names)

    numeric_columns = [
        "Age",
        "satisfaction_score",
        "property_count",
        "total_investment",
        "average_property_price",
        "average_floor_area"
    ]

    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    return data


df = load_data()


# =========================================================
# SEGMENT COLOURS
# =========================================================
SEGMENT_COLORS = {
    "Budget Buyers": "#38BDF8",          # Cyan
    "Luxury Investors": "#8B5CF6",       # Purple
    "Established Home Buyers": "#6366F1",# Indigo
    "First-Time Buyers": "#10B981"       # Emerald
}


# =========================================================
# GLOBAL CSS
# =========================================================
st.markdown(
    """
    <style>

    /* Main animated background */
    .stApp {
        background:
            radial-gradient(
                circle at 10% 5%,
                rgba(56, 189, 248, 0.17),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 8%,
                rgba(168, 85, 247, 0.18),
                transparent 32%
            ),
            radial-gradient(
                circle at 65% 90%,
                rgba(236, 72, 153, 0.10),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #020617 0%,
                #081225 40%,
                #111133 75%,
                #0f172a 100%
            );

        background-size: 170% 170%;
        animation: gradientMove 16s ease infinite;
        color: #F8FAFC;
    }

    @keyframes gradientMove {
        0% {
            background-position: 0% 50%;
        }

        50% {
            background-position: 100% 50%;
        }

        100% {
            background-position: 0% 50%;
        }
    }

    .block-container {
        max-width: 1650px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* Hero section */
    .hero {
        position: relative;
        overflow: hidden;

        background:
            linear-gradient(
                135deg,
                rgba(14, 165, 233, 0.16),
                rgba(124, 58, 237, 0.17),
                rgba(219, 39, 119, 0.12)
            );

        border: 1px solid rgba(255, 255, 255, 0.16);
        border-radius: 30px;
        padding: 38px 42px;
        margin-bottom: 26px;

        box-shadow:
            0 22px 70px rgba(0, 0, 0, 0.34),
            inset 0 1px 0 rgba(255, 255, 255, 0.08);

        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
    }

    .hero::before {
        content: "";
        position: absolute;
        width: 270px;
        height: 270px;
        top: -150px;
        right: -70px;

        background: rgba(56, 189, 248, 0.20);
        border-radius: 50%;
        filter: blur(20px);
    }

    .hero h1 {
        position: relative;
        z-index: 2;

        font-size: clamp(32px, 4vw, 52px);
        font-weight: 850;
        line-height: 1.1;
        margin: 0 0 12px 0;

        background: linear-gradient(
            90deg,
            #7DD3FC,
            #C4B5FD,
            #F9A8D4
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero p {
        position: relative;
        z-index: 2;

        color: #CBD5E1;
        font-size: 17px;
        line-height: 1.7;
        margin: 0;
        max-width: 1000px;
    }

    .hero-badge {
        display: inline-block;
        position: relative;
        z-index: 2;

        background: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.28);
        color: #BAE6FD;

        padding: 7px 13px;
        margin-bottom: 16px;
        border-radius: 999px;

        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.6px;
        text-transform: uppercase;
    }

    /* KPI cards */
    .metric-card {
        min-height: 150px;

        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.75),
                rgba(30, 41, 59, 0.58)
            );

        border: 1px solid rgba(148, 163, 184, 0.20);
        border-radius: 24px;
        padding: 23px 24px;

        box-shadow:
            0 16px 42px rgba(0, 0, 0, 0.30),
            inset 0 1px 0 rgba(255, 255, 255, 0.06);

        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);

        transition:
            transform 0.35s ease,
            border-color 0.35s ease,
            box-shadow 0.35s ease;
    }

    .metric-card:hover {
        transform: translateY(-7px) scale(1.015);
        border-color: rgba(56, 189, 248, 0.65);

        box-shadow:
            0 0 24px rgba(56, 189, 248, 0.28),
            0 0 52px rgba(124, 58, 237, 0.17),
            0 20px 45px rgba(0, 0, 0, 0.38);
    }

    .metric-icon {
        font-size: 25px;
        margin-bottom: 10px;
    }

    .metric-title {
        color: #94A3B8;
        font-size: 13px;
        font-weight: 650;
        letter-spacing: 0.3px;
        margin-bottom: 7px;
    }

    .metric-value {
        color: #F8FAFC;
        font-size: clamp(22px, 2vw, 31px);
        font-weight: 820;
        line-height: 1.15;
    }

    .metric-sub {
        color: #7DD3FC;
        font-size: 12px;
        margin-top: 9px;
    }

    /* Section headers */
    .section-heading {
        margin: 10px 0 5px 0;
    }

    .section-heading h2 {
        margin-bottom: 5px;
        font-size: 29px;
    }

    .section-heading p {
        color: #94A3B8;
        margin-top: 0;
        font-size: 14px;
    }

    /* Plotly chart card */
    [data-testid="stPlotlyChart"] {
        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.45),
                rgba(30, 41, 59, 0.30)
            ) !important;

        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 24px;
        padding: 8px;

        box-shadow:
            0 15px 40px rgba(0, 0, 0, 0.24),
            inset 0 1px 0 rgba(255, 255, 255, 0.04);

        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);

        overflow: hidden;
        transition:
            transform 0.32s ease,
            border-color 0.32s ease,
            box-shadow 0.32s ease;
    }

    [data-testid="stPlotlyChart"]:hover {
        transform: translateY(-4px);
        border-color: rgba(56, 189, 248, 0.42);

        box-shadow:
            0 0 24px rgba(56, 189, 248, 0.16),
            0 19px 46px rgba(0, 0, 0, 0.30);
    }

    .js-plotly-plot,
    .plot-container,
    .svg-container,
    .main-svg {
        background: transparent !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"]{
    gap:14px;
    padding:14px;
    border-radius:24px;

    margin-top:40px;
    margin-bottom:25px;
}

.stTabs [data-baseweb="tab"]{
    min-height:62px;
    padding:0 26px;
    border-radius:18px;
    font-size:16px;
    font-weight:700;
    transition:all .3s ease;
}

.stTabs [aria-selected="true"]{
    background:linear-gradient(
        135deg,
        #2563EB,
        #7C3AED,
        #DB2777
    ) !important;

    color:white !important;

    transform:translateY(-2px);

    padding:0 30px !important;

    border:1px solid rgba(255,255,255,.25);

    box-shadow:
        0 0 25px rgba(124,58,237,.45),
        0 0 45px rgba(56,189,248,.20);
}

    /* Sidebar */
    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                rgba(2, 6, 23, 0.98),
                rgba(15, 23, 42, 0.97)
            );

        border-right: 1px solid rgba(148, 163, 184, 0.12);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
    }
    
    .sidebar-brand {
    text-align: center;
    background:
        linear-gradient(
            145deg,
            rgba(37, 99, 235, 0.16),
            rgba(124, 58, 237, 0.18)
        );
    border: 1px solid rgba(125, 211, 252, 0.20);
    border-radius: 24px;
    padding: 24px 14px;
    margin-bottom: 24px;
    box-shadow:
        0 16px 38px rgba(0, 0, 0, 0.28),
        inset 0 1px 0 rgba(255, 255, 255, 0.08);
}

.brand-icon {
    font-size: 34px;
    margin-bottom: 7px;
}

.sidebar-brand h2 {
    margin: 0;
    color: #F8FAFC;
    font-size: 25px;
    font-weight: 800;
}

.sidebar-brand p {
    color: #94A3B8;
    margin: 8px 0 0 0;
    font-size: 11px;
    line-height: 1.5;
}

.sidebar-stat-card {
    position: relative;
    overflow: hidden;
    margin-top: 17px;
    padding: 19px;

    border-radius: 21px;
    border: 1px solid rgba(148, 163, 184, 0.18);

    background:
        linear-gradient(
            145deg,
            rgba(15, 23, 42, 0.82),
            rgba(30, 41, 59, 0.62)
        );

    box-shadow:
        0 14px 34px rgba(0, 0, 0, 0.27),
        inset 0 1px 0 rgba(255, 255, 255, 0.05);

    transition:
        transform 0.3s ease,
        box-shadow 0.3s ease,
        border-color 0.3s ease;
}

.sidebar-stat-card::before {
    content: "";
    position: absolute;
    width: 100px;
    height: 100px;
    right: -45px;
    top: -45px;
    border-radius: 50%;
    filter: blur(5px);
}

.buyers-card::before {
    background: rgba(56, 189, 248, 0.18);
}

.investment-card::before {
    background: rgba(16, 185, 129, 0.18);
}

.sidebar-stat-card:hover {
    transform: translateY(-5px);
    border-color: rgba(56, 189, 248, 0.48);
    box-shadow:
        0 0 22px rgba(56, 189, 248, 0.18),
        0 18px 38px rgba(0, 0, 0, 0.32);
}

.sidebar-stat-top {
    display: flex;
    align-items: center;
    gap: 9px;
    margin-bottom: 14px;
}

.sidebar-stat-icon {
    font-size: 19px;
}

.sidebar-stat-label {
    color: #CBD5E1;
    font-size: 12px;
    font-weight: 700;
}

.sidebar-stat-value {
    color: #F8FAFC;
    font-size: 29px;
    font-weight: 850;
    line-height: 1.15;
}

.sidebar-stat-footer {
    margin-top: 8px;
    color: #7DD3FC;
    font-size: 11px;
}

.investment-card .sidebar-stat-footer {
    color: #6EE7B7;
}

    /* Inputs */
    [data-baseweb="select"] > div,
    [data-testid="stTextInput"] input {
        background: rgba(15, 23, 42, 0.67) !important;
        border-color: rgba(148, 163, 184, 0.20) !important;
        border-radius: 14px !important;
    }

    [data-baseweb="select"] > div:hover,
    [data-testid="stTextInput"] input:hover {
        border-color: rgba(56, 189, 248, 0.50) !important;
    }

    /* Buttons */
    .stButton button,
    .stDownloadButton button,
    [data-testid="stBaseButton-secondary"] {
        border-radius: 15px !important;
        border: 1px solid rgba(56, 189, 248, 0.35) !important;

        background:
            linear-gradient(
                135deg,
                rgba(37, 99, 235, 0.90),
                rgba(124, 58, 237, 0.90)
            ) !important;

        color: white !important;
        font-weight: 700 !important;

        transition:
            transform 0.30s ease,
            box-shadow 0.30s ease,
            border-color 0.30s ease !important;
    }

    .stButton button:hover,
    .stDownloadButton button:hover,
    [data-testid="stBaseButton-secondary"]:hover {
        transform: translateY(-4px) scale(1.025);

        border-color: #7DD3FC !important;

        box-shadow:
            0 0 20px rgba(56, 189, 248, 0.46),
            0 0 36px rgba(124, 58, 237, 0.22) !important;
    }
    
    /* Table horizontal-scroll hint */
.table-scroll-hint {
    display: inline-flex;
    align-items: center;
    gap: 8px;

    margin: 2px 0 10px 0;
    padding: 7px 13px;

    border-radius: 999px;
    border: 1px solid rgba(56, 189, 248, 0.24);

    background: rgba(56, 189, 248, 0.09);
    color: #BAE6FD;

    font-size: 12px;
    font-weight: 650;
}

/* Make the dataframe scrollbar easier to notice */
[data-testid="stDataFrame"] ::-webkit-scrollbar {
    height: 12px !important;
    width: 10px !important;
}

[data-testid="stDataFrame"] ::-webkit-scrollbar-track {
    background: rgba(148, 163, 184, 0.10) !important;
    border-radius: 999px !important;
}

[data-testid="stDataFrame"] ::-webkit-scrollbar-thumb {
    background: linear-gradient(
        90deg,
        #38BDF8,
        #6366F1,
        #8B5CF6
    ) !important;

    border-radius: 999px !important;
    border: 2px solid rgba(15, 23, 42, 0.75) !important;
}

[data-testid="stDataFrame"] ::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(
        90deg,
        #7DD3FC,
        #818CF8,
        #A78BFA
    ) !important;
}

    /* AI recommendation cards */
    .ai-card {
        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.68),
                rgba(30, 41, 59, 0.50)
            );

        border: 1px solid rgba(148, 163, 184, 0.17);
        border-left: 4px solid #38BDF8;

        border-radius: 18px;
        padding: 17px 19px;
        margin-bottom: 12px;

        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.22);
        backdrop-filter: blur(14px);

        transition:
            transform 0.28s ease,
            border-color 0.28s ease,
            box-shadow 0.28s ease;
    }

    .ai-card:hover {
        transform: translateX(6px);
        border-color: rgba(56, 189, 248, 0.68);

        box-shadow:
            0 0 20px rgba(56, 189, 248, 0.17),
            0 14px 32px rgba(0, 0, 0, 0.28);
    }

    .ai-card-title {
        color: #F8FAFC;
        font-size: 15px;
        font-weight: 680;
        margin-bottom: 5px;
    }

    .ai-card-subtitle {
        color: #94A3B8;
        font-size: 12px;
    }

    /* Dataframe outer styling */
    [data-testid="stDataFrame"] {
    border: 1px solid rgba(125, 211, 252, 0.22) !important;
    border-radius: 20px !important;
    overflow: hidden !important;

    background:
        linear-gradient(
            145deg,
            rgba(15, 23, 42, 0.72),
            rgba(30, 41, 59, 0.52)
        ) !important;

    box-shadow:
        0 15px 38px rgba(0, 0, 0, 0.28),
        inset 0 1px 0 rgba(255, 255, 255, 0.05);}

    /* Header toolbar region */
    [data-testid="stDataFrame"] > div:first-child {
    background:
        linear-gradient(
            90deg,
            rgba(37, 99, 235, 0.24),
            rgba(124, 58, 237, 0.22),
            rgba(219, 39, 119, 0.14)
        ) !important;}

    /* Table text */
    [data-testid="stDataFrame"] {
    color: #F8FAFC !important;
    font-weight: 600;}  

    /* Streamlit metrics used inside tabs/sidebar */
    [data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.64),
                rgba(30, 41, 59, 0.44)
            );

        border: 1px solid rgba(148, 163, 184, 0.16);
        border-radius: 19px;

        padding: 17px;

        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.22);
    }

    h1, h2, h3 {
        color: #F8FAFC;
    }

    hr {
        border-color: rgba(148, 163, 184, 0.13);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# CHART STYLING FUNCTION
# =========================================================
def beautify_chart(
    fig,
    height=560,
    show_legend=True,
    legend_orientation="v"
):
    fig.update_layout(
        template="plotly_dark",
        height=height,

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="#CBD5E1",
            family="Arial, sans-serif",
            size=13
        ),

        title=dict(
            font=dict(
                size=21,
                color="#F8FAFC"
            ),
            x=0.03,
            xanchor="left"
        ),

        margin=dict(
            l=35,
            r=30,
            t=75,
            b=45
        ),

        hoverlabel=dict(
            bgcolor="#111827",
            bordercolor="#38BDF8",
            font=dict(color="#F8FAFC")
        ),

        legend=dict(
            visible=show_legend,
            orientation=legend_orientation,
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            font=dict(color="#CBD5E1")
        ),

        xaxis=dict(
            showgrid=False,
            zeroline=False,
            title_font=dict(color="#CBD5E1"),
            tickfont=dict(color="#CBD5E1")
        ),

        yaxis=dict(
            gridcolor="rgba(148,163,184,0.14)",
            zeroline=False,
            title_font=dict(color="#CBD5E1"),
            tickfont=dict(color="#CBD5E1")
        )
    )

    return fig


PLOT_CONFIG = {
    "displaylogo": False,
    "responsive": True,
    "scrollZoom": False,
    "modeBarButtonsToRemove": [
        "lasso2d",
        "select2d"
    ]
}


# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.markdown(
    """
    <div class="sidebar-brand">
        <div class="brand-icon">🏙️</div>
        <h2>Parcl Analytics</h2>
        <p>Real Estate Market Intelligence</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("### 🔍 Smart Filters")

country_options = sorted(df["country"].dropna().unique())
region_options = sorted(df["region"].dropna().unique())
client_type_options = sorted(df["client_type"].dropna().unique())
purpose_options = sorted(df["acquisition_purpose"].dropna().unique())

selected_countries = st.sidebar.multiselect(
    "🌍 Country",
    country_options,
    placeholder="All countries"
)

selected_regions = st.sidebar.multiselect(
    "📍 Region",
    region_options,
    placeholder="All regions"
)

selected_client_types = st.sidebar.multiselect(
    "👤 Client Type",
    client_type_options,
    placeholder="All client types"
)

selected_purposes = st.sidebar.multiselect(
    "🎯 Acquisition Purpose",
    purpose_options,
    placeholder="All purposes"
)

countries = (
    selected_countries
    if selected_countries
    else country_options
)

regions = (
    selected_regions
    if selected_regions
    else region_options
)

client_types = (
    selected_client_types
    if selected_client_types
    else client_type_options
)

purposes = (
    selected_purposes
    if selected_purposes
    else purpose_options
)

filtered = df[
    df["country"].isin(countries)
    & df["region"].isin(regions)
    & df["client_type"].isin(client_types)
    & df["acquisition_purpose"].isin(purposes)
].copy()

st.sidebar.divider()

filtered_investment = filtered["total_investment"].sum()

st.sidebar.markdown(
f"""
<div class="sidebar-stat-card buyers-card">
<div class="sidebar-stat-top">
<div class="sidebar-stat-icon">👥</div>
<div class="sidebar-stat-label">Filtered Buyers</div>
</div>
<div class="sidebar-stat-value">{len(filtered):,}</div>
<div class="sidebar-stat-footer">Active customer profiles</div>
</div>

<div class="sidebar-stat-card investment-card">
<div class="sidebar-stat-top">
<div class="sidebar-stat-icon">💎</div>
<div class="sidebar-stat-label">Filtered Investment</div>
</div>
<div class="sidebar-stat-value">${filtered_investment / 1_000_000:,.1f}M</div>
<div class="sidebar-stat-footer">Total portfolio value</div>
</div>
""",
unsafe_allow_html=True
)

st.sidebar.caption(
    "Leave a filter empty to include all available values."
)


# =========================================================
# EMPTY FILTER RESULT HANDLING
# =========================================================
if filtered.empty:
    st.warning(
        "No buyers match the selected filters. "
        "Please change or clear one or more filters."
    )
    st.stop()


# =========================================================
# HERO SECTION
# =========================================================
st.markdown("""
    <div class="hero">

    <h1>🏠 AI Buyer Intelligence Dashboard</h1>

    <p class="hero-subtitle">
        Built for <b>Parcl Co. Limited</b> • Machine Learning-Based Buyer Segmentation Platform
    </p>
    </div> """, unsafe_allow_html=True)

st.markdown(f"""
<div style="display:flex;gap:14px;flex-wrap:wrap;margin-bottom:22px;">

<div style="padding:8px 16px;background:rgba(168,85,247,.12);
border:1px solid rgba(56,189,248,.25);
border-radius:999px;font-weight:700;">
📊 {len(filtered):,} Buyers
</div>

<div style="padding:8px 16px;background:rgba(168,85,247,.12);
border:1px solid rgba(56,189,248,.25);
border-radius:999px;font-weight:700;">
🌍 {filtered['country'].nunique()} Countries
</div>

<div style="padding:8px 16px;background:rgba(168,85,247,.12);
border:1px solid rgba(168,85,247,.25);
border-radius:999px;font-weight:700;">
🏘️ {filtered['Segment'].nunique()} AI Segments
</div>

<div style="padding:8px 16px;background:rgba(168,85,247,.12);
border:1px solid rgba(16,185,129,.28);
border-radius:999px;font-weight:700;">
💰 ${filtered['total_investment'].sum()/1_000_000:.2f}M Investment
</div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# KPI CARDS
# =========================================================
total_buyers = len(filtered)
total_investment = filtered["total_investment"].sum()
average_property_price = filtered["average_property_price"].mean()
average_buyer_age = filtered["Age"].mean()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">👥</div>
            <div class="metric-title">TOTAL BUYERS</div>
            <div class="metric-value">{total_buyers:,}</div>
            <div class="metric-sub">Filtered customer population</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">💰</div>
            <div class="metric-title">TOTAL INVESTMENT</div>
            <div class="metric-value">
                ${total_investment / 1_000_000:,.1f}M
            </div>
            <div class="metric-sub">Aggregate buyer investment</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">🏙️</div>
            <div class="metric-title">AVG PROPERTY PRICE</div>
            <div class="metric-value">
                ${average_property_price:,.0f}
            </div>
            <div class="metric-sub">Average buyer-level property value</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">📊</div>
            <div class="metric-title">AVG BUYER AGE</div>
            <div class="metric-value">{average_buyer_age:.1f}</div>
            <div class="metric-sub">
                Across {filtered['Segment'].nunique()} active segments
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# CLUSTER SUMMARY
# =========================================================
cluster_summary = (
    filtered
    .groupby("Segment", observed=False)
    .agg(
        buyers=("client_id", "count"),
        avg_investment=("total_investment", "mean"),
        avg_property_price=("average_property_price", "mean"),
        avg_property_count=("property_count", "mean"),
        avg_floor_area=("average_floor_area", "mean"),
        avg_age=("Age", "mean"),
        avg_satisfaction=("satisfaction_score", "mean"),
        loan_rate=(
            "loan_applied",
            lambda values:
                values.astype(str)
                .str.strip()
                .str.lower()
                .eq("yes")
                .mean() * 100
        )
    )
    .reset_index()
)

st.markdown(
    "<div style='height:35px;'></div>",
    unsafe_allow_html=True
)

# =========================================================
# DASHBOARD TABS
# =========================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "👥 Overview",
        "📈 Investor Behaviour",
        "🌍 Geography",
        "🤖 AI Insights",
        "🔎 Buyer Explorer"
    ]
)


# =========================================================
# TAB 1 — OVERVIEW
# =========================================================
with tab1:
    st.markdown(
        """
        <div class="section-heading">
            <h2>👥 Buyer Segmentation Overview</h2>
            <p>
                Understand the size, composition and profile of each
                machine-learning-generated buyer segment.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    overview_col1, overview_col2 = st.columns(2)

    with overview_col1:
        segment_counts = (
            filtered["Segment"]
            .value_counts()
            .rename_axis("Segment")
            .reset_index(name="Buyers")
        )

        fig = px.pie(
            segment_counts,
            names="Segment",
            values="Buyers",
            color="Segment",
            color_discrete_map=SEGMENT_COLORS,
            hole=0.62,
            title="Buyer Segment Distribution"
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Buyers: %{value:,}<br>"
                "Share: %{percent}"
                "<extra></extra>"
            ),
            marker=dict(
                line=dict(
                    color="rgba(255,255,255,0.20)",
                    width=2
                )
            )
        )

        fig.add_annotation(
            text=f"<b>{len(filtered):,}</b><br>Total Buyers",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(
                size=18,
                color="#F8FAFC"
            )
        )

        fig = beautify_chart(
            fig,
            height=590,
            show_legend=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config=PLOT_CONFIG
        )

    with overview_col2:
        fig = px.bar(
            cluster_summary.sort_values(
                "buyers",
                ascending=False
            ),
            x="Segment",
            y="buyers",
            color="Segment",
            color_discrete_map=SEGMENT_COLORS,
            text="buyers",
            title="Buyer Count by Segment"
        )

        fig.update_traces(
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Buyers: %{y:,}"
                "<extra></extra>"
            ),
            marker_line_width=0
        )

        fig = beautify_chart(
            fig,
            height=590,
            show_legend=False
        )

        fig.update_layout(
            xaxis_title="",
            yaxis_title="Buyer count"
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config=PLOT_CONFIG
        )

    st.markdown(
        """
        <div class="section-heading">
            <h2>📋 Segment Performance Summary</h2>
            <p>
                Compare segment size, investment value, property behaviour,
                demographics and financing patterns.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    summary_display = cluster_summary.rename(
        columns={
            "Segment": "Segment",
            "buyers": "Buyers",
            "avg_investment": "Avg Investment",
            "avg_property_price": "Avg Property Value",
            "avg_property_count": "Avg Properties",
            "avg_floor_area": "Avg Area",
            "avg_age": "Avg Age",
            "avg_satisfaction": "Satisfaction",
            "loan_rate": "Loan Adoption"
        }
    )

    st.markdown(
    """
    <div class="table-scroll-hint">
        <span>↔</span>
        Scroll horizontally to view all performance metrics
    </div>
    """,
    unsafe_allow_html=True
)

    st.dataframe(
        summary_display,
        use_container_width=True,
        hide_index=True,
        height=185,
        column_config={
            "Segment": st.column_config.TextColumn(
                "Buyer Segment",
                help="Machine-learning-generated buyer category",
                width="large"
            ),

            "Buyers": st.column_config.NumberColumn(
                "Buyers",
                format="%,d",
                width="small"
            ),

            "Avg Investment": st.column_config.NumberColumn(
                "Avg Investment",
                format="$%,.0f",
                width="medium"
            ),

            "Avg Property Value": st.column_config.NumberColumn(
                "Avg Property Value",
                format="$%,.0f",
                width="medium"
            ),

            "Avg Properties": st.column_config.NumberColumn(
                "Properties",
                format="%.2f",
                width="small"
            ),

            "Avg Area": st.column_config.NumberColumn(
                "Avg Area",
                format="%,.0f sqft",
                width="small"
            ),

            "Avg Age": st.column_config.NumberColumn(
                "Avg Age",
                format="%.1f",
                width="small"
            ),

            "Satisfaction": st.column_config.ProgressColumn(
                "Satisfaction",
                help="Average customer satisfaction score out of 5",
                min_value=0,
                max_value=5,
                format="%.2f",
                width="medium"
            ),

            "Loan Adoption": st.column_config.ProgressColumn(
                "Loan Adoption",
                help="Percentage of buyers who applied for a loan",
                min_value=0,
                max_value=100,
                format="%.1f%%",
                width="medium"
            )
        }
    )


# =========================================================
# TAB 2 — INVESTOR BEHAVIOUR
# =========================================================
with tab2:
    st.markdown(
        """
        <div class="section-heading">
            <h2>📈 Investor Behaviour Dashboard</h2>
            <p>
                Compare buyer segments using investment, property,
                demographic and satisfaction indicators.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    metric_labels = {
        "Average Investment": "avg_investment",
        "Average Property Price": "avg_property_price",
        "Average Property Count": "avg_property_count",
        "Average Floor Area": "avg_floor_area",
        "Average Satisfaction": "avg_satisfaction",
        "Average Age": "avg_age"
    }

    selected_metric_label = st.selectbox(
        "Choose a metric to compare",
        list(metric_labels.keys())
    )

    selected_metric = metric_labels[selected_metric_label]

    metric_chart = cluster_summary.sort_values(
        selected_metric,
        ascending=False
    )

    fig = px.bar(
        metric_chart,
        x="Segment",
        y=selected_metric,
        color="Segment",
        color_discrete_map=SEGMENT_COLORS,
        text_auto=".3s",
        title=f"{selected_metric_label} by Segment"
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
        marker_line_width=0
    )

    fig = beautify_chart(
        fig,
        height=610,
        show_legend=False
    )

    fig.update_layout(
        xaxis_title="",
        yaxis_title=selected_metric_label
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config=PLOT_CONFIG
    )

    behaviour_col1, behaviour_col2 = st.columns(2)

    with behaviour_col1:
        fig = px.scatter(
            filtered,
            x="average_property_price",
            y="total_investment",
            color="Segment",
            color_discrete_map=SEGMENT_COLORS,
            size="property_count",
            size_max=36,
            opacity=0.78,
            hover_name="client_id",
            hover_data={
                "country": True,
                "region": True,
                "client_type": True,
                "property_count": True,
                "average_property_price": ":$,.0f",
                "total_investment": ":$,.0f"
            },
            title="Investment vs Average Property Price"
        )

        fig = beautify_chart(
            fig,
            height=620,
            show_legend=True
        )

        fig.update_layout(
            xaxis_title="Average property price",
            yaxis_title="Total investment"
        )

        fig.update_xaxes(tickprefix="$", tickformat="~s")
        fig.update_yaxes(tickprefix="$", tickformat="~s")

        st.plotly_chart(
            fig,
            use_container_width=True,
            config=PLOT_CONFIG
        )

    with behaviour_col2:
        fig = px.box(
            filtered,
            x="Segment",
            y="total_investment",
            color="Segment",
            color_discrete_map=SEGMENT_COLORS,
            points="outliers",
            title="Investment Distribution by Segment"
        )

        fig = beautify_chart(
            fig,
            height=620,
            show_legend=False
        )

        fig.update_layout(
            xaxis_title="",
            yaxis_title="Total investment"
        )

        fig.update_yaxes(
            tickprefix="$",
            tickformat="~s"
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config=PLOT_CONFIG
        )

    financing_col1, financing_col2 = st.columns(2)

    with financing_col1:
        loan_data = (
            filtered
            .groupby(
                ["loan_applied", "Segment"],
                observed=False
            )
            .size()
            .reset_index(name="Buyer Count")
        )

        fig = px.bar(
            loan_data,
            x="loan_applied",
            y="Buyer Count",
            color="Segment",
            color_discrete_map=SEGMENT_COLORS,
            barmode="group",
            title="Loan Adoption by Segment"
        )

        fig = beautify_chart(
            fig,
            height=540,
            show_legend=True
        )

        fig.update_layout(
            xaxis_title="Loan applied",
            yaxis_title="Buyer count"
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config=PLOT_CONFIG
        )

    with financing_col2:
        purpose_data = (
            filtered
            .groupby(
                ["acquisition_purpose", "Segment"],
                observed=False
            )
            .size()
            .reset_index(name="Buyer Count")
        )

        fig = px.bar(
            purpose_data,
            x="acquisition_purpose",
            y="Buyer Count",
            color="Segment",
            color_discrete_map=SEGMENT_COLORS,
            barmode="group",
            title="Purchase Purpose by Segment"
        )

        fig = beautify_chart(
            fig,
            height=540,
            show_legend=True
        )

        fig.update_layout(
            xaxis_title="Acquisition purpose",
            yaxis_title="Buyer count"
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config=PLOT_CONFIG
        )


# =========================================================
# TAB 3 — GEOGRAPHY
# =========================================================
with tab3:
    st.markdown(
        """
        <div class="section-heading">
            <h2>🌍 Geographic Buyer Analysis</h2>
            <p>
                Discover where buyers originate and how segment composition
                changes across countries and regions.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    country_count = (
        filtered
        .groupby("country", observed=False)
        .size()
        .reset_index(name="Buyer Count")
    )

    fig = px.choropleth(
        country_count,
        locations="country",
        locationmode="country names",
        color="Buyer Count",
        hover_name="country",
        color_continuous_scale=[
            [0.00, "#172554"],
            [0.25, "#1D4ED8"],
            [0.50, "#06B6D4"],
            [0.75, "#8B5CF6"],
            [1.00, "#EC4899"]
        ],
        title="Global Buyer Distribution"
    )

    fig.update_geos(
        bgcolor="rgba(0,0,0,0)",
        showframe=False,
        showcoastlines=True,
        coastlinecolor="rgba(148,163,184,0.30)",
        showland=True,
        landcolor="rgba(30,41,59,0.45)",
        showocean=True,
        oceancolor="rgba(2,6,23,0.35)"
    )

    fig = beautify_chart(
        fig,
        height=700,
        show_legend=False
    )

    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Buyers",
            thickness=13,
            len=0.62
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config=PLOT_CONFIG
    )

    geo_col1, geo_col2 = st.columns(2)

    with geo_col1:
        country_segment = (
            filtered
            .groupby(
                ["country", "Segment"],
                observed=False
            )
            .size()
            .reset_index(name="Buyer Count")
        )

        fig = px.bar(
            country_segment,
            x="country",
            y="Buyer Count",
            color="Segment",
            color_discrete_map=SEGMENT_COLORS,
            barmode="stack",
            title="Buyer Segments by Country"
        )

        fig = beautify_chart(
            fig,
            height=610,
            show_legend=True
        )

        fig.update_layout(
            xaxis_title="",
            yaxis_title="Buyer count"
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config=PLOT_CONFIG
        )

    with geo_col2:
        region_segment = (
            filtered
            .groupby(
                ["region", "Segment"],
                observed=False
            )
            .size()
            .reset_index(name="Buyer Count")
        )

        top_regions = (
            filtered["region"]
            .value_counts()
            .head(15)
            .index
        )

        region_segment = region_segment[
            region_segment["region"].isin(top_regions)
        ]

        fig = px.bar(
            region_segment,
            y="region",
            x="Buyer Count",
            color="Segment",
            color_discrete_map=SEGMENT_COLORS,
            orientation="h",
            barmode="stack",
            title="Top Regions by Buyer Segment"
        )

        fig = beautify_chart(
            fig,
            height=610,
            show_legend=True
        )

        fig.update_layout(
            yaxis={
                "categoryorder": "total ascending",
                "title": ""
            },
            xaxis_title="Buyer count"
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config=PLOT_CONFIG
        )


# =========================================================
# TAB 4 — AI INSIGHTS
# =========================================================
with tab4:
    st.markdown(
        """
        <div class="section-heading">
            <h2>🤖 AI Segment Recommendation Panel</h2>
            <p>
                Review data-driven segment profiles and recommended
                marketing strategies for each buyer group.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    available_segments = sorted(
        filtered["Segment"].dropna().unique()
    )

    selected_segment = st.selectbox(
        "Select a buyer segment",
        available_segments
    )

    segment_data = filtered[
        filtered["Segment"] == selected_segment
    ].copy()

    recommendations = {
        "Luxury Investors": [
            (
                "Premium positioning",
                "Promote luxury properties, premium amenities and "
                "high-value property bundles."
            ),
            (
                "Private access",
                "Offer exclusive previews, private launches and "
                "invite-only investment events."
            ),
            (
                "Relationship management",
                "Assign dedicated relationship managers for personalised "
                "property and portfolio support."
            ),
            (
                "Investment messaging",
                "Emphasise long-term appreciation, exclusivity and "
                "premium asset value."
            )
        ],

        "Established Home Buyers": [
            (
                "Lifestyle marketing",
                "Promote family-friendly homes, community facilities and "
                "long-term lifestyle benefits."
            ),
            (
                "Trust-based communication",
                "Use reliability, neighbourhood quality and long-term "
                "value as primary campaign messages."
            ),
            (
                "Financing assistance",
                "Provide documentation guidance and stable financing "
                "options."
            ),
            (
                "Referral strategy",
                "Strengthen referral campaigns and relationship-based "
                "customer acquisition."
            )
        ],

        "Budget Buyers": [
            (
                "Affordable inventory",
                "Highlight entry-level units and properties with strong "
                "price-to-value benefits."
            ),
            (
                "Flexible financing",
                "Promote loan support, flexible payment plans and "
                "EMI-friendly options."
            ),
            (
                "Transparent pricing",
                "Use clear price comparisons and cost breakdowns in "
                "digital campaigns."
            ),
            (
                "Ownership campaigns",
                "Position property ownership as accessible and achievable."
            )
        ],

        "First-Time Buyers": [
            (
                "Buyer education",
                "Provide beginner-friendly property guides and purchasing "
                "checklists."
            ),
            (
                "Financial tools",
                "Offer EMI calculators, affordability estimators and "
                "financing education."
            ),
            (
                "Guided onboarding",
                "Provide personalised support throughout the purchase "
                "journey."
            ),
            (
                "Digital-first outreach",
                "Use social media, mobile-first campaigns and interactive "
                "content."
            )
        ]
    }

    insight1, insight2, insight3, insight4 = st.columns(4)

    loan_adoption_rate = (
        segment_data["loan_applied"]
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("yes")
        .mean()
        * 100)

    insight1.metric(
        "Buyers",
        f"{len(segment_data):,}")

    insight2.metric(  
        "Avg Investment",
        f"${segment_data['total_investment'].mean():,.0f}")

    insight3.metric(
        "Avg Satisfaction",
        f"{segment_data['satisfaction_score'].mean():.2f} / 5")

    insight4.metric( 
        "Loan Adoption",
        f"{loan_adoption_rate:.1f}%")

    st.markdown("### 🎯 Recommended Marketing Strategy")

    for title, description in recommendations.get(
        selected_segment,
        []
    ):
        st.markdown(
            f"""
            <div class="ai-card">
                <div class="ai-card-title">✅ {title}</div>
                <div class="ai-card-subtitle">{description}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### 📡 Segment Behaviour Radar")

    radar_metrics = {
        "avg_investment": "Investment",
        "avg_property_price": "Property Price",
        "avg_property_count": "Property Count",
        "avg_floor_area": "Floor Area",
        "avg_satisfaction": "Satisfaction",
        "loan_rate": "Loan Adoption"
    }

    radar_data = cluster_summary.copy()

    for metric in radar_metrics:
        maximum = radar_data[metric].max()
        minimum = radar_data[metric].min()

        if maximum == minimum:
            radar_data[f"{metric}_scaled"] = 0.5
        else:
            radar_data[f"{metric}_scaled"] = (
                radar_data[metric] - minimum
            ) / (maximum - minimum)

    fig = go.Figure()

    for _, row in radar_data.iterrows():
        segment_name = row["Segment"]

        values = [
            row[f"{metric}_scaled"]
            for metric in radar_metrics
        ]

        values.append(values[0])

        categories = list(radar_metrics.values())
        categories.append(categories[0])

        fig.add_trace(
            go.Scatterpolar(
                r=values,
                theta=categories,
                fill="toself",
                name=segment_name,
                opacity=0.62,
                line=dict(
                    color=SEGMENT_COLORS.get(
                        segment_name,
                        "#38BDF8"
                    ),
                    width=3
                ),
                marker=dict(
                    color=SEGMENT_COLORS.get(
                        segment_name,
                        "#38BDF8"
                    )
                )
            )
        )

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",

            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickfont=dict(color="#94A3B8"),
                gridcolor="rgba(148,163,184,0.18)"
            ),

            angularaxis=dict(
                tickfont=dict(
                    color="#E2E8F0",
                    size=13
                ),
                gridcolor="rgba(148,163,184,0.18)"
            )
        )
    )

    fig = beautify_chart(
        fig,
        height=690,
        show_legend=True,
        legend_orientation="h"
    )

    fig.update_layout(
        title="Comparative Buyer Segment Profile",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.18,
            xanchor="center",
            x=0.5
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config=PLOT_CONFIG
    )

    gauge_col1, gauge_col2 = st.columns(2)

    with gauge_col1:
        satisfaction_value = (
            segment_data["satisfaction_score"].mean()
        )

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=satisfaction_value,

                number={
                    "suffix": " / 5",
                    "font": {
                        "color": "#F8FAFC",
                        "size": 38
                    }
                },

                title={
                    "text": "Average Satisfaction",
                    "font": {
                        "color": "#CBD5E1",
                        "size": 18
                    }
                },

                gauge={
                    "axis": {
                        "range": [0, 5],
                        "tickcolor": "#CBD5E1"
                    },

                    "bar": {
                        "color": SEGMENT_COLORS.get(
                            selected_segment,
                            "#38BDF8"
                        )
                    },

                    "bgcolor": "rgba(15,23,42,0.35)",
                    "borderwidth": 0,

                    "steps": [
                        {
                            "range": [0, 2],
                            "color": "rgba(239,68,68,0.20)"
                        },
                        {
                            "range": [2, 3.5],
                            "color": "rgba(245,158,11,0.20)"
                        },
                        {
                            "range": [3.5, 5],
                            "color": "rgba(52,211,153,0.20)"
                        }
                    ]
                }
            )
        )

        fig = beautify_chart(
            fig,
            height=450,
            show_legend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config=PLOT_CONFIG
        )

    with gauge_col2:
        purpose_mix = (
            segment_data["acquisition_purpose"]
            .value_counts()
            .rename_axis("Purpose")
            .reset_index(name="Buyers")
        )

        fig = px.pie(
            purpose_mix,
            names="Purpose",
            values="Buyers",
            hole=0.68,
            title=f"Purchase Purpose: {selected_segment}",
            color_discrete_sequence=[
                "#38BDF8",
                "#A78BFA",
                "#F59E0B",
                "#34D399"
            ]
        )

        fig.update_traces(
            textinfo="percent+label",
            marker=dict(
                line=dict(
                    color="rgba(255,255,255,0.20)",
                    width=2
                )
            )
        )

        fig = beautify_chart(
            fig,
            height=450,
            show_legend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config=PLOT_CONFIG
        )


# =========================================================
# TAB 5 — BUYER EXPLORER
# =========================================================
with tab5:
    st.markdown(
        """
        <div class="section-heading">
            <h2>🔎 Buyer-Level Explorer</h2>
            <p>
                Search individual buyers, review detailed profiles and
                export the filtered customer dataset.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    search_id = st.text_input(
        "Search Client ID",
        placeholder="Example: C0001"
    )

    explorer = filtered.copy()

    if search_id.strip():
        explorer = explorer[
            explorer["client_id"]
            .astype(str)
            .str.contains(
                search_id.strip(),
                case=False,
                na=False
            )
        ]

    explorer_columns = [
        "client_id",
        "client_type",
        "gender",
        "country",
        "region",
        "acquisition_purpose",
        "loan_applied",
        "Age",
        "property_count",
        "total_investment",
        "average_property_price",
        "average_floor_area",
        "satisfaction_score",
        "Segment"
    ]

    st.dataframe(
        explorer[explorer_columns],
        use_container_width=True,
        hide_index=True,
        height=480,
        column_config={
            "client_id": "Client ID",
            "client_type": "Client Type",
            "gender": "Gender",
            "country": "Country",
            "region": "Region",
            "acquisition_purpose": "Purpose",
            "loan_applied": "Loan",
            "Age": st.column_config.NumberColumn(
                "Age",
                format="%.0f"
            ),
            "property_count": st.column_config.NumberColumn(
                "Properties",
                format="%.0f"
            ),
            "total_investment": st.column_config.NumberColumn(
                "Total Investment",
                format="$%,.0f"
            ),
            "average_property_price":
                st.column_config.NumberColumn(
                    "Avg Property Price",
                    format="$%,.0f"
                ),
            "average_floor_area":
                st.column_config.NumberColumn(
                    "Avg Floor Area",
                    format="%,.0f sqft"
                ),
            "satisfaction_score":
                st.column_config.ProgressColumn(
                    "Satisfaction",
                    min_value=0,
                    max_value=5,
                    format="%.1f"
                ),
            "Segment": "Buyer Segment"
        }
    )

    csv_data = explorer.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download Filtered Buyer Data",
        data=csv_data,
        file_name="filtered_buyer_segments.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.markdown("### 🏆 Top 10 High-Value Buyers")

    top_buyers = (
        filtered
        .nlargest(10, "total_investment")
        .sort_values(
            "total_investment",
            ascending=True
        )
    )

    fig = px.bar(
        top_buyers,
        x="total_investment",
        y="client_id",
        orientation="h",
        color="Segment",
        color_discrete_map=SEGMENT_COLORS,
        text_auto=".3s",
        hover_data={
            "country": True,
            "region": True,
            "client_type": True,
            "property_count": True,
            "total_investment": ":$,.0f"
        },
        title="Top Buyers by Total Investment"
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False
    )

    fig = beautify_chart(
        fig,
        height=660,
        show_legend=True
    )

    fig.update_layout(
        xaxis_title="Total investment",
        yaxis_title=""
    )

    fig.update_xaxes(
        tickprefix="$",
        tickformat="~s"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config=PLOT_CONFIG
    )


# =========================================================
# FOOTER
# =========================================================
st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#64748B;
        font-size:12px;
        padding:10px 0 5px 0;
    ">
        Parcl AI Buyer Intelligence Platform • Machine Learning-based
        Real Estate Market Intelligence
    </div>
    """,
    unsafe_allow_html=True
)