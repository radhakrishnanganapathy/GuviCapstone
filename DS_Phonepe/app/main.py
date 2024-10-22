import streamlit as st
import pandas as pd
import plotly.express as px
import json
import psycopg2

def phonepe_main():
     st.header(':violet[Phonepe Pluse]')
     def db_connection():
          mydb = {
     'host': 'localhost',
     'database': 'guvi',
     'user': 'postgres',
     'password': 'ags009',
     'port': '5432'
          }
          connection = psycopg2.connect(**mydb)
          return connection     

     st.markdown(
     """
     <style>
     .sidebar-title-india {
          display: block;
          padding: 10px 20px;
          background-color: #007bff; /* Background color */
          color: white; /* Text color */
          font-size: 16px; /* Font size */
          border-radius: 5px; /* Rounded corners */
          text-align: center; /* Centered text */
          font-weight: bold; /* Bold text */
          margin-bottom: 10px; /* Space below */
     }
     .sidebar-title {
          font-size: 24px;
          font-weight: bold;
          color: green;
          padding: 10px 0;
          text-align: left;
     }
     
     </style>
     """,
     unsafe_allow_html=True
     )
     type, quoter, year = st.columns(3)


     st.sidebar.markdown('<div class="sidebar-title-india">All India</div>', unsafe_allow_html=True)

     def side_bar_tarr(year_drop,quoter_drop):
          conn = db_connection()
          cur = conn.cursor()
          tarr_query = f"select sum(transaction_amount) as amount from agg_tra where year = '{year_drop}' and quarter = '{quoter_drop}' "
          cur.execute(tarr_query)
          amt = cur.fetchone()[0]
          st.sidebar.write(f'All PhonePe transactions on **{year_drop}-Q{quoter_drop}**')
          # st.sidebar.title(f'₹ {amt}')
          st.sidebar.markdown(f'<div class="sidebar-title">{amt} Cr</div>', unsafe_allow_html=True)
          return amt


     def side_bar_user(year_drop,quoter_drop):
          conn = db_connection()
          cur = conn.cursor()
          user_query = f"select sum(user_count) as user from agg_user where year = '{year_drop}' and quarter = '{quoter_drop}' "
          cur.execute(user_query)
          user = cur.fetchone()[0]
          st.sidebar.write(f'No.of User created in phonepe on **{year_drop}-Q{quoter_drop}**')
          st.sidebar.markdown(f'<div class="sidebar-title">{user} users</div>', unsafe_allow_html=True)
          return user

     def top_states(year_drop,quoter_drop):
          conn = db_connection()
          cur = conn.cursor()
          top_query = f"select state, round(sum(transaction_amount)::numeric/10000000,2) as amt from agg_tra where year = '{year_drop}' and quarter = '{quoter_drop}' group by state order by amt desc limit 10 "
          cur.execute(top_query)
          top = cur.fetchall()
          df = pd.DataFrame(top, columns=['state','Amt in cr'])
          # st.sidebar.write(f'No.of User created in phonepe on **{year_drop}-Q{quoter_drop}**')
          st.sidebar.dataframe(df)
          return df

     def top_district(year_drop,quoter_drop):
          conn = db_connection()
          cur = conn.cursor()
          top_query = f"select district, round(sum(amount)::numeric/10000000,2) as amt from top_tra where year = '{year_drop}' and quarter = '{quoter_drop}' group by district order by amt desc limit 10 "
          cur.execute(top_query)
          top = cur.fetchall()
          df = pd.DataFrame(top, columns=['district','Amt in cr'])
          # st.sidebar.write(f'No.of User created in phonepe on **{year_drop}-Q{quoter_drop}**')
          st.sidebar.dataframe(df)
          return df

     def top_postaalcode(year_drop,quoter_drop):
          conn = db_connection()
          cur = conn.cursor()
          top_query = f"select pincode, round(sum(amount)::numeric/10000000,2) as amt from top_tra where year = '{year_drop}' and quarter = '{quoter_drop}' group by pincode order by amt desc limit 10 "
          cur.execute(top_query)
          top = cur.fetchall()
          df = pd.DataFrame(top, columns=['district','Amt in cr'])
          # st.sidebar.write(f'No.of User created in phonepe on **{year_drop}-Q{quoter_drop}**')
          st.sidebar.dataframe(df)
          return df

     def user_top_states(year_drop,quoter_drop):
          conn = db_connection()
          cur = conn.cursor()
          top_query = f"select state, sum(user_count) as users from agg_user where year = '{year_drop}' and quarter = '{quoter_drop}' group by state order by users desc limit 10 "
          cur.execute(top_query)
          top = cur.fetchall()
          df = pd.DataFrame(top, columns=['state','users'])
          # st.sidebar.write(f'No.of User created in phonepe on **{year_drop}-Q{quoter_drop}**')
          st.sidebar.dataframe(df)
          return df

     def user_top_district(year_drop,quoter_drop):
          conn = db_connection()
          cur = conn.cursor()
          top_query = f"select district, sum(registereduser) as users from top_usr where year = '{year_drop}' and quarter = '{quoter_drop}' group by district order by users desc limit 10 "
          cur.execute(top_query)
          top = cur.fetchall()
          df = pd.DataFrame(top, columns=['district','users'])
          # st.sidebar.write(f'No.of User created in phonepe on **{year_drop}-Q{quoter_drop}**')
          st.sidebar.dataframe(df)
          return df

     def user_top_postalcode(year_drop,quoter_drop):
          conn = db_connection()
          cur = conn.cursor()
          top_query = f"select pincode, sum(registereduser) as users from top_usr where year = '{year_drop}' and quarter = '{quoter_drop}' group by pincode order by users desc limit 10 "
          cur.execute(top_query)
          top = cur.fetchall()
          df = pd.DataFrame(top, columns=['district','users'])
          # st.sidebar.write(f'No.of User created in phonepe on **{year_drop}-Q{quoter_drop}**')
          st.sidebar.dataframe(df)
          return df

     def transaction_type(year_drop,quoter_drop):
          conn = db_connection()
          cur = conn.cursor()
          top_query = f"select transaction_type, round(sum(transaction_amount)::numeric/10000000,2) as amt from agg_tra where year = '{year_drop}' and quarter = '{quoter_drop}' group by transaction_type order by amt desc limit 10 "
          cur.execute(top_query)
          top = cur.fetchall()
          df = pd.DataFrame(top, columns=['catagories','amt in cr'])
          # st.sidebar.write(f'No.of User created in phonepe on **{year_drop}-Q{quoter_drop}**')
          st.sidebar.write(df)
          return df

     with type:
          
          type_drop = st.selectbox('Select Type',("transaction","user"))
          st.sidebar.title(type_drop.upper())

     with year:
          year_drop = st.selectbox('Select Year',('2018','2019','2020','2021'))

     with quoter:
          quoter_drop = st.selectbox('Select Qutor',('1','2','3','4'))

     def indian_map_tra(year_drop,quoter_drop):
          conn = db_connection()
          cur = conn.cursor()
          query = f"""
          SELECT state, SUM(transaction_amount) as transaction_amount 
          FROM agg_tra 
          WHERE year='{year_drop}' AND quarter={quoter_drop}  
          GROUP BY state 
          ORDER BY transaction_amount DESC 
          LIMIT 30
          """
          cur.execute(query)
          result = cur.fetchall()
          transactions = pd.DataFrame(result, columns=['state', 'transaction_amount'])
          transactions.head(5)

          # Load the GeoJSON file
          india_states = json.load(open("DS_Phonepe/data/states_india.geojson", "r"))

          # Prepare a state ID map for matching
          state_id_map = {}
          for feature in india_states["features"]:
               feature["id"] = feature["properties"]["state_code"]
               if feature["properties"]["st_nm"].upper() == 'ARUNANCHAL PRADESH':
                    state_id_map['ARUNACHAL PRADESH'] = feature["id"]
               elif feature["properties"]["st_nm"].upper() == 'NCT OF DELHI':
                    state_id_map['DELHI'] = feature["id"]
               else:
                    state_id_map[feature["properties"]["st_nm"].upper()] = feature["id"]

          # Add the state IDs to the transaction DataFrame
          transactions["state"] = transactions['state'].str.replace('-', ' ').str.upper()
          transactions["id"] = transactions["state"].apply(lambda x: state_id_map.get(x.upper(), None))

          # Check for any missing IDs
          # missing_ids = transactions[transactions["id"].isnull()]
          # if not missing_ids.empty:
          #      st.write("Missing IDs for the following states:")
          #      st.write(missing_ids)

          fig = px.choropleth(
          transactions,
          locations="id",
          geojson=india_states,
          color="transaction_amount",
          hover_name="state",
          hover_data=["transaction_amount"],
          # title=f"Transactions by State in {quoter_drop} {year_drop}",
          width=1000,  # Set the width of the plot
          height=700   # Set the height of the plot
          )

          # Customize the layout and lock the zoom level
          fig.update_geos(
          fitbounds="locations",
          visible=False,
          center={"lat": 20.5937, "lon": 78.9629},  # Center of India
          projection=dict(scale=5)  # Adjust the scale to zoom in or out
          )



          fig.update_layout(
          autosize=False,
          height=700,
          margin={"r":0, "t":50, "l":0, "b":0},
          #     paper_bgcolor='rgb(233,233,233)',  # Set the background color
          geo=dict(
               lakecolor='rgb(255, 255, 255)',
               projection_scale=5  # Adjust the projection scale for zoom level
          )
          )

          # st.set_page_config(layout="wide")  # Set layout to wide for better viewing
          st.title(f"Transactions by State in {quoter_drop}Q- {year_drop}")

          # Display the Plotly figure in Streamlit
          st.plotly_chart(fig, use_container_width=True)
          return "map"

     def indian_map_user(year_drop,quoter_drop):
          conn = db_connection()
          cur = conn.cursor()
          query = f"""
          SELECT state, SUM(user_count) as user
          FROM agg_user 
          WHERE year='{year_drop}' AND quarter={quoter_drop}  
          GROUP BY state 
          ORDER BY user DESC 
          LIMIT 30
          """
          cur.execute(query)
          result = cur.fetchall()
          users = pd.DataFrame(result, columns=['state', 'user'])

          # Load the GeoJSON file
          india_states = json.load(open("DS_Phonepe/data/states_india.geojson", "r"))

          # Prepare a state ID map for matching
          state_id_map = {}
          for feature in india_states["features"]:
               feature["id"] = feature["properties"]["state_code"]
               if feature["properties"]["st_nm"].upper() == 'ARUNANCHAL PRADESH':
                    state_id_map['ARUNACHAL PRADESH'] = feature["id"]
               elif feature["properties"]["st_nm"].upper() == 'NCT OF DELHI':
                    state_id_map['DELHI'] = feature["id"]
               else:
                    state_id_map[feature["properties"]["st_nm"].upper()] = feature["id"]

          # Add the state IDs to the transaction DataFrame
          users["state"] = users['state'].str.replace('-', ' ').str.upper()
          users["id"] = users["state"].apply(lambda x: state_id_map.get(x.upper(), None))

          # Check for any missing IDs
          # missing_ids = transactions[transactions["id"].isnull()]
          # if not missing_ids.empty:
          #      st.write("Missing IDs for the following states:")
          #      st.write(missing_ids)

          fig = px.choropleth(
          users,
          locations="id",
          geojson=india_states,
          color="user",
          hover_name="state",
          hover_data=["user"],
          # title=f"Transactions by State in {quoter_drop} {year_drop}",
          width=1000,  # Set the width of the plot
          height=700   # Set the height of the plot
          )

          # Customize the layout and lock the zoom level
          fig.update_geos(
          fitbounds="locations",
          visible=False,
          center={"lat": 20.5937, "lon": 78.9629},  # Center of India
          projection=dict(scale=5)  # Adjust the scale to zoom in or out
          )



          fig.update_layout(
          autosize=False,
          height=700,
          margin={"r":0, "t":50, "l":0, "b":0},
          #     paper_bgcolor='rgb(233,233,233)',  # Set the background color
          geo=dict(
               lakecolor='rgb(255, 255, 255)',
               projection_scale=5  # Adjust the projection scale for zoom level
          )
          )

          # st.set_page_config(layout="wide")  # Set layout to wide for better viewing
          st.title(f"users by State in {quoter_drop}Q- {year_drop}")

          # Display the Plotly figure in Streamlit
          st.plotly_chart(fig, use_container_width=True)
          return "map"

     def pie_chart_tra(year_drop,quoter_drop):
          conn = db_connection()
          cur = conn.cursor()
          query = f"select state, round(sum(transaction_amount)::numeric/10000000,2) as amt from agg_tra where year = '{year_drop}' and quarter = {quoter_drop} group by state order by amt desc limit 20"
          cur.execute(query)
          data = cur.fetchall()
          df = pd.DataFrame(data, columns=['state','amt'])
          pie_chart = px.pie(df, values=df['amt'],names=df['state'],title=f'Top 20 States Transactions in Q{quoter_drop}-{year_drop}')
          st.write(pie_chart)
          return df

     def tra_query(year_drop,quoter_drop):
          conn = db_connection()
          cur = conn.cursor()
          query = f"select state, round(sum(transaction_amount)::numeric/10000000,2) as amt from agg_tra where year = '{year_drop}' and quarter = {quoter_drop} group by state order by amt desc limit 20"
          cur.execute(query)
          data = cur.fetchall()
          df = pd.DataFrame(data, columns=['state','amt'])
          return df

     def user_query(year_drop,quoter_drop):
          conn = db_connection()
          cur = conn.cursor()
          query = f"select state, sum(user_count) as users from agg_user where year = '{year_drop}' and quarter = {quoter_drop} group by state order by users desc limit 20"
          cur.execute(query)
          data = cur.fetchall()
          df = pd.DataFrame(data, columns=['state','users'])
          return df

     def pie_chart_usr(year_drop,quoter_drop):
          conn = db_connection()
          cur = conn.cursor()
          query = f"select state, sum(user_count) as users from agg_user where year = '{year_drop}' and quarter = {quoter_drop} group by state order by users desc limit 20"
          cur.execute(query)
          data = cur.fetchall()
          df = pd.DataFrame(data, columns=['state','users'])
          pie_chart = px.pie(df, values=df['users'],names=df['state'],title=f'Top 20 States Users in Q{quoter_drop}-{year_drop}')
          st.write(pie_chart)
          return df

     def bar_tar(year_drop,quoter_drop):
          df = tra_query(year_drop,quoter_drop)
          bar_chart = px.bar(
               df, y='amt', x='state', 
               title=f'Top 20 States Transactions in Q{quoter_drop}-{year_drop}',
               color='amt')
          bar_chart.update_layout(
     title={'text': f'Top 20 States Transactions in Q{quoter_drop}-{year_drop}', 'x': 0.5},
     xaxis_title='State',
     yaxis_title='Transaction Amount (in Crores)',
     yaxis_tickformat=',.2f',  # Format y-axis ticks
     yaxis=dict(tickangle=-45),  # Rotate y-axis ticks
     plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
     paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
     font=dict(
          family='Arial, sans-serif',
          size=12,
          color='Black'
     )
     )
          st.write(bar_chart)
          return bar_chart

     def bar_usr(year_drop,quoter_drop):
          df = user_query(year_drop,quoter_drop)
          bar_chart = px.bar(
               df, y='users', x='state', 
               title=f'Top 20 States Users in Q{quoter_drop}-{year_drop}',
               color='users')
          bar_chart.update_layout(
     title={'text': f'Top 20 States Users in Q{quoter_drop}-{year_drop}', 'x': 0.5},
     xaxis_title='State',
     yaxis_title='Transaction Users ',
     yaxis_tickformat=',.2f',  # Format y-axis ticks
     yaxis=dict(tickangle=-45),  # Rotate y-axis ticks
     plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
     paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
     font=dict(
          family='Arial, sans-serif',
          size=12,
          color='Black'
     )
     )
          st.write(bar_chart)
          return bar_chart

     tab1, tab2, tab3 = st.tabs(['Indian Map', 'Pie chart','Bar Grapth'])
     with tab1:
          if type_drop == 'transaction':
               indian_map_tra(year_drop,quoter_drop)
          else:
               indian_map_user(year_drop,quoter_drop)
     with tab2:
          if type_drop == 'transaction':
               pie_chart_tra(year_drop,quoter_drop)
          else:
               pie_chart_usr(year_drop,quoter_drop)

     with tab3:
          if type_drop == 'transaction':
               bar_tar(year_drop,quoter_drop)
          else:
               bar_usr(year_drop,quoter_drop)
                    
     if type_drop == 'transaction':
          amt = side_bar_tarr(year_drop,quoter_drop)
     else:
          user = side_bar_user(year_drop,quoter_drop)

     transaction_type(year_drop,quoter_drop)

     # tab = st.sidebar.tabs(['States','Districts','PostalCode'])
     option = st.sidebar.radio(' ',('States','Districts','Postal'),horizontal=True)


     if option == 'States' and type_drop == 'transaction':
          top_states(year_drop,quoter_drop)
     elif option ==  'Districts' and type_drop == 'transaction':
          top_district(year_drop,quoter_drop)
     elif option == 'Postal' and type_drop == 'transaction':
          top_postaalcode(year_drop,quoter_drop)
     elif option == 'States' and type_drop == 'user':
          user_top_states(year_drop,quoter_drop)
     elif option ==  'Districts' and type_drop == 'user':
          user_top_district(year_drop,quoter_drop)
     elif option == 'Postal' and type_drop == 'user':
          user_top_postalcode(year_drop,quoter_drop)
     else:
          pass

          

