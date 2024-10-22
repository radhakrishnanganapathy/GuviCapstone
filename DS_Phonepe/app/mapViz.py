import psycopg2
import pandas as pd
import plotly.express as px
import json
import streamlit as st

# Database connection details
mydb = {
    'host': 'localhost',
    'database': 'guvi',
    'user': 'postgres',
    'password': 'ags009',
    'port': '5432'
}

# Connect to the database
connection = psycopg2.connect(**mydb)
cursor = connection.cursor()
st.sidebar.title("menu")
# Fetch transaction data from the database
query = """
SELECT state, SUM(transaction_amount) as transaction_amount 
FROM agg_tra 
WHERE year='2021' AND quarter=1 AND transaction_type='Financial Services' 
GROUP BY state 
ORDER BY transaction_amount DESC 
LIMIT 30
"""
cursor.execute(query)
result = cursor.fetchall()
transactions = pd.DataFrame(result, columns=['state', 'transaction_amount'])
transactions.head(5)

# Load the GeoJSON file
india_states = json.load(open("../data/states_india.geojson", "r"))

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
missing_ids = transactions[transactions["id"].isnull()]
if not missing_ids.empty:
    st.write("Missing IDs for the following states:")
    st.write(missing_ids)

fig = px.choropleth(
    transactions,
    locations="id",
    geojson=india_states,
    color="transaction_amount",
    hover_name="state",
    hover_data=["transaction_amount"],
    title="Financial Services Transactions by State in Q1 2021",
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
st.title("Financial Services Transactions by State in Q1 2021")

# Display the Plotly figure in Streamlit
st.plotly_chart(fig, use_container_width=True)
cursor.close()
connection.close()