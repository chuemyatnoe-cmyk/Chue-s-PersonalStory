import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re

# --- Load dataset ---
df = pd.read_csv("your_dataset.csv")

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

# --- Charts ---
fig1 = px.line(df[df["Journey Type"]=="Employment"], x="Year", y="SalaryClean",
               color="Organization/Event", markers=True, title="Salary Growth Over Time")

fig2 = go.Figure([
    go.Bar(x=df[df["Journey Type"]=="Volunteer"]["Year"],
           y=df[df["Journey Type"]=="Volunteer"]["Duration (Months)"],
           name="Volunteer Months", marker_color="green"),
    go.Bar(x=df[df["Journey Type"]=="Employment"]["Year"],
           y=df[df["Journey Type"]=="Employment"]["SalaryClean"],
           name="Employment Salary", marker_color="blue")
])
fig2.update_layout(title="Volunteer vs Employment Comparison", barmode="group")

fig3 = px.timeline(df, x_start="Start Date", x_end="End Date", y="Role", color="Journey Type")
fig3.update_yaxes(autorange="reversed")
fig3.update_layout(title="Timeline of Roles")

fig4 = px.pie(df[df["Journey Type"]=="Volunteer"], names="Role", title="Volunteer Role Distribution")

fig5 = px.bar(df, x="Year", y="Success Index", color="Journey Type", text_auto=True, title="Success Index")

rej = pd.DataFrame({"Outcome":["Rejections","Acceptances"],"Count":[10,1]})
fig6 = px.pie(rej, names="Outcome", values="Count", title="Rejections vs Acceptances")
fig7 = px.bar(rej, x="Outcome", y="Count", color="Outcome", title="Rejections vs Acceptances (Ratio)")

# --- Save all charts into one index.html ---
with open("index.html", "w") as f:
    f.write(fig1.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig2.to_html(full_html=False, include_plotlyjs=False))
    f.write(fig3.to_html(full_html=False, include_plotlyjs=False))
    f.write(fig4.to_html(full_html=False, include_plotlyjs=False))
    f.write(fig5.to_html(full_html=False, include_plotlyjs=False))
    f.write(fig6.to_html(full_html=False, include_plotlyjs=False))
    f.write(fig7.to_html(full_html=False, include_plotlyjs=False))
