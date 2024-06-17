
# GITHUB CLONING
# Git Download
# open the downloaded file
# install the file
# open the command prompt
# type git and press enter
# type git config --global user.name "give your user name" press enter
# type git config --global user.email "give your mail id" press enter

# Create a new file with name of project on desktop and then open VS code and open the file
# and then open the terminal and type git clone and then go to the GITHUB link provided 
# from where open the code option and copy the link provided there and paste in vscode terminal and press enter

# importing libraries
import os
import streamlit as st 
from streamlit_option_menu import option_menu
import pandas as pd
import mysql.connector
import plotly.express as px
import requests
import json
from PIL import Image

# DataFrame Creation

mydb=mysql.connector.connect(
                host='localhost',
                user='root',
                password='-----------',
                database ='Phonepe_data'
                )
mycursor=mydb.cursor()

# aggregated_insurance_df
mycursor.execute("SELECT * FROM aggregated_insurance")
table1=mycursor.fetchall()

Aggre_insurance=pd.DataFrame(table1, columns=("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))
mydb.commit()

# aggregated_transaction_df
mycursor.execute("SELECT * FROM aggregated_transaction")
table2=mycursor.fetchall()

Aggre_transaction=pd.DataFrame(table2, columns=("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))
mydb.commit()

# aggregated_user_df
mycursor.execute("SELECT * FROM aggregated_user")
table3=mycursor.fetchall()

Aggre_user=pd.DataFrame(table3, columns=("States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"))
mydb.commit()

# map_insurance_df
mycursor.execute("SELECT * FROM map_insurance")
table4=mycursor.fetchall()

Map_insurance=pd.DataFrame(table4, columns=("States", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"))
mydb.commit()

# map_transaction_df
mycursor.execute("SELECT * FROM map_transaction")
table5=mycursor.fetchall()

Map_transaction=pd.DataFrame(table5, columns=("States", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"))
mydb.commit()

# map_user_df
mycursor.execute("SELECT * FROM map_user")
table6=mycursor.fetchall()

Map_user=pd.DataFrame(table6, columns=("States", "Years", "Quarter", "Districts", "RegisteredUsers", "AppOpens"))
mydb.commit()

# top_insurance_df
mycursor.execute("SELECT * FROM top_insurance")
table7=mycursor.fetchall()

Top_insurance=pd.DataFrame(table7, columns=("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))
mydb.commit()

# top_transaction_df
mycursor.execute("SELECT * FROM top_transaction")
table8=mycursor.fetchall()

Top_transaction=pd.DataFrame(table8, columns=("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))
mydb.commit()

# top_user_df
mycursor.execute("SELECT * FROM top_user")
table9=mycursor.fetchall()

Top_user=pd.DataFrame(table9, columns=("States", "Years", "Quarter", "Pincodes", "RegisteredUsers"))
mydb.commit()

# Transaction_amount_count_Y
def Transaction_amount_count_Y(df, year):
    
    tacy= df[df["Years"] == year]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)
    
    col1,col2 = st.columns(2)
    with col1:
        
        fig_amount= px.bar(tacyg, x="States", y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Viridis, height=650, width=600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count= px.bar(tacyg, x="States", y="Transaction_count", title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Plasma, height=650, width=600)

        st.plotly_chart(fig_count)
    
    col1,col2 = st.columns(2) 
    with col1:
          
        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name= []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()

        fig_india_1=px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_amount", color_continuous_scale="Rainbow",
                                range_color= (tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name= "States", title= f"{year} TRANSACTION AMOUNT", fitbounds= "locations",
                                height= 600,width= 600)
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)
    
    with col2:
        
        fig_india_2=px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_count", color_continuous_scale="Rainbow",
                                range_color= (tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name= "States", title= f"{year} TRANSACTION COUNT", fitbounds= "locations",
                                height= 600,width= 600)
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)
        
    return tacy

# Transaction_amount_count_Y_Q
def Transaction_amount_count_Y_Q(df, quarter):
    tacy=df[df["Quarter"] == quarter]
    tacy.reset_index(drop = True, inplace= True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    with col1:
        
        fig_amount= px.bar(tacyg, x="States", y="Transaction_amount", title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Viridis, height= 650,width= 600)
        st.plotly_chart(fig_amount)
    with col2:
        fig_count= px.bar(tacyg, x="States", y="Transaction_count", title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Plasma, height= 650,width= 600)

        st.plotly_chart(fig_count)
    col1,col2=st.columns(2)  
    with col1:
         
        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name= []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()

        fig_india_1= px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_amount", color_continuous_scale="Rainbow",
                                range_color= (tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name= "States", title= f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds= "locations",
                                height= 600,width= 600)
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)
    with col2:
        fig_india_2= px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_count", color_continuous_scale="Rainbow",
                                range_color= (tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name= "States", title= f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds= "locations",
                                height= 600,width= 600)
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)
        
    return tacy
    
# Aggre_Tran_Transaction_type        
def Aggre_Tran_Transaction_type(df, state):

    tacy=df[df["States"] == state]
    tacy.reset_index(drop = True, inplace= True)

    tacyg=tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_pie_1=px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_amount",
                        width= 600, title= f"{state.upper()} TRANSACTION AMOUNT", hole= 0.5)
        st.plotly_chart(fig_pie_1)
    with col2:
        fig_pie_2=px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_count",
                        width= 600, title= f"{state.upper()} TRANSACTION COUNT", hole= 0.5)
        st.plotly_chart(fig_pie_2)
        
### Aggre_user_analysis_1
def Aggre_user_plot_1(df, year):
    aguy= df[df["Years"]== year]
    aguy.reset_index(drop= True, inplace= True)

    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_bar_1=px.bar(aguyg, x= "Brands", y= "Transaction_count", title= f"{year} BRANDS AND TRANSACTION COUNT",
                    width= 1000, color_discrete_sequence= px.colors.sequential.Aggrnyl_r, hover_name= "Brands")
    st.plotly_chart(fig_bar_1)
    
    return aguy

### Aggre_user_analysis_2
def Aggre_user_plot_2(df, quarter):
    aguyq= df[df["Quarter"]== quarter]
    aguyq.reset_index(drop= True, inplace= True)

    aguyqg= pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace= True)

    fig_bar_1=px.bar(aguyqg, x= "Brands", y= "Transaction_count", title= f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",
                        width= 1000, color_discrete_sequence= px.colors.sequential.Magenta_r, hover_name= "Brands")
    st.plotly_chart(fig_bar_1)
    
    return aguyq

## Aggre_user_analysis_3
def Aggre_user_plot_3(df, state):
    auyqs= df[df["States"] == state]
    auyqs.reset_index(drop= True, inplace= True)

    fig_line_1= px.line(auyqs, x= "Brands", y= "Transaction_count", hover_data= "Percentage",
                        title= f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE", width= 1000, markers= True)
    st.plotly_chart(fig_line_1)
    
    return auyqs

# Map_insurance_District
def Map_insur_District(df, state):

    tacy=df[df["States"] == state]
    tacy.reset_index(drop = True, inplace= True)

    tacyg=tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1.col2= st.columns(2)
    with col1:   
        fig_bar_1= px.bar(tacyg, x= "Transaction_amount", y= "Districts", orientation= "h", height= 600,
                        title= f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)
    with col2:
        fig_bar_2= px.bar(tacyg, x= "Transaction_count", y= "Districts", orientation= "h", height= 600,
                        title= f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence= px.colors.sequential.Bluered)
        st.plotly_chart(fig_bar_2)
        
# Map_user_plot_1
def Map_user_plot_1(df, year):
    muy= df[df["Years"]== year]
    muy.reset_index(drop= True, inplace= True)

    muyg= pd.DataFrame(muy.groupby("States")[["RegisteredUsers", "AppOpens"]].sum())
    muyg.reset_index(inplace= True)

    fig_line_1= px.line(muyg, x= "States", y= ["RegisteredUsers", "AppOpens"],
                            title= f"{year} REGISTERED USERS, APPOPENS", width= 1000, height= 800, markers= True)
    st.plotly_chart(fig_line_1)
    
    return muy

# Map_user_plot_2
def Map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"]== quarter]
    muyq.reset_index(drop= True, inplace= True)

    muyqg= pd.DataFrame(muyq.groupby("States")[["RegisteredUsers", "AppOpens"]].sum())
    muyqg.reset_index(inplace= True)

    fig_line_2= px.line(muyqg, x= "States", y= ["RegisteredUsers", "AppOpens"],
                            title= f"{df["Years"].min()} YEAR {quarter} QUARTER REGISTERED USERS, APPOPENS", width= 1000, height= 800, markers= True,
                            color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_2)
    
    return muyq

# Map_user_plot_3
def Map_user_plot_3(df, states):
    muyqs= df[df["States"]== states]
    muyqs.reset_index(drop= True, inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_bar_1= px.bar(muyqs, x= "RegisteredUsers", y= "Districts", orientation= "h",
                                title= f"{states.upper()} REGISTERED USER", height= 800, color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_1)
    with col2:
        fig_map_user_bar_2= px.bar(muyqs, x= "AppOpens", y= "Districts", orientation= "h",
                                title= f"{states.upper()} APPOPENS", height= 800, color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_bar_2)
        
# Top_insurance_plot_1
def Top_insurance_plot_1(df, state):
    tiy= df[df["States"]== state]
    tiy.reset_index(drop= True, inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_top_insur_bar_1= px.bar(tiy, x= "Quarter", y= "Transaction_amount", hover_data= "Pincodes",
                                    title= "TRANSACTION AMOUNT", height= 650, width= 600, color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_top_insur_bar_1)
    with col2:  
        fig_top_insur_bar_2= px.bar(tiy, x= "Quarter", y= "Transaction_count", hover_data= "Pincodes",
                                    title= "TRANSACTION COUNT", height= 650, width= 600, color_discrete_sequence= px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_top_insur_bar_2)
 
# Top_user_plot_1       
def Top_user_plot_1(df, year):
    tuy= df[df["Years"]== year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["States", "Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_user_plot_1= px.bar(tuyg, x= "States", y= "RegisteredUsers", color= "Quarter", width= 1000, height= 800,
                                color_discrete_sequence= px.colors.sequential.Burgyl, hover_name= "States",
                                title= f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_user_plot_1)
    
    return tuy
        
# Top_user_plot_2
def Top_user_plot_2(df, state):
    tuys= df[df["States"]== state]
    tuys.reset_index(drop= True, inplace= True)

    fig_top_user_plot_2= px.bar(tuys, x= "Quarter", y= "RegisteredUsers", title= "REGISTERED USERS, PINCODES, QUARTER",
                                width= 1000, height= 800, color= "RegisteredUsers", hover_data= "Pincodes",
                                color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_user_plot_2)


# top_chart_transaction_amount

def top_chart_transaction_amount(table_name):
    mydb=mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='-----------',
                    database ='Phonepe_data'
                    )
    mycursor=mydb.cursor()


    # plot_1
    query1= f'''SELECT States, SUM(Transaction_amount) AS Transaction_amount FROM {table_name} GROUP BY States
            ORDER BY Transaction_amount DESC LIMIT 10'''

    mycursor.execute(query1)
    table_1= mycursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=["States", "Transaction_amount"])

    col1,col2= st.columns(2)
    with col1:

        fig_amount_1=px.bar(df_1, x="States", y="Transaction_amount", title= "TOP 10 TRANSACTION AMOUNT", hover_name= "States",
                            color_discrete_sequence=px.colors.sequential.Viridis, height= 650, width= 600)
        st.plotly_chart(fig_amount_1)

    # plot_2
    query2= f'''SELECT States, SUM(Transaction_amount) AS Transaction_amount FROM {table_name} GROUP BY States
            ORDER BY Transaction_amount  LIMIT 10'''

    mycursor.execute(query2)
    table_2= mycursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=["States", "Transaction_amount"])
        
    with col2:
        fig_amount_2=px.bar(df_2, x="States", y="Transaction_amount", title= "LAST 10 TRANSACTION AMOUNT", hover_name= "States",
                            color_discrete_sequence=px.colors.sequential.Viridis_r, height= 650, width= 600)
        st.plotly_chart(fig_amount_2)

    # plot_3
    query3= f'''SELECT States, AVG(Transaction_amount) AS Transaction_amount FROM {table_name} GROUP BY States
                ORDER BY Transaction_amount'''

    mycursor.execute(query3)
    table_3= mycursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=["States", "Transaction_amount"])
    fig_amount_3=px.bar(df_3, x="Transaction_amount", y="States", title= "AVERAGE OF TRANSACTION AMOUNT", hover_name= "States", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800, width= 1000)
    st.plotly_chart(fig_amount_3)
    
def top_chart_transaction_count(table_name):
    mydb=mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='-----------',
                    database ='Phonepe_data'
                    )
    mycursor=mydb.cursor()

    # plot_1
    query1= f'''SELECT States, SUM(Transaction_count) AS Transaction_count FROM {table_name} GROUP BY States
            ORDER BY Transaction_count DESC LIMIT 10'''

    mycursor.execute(query1)
    table_1= mycursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=["States", "Transaction_count"])
    
    col1,col2= st.columns(2)
    with col1:
        fig_amount_1=px.bar(df_1, x="States", y="Transaction_count", title= "TOP 10 TRANSACTION COUNT", hover_name= "States",
                            color_discrete_sequence=px.colors.sequential.Viridis, height= 650, width= 600)
        st.plotly_chart(fig_amount_1)

    # plot_2
    query2= f'''SELECT States, SUM(Transaction_count) AS Transaction_count FROM {table_name} GROUP BY States
            ORDER BY Transaction_count  LIMIT 10'''

    mycursor.execute(query2)
    table_2= mycursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=["States", "Transaction_count"])
    with col2:
        fig_amount_2=px.bar(df_2, x="States", y="Transaction_count", title= "LAST 10 TRANSACTION COUNT", hover_name= "States",
                            color_discrete_sequence=px.colors.sequential.Viridis_r, height= 650, width= 600)
        st.plotly_chart(fig_amount_2)

    # plot_3
    query3= f'''SELECT States, AVG(Transaction_count) AS Transaction_count FROM {table_name} GROUP BY States
                ORDER BY Transaction_count'''

    mycursor.execute(query3)
    table_3= mycursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=["States", "Transaction_count"])
    fig_amount_3=px.bar(df_3, x="Transaction_count", y="States", title= "AVERAGE OF TRANSACTION COUNT", hover_name= "States", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800, width=  1000)
    st.plotly_chart(fig_amount_3)
    
def top_chart_registered_user(table_name, state):
    mydb=mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='-----------',
                    database ='Phonepe_data'
                    )
    mycursor=mydb.cursor()


    # plot_1
    query1= f'''SELECT Districts, SUM(RegisteredUsers) AS RegisteredUsers FROM {table_name} WHERE States= '{state}'
                                        GROUP BY Districts ORDER BY RegisteredUsers DESC LIMIT 10'''

    mycursor.execute(query1)
    table_1= mycursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=["Districts", "RegisteredUsers"])
    col1,col2= st.columns(2)
    with col1:
        fig_amount_1=px.bar(df_1, x="Districts", y="RegisteredUsers", title= "TOP 10 REGISTERED USERS", hover_name= "Districts",
                            color_discrete_sequence=px.colors.sequential.Viridis, height= 650,width= 600)
        st.plotly_chart(fig_amount_1)

    # plot_2
    query2= f'''SELECT Districts, SUM(RegisteredUsers) AS RegisteredUsers FROM {table_name} WHERE States= '{state}'
                                        GROUP BY Districts ORDER BY RegisteredUsers LIMIT 10'''

    mycursor.execute(query2)
    table_2= mycursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=["Districts", "RegisteredUsers"])
    with col2:
        fig_amount_2=px.bar(df_2, x="Districts", y="RegisteredUsers", title= "LAST 10 REGISTERED USERS", hover_name= "Districts",
                            color_discrete_sequence=px.colors.sequential.Viridis_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    # plot_3
    query3= f'''SELECT Districts, AVG(RegisteredUsers) AS RegisteredUsers FROM {table_name} WHERE States= '{state}'
                                        GROUP BY Districts ORDER BY RegisteredUsers'''

    mycursor.execute(query3)
    table_3= mycursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=["Districts", "RegisteredUsers"])
    fig_amount_3=px.bar(df_3, x="RegisteredUsers", y="Districts", title= "AVERAGE OF REGISTERED USERS", hover_name= "Districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800, width= 1000)
    st.plotly_chart(fig_amount_3)
    
def top_chart_appopens(table_name, state):
    mydb=mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='-----------',
                    database ='Phonepe_data'
                    )
    mycursor=mydb.cursor()


    # plot_1
    query1= f'''SELECT Districts, SUM(AppOpens) AS AppOpens FROM {table_name} WHERE States= '{state}'
                                        GROUP BY Districts ORDER BY AppOpens DESC LIMIT 10'''

    mycursor.execute(query1)
    table_1= mycursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=["Districts", "AppOpens"])
    col1,col2= st.columns(2)
    with col1:
        fig_amount_1=px.bar(df_1, x="Districts", y="AppOpens", title= "TOP 10 APPOPENS", hover_name= "Districts",
                            color_discrete_sequence=px.colors.sequential.Viridis, height= 650,width= 600)
        st.plotly_chart(fig_amount_1)

    # plot_2
    query2= f'''SELECT Districts, SUM(AppOpens) AS AppOpens FROM {table_name} WHERE States= '{state}'
                                        GROUP BY Districts ORDER BY AppOpens LIMIT 10'''

    mycursor.execute(query2)
    table_2= mycursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=["Districts", "AppOpens"])
    with col2:
        fig_amount_2=px.bar(df_2, x="Districts", y="AppOpens", title= "LAST 10 APPOPENS", hover_name= "Districts",
                            color_discrete_sequence=px.colors.sequential.Viridis_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    # plot_3
    query3= f'''SELECT Districts, AVG(AppOpens) AS AppOpens FROM {table_name} WHERE States= '{state}'
                                        GROUP BY Districts ORDER BY AppOpens'''

    mycursor.execute(query3)
    table_3= mycursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=["Districts", "AppOpens"])
    fig_amount_3=px.bar(df_3, x="AppOpens", y="Districts", title= "AVERAGE OF APPOPENS", hover_name= "Districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800, width= 1000)
    st.plotly_chart(fig_amount_3)
    
def top_chart_registered_users(table_name):
    mydb=mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='-----------',
                    database ='Phonepe_data'
                    )
    mycursor=mydb.cursor()


    # plot_1
    query1= f'''SELECT States, SUM(RegisteredUsers) AS RegisteredUsers FROM {table_name} GROUP BY States 
                                    ORDER BY RegisteredUsers DESC LIMIT 10'''

    mycursor.execute(query1)
    table_1= mycursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=["States", "RegisteredUsers"])
    col1,col2= st.columns(2)
    with col1:
        fig_amount_1=px.bar(df_1, x="States", y="RegisteredUsers", title= "TOP 10 REGISTERED USERS", hover_name= "States",
                            color_discrete_sequence=px.colors.sequential.Viridis, height= 650,width= 600)
        st.plotly_chart(fig_amount_1)

    # plot_2
    query2= f'''SELECT States, SUM(RegisteredUsers) AS RegisteredUsers FROM {table_name} GROUP BY States
                                    ORDER BY RegisteredUsers LIMIT 10;'''

    mycursor.execute(query2)
    table_2= mycursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=["States", "RegisteredUsers"])
    with col2:
        fig_amount_2=px.bar(df_2, x="States", y="RegisteredUsers", title= "LAST 10 REGISTERED USERS", hover_name= "States",
                            color_discrete_sequence=px.colors.sequential.Viridis_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    # plot_3
    query3= f'''SELECT States, AVG(RegisteredUsers) AS RegisteredUsers FROM {table_name} GROUP BY States
                                    ORDER BY RegisteredUsers;'''

    mycursor.execute(query3)
    table_3= mycursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=["States", "RegisteredUsers"])
    fig_amount_3=px.bar(df_3, x="RegisteredUsers", y="States", title= "AVERAGE OF REGISTERED USERS", hover_name= "States", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800, width= 1000)
    st.plotly_chart(fig_amount_3)
    
def top_chart_brand_user(table_name, state):
    mydb=mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='-----------',
                    database ='Phonepe_data'
                    )
    mycursor=mydb.cursor()


    # plot_1
    query1= f'''SELECT Brands , SUM(Transaction_count) AS Transaction_count FROM {table_name} WHERE States= '{state}'
                                    GROUP BY Brands ORDER BY Transaction_count DESC LIMIT 10;'''

    mycursor.execute(query1)
    table_1= mycursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=["Brands", "Transaction_count"])
    col1,col2=st.columns(2)
    with col1:
        fig_amount_1=px.bar(df_1, x="Brands", y="Transaction_count", title= "TOP 10 TRANSACTION COUNT", hover_name= "Brands",
                            color_discrete_sequence=px.colors.sequential.Viridis, height= 650,width= 600)
        st.plotly_chart(fig_amount_1)

    # plot_2
    query2= f'''SELECT Brands , SUM(Transaction_count) AS Transaction_count FROM {table_name} WHERE States= '{state}'
                                    GROUP BY Brands ORDER BY Transaction_count LIMIT 10'''

    mycursor.execute(query2)
    table_2= mycursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=["Brands", "Transaction_count"])
    with col2:
        fig_amount_2=px.bar(df_2, x="Brands", y="Transaction_count", title= "LAST 10 TRANSACTION COUNT", hover_name= "Brands",
                            color_discrete_sequence=px.colors.sequential.Viridis_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    # plot_3
    query3= f'''SELECT Brands , AVG(Transaction_count) AS Transaction_count FROM {table_name} WHERE States= '{state}'
                                    GROUP BY Brands ORDER BY Transaction_count LIMIT 10'''

    mycursor.execute(query3)
    table_3= mycursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=["Brands", "Transaction_count"])
    fig_amount_3=px.bar(df_3, x="Transaction_count", y="Brands", title= "AVERAGE OF TRANSACTION COUNT", hover_name= "Brands", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800, width= 1000)
    st.plotly_chart(fig_amount_3)
    
# Streamlit Part

import streamlit as st

# Set page configuration
st.set_page_config(layout="wide")

# Title
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

# Sidebar menu
select = st.sidebar.selectbox("Main Menu", ["HOME", "DATA EXPLORATION", "TOP CHARTS"])


if select == "HOME":
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.image(Image.open(r"C:\Users\Hp\OneDrive\Desktop\python\images.jfif"),width= 450)

    col3,col4= st.columns(2)
    
    with col3:
        st.image(Image.open(r"C:\Users\Hp\OneDrive\Desktop\python\images (1).jfif"),width=500)

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.image(Image.open(r"C:\Users\Hp\OneDrive\Desktop\python\images (2).jfif"),width= 600)
  
elif select == "DATA EXPLORATION":
    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])
    
    with tab1:
        method_1 = st.radio("Select The Method", ["Agg Insurance Analysis", "Agg Transaction Analysis", "Agg User Analysis"])
        
        if method_1 == "Agg Insurance Analysis":
            
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year_ai", min_value=Aggre_insurance["Years"].min(), max_value=Aggre_insurance["Years"].max(), value=Aggre_insurance["Years"].min())
            tac_Y= Transaction_amount_count_Y(Aggre_insurance, years)
            
            col1,col2= st.columns(2)
            with col1:
                quarters = st.slider("Select The Quarter_ai", min_value= tac_Y["Quarter"].min(), max_value=tac_Y["Quarter"].max(), value=tac_Y["Quarter"].min())
            Transaction_amount_count_Y_Q(tac_Y, quarters)
                
        elif method_1 == "Agg Transaction Analysis":
            
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year_at", min_value=Aggre_transaction["Years"].min(), max_value=Aggre_transaction["Years"].max(), value=Aggre_transaction["Years"].min())
            Aggre_tran_tac_Y= Transaction_amount_count_Y(Aggre_transaction, years)
            
            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_at", Aggre_tran_tac_Y["States"].unique())   
            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y, states)
            
            col1,col2= st.columns(2)
            with col1:
                quarters = st.slider("Select The Quarter_at", min_value= Aggre_tran_tac_Y["Quarter"].min(), max_value=Aggre_tran_tac_Y["Quarter"].max(), value=Aggre_tran_tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q= Transaction_amount_count_Y_Q(Aggre_tran_tac_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_ata", Aggre_tran_tac_Y_Q["States"].unique())   
            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y_Q, states)            
        
        
        elif method_1 == "Agg User Analysis":
            
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year_au", min_value=Aggre_user["Years"].min(), max_value=Aggre_user["Years"].max(), value=Aggre_user["Years"].min())
            Aggre_user_Y= Aggre_user_plot_1(Aggre_user, years) 
        
            col1,col2= st.columns(2)
            with col1:
                quarters = st.slider("Select The Quarter_au", min_value= Aggre_user_Y["Quarter"].min(), max_value=Aggre_user_Y["Quarter"].max(), value=Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q= Aggre_user_plot_2(Aggre_user_Y, quarters)


            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_au", Aggre_user_Y_Q["States"].unique())   
            Aggre_user_plot_3(Aggre_user_Y_Q, states)
    
    
    with tab2:
        method_2=st.radio("Select The Method", ["Map Insurance Analysis", "Map Transaction Analysis", "Map User Analysis"])
        
        if method_2 =="Map Insurance Analysis":
            
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year_mi", min_value= Map_insurance["Years"].min(), max_value= Map_insurance["Years"].max(), value= Map_insurance["Years"].min())
            Map_insur_tac_Y= Transaction_amount_count_Y(Map_insurance, years) 
            
            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_mi", Map_insur_tac_Y["States"].unique())   
            Map_insur_District(Map_insur_tac_Y, states)
            
            col1,col2= st.columns(2)
            with col1:
                quarters = st.slider("Select The Quarter_mi", min_value= Map_insur_tac_Y["Quarter"].min(), max_value= Map_insur_tac_Y["Quarter"].max(), value= Map_insur_tac_Y["Quarter"].min())
            Map_insur_tac_Y_Q= Transaction_amount_count_Y_Q(Map_insur_tac_Y, quarters)
            
            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_mia", Map_insur_tac_Y_Q["States"].unique())   
            Map_insur_District(Map_insur_tac_Y_Q, states)
            
        elif method_2 == "Map Transaction Analysis":
            
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year_mt", min_value= Map_transaction["Years"].min(), max_value= Map_transaction["Years"].max(), value= Map_transaction["Years"].min())
            Map_tran_tac_Y= Transaction_amount_count_Y(Map_transaction, years) 
            
            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_mt", Map_tran_tac_Y["States"].unique())   
            Map_insur_District(Map_tran_tac_Y, states)
            
            col1,col2= st.columns(2)
            with col1:
                quarters = st.slider("Select The Quarter_mt", min_value= Map_tran_tac_Y["Quarter"].min(), max_value= Map_tran_tac_Y["Quarter"].max(), value= Map_tran_tac_Y["Quarter"].min())
            Map_tran_tac_Y_Q= Transaction_amount_count_Y_Q(Map_tran_tac_Y, quarters)
            
            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_mty", Map_tran_tac_Y_Q["States"].unique())   
            Map_insur_District(Map_tran_tac_Y_Q, states)
            
        elif method_2 == "Map User Analysis":
            
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year_mu", min_value= Map_user["Years"].min(), max_value= Map_user["Years"].max(), value= Map_user["Years"].min())
            Map_user_Y= Map_user_plot_1(Map_user, years)
    
            quarters_min = Map_user_Y["Quarter"].min()
            quarters_max = Map_user_Y["Quarter"].max()
            
            if quarters_min == quarters_max:
                quarters_min = 1
                quarters_max = 4

            col1,col2= st.columns(2)
            with col1:
                quarters = st.slider("Select The Quarter_mu", min_value=quarters_min, max_value=quarters_max, value=quarters_min)
                Map_user_Y_Q= Map_user_plot_2(Map_user_Y, quarters)
   
            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_mu", Map_user_Y_Q["States"].unique())   
            Map_user_plot_3(Map_user_Y_Q, states)


    with tab3:
        method_3=st.radio("Select The Method", ["Top Insurance Analysis", "Top Transaction Analysis", "Top User Analysis"])
        if method_3 =="Top Insurance Analysis":
            
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year_ti", min_value= Top_insurance["Years"].min(), max_value= Top_insurance["Years"].max(), value= Top_insurance["Years"].min())
            Top_insur_tac_Y= Transaction_amount_count_Y(Top_insurance, years) 
        
            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_ti", Top_insur_tac_Y["States"].unique())   
            Top_insurance_plot_1(Top_insur_tac_Y, states)
        
            col1,col2= st.columns(2)
            with col1:
                quarters = st.slider("Select The Quarter_ti", min_value= Top_insur_tac_Y["Quarter"].min(), max_value= Top_insur_tac_Y["Quarter"].max(), value= Top_insur_tac_Y["Quarter"].min())
            Top_insur_tac_Y_Q= Transaction_amount_count_Y_Q(Top_insur_tac_Y, quarters)
        
        elif method_3 == "Top Transaction Analysis":
            
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year_tt", min_value= Top_transaction["Years"].min(), max_value= Top_transaction["Years"].max(), value= Top_transaction["Years"].min())
            Top_tran_tac_Y= Transaction_amount_count_Y(Top_transaction, years) 
        
            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_tt", Top_tran_tac_Y["States"].unique())   
            Top_insurance_plot_1(Top_tran_tac_Y, states)
        
            col1,col2= st.columns(2)
            with col1:
                quarters = st.slider("Select The Quarter_tt", min_value= Top_tran_tac_Y["Quarter"].min(), max_value= Top_tran_tac_Y["Quarter"].max(), value= Top_tran_tac_Y["Quarter"].min())
            Top_tran_tac_Y_Q= Transaction_amount_count_Y_Q(Top_tran_tac_Y, quarters)
        
        elif method_3 == "Top User Analysis":
            
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year_tu", min_value= Top_user["Years"].min(), max_value= Top_user["Years"].max(), value= Top_user["Years"].min())
            Top_user_Y= Top_user_plot_1(Top_user, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_tu", Top_user_Y["States"].unique())   
            Top_user_plot_2(Top_user_Y, states)


elif select == "TOP CHARTS":
    question= st.selectbox("Select the Question",["1.Transaction Amount and Count of Aggregated Insurance",
                                                  "2.Transaction Amount and Count of Map Insurance",
                                                  "3.Transaction Amount and Count of Top Insurance",
                                                  "4.Transaction Amount and Count of Aggregated Transaction",
                                                  "5.Transaction Amount and Count of Map Transaction",
                                                  "6.Brand Name and Transaction Count of Aggregated user",
                                                  "7.Transaction Count of Aggregated user",
                                                  "8.Registered users of Map user", 
                                                  "9.AppOpens of Map user", 
                                                  "10.Registered users of Top User"])            

 
    if question == "1.Transaction Amount and Count of Aggregated Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")
        
    elif question == "2.Transaction Amount and Count of Map Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")
        
    elif question == "3.Transaction Amount and Count of Top Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")
        
    elif question == "4.Transaction Amount and Count of Aggregated Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")
        
    elif question == "5.Transaction Amount and Count of Map Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")
        
    elif question == "6.Brand Name and Transaction Count of Aggregated user":
        
        states= st.selectbox("Select The state", Aggre_user["States"].unique())
        st.subheader("TRANSACTION COUNT")
        top_chart_brand_user("aggregated_user", states)
        
    elif question == "7.Transaction Count of Aggregated user":
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user") 
                                                         
    elif question == "8.Registered users of Map user":
        
        states= st.selectbox("Select The state", Map_user["States"].unique())
        st.subheader("REGISTERED USERS")
        top_chart_registered_user("map_user", states)
        
    elif question == "9.AppOpens of Map user":
        
        states= st.selectbox("Select The state", Map_user["States"].unique())
        st.subheader("APPOPENS")
        top_chart_appopens("map_user", states)
        
    elif question == "10.Registered users of Top User":
        
        st.subheader("REGISTERED USERS")
        top_chart_registered_users("top_user")  