
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ------------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------------

st.set_page_config(
    page_title="Customer Lifetime Value & Churn Intelligence",
    page_icon="📊",
    layout="wide"
)

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("customer_intelligence_final.csv")


df = load_data()


# ------------------------------------------------------------
# TITLE
# ------------------------------------------------------------

st.title("📊 Customer Lifetime Value & Churn Intelligence System")

st.caption(
    "AI-powered churn prediction, customer lifetime value, "
    "retention targeting and campaign ROI optimization."
)


# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------

st.sidebar.header("Dashboard Filters")

risk_threshold = st.sidebar.slider(
    "High-Risk Churn Threshold",
    min_value=0.10,
    max_value=0.90,
    value=0.50,
    step=0.05
)

high_risk_df = df[
    df["ChurnProbability"] >= risk_threshold
].copy()


# ------------------------------------------------------------
# TABS
# ------------------------------------------------------------

tabs = st.tabs([
    "🏠 Executive Dashboard",
    "👤 Customer Explorer",
    "⚠️ Churn Intelligence",
    "💰 Survival & CLV",
    "🎯 Retention Targeting",
    "📈 ROI Simulator"
])


# ============================================================
# TAB 1: EXECUTIVE DASHBOARD
# ============================================================

with tabs[0]:

    st.header("Executive Customer Intelligence")

    total_customers = len(df)

    avg_churn_risk = df[
        "ChurnProbability"
    ].mean()

    high_risk_count = len(
        high_risk_df
    )

    total_clv = df[
        "DiscountedCLV"
    ].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Customers",
        f"{total_customers:,}"
    )

    col2.metric(
        "Average Churn Risk",
        f"{avg_churn_risk:.1%}"
    )

    col3.metric(
        "High-Risk Customers",
        f"{high_risk_count:,}"
    )

    col4.metric(
        "Portfolio CLV",
        f"${total_clv:,.0f}"
    )


    st.subheader("Customer Risk Distribution")

    fig = px.histogram(
        df,
        x="ChurnProbability",
        nbins=30,
        title="Predicted Churn Probability Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    if "BusinessSegment" in df.columns:

        st.subheader(
            "Customer Business Segments"
        )

        segment_counts = (
            df["BusinessSegment"]
            .value_counts()
            .reset_index()
        )

        segment_counts.columns = [
            "Segment",
            "Customers"
        ]

        fig = px.bar(
            segment_counts,
            x="Segment",
            y="Customers",
            title="Customer Segmentation"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# TAB 2: CUSTOMER EXPLORER
# ============================================================

with tabs[1]:

    st.header("Customer Explorer")

    customer_id = st.selectbox(
        "Select Customer",
        df["customerID"].astype(str).tolist()
    )

    customer = df[
        df["customerID"].astype(str)
        == str(customer_id)
    ].iloc[0]


    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Churn Probability",
        f"{customer['ChurnProbability']:.1%}"
    )

    col2.metric(
        "Discounted CLV",
        f"${customer['DiscountedCLV']:,.2f}"
    )

    if "ExpectedLifetimeMonths" in df.columns:

        col3.metric(
            "Expected Lifetime",
            f"{customer['ExpectedLifetimeMonths']:.1f} months"
        )

    else:

        col3.metric(
            "Monthly Charges",
            f"${customer['MonthlyCharges']:,.2f}"
        )


    if "CLVSegment" in df.columns:

        col4.metric(
            "CLV Segment",
            str(customer["CLVSegment"])
        )


    st.subheader("Customer Profile")

    profile_fields = [
        "gender",
        "SeniorCitizen",
        "tenure",
        "Contract",
        "InternetService",
        "TechSupport",
        "PaymentMethod",
        "MonthlyCharges",
        "TotalCharges"
    ]

    available_fields = [
        x for x in profile_fields
        if x in df.columns
    ]

    profile_df = pd.DataFrame({
        "Attribute": available_fields,
        "Value": [
            customer[x]
            for x in available_fields
        ]
    })

    st.dataframe(
        profile_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TAB 3: CHURN INTELLIGENCE
# ============================================================

with tabs[2]:

    st.header("Churn Intelligence")

    col1, col2 = st.columns(2)

    with col1:

        fig = px.histogram(
            df,
            x="ChurnProbability",
            color="ChurnFlag",
            nbins=30,
            title="Predicted Risk vs Actual Churn"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        if "Contract" in df.columns:

            contract_risk = (
                df.groupby("Contract")[
                    "ChurnProbability"
                ]
                .mean()
                .reset_index()
            )

            fig = px.bar(
                contract_risk,
                x="Contract",
                y="ChurnProbability",
                title="Average Churn Risk by Contract"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    st.subheader(
        f"Customers Above {risk_threshold:.0%} Risk"
    )

    risk_columns = [
        "customerID",
        "ChurnProbability",
        "MonthlyCharges",
        "DiscountedCLV",
        "Contract",
        "InternetService"
    ]

    risk_columns = [
        c for c in risk_columns
        if c in df.columns
    ]

    st.dataframe(
        high_risk_df[
            risk_columns
        ].sort_values(
            "ChurnProbability",
            ascending=False
        ),
        use_container_width=True
    )


# ============================================================
# TAB 4: SURVIVAL & CLV
# ============================================================

with tabs[3]:

    st.header(
        "Customer Lifetime Value Intelligence"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average CLV",
        f"${df['DiscountedCLV'].mean():,.2f}"
    )

    col2.metric(
        "Median CLV",
        f"${df['DiscountedCLV'].median():,.2f}"
    )

    col3.metric(
        "Maximum CLV",
        f"${df['DiscountedCLV'].max():,.2f}"
    )


    fig = px.scatter(
        df,
        x="ChurnProbability",
        y="DiscountedCLV",
        hover_name="customerID",
        title="Customer Value vs Churn Risk"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    if "CLVSegment" in df.columns:

        clv_summary = (
            df.groupby(
                "CLVSegment",
                observed=True
            )
            .agg(
                Customers=("customerID", "count"),
                Average_CLV=("DiscountedCLV", "mean"),
                Average_Churn_Risk=("ChurnProbability", "mean")
            )
            .reset_index()
        )

        st.dataframe(
            clv_summary,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# TAB 5: RETENTION TARGETING
# ============================================================

with tabs[4]:

    st.header(
        "Retention Targeting"
    )

    target_percent = st.slider(
        "Target highest-risk customers",
        min_value=5,
        max_value=50,
        value=10,
        step=5
    )


    cutoff = df[
        "ChurnProbability"
    ].quantile(
        1 - target_percent / 100
    )


    target_df = df[
        df["ChurnProbability"] >= cutoff
    ].copy()


    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Customers Targeted",
        f"{len(target_df):,}"
    )

    col2.metric(
        "Risk Cutoff",
        f"{cutoff:.1%}"
    )

    col3.metric(
        "Target Portfolio CLV",
        f"${target_df['DiscountedCLV'].sum():,.0f}"
    )


    target_columns = [
        "customerID",
        "ChurnProbability",
        "DiscountedCLV",
        "CLVSegment",
        "BusinessSegment",
        "RetentionStrategy"
    ]

    target_columns = [
        c for c in target_columns
        if c in target_df.columns
    ]


    st.dataframe(
        target_df[
            target_columns
        ].sort_values(
            [
                "ChurnProbability",
                "DiscountedCLV"
            ],
            ascending=False
        ),
        use_container_width=True
    )


# ============================================================
# TAB 6: ROI SIMULATOR
# ============================================================

with tabs[5]:

    st.header(
        "Retention Campaign ROI Simulator"
    )

    st.info(
        "Retention uplift is a scenario assumption. "
        "The separate Criteo uplift experiment validates "
        "the causal targeting methodology."
    )


    col1, col2 = st.columns(2)


    with col1:

        discount_rate = st.slider(
            "Discount Offered",
            min_value=1,
            max_value=30,
            value=5,
            step=1
        ) / 100


        offer_months = st.slider(
            "Offer Duration (Months)",
            min_value=1,
            max_value=12,
            value=3,
            step=1
        )


    with col2:

        retention_uplift = st.slider(
            "Expected Incremental Retention Uplift",
            min_value=1,
            max_value=30,
            value=10,
            step=1
        ) / 100


        campaign_target = st.slider(
            "Target Population",
            min_value=5,
            max_value=50,
            value=10,
            step=5
        ) / 100


    churn_cutoff = df[
        "ChurnProbability"
    ].quantile(
        1 - campaign_target
    )


    campaign_df = df[
        df["ChurnProbability"] >= churn_cutoff
    ].copy()


    campaign_df["OfferCost"] = (
        campaign_df["MonthlyCharges"]
        * discount_rate
        * offer_months
    )


    campaign_df["IncrementalValue"] = (
        retention_uplift
        * campaign_df["DiscountedCLV"]
    )


    total_cost = campaign_df[
        "OfferCost"
    ].sum()


    expected_value = campaign_df[
        "IncrementalValue"
    ].sum()


    net_benefit = (
        expected_value
        -
        total_cost
    )


    roi = (
        net_benefit / total_cost
        if total_cost > 0
        else 0
    )


    total_target_clv = campaign_df[
        "DiscountedCLV"
    ].sum()


    break_even_uplift = (
        total_cost / total_target_clv
        if total_target_clv > 0
        else 0
    )


    st.divider()

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Customers",
        f"{len(campaign_df):,}"
    )

    c2.metric(
        "Campaign Cost",
        f"${total_cost:,.0f}"
    )

    c3.metric(
        "Expected Value",
        f"${expected_value:,.0f}"
    )

    c4.metric(
        "Net Benefit",
        f"${net_benefit:,.0f}"
    )

    c5.metric(
        "ROI",
        f"{roi:.1%}"
    )


    st.metric(
        "Break-Even Retention Uplift",
        f"{break_even_uplift:.2%}"
    )


    if retention_uplift > break_even_uplift:

        st.success(
            "✅ Campaign is expected to generate positive ROI."
        )

    else:

        st.warning(
            "⚠️ Expected uplift is below the break-even threshold."
        )


    # --------------------------------------------------------
    # ROI SENSITIVITY
    # --------------------------------------------------------

    uplift_range = np.arange(
        0.01,
        0.31,
        0.01
    )

    sensitivity = pd.DataFrame({
        "Retention Uplift": uplift_range
    })


    sensitivity[
        "Expected Value"
    ] = (
        uplift_range
        * total_target_clv
    )


    sensitivity[
        "Net Benefit"
    ] = (
        sensitivity["Expected Value"]
        -
        total_cost
    )


    fig = px.line(
        sensitivity,
        x="Retention Uplift",
        y="Net Benefit",
        title="Campaign Profitability Sensitivity"
    )

    fig.add_hline(
        y=0,
        line_dash="dash"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------

st.divider()

st.caption(
    "Customer Lifetime Value & Churn Intelligence System | "
    "LightGBM • SHAP • Survival Analysis • Uplift Modeling • CLV"
)
