import pandas as pd
import plotly.io as pio
import streamlit as st
from fpdf import FPDF

from src.analysis import (
    area_data,
    covid_data,
    get_kpis,
    monthly_data,
    regional_data,
    yearly_data,
)

from src.charts import (
    area_chart,
    monthly_chart,
    overall_trend,
    regional_chart,
    yearly_chart,
)

from src.insights import generate_insights


# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Unemployment Analytics",
    layout="wide",
)


# =====================================================
# DATA
# =====================================================
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)

    df.columns = df.columns.str.strip()

    df = df.dropna()
    df = df.drop_duplicates()

    df["Date"] = pd.to_datetime(
        df["Date"],
        dayfirst=True,
    )

    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month_name()

    return df


# =====================================================
# PDF
# =====================================================
def create_pdf(insights):
    pdf = FPDF()

    pdf.add_page()

    pdf.set_font(
        "Arial",
        size=12,
    )

    pdf.cell(
        200,
        10,
        txt="Unemployment Analysis Report",
        ln=True,
    )

    for item in insights:
        pdf.multi_cell(
            0,
            10,
            item,
        )

    return pdf.output(
        dest="S"
    ).encode(
        "latin-1"
    )


# =====================================================
# HEADER
# =====================================================
st.title(
    "📊 Unemployment Analysis Dashboard"
)

st.caption(
    "Economic, Covid-19 and Seasonal Analysis"
)


# =====================================================
# FILE UPLOAD
# =====================================================
uploaded_file = st.sidebar.file_uploader(
    "Upload Dataset",
    type=["csv"],
)


if uploaded_file is None:
    st.info(
        "Upload unemployment dataset."
    )
    st.stop()


df = load_data(
    uploaded_file
)


# =====================================================
# PROFESSIONAL FILTER PANEL
# =====================================================
st.sidebar.title(
    "🔎 Filter Panel"
)


# ---------- reset ----------
if st.sidebar.button(
    "Reset Filters"
):
    st.cache_data.clear()
    st.rerun()


# ---------- region ----------
with st.sidebar.expander(
    "State Filter",
    expanded=True,
):

    all_regions = sorted(
        df["Region"].unique()
    )

    select_all = st.checkbox(
        "Select All States",
        value=True,
    )

    selected_regions = st.multiselect(
        "Search State",
        options=all_regions,
        default=(
            all_regions
            if select_all
            else []
        ),
    )


# ---------- area ----------
with st.sidebar.expander(
    "Area Filter"
):

    all_areas = sorted(
        df["Area"].unique()
    )

    selected_areas = st.multiselect(
        "Search Area",
        options=all_areas,
        default=all_areas,
    )


# ---------- year ----------
with st.sidebar.expander(
    "Year Filter"
):

    all_years = sorted(
        df["Year"].unique()
    )

    selected_years = st.multiselect(
        "Search Year",
        options=all_years,
        default=all_years,
    )


# ---------- month ----------
with st.sidebar.expander(
    "Month Filter"
):

    all_months = list(
        df["Month"].unique()
    )

    selected_months = st.multiselect(
        "Search Month",
        options=all_months,
        default=all_months,
    )


# ---------- date ----------
with st.sidebar.expander(
    "Date Filter"
):

    date_range = st.date_input(
        "Choose Date Range",
        (
            df["Date"].min(),
            df["Date"].max(),
        ),
    )


# =====================================================
# FILTER LOGIC
# =====================================================
filtered_df = df.copy()


filtered_df = filtered_df[
    filtered_df["Region"].isin(
        selected_regions
    )
]

filtered_df = filtered_df[
    filtered_df["Area"].isin(
        selected_areas
    )
]

filtered_df = filtered_df[
    filtered_df["Year"].isin(
        selected_years
    )
]

filtered_df = filtered_df[
    filtered_df["Month"].isin(
        selected_months
    )
]


filtered_df = filtered_df[
    (
        filtered_df["Date"]
        >= pd.Timestamp(
            date_range[0]
        )
    )
    &
    (
        filtered_df["Date"]
        <= pd.Timestamp(
            date_range[1]
        )
    )
]


if filtered_df.empty:
    st.warning(
        "No records found."
    )
    st.stop()


# =====================================================
# KPI
# =====================================================
kpi = get_kpis(
    filtered_df
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Average Rate",
    kpi["avg"],
)

c2.metric(
    "Maximum Rate",
    kpi["max"],
)

c3.metric(
    "Minimum Rate",
    kpi["min"],
)

c4.metric(
    "Regions",
    kpi["states"],
)


# =====================================================
# TABS
# =====================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    [
        "Dataset",
        "Trend",
        "Covid-19",
        "Seasonal",
        "Regional",
        "Area",
        "Insights",
    ]
)


# =====================================================
# 1 DATASET
# =====================================================
with tab1:

    st.header(
        "Dataset Overview"
    )

    st.dataframe(
        filtered_df,
        use_container_width=True,
    )


# =====================================================
# 2 TREND
# =====================================================
with tab2:

    st.header(
        "Unemployment Rate Trend Analysis"
    )

    fig = overall_trend(
        filtered_df
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# =====================================================
# 3 COVID
# =====================================================
with tab3:

    st.header(
        "Impact of Covid-19 on Employment"
    )

    fig = overall_trend(
        covid_data(
            filtered_df
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# =====================================================
# 4 SEASONAL
# =====================================================
with tab4:

    st.header(
        "Seasonal Trend Analysis"
    )

    fig = monthly_chart(
        monthly_data(
            filtered_df
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# =====================================================
# 5 REGION
# =====================================================
with tab5:

    st.header(
        "Regional Comparison"
    )

    fig = regional_chart(
        regional_data(
            filtered_df
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# =====================================================
# 6 AREA
# =====================================================
with tab6:

    st.header(
        "Urban vs Rural Analysis"
    )

    fig = area_chart(
        area_data(
            filtered_df
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# =====================================================
# 7 INSIGHTS
# =====================================================
with tab7:

    st.header(
        "Policy Insights"
    )

    insights = generate_insights(
        filtered_df
    )

    for item in insights:
        st.success(
            item
        )

    pdf = create_pdf(
        insights
    )

    st.download_button(
        "Download PDF Report",
        pdf,
        "report.pdf",
    )