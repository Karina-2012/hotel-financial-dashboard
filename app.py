import os
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE SETUP ----------------
st.set_page_config(
    page_title="Hotel Financial & Stock Performance",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
file_path = os.path.join(os.path.dirname(__file__), "top4_hotels_annual_2018_2025.csv")
df = pd.read_csv(file_path)

df["year_comp"] = df["year_comp"].astype(int)

metric_options = {
    "ROA – Return on Assets": "ROA",
    "ROE – Return on Equity": "ROE",
    "Profit Margin": "profit_margin",
    "Asset Turnover": "asset_turnover",
    "EPS – Earnings per Share": "EPS",
    "P/E Ratio": "PE_ratio",
    "P/B Ratio": "PB_ratio",
    "FCF – Free Cash Flow": "FCF"
}

metric_labels = {
    "ROA": "ROA",
    "ROE": "ROE",
    "profit_margin": "Profit Margin",
    "asset_turnover": "Asset Turnover",
    "EPS": "EPS",
    "PE_ratio": "P/E Ratio",
    "PB_ratio": "P/B Ratio",
    "FCF": "FCF"
}


percent_metrics = ["ROA", "ROE", "profit_margin"]

def metric_axis_title(metric):
    if metric in percent_metrics:
        return f"{metric_labels[metric]} (%)"
    elif metric == "EPS":
        return "EPS ($ per share)"
    elif metric == "FCF":
        return "Free Cash Flow ($ in millions)"
    else:
        return metric_labels[metric]

def metric_hover_format(metric):
    if metric in percent_metrics:
        return "%{y:.2%}"
    elif metric == "EPS":
        return "$%{y:.2f}"
    elif metric == "FCF":
        return "$%{y:,.0f}M"
    else:
        return "%{y:.2f}"
    
percent_metrics = ["ROA", "ROE", "profit_margin"]

def format_metric_value(value, metric):
    if pd.isna(value):
        return "N/A"
    elif metric in percent_metrics:
        return f"{value:.2%}"
    elif metric == "EPS":
        return f"${value:.2f}"
    elif metric == "FCF":
        if abs(value) >= 1000:
            return f"${value/1000:.2f}B"
        else:
            return f"${value:.0f}M"
    else:
        return f"{value:.2f}"
    
company_labels = {
    "HILTON WORLDWIDE HOLDINGS": "Hilton",
    "HYATT HOTELS CORP": "Hyatt",
    "MARRIOTT INTL INC": "Marriott",
    "INTERCONTINENTAL HOTELS GRP": "IHG"
}

df["company_short"] = df["company_name"].map(company_labels)

colors = {
    "Hilton": "#1f77b4",      # strong blue
    "Hyatt": "#6baed6",       # light blue
    "IHG": "#d62728",         # red (for contrast)
    "Marriott": "#ff9896"     # soft red
}
def style_chart(fig):
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=14),
        margin=dict(l=40, r=40, t=70, b=60)
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False
    )

    fig.update_yaxes(
        gridcolor="#e5e7eb",
        zeroline=False
    )

    return fig
# ---------------- TITLE ----------------
st.markdown(
    '<h1 style="text-align: center;">Hotel Companies Financial & Stock Performance Dashboard</h1>',
    unsafe_allow_html=True
)

st.markdown("""
This dashboard analyzes the financial and stock performance of four major global hotel companies.

**Companies included:**
""")

st.markdown("""
<div style="margin-top: 15px; margin-bottom: 25px; text-align:center;">

<div style="display:inline-block; width:60%; padding:14px; border-radius:10px; background-color:#fef3c7; border:1px solid #fcd34d; margin-bottom:12px; font-size:17px;">
<b>Hilton Worldwide Holdings</b> (Hilton)
</div><br>

<div style="display:inline-block; width:60%; padding:14px; border-radius:10px; background-color:#fef3c7; border:1px solid #fcd34d; margin-bottom:12px; font-size:17px;">
<b>Hyatt Hotels Corporation</b> (Hyatt)
</div><br>

<div style="display:inline-block; width:60%; padding:14px; border-radius:10px; background-color:#fef3c7; border:1px solid #fcd34d; margin-bottom:12px; font-size:17px;">
<b>Marriott International</b> (Marriott)
</div><br>

<div style="display:inline-block; width:60%; padding:14px; border-radius:10px; background-color:#fef3c7; border:1px solid #fcd34d; font-size:17px;">
<b>InterContinental Hotels Group</b> (IHG)
</div>

</div>
""", unsafe_allow_html=True)

st.markdown("""
**Objective:**  
To evaluate whether financial performance aligns with stock market performance over time.
""")

st.info(
    "Context note: The hotel industry was significantly affected during the COVID-19 pandemic (2020–2021), which led to sharp declines in both financial performance and stock returns."
)
# ---------------- SIDEBAR ----------------
st.sidebar.header("Filters")

selected_companies_short = st.sidebar.multiselect(
    "**Select companies**",
    options=sorted(df["company_short"].dropna().unique()),
    default=sorted(df["company_short"].dropna().unique())
)

year_range = st.sidebar.slider(
    "**Select year range**",
    int(df["year_comp"].min()),
    int(df["year_comp"].max()),
    (int(df["year_comp"].min()), int(df["year_comp"].max()))
)

selected_metric_name = st.sidebar.selectbox(
    "**Select financial metric for analysis**",
    options=list(metric_options.keys())
)

metric = metric_options[selected_metric_name]

filtered = df[
    (df["company_short"].isin(selected_companies_short)) &
    (df["year_comp"].between(year_range[0], year_range[1]))
]

# ---------------- SAFETY CHECK ----------------
if filtered.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# ---------------- SUMMARY INSIGHTS ----------------
st.markdown(
    "<hr style='border: 1.5px solid #d0d7de; margin-top: 40px; margin-bottom: 40px;'>",
    unsafe_allow_html=True
)
st.markdown(
    "<h2 style='text-align: center; margin-bottom: 10px;'>Summary Insights</h2>",
    unsafe_allow_html=True
)

summary_data = filtered.dropna(subset=["annual_return"]).copy()

if summary_data.empty:
    st.warning("No stock return data available for the selected filters.")
else:
    best_return_row = summary_data.loc[summary_data["annual_return"].idxmax()]
    best_roa_row = summary_data.loc[summary_data["ROA"].idxmax()]
    best_roe_row = summary_data.loc[summary_data["ROE"].idxmax()]
    avg_return = summary_data["annual_return"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Best Stock Return",
        f"{best_return_row['annual_return']:.2f}%",
        f"{best_return_row['company_name']} ({int(best_return_row['year_comp'])})"
    )

    col2.metric(
        "Highest ROA",
        f"{best_roa_row['ROA']:.2%}",
        f"{best_roa_row['company_name']} ({int(best_roa_row['year_comp'])})"
    )

    col3.metric(
        "Highest ROE",
        f"{best_roe_row['ROE']:.2%}",
        f"{best_roe_row['company_name']} ({int(best_roe_row['year_comp'])})"
    )

    col4.metric(
        "Average Stock Return",
        f"{avg_return:.2f}%",
        "Across selected companies/years"
    )

    st.caption(
        "These indicators update based on the selected companies and year range. "
        "They highlight the strongest financial and stock market observations in the filtered dataset."
    )

# ---------------- FINANCIAL PERFORMANCE ----------------
st.markdown(
    "<div style='margin-top: 50px;'></div>",
    unsafe_allow_html=True
)
st.markdown(
    "<hr style='border: 1.5px solid #d0d7de; margin-top: 40px; margin-bottom: 40px;'>",
    unsafe_allow_html=True
)
st.markdown(
    "<h2 style='text-align: center; margin-bottom: 10px;'>Financial Performance Over Time</h2>",
    unsafe_allow_html=True
)

fig1 = px.line(
    filtered,
    x="year_comp",
    y=metric,
    color="company_short",
    color_discrete_map=colors,
    markers=True,
    title=None,
    labels={
        "year_comp": "Year",
        metric: metric_labels[metric],
        "company_short": "Company"
    }
)

fig1.update_layout(
    xaxis_title="<b>Year</b>",
    yaxis_title=f"<b>{metric_axis_title(metric)}</b>",
    legend_title_text="<b>Company</b>",
    hovermode="closest",
    hoverdistance=5,
    spikedistance=-1,
    dragmode=False
)

fig1.update_traces(
    hovertemplate="<b>%{fullData.name}</b><br>"
                  "Year: %{x}<br>"
                  f"{metric_labels[metric]}: " + metric_hover_format(metric) + "<extra></extra>"
)
st.markdown(
    f"<p style='font-weight: 600; margin-top: 25px; margin-bottom: 0px;'>"
    f"{metric_labels[metric]} - Company Comparison"
    f"</p>",
    unsafe_allow_html=True
)
fig1 = style_chart(fig1)
st.plotly_chart(fig1, width="stretch", config={"displayModeBar": False})

best_metric_row = filtered.dropna(subset=[metric]).loc[
    filtered.dropna(subset=[metric])[metric].idxmax()
]
st.markdown(f"""
This chart compares **{metric_labels[metric]}** across the selected companies and years.  
The highest selected value is **{format_metric_value(best_metric_row[metric], metric)}**, recorded by **{best_metric_row["company_short"]}** in **{int(best_metric_row["year_comp"])}**.
""")
# ---------------- STOCK PERFORMANCE ----------------
st.markdown(
    "<div style='margin-top: 50px;'></div>",
    unsafe_allow_html=True
)
st.markdown(
    "<hr style='border: 1.5px solid #d0d7de; margin-top: 40px; margin-bottom: 40px;'>",
    unsafe_allow_html=True
)
st.markdown(
    "<h2 style='text-align: center; margin-bottom: 10px;'>Annual Stock Return Over Time</h2>",
    unsafe_allow_html=True
)
st.warning("Annual stock return data are not available for 2025, as full-year market data are not yet complete.")

fig2 = px.line(
    filtered,
    x="year_comp",
    y="annual_return",
    color="company_short",
    color_discrete_map=colors,
    markers=True,
    title=None,
    labels={
        "year_comp": "Year",
        "annual_return": "Annual Stock Return",
        "company_short": "Company"
    }
)

fig2.update_layout(
    xaxis_title="<b>Year</b>",
    yaxis_title="<b>Annual Stock Return</b>",
    legend_title_text="<b>Company</b>",
    hovermode="closest",
    hoverdistance=5,
    spikedistance=-1,
    dragmode=False
)

fig2.update_traces(
    hovertemplate="<b>%{fullData.name}</b><br>"
                  "Year: %{x}<br>"
                  "Annual Stock Return: %{y:.2f}%<extra></extra>"
)

st.markdown(
    "<p style='font-weight: 600; margin-top: 25px; margin-bottom: 0px;'>"
    "Annual Stock Return - Company Comparison"
    "</p>",
    unsafe_allow_html=True
)

fig2 = style_chart(fig2)

st.plotly_chart(fig2, width="stretch", config={"displayModeBar": False})

return_data = filtered.dropna(subset=["annual_return"])

if not return_data.empty:
    best_return_row = return_data.loc[return_data["annual_return"].idxmax()]
    worst_return_row = return_data.loc[return_data["annual_return"].idxmin()]

    st.markdown(f"""
    This chart compares compounded annual stock returns across the selected companies and years.  
    The strongest selected stock return is **{best_return_row["annual_return"]:.2f}%** for **{best_return_row["company_short"]}** in **{int(best_return_row["year_comp"])}**, while the weakest is **{worst_return_row["annual_return"]:.2f}%** for **{worst_return_row["company_short"]}** in **{int(worst_return_row["year_comp"])}**.
    """)
else:
    st.markdown("Stock return data are not available for the selected filters.")

# ---------------- FINANCIAL–MARKET PERFORMANCE ALIGNMENT ----------------
st.markdown(
    "<div style='margin-top: 50px;'></div>",
    unsafe_allow_html=True
)
st.markdown(
    "<hr style='border: 1.5px solid #d0d7de; margin-top: 40px; margin-bottom: 40px;'>",
    unsafe_allow_html=True
)
st.markdown(
    "<h2 style='text-align: center; margin-bottom: 10px;'>Financial–Market Performance Alignment</h2>",
    unsafe_allow_html=True
)

st.markdown("""
This section focuses on percentage-based financial metrics (such as ROA, ROE, and profit margin) to enable direct comparison with annual stock returns.

It helps assess whether improvements in financial performance are reflected in market performance over time.
""")

# ---- Only percentage-based metrics for alignment ----
alignment_metric_options = {
    "Return on Assets": "ROA",
    "Return on Equity": "ROE",
    "Profit Margin": "profit_margin"
}

# ---- Local controls (NOT sidebar) ----
col1, col2, col3 = st.columns(3)

with col1:
    alignment_company = st.selectbox(
        "Select company",
        options=sorted(df["company_short"].unique())
    )

with col2:
    alignment_metric_names = st.multiselect(
        "Select financial metrics",
        options=list(alignment_metric_options.keys()),
        default=["Return on Assets", "Return on Equity"]
    )

with col3:
    alignment_year_range = st.slider(
        "Select year range",
        int(df["year_comp"].min()),
        int(df["year_comp"].max()),
        (int(df["year_comp"].min()), int(df["year_comp"].max()))
    )

# ---- Warning if too many metrics ----
if len(alignment_metric_names) > 3:
    st.warning("For readability, selecting 1–3 financial metrics is recommended.")

# ---- Convert to column names ----
alignment_metric_cols = [alignment_metric_options[m] for m in alignment_metric_names]

# ---- Filter data ----
alignment_data = df[
    (df["company_short"] == alignment_company) &
    (df["year_comp"].between(alignment_year_range[0], alignment_year_range[1]))
].sort_values("year_comp")

# ---- Create plot ----
y_values = alignment_metric_cols + ["annual_return"]

fig3 = px.line(
    alignment_data,
    x="year_comp",
    y=y_values,
    markers=True,
    title=None,
    labels={
        "year_comp": "Year",
        "value": "Value",
        "variable": "Indicator"
    }
)

# ---- Rename legend nicely ----
def rename_trace(trace):
    if trace.name in metric_labels:
        trace.name = metric_labels[trace.name]
    elif trace.name == "annual_return":
        trace.name = "Annual Stock Return"

fig3.for_each_trace(rename_trace)

# ---- Layout & hover fixes ----
fig3.update_layout(
    xaxis_title="<b>Year</b>",
    yaxis_title="<b>Value</b>",
    legend_title_text="<b>Indicator</b>",
    hovermode="closest",
    hoverdistance=5,
    spikedistance=-1,
    dragmode=False
)

fig3.update_traces(
    hovertemplate="<b>%{fullData.name}</b><br>"
                  "Year: %{x}<br>"
                  "Value: %{y:.2f}%<extra></extra>"
)

st.markdown(
    f"<p style='font-weight: 600; margin-top: 20px; margin-bottom: -5px;'>"
    f"{', '.join([metric_labels[alignment_metric_options[m]] for m in alignment_metric_names])} vs. Stock Return"
    "</p>",
    unsafe_allow_html=True
)

fig3 = style_chart(fig3)

st.plotly_chart(fig3, width="stretch", config={"displayModeBar": False})

st.markdown(f"""
This chart tracks how **{', '.join([metric_labels[alignment_metric_options[m]] for m in alignment_metric_names])}** 
and **Stock Return** evolved over time.
""")

# ---------------- INTERPRETATION SUMMARY ----------------
def explain_metric_value(value, metric):
    if pd.isna(value):
        return ""

    if metric == "ROA":
        if value < 0:
            return "This indicates the company generated a loss relative to its asset base."
        elif value < 0.05:
            return "This suggests relatively low efficiency in generating profit from assets."
        elif value < 0.10:
            return "This suggests moderate efficiency in using assets to generate profit."
        else:
            return "This suggests strong efficiency in generating profit from assets."

    elif metric == "ROE":
        if value < 0:
            return "This indicates negative returns for shareholders."
        elif value < 0.10:
            return "This suggests relatively low shareholder profitability."
        elif value < 0.20:
            return "This suggests solid returns generated for shareholders."
        else:
            return "This suggests strong shareholder profitability."

    elif metric == "profit_margin":
        if value < 0:
            return "This indicates the company operated at a loss."
        elif value < 0.10:
            return "This suggests relatively low profitability from revenue."
        elif value < 0.20:
            return "This suggests a reasonable level of profitability."
        else:
            return "This suggests strong profit generation from revenue."

    elif metric == "asset_turnover":
        return f"This means the company generated approximately {value:.2f} dollars of revenue for each dollar of assets."

    elif metric == "EPS":
        return "This shows the amount of earnings generated for each share."

    elif metric == "PE_ratio":
        return f"This suggests investors were willing to pay approximately {value:.2f} dollars for each dollar of earnings."

    elif metric == "PB_ratio":
        return f"This indicates the market valued the company at about {value:.2f} times its book value."

    elif metric == "FCF":
        return "This shows the cash generated after capital expenditures."

    return ""
st.markdown(
    "<div style='margin-top: 50px;'></div>",
    unsafe_allow_html=True
)
st.markdown(
    "<hr style='border: 1.5px solid #d0d7de; margin-top: 40px; margin-bottom: 40px;'>",
    unsafe_allow_html=True
)
st.markdown(
    "<h2 style='text-align: center; margin-bottom: 10px;'>Interpretation Summary</h2>",
    unsafe_allow_html=True
)

st.markdown("""
This section provides a focused explanation for one company, one year, and one financial metric.
It combines cross-company comparison with the company's own year-to-year change.
""")

col1, col2, col3 = st.columns(3)

with col1:
    interpretation_company = st.selectbox(
        "Select company",
        options=sorted(filtered["company_short"].unique()),
        key="interpretation_company"
    )

with col2:
    interpretation_metric_name = st.selectbox(
        "Select financial metric",
        options=list(metric_options.keys()),
        key="interpretation_metric"
    )
st.caption("Note: Annual stock return is automatically included for comparison.")
interpretation_metric = metric_options[interpretation_metric_name]

available_years = sorted(
    filtered[filtered["company_short"] == interpretation_company]["year_comp"].unique()
)

with col3:
    interpretation_year = st.selectbox(
        "Select year",
        options=available_years,
        index=len(available_years) - 1,
        key="interpretation_year"
    )

selected_row = filtered[
    (filtered["company_short"] == interpretation_company) &
    (filtered["year_comp"] == interpretation_year)
].iloc[0]

same_year_data = filtered[filtered["year_comp"] == interpretation_year].copy()

company_history = filtered[
    filtered["company_short"] == interpretation_company
].sort_values("year_comp")

previous_year_data = company_history[
    company_history["year_comp"] < interpretation_year
]

st.markdown(
    f"<h3 style='margin-bottom: 5px;'>{interpretation_company} in {int(interpretation_year)}</h3>",
    unsafe_allow_html=True
)
analysis_points = []

# 1. Current metric value
metric_explanation = explain_metric_value(
    selected_row[interpretation_metric],
    interpretation_metric
)

analysis_points.append(
    f"{interpretation_company}'s **{metric_labels[interpretation_metric]}** in {int(interpretation_year)} was "
    f"**{format_metric_value(selected_row[interpretation_metric], interpretation_metric)}**. "
    f"{metric_explanation}"
)
# 2. Peer comparison
peer_metric_data = same_year_data.dropna(subset=[interpretation_metric])

if len(peer_metric_data) > 1:
    peer_avg = peer_metric_data[interpretation_metric].mean()

    if selected_row[interpretation_metric] > peer_avg:
        analysis_points.append(
            f"This was **above the selected peer average** of **{format_metric_value(peer_avg, interpretation_metric)}** for the same year."
        )
    elif selected_row[interpretation_metric] < peer_avg:
        analysis_points.append(
            f"This was **below the selected peer average** of **{format_metric_value(peer_avg, interpretation_metric)}** for the same year."
        )
    else:
        analysis_points.append(
            f"This was close to the selected peer average of **{format_metric_value(peer_avg, interpretation_metric)}** for the same year."
        )
else:
    analysis_points.append(
        "Because only one company is selected, peer comparison is not available for this year."
    )

# 3. Year-to-year company trend
if not previous_year_data.empty:
    prev_row = previous_year_data.iloc[-1]
    prev_year = int(prev_row["year_comp"])
    change = selected_row[interpretation_metric] - prev_row[interpretation_metric]

    if pd.notna(change):
        if change > 0:
            analysis_points.append(
                f"Compared with {prev_year}, {metric_labels[interpretation_metric]} increased by **{format_metric_value(change, interpretation_metric)}**, "
                f"suggesting improvement in this selected financial measure."
            )
        elif change < 0:
            analysis_points.append(
                f"Compared with {prev_year}, {metric_labels[interpretation_metric]} decreased by **{format_metric_value(abs(change), interpretation_metric)}**, "
                f"suggesting weaker performance in this selected financial measure."
            )
        else:
            analysis_points.append(
                f"Compared with {prev_year}, {metric_labels[interpretation_metric]} remained broadly unchanged."
            )
else:
    analysis_points.append(
        "No earlier year is available in the selected range, so year-to-year comparison is not available."
    )

# 4. Stock return analysis
if pd.isna(selected_row["annual_return"]):
    analysis_points.append(
        "Annual stock return is not available for this company-year, so market performance cannot be assessed for this point."
    )
else:
    analysis_points.append(
        f"The annual stock return in {int(interpretation_year)} was **{selected_row['annual_return']:.2f}%**."
    )

    peer_return_data = same_year_data.dropna(subset=["annual_return"])

    if len(peer_return_data) > 1:
        peer_return_avg = peer_return_data["annual_return"].mean()

        if selected_row["annual_return"] > peer_return_avg:
            analysis_points.append(
                f"This stock return was **above the selected peer average** of **{peer_return_avg:.2f}%**."
            )
        elif selected_row["annual_return"] < peer_return_avg:
            analysis_points.append(
                f"This stock return was **below the selected peer average** of **{peer_return_avg:.2f}%**."
            )
        else:
            analysis_points.append(
                f"This stock return was close to the selected peer average of **{peer_return_avg:.2f}%**."
            )

# 5. Alignment comment
if not pd.isna(selected_row["annual_return"]) and len(peer_metric_data) > 1:
    peer_avg = peer_metric_data[interpretation_metric].mean()
    metric_above_peer = selected_row[interpretation_metric] >= peer_avg

    peer_return_data = same_year_data.dropna(subset=["annual_return"])

    if len(peer_return_data) > 1:
        peer_return_avg = peer_return_data["annual_return"].mean()
        return_above_peer = selected_row["annual_return"] >= peer_return_avg

        if metric_above_peer == return_above_peer:
            analysis_points.append(
                "Overall, the financial metric and stock return show a similar relative position against selected peers, "
                "which suggests some alignment between accounting performance and market response."
            )
        else:
            analysis_points.append(
                "Overall, the financial metric and stock return show different relative positions against selected peers. "
                "This suggests that stock performance may also reflect expectations, market sentiment, or other external factors."
            )
    else:
        analysis_points.append(
            "A peer-based alignment conclusion is limited because stock return data are not available for enough selected companies."
        )
else:
    analysis_points.append(
        "A stronger alignment conclusion requires both peer comparison and available stock return data."
    )

# Display in a clean professional box
st.markdown(
    "<div style='line-height: 1.7; font-size: 16px;'>",
    unsafe_allow_html=True
)

for point in analysis_points:
    st.markdown(f"- {point}")

st.markdown("</div>", unsafe_allow_html=True)


# ---------------- DATA TABLE ----------------
with st.expander("View filtered dataset"):
    st.dataframe(filtered, use_container_width=True)

# ---------------- PROJECT LOGIC ----------------
st.markdown(
    "<h2 style='text-align: center; margin-bottom: 10px;'>Project Methodology</h2>",
    unsafe_allow_html=True
)

with st.expander("View Methodology Details"):
    st.markdown("""
This analysis combines financial data (Compustat) and stock data (CRSP).

Financial metrics are calculated on an annual basis. Monthly stock returns are compounded into annual returns to ensure consistency in time horizons.

The objective is to assess whether changes in financial performance are reflected in stock market performance.
""")