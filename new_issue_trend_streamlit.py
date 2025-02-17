import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

def plot_new_issue_trend(df):
    

    st.write("### New Issues Trend Analysis")

    # Calculate percentage change
    df["pre_wk_issue_count"] = df[issue_type].shift(1)
    df["percentage_change"] = ((df[issue_type] - df["pre_wk_issue_count"]) / df["pre_wk_issue_count"]) * 100
    df["color"] = ["red" if x > 10 else "green" for x in df["percentage_change"]]

    # Create Plotly figure
    fig = go.Figure()

    # Add line segments with color coding
    for i in range(1, len(df)):
        fig.add_trace(go.Scatter(
            x=list(map(str, df.index[i-1:i+1])),  # Convert index to string for better labels
            y=df[issue_type].iloc[i-1:i+1], 
            mode="lines",
            line=dict(color=df["color"].iloc[i], width=3),
            name=issue_type,  # Issue Type as legend
            showlegend=False  # Hide these lines from the legend
        ))

    # Manually add legend entries for color categories
    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode='lines',
        line=dict(color="green", width=3),
        name="Normal (≤ 10% increase)"
    ))

    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode='lines',
        line=dict(color="red", width=3),
        name="High Increase (> 10%)"
    ))

    # Layout settings
    fig.update_layout(
        title="Trend Analysis of New Issues",
        xaxis_title="Week Number",
        yaxis_title="Issue Count",
        legend_title="Change Category",
        template="plotly_white",
    )

    # Display in Streamlit
    st.plotly_chart(fig)


if __name__ == '__main__':

    #read the data from the excel files
    df_1=pd.read_excel("D210-New_Issue_Summary.xlsx")
    df_2=pd.read_excel("D215-New_Issue_Summary.xlsx")
    df_3=pd.read_excel("D410-New_Issue_Summary.xlsx")
    df_4=pd.read_excel("D430-New_Issue_Summary.xlsx")
    df_5=pd.read_excel("D450-New_Issue_Summary.xlsx")
    
    #preprocess the data for analysis
    issues = ["Device Failure","Device Not Responding","GPS Issue","Mount Issue","SD Card Issue","SIM Issue","Wiring Issue","Lens Issue","Grand Total"]
    df_1=df_1[df_1["New Issues that need field visit"].isin(issues)].set_index("New Issues that need field visit").T.reset_index().rename(columns={"index":"week"})
    df_1["product_type"]="D210"
    df_2=df_2[df_2["New Issues that need field visit"].isin(issues)].set_index("New Issues that need field visit").T.reset_index().rename(columns={"index":"week"})
    df_2["product_type"]="D215"
    df_3=df_3[df_3["New Issues that need field visit"].isin(issues)].set_index("New Issues that need field visit").T.reset_index().rename(columns={"index":"week"})
    df_3["product_type"]="D410"
    df_4=df_4[df_4["New Issues that need field visit"].isin(issues)].set_index("New Issues that need field visit").T.reset_index().rename(columns={"index":"week"})
    df_4["product_type"]="D430"
    df_5=df_5[df_5["New Issues that need field visit"].isin(issues)].set_index("New Issues that need field visit").T.reset_index().rename(columns={"index":"week"})
    df_5["product_type"]="D450"
    df=pd.concat([df_1,df_2,df_3,df_4,df_5]).fillna(0)
    df["week_no"]=(df["week"].str.extract(r"(\d{4})").astype(int) * 100  + df["week"].str.extract(r"Week (\d+)").astype(int))
    df.drop(columns=["week"],inplace=True)

    st.sidebar.subheader("Please select the required filters to analyze the data")

    # Filter by week range and select last 8 weeks as default
    weeks = sorted(df["week_no"].unique())
    week_range = st.sidebar.select_slider("Select Week Range:",options=weeks, value=(weeks[-8], weeks[-1]))
    df = df[df["week_no"].between(week_range[0], week_range[1])]
    
    # Filter by product type
    product_type = st.sidebar.multiselect("Select Product Type:", df["product_type"].unique(), default=df["product_type"].unique())
    df = df[df["product_type"].isin(product_type)]

    #Ask to select any one issue type by default select Device Failure using radio button
    issue_type = st.sidebar.radio("Select Issue Type",issues,0)

    df=df.groupby("week_no")[[issue_type]].sum()

    plot_new_issue_trend(df)


