import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth
import plotly.graph_objects as go

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Water Quality Dashboard", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="expanded", menu_items={
         'Get Help': None,
         'Report a bug': None,
         'About': "This is a dashboard for monitoring of Wastewater Quality Parameters"
     })

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


# Login Details
names = ['IIT Ropar']
usernames = ['iitrpr']
passwords = ['iitrpr']

hashed_passwords = stauth.Hasher(passwords).generate()
authenticator = stauth.Authenticate(names,usernames,hashed_passwords, 'some_cookie_name', 'some_signature_key', cookie_expiry_days=30)
name, authentication_status, username = authenticator.login('Login','main')



if st.session_state['authentication_status']:
    def get_data_from_excel():
        df = pd.read_excel(
            io="year_data.xlsx",
            engine="openpyxl",
            sheet_name="Sheet1",
            skiprows=0,
            usecols="A:G",
            nrows=1000,
        )
        return df

    df = get_data_from_excel()

    # ---- SIDEBAR ----

    st.sidebar.header("Apply Data Filters")

    last_date = st.sidebar.date_input(
        "Select Date",
        df["Date"].iloc[-1],
        df["Date"].iloc[0],
        df["Date"].iloc[-1]
    )

    mask = df['Date'] <= pd.Timestamp(last_date)
    df_s = df.loc[mask]

    days = st.sidebar.selectbox(
        "Select number of days:",
        options=[1, 2, 3, 5, 10, 15, 20, 30],
        index=2
    )

    df_selection = df_s.tail(days)

    # customer_type = st.sidebar.multiselect(
    #     "Select the Customer Type:",
    #     options=df["Customer_type"].unique(),
    #     default=df["Customer_type"].unique(),
    # )

    # gender = st.sidebar.multiselect(
    #     "Select the Gender:",
    #     options=df["Gender"].unique(),
    #     default=df["Gender"].unique()
    # )

    # df_selection = df.query(
    #     "City == @city & Customer_type ==@customer_type & Gender == @gender"
    # )


    # ---- MAINPAGE ----

    st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 4rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

    st.title(":bar_chart: Water Quality Dashboard")
    st.markdown("##")

    kpi_filter = st.date_input(
        "Show Values For",
        df["Date"].iloc[-1],
        df["Date"].iloc[0],
        df["Date"].iloc[-1]
    )
    kpi_index = df[df['Date'] == pd.Timestamp(kpi_filter)].index.values[0]
    kpi_day_data = df.iloc[kpi_index]
    prev_day_data = df.iloc[kpi_index-1]

    if kpi_index != 0:
        kpi1, kpi2, kpi3 = st.columns(3)
        if prev_day_data["pH"] <= 7:
            kpi1.metric("pH", kpi_day_data['pH'], round(kpi_day_data['pH'] - prev_day_data['pH'],2), delta_color="normal")
        elif prev_day_data['pH'] > 7:
            kpi1.metric("pH", kpi_day_data['pH'], round(kpi_day_data['pH'] - prev_day_data['pH'],2), delta_color="inverse")
    
        kpi2.metric("BOD", kpi_day_data["BOD"], round(kpi_day_data['BOD'] - prev_day_data["BOD"], 2), delta_color="inverse")
        kpi3.metric("ORP", kpi_day_data["ORP"], round(kpi_day_data['ORP'] - prev_day_data["ORP"], 2), delta_color="normal")

        kpi4, kpi5, kpi6 = st.columns(3)
        kpi4.metric("DO", kpi_day_data["DO"], round(kpi_day_data['DO'] - prev_day_data["DO"], 2), delta_color="normal")
        kpi5.metric("TSS", kpi_day_data["TSS"], round(kpi_day_data['TSS'] -prev_day_data["TSS"], 2), delta_color="inverse")
        kpi6.metric("RC", kpi_day_data["RC"], round(kpi_day_data['RC'] - prev_day_data["RC"], 2), delta_color="inverse")


    df_shown = df
    df_shown.Date = df_shown.Date.apply(lambda x: x.date())

    st.markdown("## Data Table")
    st.dataframe(df_shown)


    
    ################################
    pH_graph = go.Figure()
    pH_graph.add_trace(
        go.Line(
            x = df_selection['Date'],
            y=[8]*len(df_selection),
            name="Upper Limit",
            marker=dict(color="red")
        )
    )
    pH_graph.add_trace(
        go.Line(
            x = df_selection['Date'],
            y=[6.9]*len(df_selection),
            name="Lower Limit",
            marker=dict(color="purple")
        )
    )
    pH_graph.add_trace(
        go.Bar(
            x = df_selection['Date'],
            y=df_selection['pH'],
            name="pH",
            marker=dict(color="cyan")
        )
    )

    # pH_graph.add_bar(
    #     df_selection,
    #     x="date",
    #     y="pH",
    #     title="<b>pH</b>",
    #     # color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    #     template="plotly_white",
    # )

    pH_graph.update_layout(
        title="<b>pH Value</b>",
        showlegend=False,
        template="plotly_white",
        xaxis=dict(showgrid=False, tickmode="linear", title_text="Date"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showgrid=False, title_text="pH"),
    )
   
   
    ###################################
    BOD_graph = go.Figure()
    BOD_graph.add_trace(
        go.Line(
            x = df_selection['Date'],
            y=[22]*len(df_selection),
            name="Upper Limit",
            marker=dict(color="red")
        )
    )
    BOD_graph.add_trace(
        go.Bar(
            x = df_selection['Date'],
            y=df_selection['BOD'],
            name="BOD",
            marker=dict(color="cyan")
        )
    )

    # BOD_graph = px.bar(
    #     df_selection,
    #     x="date",
    #     y="BOD",
    #     title="<b>BOD (Biochemical Oxygen Demand)</b>",
    #     labels={"BOD":"BOD (mg/l)"},
    #     # color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    #     template="plotly_white",
    # )

    BOD_graph.update_layout(
        title="<b>BOD (Biochemical Oxygen Demand)</b>",
        showlegend=False,
        template="plotly_white",
        xaxis=dict(showgrid=False, tickmode="linear", title_text="Date"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showgrid=False, title_text="BOD"),
    )
   
   
    #################################
    ORP_graph = go.Figure()
    ORP_graph.add_trace(
        go.Line(
            x = df_selection['Date'],
            y=[100]*len(df_selection),
            name="Lower Limit",
            marker=dict(color="Green")
        )
    )
    ORP_graph.add_trace(
        go.Bar(
            x = df_selection['Date'],
            y=df_selection['ORP'],
            name="ORP",
            marker=dict(color="lightgreen")
        )
    )

    # ORP_graph = px.bar(
    #     df_selection,
    #     x="date",
    #     y="ORP",
    #     title="<b>ORP (Oxydation Reduction Potential</b>",
    #     labels={"ORP":"ORP (mV)"},
    #     # color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    #     template="plotly_white",
    # )
    ORP_graph.update_layout(
        title="<b>ORP (Oxydation Reduction Potential</b>",
        showlegend=False,
        template="plotly_white",
        xaxis=dict(showgrid=False, tickmode="linear", title_text="Date"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showgrid=False, title_text="ORP"),
    )
    ###############################


    left_column1, mid_column1, right_column1 = st.columns(3)
    left_column1.plotly_chart(pH_graph, use_container_width=True)
    mid_column1.plotly_chart(BOD_graph, use_container_width=True)
    right_column1.plotly_chart(ORP_graph, use_container_width=True)


    ################################
    DO_graph = go.Figure()
    DO_graph.add_trace(
        go.Line(
            x = df_selection['Date'],
            y=[2]*len(df_selection),
            name="Lower Limit",
            marker=dict(color="Green")
        )
    )
    DO_graph.add_trace(
        go.Bar(
            x = df_selection['Date'],
            y=df_selection['DO'],
            name="DO",
            marker=dict(color="skyblue")
        )
    )

    # DO_graph = px.bar(
    #     df_selection,
    #     x="date",
    #     y="DO",
    #     title="<b>Dissolved Oxygen</b>",
    #     labels={"Dissolved Oxygen":"Dissolved Oxygen (mg/L)"},
    #     # color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    #     template="plotly_white",
    # )
    DO_graph.update_layout(
        title="<b>Dissolved Oxygen</b>",
        showlegend=False,
        template="plotly_white",
        xaxis=dict(showgrid=False, tickmode="linear", title_text="Date"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showgrid=False, title_text="DO"),
    )


    ###################################
    TSS_graph = go.Figure()
    TSS_graph.add_trace(
        go.Line(
            x = df_selection['Date'],
            y=[20]*len(df_selection),
            name="Upper Limit",
            marker=dict(color="red")
        )
    )
    TSS_graph.add_trace(
        go.Bar(
            x = df_selection['Date'],
            y=df_selection['TSS'],
            name="TSS",
            marker=dict(color="yellow")
        )
    )

    # TSS_graph = px.bar(
    #     df_selection,
    #     x="date",
    #     y="TSS",
    #     title="<b>Total Suspended Solids</b>",
    #     labels={"Total Suspended Solids":"Total Suspended Solids (mg/l)"},
    #     # color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    #     template="plotly_white",
    # )

    TSS_graph.update_layout(
        title="<b>Total Suspended Solids</b>",
        showlegend=False,
        template="plotly_white",
        xaxis=dict(showgrid=False, tickmode="linear", title_text="Date"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showgrid=False, title_text="TSS"),
    )


    #################################
    RC_graph = go.Figure()
    RC_graph.add_trace(
        go.Line(
            x = df_selection['Date'],
            y=[0.3]*len(df_selection),
            name="Upper Limit",
            marker=dict(color="red")
        )
    )
    RC_graph.add_trace(
        go.Bar(
            x = df_selection['Date'],
            y=df_selection['RC'],
            name="RC",
            marker=dict(color="pink")
        )
    )

    # RC_graph = px.bar(
    #     df_selection,
    #     x="date",
    #     y="RC",
    #     title="<b>Residual Chlorine</b>",
    #     labels={"Residual Chlorine":"Residual Chlorine (mg/l)"},
    #     # color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    #     template="plotly_white",
    # )
    RC_graph.update_layout(
        title="<b>Residual Chlorine</b>",
        showlegend=False,
        template="plotly_white",
        xaxis=dict(showgrid=False, tickmode="linear", title_text="Date"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showgrid=False, title_text="RC"),
    )
    ###############################


    left_column2, mid_column2, right_column2 = st.columns(3)
    left_column2.plotly_chart(DO_graph, use_container_width=True)
    mid_column2.plotly_chart(TSS_graph, use_container_width=True)
    right_column2.plotly_chart(RC_graph, use_container_width=True)


    authenticator.logout('Logout', 'main')


    


elif st.session_state['authentication_status'] == False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] == None:
    st.warning('Please enter your username and password')