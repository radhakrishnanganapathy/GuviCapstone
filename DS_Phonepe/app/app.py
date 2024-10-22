import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import requests
# name = st.text_input("name")

file_path = r'Z:\radhakrishnan\DS_Phonepe\data\top\transaction\country\india\2018\1.json'
file_2019 = r'Z:\radhakrishnan\DS_Phonepe\data\top\transaction\country\india\2019\1.json'
git_file = 'https://github.com/radhakrishnanganapathy/DS_Phonepe/blob/main/data/top/transaction/country/india/2018/1.json'

year = st.sidebar.selectbox('select' , [file_path,file_2019,git_file])
# response = requests.get(git_file)
with open(year, 'r') as json_file:
     json_data = json.load(json_file)

# json_data = response.json()
# st.write(json_data.keys())
data = json_data.get("data",{})
df_states = data.get("states", [])
# Flatten the nested structure
flattened_data = [{'entityName': item['entityName'], **item['metric']} for item in df_states]

# print(flattened_data)

df = pd.DataFrame(flattened_data)
select = ['fig','scatter_fig','pie_chart','scatter_3d','funnel','bar','box','density_heatmap','line_3d','density_mapbox','bar_polar','violin']
dropdown = st.sidebar.selectbox('select',select)

if 'fig' == dropdown:
     fig = px.bar(df, x='entityName' , y='amount', text='amount', title='Amount by EntityName')
     fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
     fig.update_layout(xaxis_title='EntityName', yaxis_title='Amount')
     st.plotly_chart(fig)

if 'scatter_fig' == dropdown:
     scatter_fig = px.scatter(df, x='entityName' , y='amount',)
     st.write(scatter_fig)

if 'pie_chart' == dropdown:
     pie_chart = px.pie(df, values='amount', names='entityName', title='phonepay')
     st.write(pie_chart)

if 'scatter_3d' == dropdown:
     scatter_3d = px.scatter_3d(df,x='entityName',y='amount',z='count', title= 'scatter_3d')
     st.write(scatter_3d)

if 'funnel' == dropdown:
     funnel = px.funnel(df,x='entityName', y='amount')
     st.write(funnel)

if 'bar' == dropdown:
     bar = px.bar(df,x='entityName', y='amount')
     st.write(bar)

if 'box' == dropdown:
     box = px.box(df,x='entityName', y='amount', title='box')
     st.write(box)

if 'line' == dropdown:
     line = px.line(df,x='amount', y='count')
     line.update_traces(line_color='purple')
     st.write(line)

if 'density_heatmap' == dropdown:
     density_heatmap = px.density_heatmap(df,x='entityName',y='amount')
     st.write(density_heatmap)

if 'line_3d' == dropdown:
     line_3d = px.line_3d(df,x='entityName',y='amount', z='count')
     st.write(line_3d)

if 'density_mapbox' == dropdown:
     density_mapbox = px.strip(df,x='entityName',y='amount')
     st.write(density_mapbox)

if 'bar_polar' == dropdown:
     bar_polar = px.bar_polar(df,r='entityName',theta='amount')
     st.write(bar_polar)

if 'violin' == dropdown:
     violin = px.violin(df,x='entityName',y='amount', title='violin')
     violin.update_layout(title='Violin Plot Example', xaxis_title='Entity Name', yaxis_title='Amount')
     violin.update_traces(marker=dict(color='blue'), line=dict(color='black'))
     violin.add_violin(x=df['entityName'], y=df['amount']*1.1, line_color='red', side='positive', name='Additional Violin')
     violin.update_xaxes(title_text='Entity Name', tickangle=45)
     violin.update_yaxes(title_text='Amount', showgrid=True)
     violin.update_coloraxes(colorbar_title='Color Scale', colorbar_tickvals=[0, 1, 2], colorbar_ticktext=['Low', 'Medium', 'High'])
     # violin.update_traces(color='green')
     st.write(violin)

if 'line_ternary' == dropdown:
     line_ternary = px.line_ternary(df,a='entityName',b='amount', title='sunburst')
     st.write(line_ternary)

if 'go_pie' == dropdown:
     go_pie = go.Figure(data=[go.Pie(labels=df['entityName'],
                                   values=df['amount'],
                                   )])
     # go_pie.update_layout(title='pie')
     st.write(go_pie)

attribute = dir(go)
for i in attribute:
     print(i)
print('```````````````````````')


