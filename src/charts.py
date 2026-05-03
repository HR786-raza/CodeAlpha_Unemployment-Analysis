import plotly.express as px
from src.analysis import RATE

def overall_trend(df):
    return px.line(
        df,
        x="Date",
        y=RATE,
        title="Overall Unemployment Trend",
    )

def yearly_chart(df):
    return px.bar(
        df,
        x="Year",
        y=RATE,
        title="Yearly Analysis",
    )

def monthly_chart(df):
    return px.line(
        df,
        x="Month",
        y=RATE,
        markers=True,
        title="Seasonal Trend",
    )

def regional_chart(df):
    return px.bar(
        df,
        x="Region",
        y=RATE,
        title="State-wise Analysis",
    )

def area_chart(df):
    return px.pie(
        df,
        names="Area",
        values=RATE,
        title="Urban vs Rural",
    )