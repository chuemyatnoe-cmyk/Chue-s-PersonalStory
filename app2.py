import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="Personal Story Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data

def load_data():
    df = pd.read_csv(
        "Chue Myat Noe_Personal Story Dataset.csv",
        encoding="latin1"
    )

    # Clean salary column
    df["Salary (MMK)"] = pd.to_numeric(df["Salary (MMK)"], errors="coerce").fillna(0)

    # Clean year
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

    return df


df = load_data()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.title("🎛️ Dashboard Filters")

journey_filter = st.sidebar.multiselect(
    "Select Journey Type",
    options=df["Journey Type"].unique(),
    default=df["Journey Type"].unique()
)

selected_years = st.sidebar.slider(
    "Select Year Range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (
        int(df["Year"].min()),
        int(df["Year"].max())
    )
)

filtered_df = df[
    (df["Journey Type"].isin(journey_filter)) &
    (df["Year"] >= selected_years[0]) &
    (df["Year"] <= selected_years[1])
]

# -----------------------------
# TITLE
# -----------------------------
st.title("📖 My Volunteering & Salary Growth Journey")

st.markdown(
    """
This dashboard tells the story of my personal growth through volunteering,
leadership experiences, and career development over time.

The dashboard explores:
- My volunteering journey
- Salary growth over time
- Leadership and organizational involvement
- Key insights from my personal experiences
- Ethical responsibilities in storytelling through data
"""
)

# -----------------------------
# METRICS
# -----------------------------
st.subheader("📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Experiences",
        len(filtered_df)
    )

with col2:
    st.metric(
        "Volunteer Roles",
        len(filtered_df[filtered_df["Journey Type"] == "Volunteer"])
    )

with col3:
    st.metric(
        "Highest Salary (MMK)",
        f"{int(filtered_df['Salary (MMK)'].max()):,}"
    )

with col4:
    st.metric(
        "Organizations Involved",
        filtered_df["Organization/Event"].nunique()
    )

# -----------------------------
# VISUALIZATION 1
# SALARY GROWTH OVER TIME
# -----------------------------
st.subheader("📈 Salary Growth Over Time")

salary_by_year = filtered_df.groupby("Year")["Salary (MMK)"].mean().reset_index()

fig_salary = px.line(
    salary_by_year,
    x="Year",
    y="Salary (MMK)",
    markers=True,
    title="Average Salary Growth by Year"
)

fig_salary.update_layout(
    xaxis_title="Year",
    yaxis_title="Salary (MMK)"
)

st.plotly_chart(fig_salary, use_container_width=True)

st.markdown(
    "**Insight:** The chart shows how salary opportunities increased over time alongside skill development and leadership experiences."
)

# -----------------------------
# VISUALIZATION 2
# JOURNEY TYPE DISTRIBUTION
# -----------------------------
st.subheader("📊 Journey Type Distribution")

journey_counts = filtered_df["Journey Type"].value_counts().reset_index()
journey_counts.columns = ["Journey Type", "Count"]

fig_pie = px.pie(
    journey_counts,
    names="Journey Type",
    values="Count",
    title="Distribution of Experiences"
)

st.plotly_chart(fig_pie, use_container_width=True)

st.markdown(
    "**Insight:** Volunteering experiences played a major role in shaping leadership, communication, and organizational skills."
)

# -----------------------------
# VISUALIZATION 3
# ORGANIZATION INVOLVEMENT
# -----------------------------
st.subheader("🏢 Organizations & Events Participation")

org_counts = filtered_df["Organization/Event"].value_counts().reset_index()
org_counts.columns = ["Organization/Event", "Count"]

fig_org = px.bar(
    org_counts,
    x="Organization/Event",
    y="Count",
    title="Participation Across Organizations",
)

fig_org.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig_org, use_container_width=True)

st.markdown(
    "**Insight:** Participation across different organizations helped build adaptability and networking skills."
)

# -----------------------------
# VISUALIZATION 4
# VOLUNTEERING TIMELINE
# -----------------------------
st.subheader("🕒 Volunteering Timeline")

fig_timeline = px.scatter(
    filtered_df,
    x="Year",
    y="Role",
    color="Journey Type",
    hover_data=["Organization/Event"],
    title="Timeline of Roles and Experiences",
    size_max=12
)

st.plotly_chart(fig_timeline, use_container_width=True)

st.markdown(
    "**Insight:** Leadership roles became more complex over time, reflecting personal and professional growth."
)

# -----------------------------
# KEY INSIGHTS SECTION
# -----------------------------
st.header("🔍 Key Insights")

st.markdown(
    """
### Major Findings

1. Volunteering experiences created opportunities for leadership development.
2. Increased responsibilities were connected with salary growth over time.
3. Participation in multiple organizations improved communication and teamwork skills.
4. Long-term involvement in community and youth activities contributed to personal confidence and career readiness.
"""
)

# -----------------------------
# DECISION-MAKING SECTION
# -----------------------------
st.header("🎯 Decision-Making Section")

st.markdown(
    """
### What Should I Do Differently in the Future?

Based on the data, I should:

- Continue joining leadership and volunteering opportunities because they contributed to both skill development and career growth.
- Focus more on long-term projects that create stronger professional experience.
- Improve balance between volunteer work and career advancement.
- Build specialized technical skills alongside leadership experience.

### Responsible Interpretation

The data suggests a relationship between volunteering, leadership, and salary growth.
However, the dashboard does not prove direct causation because many external factors can also influence career opportunities.
"""
)

# -----------------------------
# ETHICS SECTION
# -----------------------------
st.header("⚖️ Ethics & Responsibility")

# Privacy
st.subheader("🔒 Privacy Statement")

st.markdown(
    """
- Personal and third-party information has been anonymized.
- No sensitive personal data is included.
- Organization names are used only for educational storytelling purposes.
- Salary data is simplified and does not represent exact financial records.
"""
)

# Bias
st.subheader("⚠️ Bias & Limitation Disclosure")

st.markdown(
    """
### Limitations

- The dataset is small and based on personal experiences.
- Some information depends on memory and subjective interpretation.
- Salary and impact measurements may not fully represent real-world complexity.
- Volunteering impact cannot be measured only through numbers.
"""
)

# Visualization justification
st.subheader("📊 Visualization Justification")

st.markdown(
    """
### Why These Charts Were Chosen

- **Line Chart:** Shows salary growth trends clearly over time.
- **Pie Chart:** Helps compare the proportion of different experiences.
- **Bar Chart:** Makes organization participation easier to compare.
- **Timeline Scatter Plot:** Visualizes progression and development across years.

### Risk of Misinterpretation

- Visual trends may appear stronger than the actual dataset supports.
- Correlation between volunteering and salary growth should not be interpreted as direct causation.
"""
)

# Responsible decision
st.subheader("🎯 Responsible Decision")

st.markdown(
    """
The dashboard supports reflective decision-making rather than prediction.
Future decisions should consider additional factors such as economic conditions,
mental health, academic workload, and access to opportunities.
"""
)

# -----------------------------
# RAW DATA
# -----------------------------
st.header("📂 Dataset Preview")

st.dataframe(filtered_df)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Created using Streamlit for a personal storytelling and ethical data visualization project.")
