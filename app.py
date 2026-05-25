import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re

st.title("📊 My Journey Dashboard (Colab Preview)")

# --- Upload CSV ---
uploaded = st.file_uploader("Upload your dataset (CSV)", type="csv")
if uploaded:
    df = pd.read_csv(uploaded)

    # --- Clean salary ---
    def clean_salary(val):
        if pd.isna(val): return None
        val = str(val)
        if "–" in val or "-" in val:
            parts = re.split("–|-", val)
            nums = [int(re.sub(r"[^\d]", "", p)) for p in parts if re.sub(r"[^\d]", "", p)]
            return sum(nums)/len(nums) if nums else None
        val = re.sub(r"[^\d]", "", val)
        return float(val) if val else None

    df["SalaryClean"] = df["Annual Avg Salary (MMK)"].apply(clean_salary)

    # --- Success Index ---
    df["Acceptances"] = df["Journey Type"].eq("Employment").astype(int)
    df["Rejections"] = df["Journey Type"].eq("Employment").astype(int)*10
    df["Success Index"] = (df["Acceptances"]/(df["Rejections"]+1)
                           + df["SalaryClean"].fillna(0)/1e6
                           + df["Duration (Months)"].fillna(0)/12)

    # --- Sidebar Filters ---
    st.sidebar.header("Filters")
    journey_filter = st.sidebar.multiselect("Select Journey Type", df["Journey Type"].unique(), df["Journey Type"].unique())
    org_filter = st.sidebar.multiselect("Select Organization/Event", df["Organization/Event"].unique(), df["Organization/Event"].unique())
    year_min, year_max = int(df["Year"].min()), int(df["Year"].max())
    year_range = st.sidebar.slider("Select Year Range", year_min, year_max, (year_min, year_max))

    # --- Apply Filters ---
    df_filtered = df[df["Journey Type"].isin(journey_filter) & df["Organization/Event"].isin(org_filter)]
    df_filtered = df_filtered[(df_filtered["Year"] >= year_range[0]) & (df_filtered["Year"] <= year_range[1])]

    # --- Salary Growth ---
    st.subheader("1. Salary Growth Over Time")
    fig1 = px.line(df_filtered[df_filtered["Journey Type"]=="Employment"], x="Year", y="SalaryClean",
                   color="Organization/Event", markers=True)
    st.plotly_chart(fig1)

    # --- Volunteer vs Employment ---
    st.subheader("2. Volunteer vs Employment Comparison")
    vol = df_filtered[df_filtered["Journey Type"]=="Volunteer"].groupby("Year")["Duration (Months)"].sum().reset_index()
    emp = df_filtered[df_filtered["Journey Type"]=="Employment"].groupby("Year")["SalaryClean"].mean().reset_index()
    fig2 = go.Figure([
        go.Bar(x=vol["Year"], y=vol["Duration (Months)"], name="Volunteer Months", marker_color="green"),
        go.Bar(x=emp["Year"], y=emp["SalaryClean"], name="Employment Salary", marker_color="blue")
    ])
    fig2.update_layout(barmode="group")
    st.plotly_chart(fig2)

    # --- Timeline of Roles ---
    st.subheader("3. Timeline of Roles")
    fig3 = px.timeline(df_filtered, x_start="Start Date", x_end="End Date", y="Role", color="Journey Type")
    fig3.update_yaxes(autorange="reversed")
    st.plotly_chart(fig3)

    # --- Volunteer Role Distribution ---
    st.subheader("4. Volunteer Role Distribution")
    fig4 = px.pie(df_filtered[df_filtered["Journey Type"]=="Volunteer"], names="Role")
    st.plotly_chart(fig4)

    # --- Success Index ---
    st.subheader("5. Success Index")
    fig5 = px.bar(df_filtered, x="Year", y="Success Index", color="Journey Type", text_auto=True)
    st.plotly_chart(fig5)

    # --- Rejections vs Acceptances ---
    st.subheader("6. Rejections vs Acceptances")
    rej = pd.DataFrame({"Outcome":["Rejections","Acceptances"],"Count":[10,1]})
    st.plotly_chart(px.pie(rej, names="Outcome", values="Count"))
    st.plotly_chart(px.bar(rej, x="Outcome", y="Count", color="Outcome"))

    # --- Download filtered dataset ---
    st.subheader("📥 Download Filtered Data")
    csv = df_filtered.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "filtered_data.csv", "text/csv")
