import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Water Quality Dashboard", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="collapsed", menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help',
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a header. This is an *extremely* cool app!"
     })

names = ['John Smith','Rebecca Briggs']
usernames = ['jsmith','rbriggs']
passwords = ['123','456']

hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(names,usernames,hashed_passwords, 'some_cookie_name', 'some_signature_key', cookie_expiry_days=30)

name, authentication_status, username = authenticator.login('Login','main')


if st.session_state['authentication_status']:
    
    # st.write('Welcome *%s*' % (st.session_state['name']))
    # st.title('Some content')

    # ---- READ EXCEL ----
    @st.cache
    def get_data_from_excel():
        df = pd.read_excel(
            io="parameters.xlsx",
            engine="openpyxl",
            sheet_name="Sheet1",
            skiprows=1,
            usecols="A:G",
            nrows=1000,
        )
        # Add 'hour' column to dataframe
        # df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
        return df

    df = get_data_from_excel()

    # ---- SIDEBAR ----
    st.sidebar.header("Please Filter Here:")
    days = st.sidebar.selectbox(
        "Select number of days:",
        options=[1, 2, 3, 5, 10, 15, 20, 30]
    )

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

    df_selection = df.tail(days)

    # ---- MAINPAGE ----
    st.title(":bar_chart: Water Quality Dashboard")
    st.markdown("##")

    # TOP KPI's
    # total_sales = int(df_selection["Total"].sum())
    # average_rating = round(df_selection["Rating"].mean(), 1)
    # star_rating = ":star:" * int(round(average_rating, 0))
    # average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

    # left_column, middle_column, right_column = st.columns(3)
    # with left_column:
    #     st.subheader("Total Sales:")
    #     st.subheader(f"US $ {total_sales:,}")
    # with middle_column:
    #     st.subheader("Average Rating:")
    #     st.subheader(f"{average_rating} {star_rating}")
    # with right_column:
    #     st.subheader("Average Sales Per Transaction:")
    #     st.subheader(f"US $ {average_sale_by_transaction}")

    # st.markdown("""---""")



    # SALES BY PRODUCT LINE [BAR CHART]
    # sales_by_product_line = (
    #     df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
    # )
    # fig_product_sales = px.bar(
    #     sales_by_product_line,
    #     x="Total",
    #     y=sales_by_product_line.index,
    #     orientation="h",
    #     title="<b>Sales by Product Line</b>",
    #     color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    #     template="plotly_white",
    # )
    # fig_product_sales.update_layout(
    #     plot_bgcolor="rgba(0,0,0,0)",
    #     xaxis=(dict(showgrid=False))
    # )

    # SALES BY HOUR [BAR CHART] 1

    # sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]


    ################################
    pH_graph = px.bar(
        df_selection,
        x="Day",
        y="pH",
        title="<b>pH</b>",
        # color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
        template="plotly_white",
    )
    pH_graph.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
    ###################################
    BOD_graph = px.bar(
        df_selection,
        x="Day",
        y="BOD",
        title="<b>BOD (Biochemical Oxygen Demand)</b>",
        labels={"BOD":"BOD (mg/l)"},
        # color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
        template="plotly_white",
    )
    BOD_graph.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
    #################################
    ORP_graph = px.bar(
        df_selection,
        x="Day",
        y="ORP",
        title="<b>ORP (Oxydation Reduction Potential</b>",
        labels={"ORP":"ORP (mV)"},
        # color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
        template="plotly_white",
    )
    ORP_graph.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
    ###############################

    left_column1, mid_column1, right_column1 = st.columns(3)
    left_column1.plotly_chart(pH_graph, use_container_width=True)
    mid_column1.plotly_chart(BOD_graph, use_container_width=True)
    right_column1.plotly_chart(ORP_graph, use_container_width=True)


    ################################
    turbidity_graph = px.bar(
        df_selection,
        x="Day",
        y="Turbidity",
        title="<b>Turbidity</b>",
        labels={"Turbidity":"Turbidity (NTU)"},
        # color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
        template="plotly_white",
    )
    turbidity_graph.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
    ###################################
    RC_graph = px.bar(
        df_selection,
        x="Day",
        y="Residual Chlorine",
        title="<b>Residual Chlorine</b>",
        labels={"Residual Chlorine":"Residual Chlorine (mg/l)"},
        # color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
        template="plotly_white",
    )
    RC_graph.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
    #################################
    FC_graph = px.bar(
        df_selection,
        x="Day",
        y="Fecal Coliform",
        title="<b>Fecal Coliform</b>",
        labels={"Fecal Coliform":"Fecal Coliform (per 100 ml)"},
        # color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
        template="plotly_white",
    )
    FC_graph.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
    ###############################


    left_column2, mid_column2, right_column2 = st.columns(3)
    left_column2.plotly_chart(turbidity_graph, use_container_width=True)
    mid_column2.plotly_chart(RC_graph, use_container_width=True)
    right_column2.plotly_chart(FC_graph, use_container_width=True)




    # sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
    # fig_hourly_sales_2 = px.bar(
    #     sales_by_hour,
    #     x=sales_by_hour.index,
    #     y="Total",
    #     title="<b>BOD (Biochemical Oxygen Demand)</b>",
    #     color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    #     template="plotly_white",
    # )
    # fig_hourly_sales_2.update_layout(
    #     xaxis=dict(tickmode="linear"),
    #     plot_bgcolor="rgba(0,0,0,0)",
    #     yaxis=(dict(showgrid=False)),
    # )

    # sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
    # fig_hourly_sales_3 = px.bar(
    #     sales_by_hour,
    #     x=sales_by_hour.index,
    #     y="Total",
    #     title="<b>ORP (Oxydation Reduction Potential</b>",
    #     color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    #     template="plotly_white",
    # )
    # fig_hourly_sales_3.update_layout(
    #     xaxis=dict(tickmode="linear"),
    #     plot_bgcolor="rgba(0,0,0,0)",
    #     yaxis=(dict(showgrid=False)),
    # )

    # left_column, mid_column, right_column = st.columns(3)
    # left_column.plotly_chart(fig_hourly_sales_1, use_container_width=True)
    # mid_column.plotly_chart(fig_hourly_sales_2, use_container_width=True)
    # right_column.plotly_chart(fig_hourly_sales_3, use_container_width=True)


    # # SALES BY HOUR [BAR CHART] 4, 5, 6
    # sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
    # fig_hourly_sales_4 = px.bar(
    #     sales_by_hour,
    #     x=sales_by_hour.index,
    #     y="Total",
    #     title="<b>Turbidity</b>",
    #     color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    #     template="plotly_white",
    # )
    # fig_hourly_sales_4.update_layout(
    #     xaxis=dict(tickmode="linear"),
    #     plot_bgcolor="rgba(0,0,0,0)",
    #     yaxis=(dict(showgrid=False)),
    # )

    # sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
    # fig_hourly_sales_5 = px.bar(
    #     sales_by_hour,
    #     x=sales_by_hour.index,
    #     y="Total",
    #     title="<b>Residual Chlorine</b>",
    #     color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    #     template="plotly_white",
    # )
    # fig_hourly_sales_5.update_layout(
    #     xaxis=dict(tickmode="linear"),
    #     plot_bgcolor="rgba(0,0,0,0)",
    #     yaxis=(dict(showgrid=False)),
    # )

    # sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
    # fig_hourly_sales_6 = px.bar(
    #     sales_by_hour,
    #     x=sales_by_hour.index,
    #     y="Total",
    #     title="<b>Fecal Coliform</b>",
    #     color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    #     template="plotly_white",
    # )
    # fig_hourly_sales_6.update_layout(
    #     xaxis=dict(tickmode="linear"),
    #     plot_bgcolor="rgba(0,0,0,0)",
    #     yaxis=(dict(showgrid=False)),
    # )

    # left_column, mid_column, right_column = st.columns(3)
    # left_column.plotly_chart(fig_hourly_sales_4, use_container_width=True)
    # mid_column.plotly_chart(fig_hourly_sales_5, use_container_width=True)
    # right_column.plotly_chart(fig_hourly_sales_6, use_container_width=True)

    authenticator.logout('Logout', 'main')


    # ---- HIDE STREAMLIT STYLE ----
    hide_st_style = """
                <style>
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)


elif st.session_state['authentication_status'] == False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] == None:
    st.warning('Please enter your username and password')



# # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
# st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

# # ---- READ EXCEL ----
# @st.cache
# def get_data_from_excel():
#     df = pd.read_excel(
#         io="parameters.xlsx",
#         engine="openpyxl",
#         sheet_name="Sheet1",
#         skiprows=1,
#         usecols="A:G",
#         nrows=1000,
#     )
#     # Add 'hour' column to dataframe
#     # df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
#     return df

# df = get_data_from_excel()

# # ---- SIDEBAR ----
# st.sidebar.header("Please Filter Here:")
# days = st.sidebar.selectbox(
#     "Select number of days:",
#     options=[1, 2, 3, 5, 10, 15, 20, 30]
# )

# # customer_type = st.sidebar.multiselect(
# #     "Select the Customer Type:",
# #     options=df["Customer_type"].unique(),
# #     default=df["Customer_type"].unique(),
# # )

# # gender = st.sidebar.multiselect(
# #     "Select the Gender:",
# #     options=df["Gender"].unique(),
# #     default=df["Gender"].unique()
# # )

# # df_selection = df.query(
# #     "City == @city & Customer_type ==@customer_type & Gender == @gender"
# # )

# df_selection = df.tail(days)

# # ---- MAINPAGE ----
# st.title(":bar_chart: Water Quality Dashboard")
# st.markdown("##")

# # TOP KPI's
# # total_sales = int(df_selection["Total"].sum())
# # average_rating = round(df_selection["Rating"].mean(), 1)
# # star_rating = ":star:" * int(round(average_rating, 0))
# # average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

# # left_column, middle_column, right_column = st.columns(3)
# # with left_column:
# #     st.subheader("Total Sales:")
# #     st.subheader(f"US $ {total_sales:,}")
# # with middle_column:
# #     st.subheader("Average Rating:")
# #     st.subheader(f"{average_rating} {star_rating}")
# # with right_column:
# #     st.subheader("Average Sales Per Transaction:")
# #     st.subheader(f"US $ {average_sale_by_transaction}")

# # st.markdown("""---""")



# # SALES BY PRODUCT LINE [BAR CHART]
# # sales_by_product_line = (
# #     df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
# # )
# # fig_product_sales = px.bar(
# #     sales_by_product_line,
# #     x="Total",
# #     y=sales_by_product_line.index,
# #     orientation="h",
# #     title="<b>Sales by Product Line</b>",
# #     color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
# #     template="plotly_white",
# # )
# # fig_product_sales.update_layout(
# #     plot_bgcolor="rgba(0,0,0,0)",
# #     xaxis=(dict(showgrid=False))
# # )

# # SALES BY HOUR [BAR CHART] 1

# # sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]


# ################################
# pH_graph = px.bar(
#     df_selection,
#     x="Day",
#     y="pH",
#     title="<b>pH</b>",
#     # color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
#     template="plotly_white",
# )
# pH_graph.update_layout(
#     xaxis=dict(tickmode="linear"),
#     plot_bgcolor="rgba(0,0,0,0)",
#     yaxis=(dict(showgrid=False)),
# )
# ###################################
# BOD_graph = px.bar(
#     df_selection,
#     x="Day",
#     y="BOD",
#     title="<b>BOD (Biochemical Oxygen Demand)</b>",
#     labels={"BOD":"BOD (mg/l)"},
#     # color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
#     template="plotly_white",
# )
# BOD_graph.update_layout(
#     xaxis=dict(tickmode="linear"),
#     plot_bgcolor="rgba(0,0,0,0)",
#     yaxis=(dict(showgrid=False)),
# )
# #################################
# ORP_graph = px.bar(
#     df_selection,
#     x="Day",
#     y="ORP",
#     title="<b>ORP (Oxydation Reduction Potential</b>",
#     labels={"ORP":"ORP (mV)"},
#     # color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
#     template="plotly_white",
# )
# ORP_graph.update_layout(
#     xaxis=dict(tickmode="linear"),
#     plot_bgcolor="rgba(0,0,0,0)",
#     yaxis=(dict(showgrid=False)),
# )
# ###############################

# left_column1, mid_column1, right_column1 = st.columns(3)
# left_column1.plotly_chart(pH_graph, use_container_width=True)
# mid_column1.plotly_chart(BOD_graph, use_container_width=True)
# right_column1.plotly_chart(ORP_graph, use_container_width=True)


# ################################
# turbidity_graph = px.bar(
#     df_selection,
#     x="Day",
#     y="Turbidity",
#     title="<b>Turbidity</b>",
#     labels={"Turbidity":"Turbidity (NTU)"},
#     # color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
#     template="plotly_white",
# )
# turbidity_graph.update_layout(
#     xaxis=dict(tickmode="linear"),
#     plot_bgcolor="rgba(0,0,0,0)",
#     yaxis=(dict(showgrid=False)),
# )
# ###################################
# RC_graph = px.bar(
#     df_selection,
#     x="Day",
#     y="Residual Chlorine",
#     title="<b>Residual Chlorine</b>",
#     labels={"Residual Chlorine":"Residual Chlorine (mg/l)"},
#     # color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
#     template="plotly_white",
# )
# RC_graph.update_layout(
#     xaxis=dict(tickmode="linear"),
#     plot_bgcolor="rgba(0,0,0,0)",
#     yaxis=(dict(showgrid=False)),
# )
# #################################
# FC_graph = px.bar(
#     df_selection,
#     x="Day",
#     y="Fecal Coliform",
#     title="<b>Fecal Coliform</b>",
#     labels={"Fecal Coliform":"Fecal Coliform (per 100 ml)"},
#     # color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
#     template="plotly_white",
# )
# FC_graph.update_layout(
#     xaxis=dict(tickmode="linear"),
#     plot_bgcolor="rgba(0,0,0,0)",
#     yaxis=(dict(showgrid=False)),
# )
# ###############################


# left_column2, mid_column2, right_column2 = st.columns(3)
# left_column2.plotly_chart(turbidity_graph, use_container_width=True)
# mid_column2.plotly_chart(RC_graph, use_container_width=True)
# right_column2.plotly_chart(FC_graph, use_container_width=True)




# # sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
# # fig_hourly_sales_2 = px.bar(
# #     sales_by_hour,
# #     x=sales_by_hour.index,
# #     y="Total",
# #     title="<b>BOD (Biochemical Oxygen Demand)</b>",
# #     color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
# #     template="plotly_white",
# # )
# # fig_hourly_sales_2.update_layout(
# #     xaxis=dict(tickmode="linear"),
# #     plot_bgcolor="rgba(0,0,0,0)",
# #     yaxis=(dict(showgrid=False)),
# # )

# # sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
# # fig_hourly_sales_3 = px.bar(
# #     sales_by_hour,
# #     x=sales_by_hour.index,
# #     y="Total",
# #     title="<b>ORP (Oxydation Reduction Potential</b>",
# #     color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
# #     template="plotly_white",
# # )
# # fig_hourly_sales_3.update_layout(
# #     xaxis=dict(tickmode="linear"),
# #     plot_bgcolor="rgba(0,0,0,0)",
# #     yaxis=(dict(showgrid=False)),
# # )

# # left_column, mid_column, right_column = st.columns(3)
# # left_column.plotly_chart(fig_hourly_sales_1, use_container_width=True)
# # mid_column.plotly_chart(fig_hourly_sales_2, use_container_width=True)
# # right_column.plotly_chart(fig_hourly_sales_3, use_container_width=True)


# # # SALES BY HOUR [BAR CHART] 4, 5, 6
# # sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
# # fig_hourly_sales_4 = px.bar(
# #     sales_by_hour,
# #     x=sales_by_hour.index,
# #     y="Total",
# #     title="<b>Turbidity</b>",
# #     color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
# #     template="plotly_white",
# # )
# # fig_hourly_sales_4.update_layout(
# #     xaxis=dict(tickmode="linear"),
# #     plot_bgcolor="rgba(0,0,0,0)",
# #     yaxis=(dict(showgrid=False)),
# # )

# # sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
# # fig_hourly_sales_5 = px.bar(
# #     sales_by_hour,
# #     x=sales_by_hour.index,
# #     y="Total",
# #     title="<b>Residual Chlorine</b>",
# #     color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
# #     template="plotly_white",
# # )
# # fig_hourly_sales_5.update_layout(
# #     xaxis=dict(tickmode="linear"),
# #     plot_bgcolor="rgba(0,0,0,0)",
# #     yaxis=(dict(showgrid=False)),
# # )

# # sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
# # fig_hourly_sales_6 = px.bar(
# #     sales_by_hour,
# #     x=sales_by_hour.index,
# #     y="Total",
# #     title="<b>Fecal Coliform</b>",
# #     color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
# #     template="plotly_white",
# # )
# # fig_hourly_sales_6.update_layout(
# #     xaxis=dict(tickmode="linear"),
# #     plot_bgcolor="rgba(0,0,0,0)",
# #     yaxis=(dict(showgrid=False)),
# # )

# # left_column, mid_column, right_column = st.columns(3)
# # left_column.plotly_chart(fig_hourly_sales_4, use_container_width=True)
# # mid_column.plotly_chart(fig_hourly_sales_5, use_container_width=True)
# # right_column.plotly_chart(fig_hourly_sales_6, use_container_width=True)



# # ---- HIDE STREAMLIT STYLE ----
# hide_st_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_st_style, unsafe_allow_html=True)
