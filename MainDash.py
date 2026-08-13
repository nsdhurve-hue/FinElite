import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
st.set_page_config(
    page_title="FinElite Banking Intelligence Dashboard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>

.stApp{
background:#F5F7FB;
}

[data-testid="stSidebar"]{
background:#172554;
}

[data-testid="stSidebar"] *{
color:white;
}

.kpi{
background:white;
padding:18px;
border-radius:12px;
box-shadow:0px 4px 15px rgba(0,0,0,.08);
}

.header{
font-size:2.6rem;
font-weight:800;
color:#172554;
}

.sub{
color:#64748B;
}

</style>
""",unsafe_allow_html=True)
@st.cache_data
def load_data(file):

    df=pd.read_excel(file)

    df.columns=(df.columns
        .str.strip()
        .str.replace(" ","_",regex=False))

    df["Age_Group"]=pd.cut(
        df["Age"],
        bins=[18,25,35,50,65,100],
        labels=["18-25","26-35","36-50","51-65","65+"]
    )

    df["High_Risk"]=np.where(
        (df["Credit_Score"]<600)|
        (df["Credit_Utilization"]>75)|
        (df["Missed_Payments"]>=3),
        "High Risk",
        "Standard"
    )

    return df
  uploaded = st.sidebar.file_uploader(
    "📂 Upload Banking Excel File",
    type=["xlsx", "xls"]
)

if uploaded is None:
    st.info("Please upload the Credit Card Banking Excel dataset.")
    st.stop()

df = load_data(uploaded)
filtered = df.copy()

df=load_data(uploaded)
gender=st.sidebar.multiselect(
"Gender",
sorted(df.Gender.unique()),
default=sorted(df.Gender.unique())
)

employment=st.sidebar.multiselect(
"Employment",
sorted(df.Employment_Type.unique()),
default=sorted(df.Employment_Type.unique())
)

age=st.sidebar.slider(
"Age",
int(df.Age.min()),
int(df.Age.max()),
(int(df.Age.min()),int(df.Age.max()))
)

score=st.sidebar.slider(
"Credit Score",
300,
850,
(300,850)
)

util=st.sidebar.slider(
"Credit Utilization %",
0,
100,
100
)
filtered=df[
(df.Gender.isin(gender))&
(df.Employment_Type.isin(employment))&
(df.Age.between(age[0],age[1]))&
(df.Credit_Score.between(score[0],score[1]))&
(df.Credit_Utilization<=util)
]
st.markdown(
'<div class="header">💳 FinElite Banking Intelligence Dashboard</div>',
unsafe_allow_html=True)

st.markdown(
'<div class="sub">Customer Intelligence • Financial Health • Credit Risk • Fraud Detection</div>',
unsafe_allow_html=True)
c1,c2,c3,c4,c5,c6=st.columns(6)

c1.metric("Customers",len(filtered))

c2.metric(
"Avg Spending",
f"₹{filtered.Avg_Monthly_Spending.mean():,.0f}"
)

c3.metric(
"Credit Score",
f"{filtered.Credit_Score.mean():.0f}"
)

c4.metric(
"Utilization",
f"{filtered.Credit_Utilization.mean():.1f}%"
)

c5.metric(
"Total Savings",
f"₹{filtered.Savings_Balance.sum():,.0f}"
)

c6.metric(
"High Risk",
(filtered.High_Risk=="High Risk").sum()
)
tab1,tab2,tab3,tab4,tab5,tab6=st.tabs([
"Executive",
"Customer Behavior",
"Financial",
"Credit Risk",
"Compliance",
"AI Insights"
])
with tab1:

    score=filtered.Credit_Score.mean()/850*100

    fig=go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text":"Portfolio Health"}
    ))

    st.plotly_chart(fig,use_container_width=True)
  fig=px.bar(
filtered.groupby("Age_Group").Avg_Monthly_Spending.mean().reset_index(),
x="Age_Group",
y="Avg_Monthly_Spending",
color="Avg_Monthly_Spending"
)

st.plotly_chart(fig,use_container_width=True)
fig=px.scatter(
filtered,
x="Annual_Income",
y="Avg_Monthly_Spending",
size="Credit_Limit",
color="Credit_Score"
)

st.plotly_chart(fig,use_container_width=True)
fig=px.histogram(
filtered,
x="Avg_Monthly_Transactions",
nbins=30
)

st.plotly_chart(fig,use_container_width=True)
fig=px.scatter(
filtered,
x="Savings_Balance",
y="Investment_Value",
color="Employment_Type",
size="Annual_Income"
)

st.plotly_chart(fig,use_container_width=True)
fig=px.scatter(
filtered,
x="EMI_Per_Month",
y="Debt_To_Income_Ratio",
color="Credit_Score"
)

st.plotly_chart(fig,use_container_width=True)
fig=px.pie(
filtered,
names="High_Risk",
hole=.5
)

st.plotly_chart(fig,use_container_width=True)
fig=px.box(
filtered,
x="High_Risk",
y="Credit_Utilization",
color="High_Risk"
)

st.plotly_chart(fig,use_container_width=True)
corr=filtered.select_dtypes("number").corr()

fig=px.imshow(
corr,
text_auto=".2f",
color_continuous_scale="RdBu_r"
)

st.plotly_chart(fig,use_container_width=True)
st.subheader("Live Risk Calculator")

score=st.slider("Credit Score",300,850,600)
util=st.slider("Utilization",0,100,70)
miss=st.slider("Missed Payments",0,10,2)

risk="High Risk" if score<600 or util>75 or miss>=3 else "Standard"

st.metric("Decision",risk)
fig=px.bar(
filtered.KYC_Status.value_counts().reset_index(),
x="KYC_Status",
y="count"
)

st.plotly_chart(fig,use_container_width=True)
fig=px.pie(
filtered,
names="Fraud_Flag"
)

st.plotly_chart(fig,use_container_width=True)
top_age=filtered.groupby("Age_Group").Avg_Monthly_Spending.mean().idxmax()

st.success(
f"{top_age} customers have the highest spending."
)

if filtered.Credit_Utilization.mean()>60:
    st.warning(
    "Portfolio utilization is above healthy range."
    )

if filtered.Debt_To_Income_Ratio.mean()>0.4:
    st.error(
    "Debt pressure is relatively high."
    )
