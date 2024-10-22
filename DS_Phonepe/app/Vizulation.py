import streamlit as st
import psycopg2 
import pandas as pd
import plotly.express as px
from DS_Phonepe.ELT import data_processing
import geopandas as gpd
import matplotlib.pyplot as plt


####################################### DB Config ###############################################
mydb = {
    'host' : 'localhost',
    'database' : 'guvi',
    'user' :'postgres',
    'password' : 'ags009',
    'port' : '5432'

}
# mydb = {
#     'host' : 'dpg-cmmvudocmk4c73e4qfh0-a.oregon-postgres.render.com',
#     'database' : 'guvi_yby8',
#     'user' :'guvi_yby8_user',
#     'password' : 'MFyUGk2fbpvmiRZ8FaXIBt56uXD9eMWc',
#     'port' : '5432'
# }
connection = psycopg2.connect(**mydb)
cursor = connection.cursor()


# DATABASE_URI =  "postgresql://guvi_yby8_user:MFyUGk2fbpvmiRZ8FaXIBt56uXD9eMWc@dpg-cmmvudocmk4c73e4qfh0-a.oregon-postgres.render.com:5432/guvi_yby8"
        

# engine = create_engine(DATABASE_URI)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# def CreateTables():
#     Base.metadata.create_all(bind=engine)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

######################################## DB config End ##########################################

######################################## Main Page Setup ##########################################s
st.header(':violet[Phonepe Pulse Data Visualization ]')
st.write('**(Note)**:-This data between **2018** to **2022** in **INDIA**')
if st.button('Get data'):
    data_processing()
option = st.radio('**Select your Option**',('All India','State Wise','Top Ten'),horizontal=True)

if option == "All India":
    tab1, tab2 = st.tabs(['Transaction','User'])
    india_shapefile_path = 'gadm41_IND_shp/gadm41_IND_1.shp'
    india = gpd.read_file(india_shapefile_path)

    # world = gpd.read_file(gpd.datasets.get_path('gadm41_IND_shp/gadm41_IND_1.shp'))
    st.write(india)

    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            year = st.selectbox('**Select Year**',   ('2018','2019','2020','2021'),key='year')
        with col2:
            quarter = st.selectbox('**Select Quarter**',('1','2','3','4'),key='quarter')
        with col3:
            type = st.selectbox('**Select Type**',('Recharge & bill payments','Financial Services','Merchant payments','Peer-to-peer payments'),key='type')

        cursor.execute(f"select state, transaction_amount from agg_tra where year='{year}' and quarter='{quarter}' and transaction_type='{type}' group by state,transaction_amount order by transaction_amount desc limit 30" )
        result = cursor.fetchall()
        transactions = pd.DataFrame(result,columns=['state','transaction_amount'] )
        transactions['state'] = transactions['state'].str.upper()
        india['NAME_1'] = india['NAME_1'].str.upper()
        india = india.merge(transactions, how='left', left_on='NAME_1', right_on='state')
        fig, ax = plt.subplots(1, 1, figsize=(15, 15))
        india.boundary.plot(ax=ax, linewidth=1)
        india.plot(column='transaction_amount', ax=ax, legend=True, 
                legend_kwds={'label': "Transaction Amount by State",
                                'orientation': "horizontal"},
                cmap='OrRd')  # OrRd colormap for better visual
        plt.title('Online Payment Transactions by State in India')
        # plt.show()
        st.pyplot(fig)

        cursor.execute(f"select state, transaction_amount from agg_tra where year='{year}' and quarter='{quarter}' and transaction_type='{type}' group by state,transaction_amount order by transaction_amount desc limit 10" )
        result = cursor.fetchall()
        df_result = pd.DataFrame(result,columns=['state','transaction_amount'] )
        pie_chart = px.pie(df_result, values='transaction_amount', names='state', title='Top 10 States phonepay')
        st.write(pie_chart)

        least_usegae = (f"select state, transaction_amount from agg_tra where year='{year}' and quarter='{quarter}' and transaction_type='{type}' group by state,transaction_amount order by transaction_amount asc limit 10" )
        cursor.execute(least_usegae)
        result_least = cursor.fetchall()
        df_result_least = pd.DataFrame(result_least,columns=['state','transaction_amount'] )
        pie_chart_least = px.pie(df_result_least, values='transaction_amount', names='state', title='Least 10 States phonepay')
        st.write(pie_chart_least)

        # st.write(df_result)
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            agg_usr_year = st.selectbox('**Select Year**',   ('2018','2019','2020','2021'),key='agg_usr_year')
        with col2:
            agg_usr_quarter = st.selectbox('**Select Quarter**',('1','2','3','4'),key='agg_usr_quarter')
        
        cursor.execute(f"select state, brands,user_count,user_percentage from agg_user where year='{agg_usr_year}' and quarter='{agg_usr_quarter}'")
        agg_usr_result = cursor.fetchall()
        df_result = pd.DataFrame(agg_usr_result,columns=['state','brands','user_count','user_percentage'] )
        # pie_chart = px.pie(df_result, values='transaction_amount', names='state', title='phonepay')
        st.write(df_result)


if option == "State Wise":
    tab1, tab2 = st.tabs(['Transaction','User'])

    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            year = st.selectbox('**Select Year**',   ('2018','2019','2020','2021'),key='year')
        with col2:
            quarter = st.selectbox('**Select Quarter**',('1','2','3','4'),key='quarter')
        with col3:
            type = st.selectbox('**Select Type**',('Recharge & bill payments','Financial Services','Merchant payments','Peer-to-peer payments'),key='type')
        with col4:
            state = ["nagaland","punjab","chhattisgarh","gujarat","jammu-&-kashmir","goa","arunachal-pradesh","kerala","delhi","tamil-nadu","puducherry","haryana","lakshadweep","dadra-&-nagar-haveli-&-daman-&-diu","maharashtra","assam","uttar-pradesh","manipur","odisha","uttarakhand","tripura","karnataka","andaman-&-nicobar-islands","chandigarh","jharkhand","himachal-pradesh","andhra-pradesh","rajasthan","madhya-pradesh","west-bengal","telangana","mizoram","ladakh","bihar","meghalaya","sikkim"]
            states = st.selectbox('**Select state**',state,key='states')


        cursor.execute(f"select state, transaction_amount from agg_tra where year='{year}' and quarter='{quarter}' and transaction_type='{type}' and state = '{states}' group by state, transaction_amount ")
        result = cursor.fetchall()
        # df_result = pd.DataFrame(result,columns=['state','transaction_amount'] )
        # pie_chart = px.pie(df_result, values='transaction_amount', names='state', title='phonepay')
        # st.write(pie_chart)
        st.header(result[0][0].upper())
        st.header(result[0][1])
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            agg_usr_year = st.selectbox('**Select Year**',   ('2018','2019','2020','2021'),key='agg_usr_year')
        with col2:
            agg_usr_quarter = st.selectbox('**Select Quarter**',('1','2','3','4'),key='agg_usr_quarter')
        
        cursor.execute(f"select state, brands,user_count,user_percentage from agg_user where year='{agg_usr_year}' and quarter='{agg_usr_quarter}'")
        agg_usr_result = cursor.fetchall()
        df_result = pd.DataFrame(agg_usr_result,columns=['state','brands','user_count','user_percentage'] )
        # pie_chart = px.pie(df_result, values='transaction_amount', names='state', title='phonepay')
        st.write(df_result)



if option == "Top Ten":
    tab1, tab2 = st.tabs(['Transaction','User'])

    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            year = st.selectbox('**Select Year**',   ('2018','2019','2020','2021'),key='year')
        with col2:
            quarter = st.selectbox('**Select Quarter**',('1','2','3','4'),key='quarter')
        with col3:
            type = st.selectbox('**Select Type**',('Recharge & bill payments','Financial Services','Merchant payments','Peer-to-peer payments'),key='type')
        with col4:
            state = ["nagaland","punjab","chhattisgarh","gujarat","jammu-&-kashmir","goa","arunachal-pradesh","kerala","delhi","tamil-nadu","puducherry","haryana","lakshadweep","dadra-&-nagar-haveli-&-daman-&-diu","maharashtra","assam","uttar-pradesh","manipur","odisha","uttarakhand","tripura","karnataka","andaman-&-nicobar-islands","chandigarh","jharkhand","himachal-pradesh","andhra-pradesh","rajasthan","madhya-pradesh","west-bengal","telangana","mizoram","ladakh","bihar","meghalaya","sikkim"]
            states = st.selectbox('**Select state**',state,key='states')


        cursor.execute(f"select state, transaction_amount from agg_tra where year='{year}' and quarter='{quarter}' and transaction_type='{type}'  group by state, transaction_amount order by transaction_amount DESC limit 10 ")
        result = cursor.fetchall()
        df_result = pd.DataFrame(result,columns=['state','transaction_amount'] )
        # pie_chart = px.pie(df_result, values='transaction_amount', names='state', title='phonepay')
        # st.write(pie_chart)
        # st.header(result[0][0].upper())
        st.write(df_result)
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            agg_usr_year = st.selectbox('**Select Year**',   ('2018','2019','2020','2021'),key='agg_usr_year')
        with col2:
            agg_usr_quarter = st.selectbox('**Select Quarter**',('1','2','3','4'),key='agg_usr_quarter')
        
        cursor.execute(f"select state, brands,user_count,user_percentage from agg_user where year='{agg_usr_year}' and quarter='{agg_usr_quarter}'")
        agg_usr_result = cursor.fetchall()
        df_result = pd.DataFrame(agg_usr_result,columns=['state','brands','user_count','user_percentage'] )
        # pie_chart = px.pie(df_result, values='transaction_amount', names='state', title='phonepay')
        st.write(df_result)

cursor.close()
connection.close()