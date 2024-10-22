import pandas as pd
import os
import json

import psycopg2

import streamlit as st


def data_processing():
    '''                      Aggregated . Transaction                          '''

    path_1 = "Z:/radhakrishnan/DS_Phonepe/data/aggregated/transaction/country/india/state/"
    Agg_tran_state_list = os.listdir(path_1)

    Agg_tra = {'State': [], 'Year': [], 'Quarter': [], 'Transaction_type': [], 'Transaction_count': [], 'Transaction_amount': []}

    for i in Agg_tran_state_list:
        p_i = path_1 + i + "/"
        Agg_yr = os.listdir(p_i)
    #     print(Agg_yr)

        for j in Agg_yr:
            p_j = p_i + j + "/"
            agg_yr_list = os.listdir(p_j)

            for k in agg_yr_list:
                p_k = p_j + k
                data = open(p_k,'r')
                a = json.load(data)

                for l in a['data']['transactionData']:
                    name = l['name']
                    count = l['paymentInstruments'][0]['count']
                    amount = l['paymentInstruments'][0]['amount']
                    Agg_tra['State'].append(i)
                    Agg_tra['Year'].append(j)
                    Agg_tra['Quarter'].append(int(k.strip('.json')))
                    Agg_tra['Transaction_type'].append(name)
                    Agg_tra['Transaction_count'].append(count)
                    Agg_tra['Transaction_amount'].append(amount)

    df_aggregated_transaction = pd.DataFrame(Agg_tra)
    st.write(df_aggregated_transaction)

    '''                                   Aggregated . User                                '''

    agg_usr_path = "Z:/radhakrishnan/DS_Phonepe/data/aggregated/user/country/india/state/"
    agg_usr_year_list = os.listdir(agg_usr_path)

    agg_user = {'State':[],'Year':[],'Quarter' :[],'Brands':[],'user_count':[],'User_percentage':[]}

    for i in agg_usr_year_list:
        p_i = agg_usr_path + i + '/'
        usr_state = os.listdir(p_i)

        for j in usr_state:
            p_j = p_i + j + '/'
            user_year = os.listdir(p_j)
        
            for k in user_year:
                p_k = p_j + k
                data = open(p_k, 'r')
                b = json.load(data)

                user_device = b["data"].get("usersByDevice")
                if user_device is not None and isinstance(user_device, list):
                    for l in user_device:
                        brand_name = l["brand"]
                        count_ =l["count"]
                        all_percentage = l["percentage"]
                        agg_user['State'].append(i)
                        agg_user['Year'].append(j)
                        agg_user['Quarter'].append(int(k.strip('.json')))
                        agg_user['Brands'].append(brand_name)
                        agg_user['user_count'].append(count_)
                        agg_user['User_percentage'].append(all_percentage)
    df_aggregated_user = pd.DataFrame(agg_user)
    st.write(df_aggregated_user)


    '''                                   map . Transaction                                '''
    map_transaction_path = "Z:/radhakrishnan/DS_Phonepe/data/map/transaction/hover/country/india/state/"
    map_tra_year_list = os.listdir(map_transaction_path)

    map_transaction = {'State' : [],"Year":[],"Quarter":[],"Name":[],"count":[],"amount":[]}

    for i in map_tra_year_list:
        p_i = map_transaction_path + i + '/'
        state_list = os.listdir(p_i)

        for j in state_list:
            p_j = p_i + j + "/"
            year_list = os.listdir(p_j)

            for k in year_list:
                p_k = p_j + k
                data = open(p_k,'r')
                c =  json.load(data)

                for l in c["data"]["hoverDataList"]:
                    name = l["name"]
                    count = l["metric"][0]["count"]
                    amount = l["metric"][0]["amount"]
                    map_transaction['Name'].append(name)
                    map_transaction['State'].append(i)
                    map_transaction['Year'].append(j)
                    map_transaction['Quarter'].append(int(k.strip('.json')))
                    map_transaction["count"].append(count)
                    map_transaction["amount"].append(amount)
    df_map_transaction = pd.DataFrame(map_transaction)
    st.write(df_map_transaction)

    '''                                   map . User                                '''

    map_user_path = "Z:/radhakrishnan/DS_Phonepe/data/map/user/hover/country/india/state/"
    # sql connect
    map_user = {"State":[],"Year":[],"Quarter":[], "district":[],"registeredUsers":[]}
    map_user_state_list = os.listdir(map_user_path)

    for i in map_user_state_list:
        p_i = map_user_path + i + "/"
        state_list = os.listdir(p_i)

        for j in state_list:
            p_j = p_i + j + "/"
            year_list = os.listdir(p_j)

            for k in year_list:
                p_k = p_j + k
                data = open(p_k , 'r')
                d = json.load(data)

                for l in d["data"]["hoverData"]:
                    map_user["State"].append(i)
                    map_user["Year"].append(j)
                    map_user["Quarter"].append(int(k.strip('.json')))
                    map_user["district"].append(l)
                    reg_user = d["data"]["hoverData"][l]["registeredUsers"]
                    map_user["registeredUsers"].append(reg_user)

    df_map_user = pd.DataFrame(map_user)
    st.write(df_map_user)

    '''                                   Top . Transaction                                '''
    top_transaction_path = "Z:/radhakrishnan/DS_Phonepe/data/top/transaction/country/india/state/"
    topTransaction = {"State":[],"Year":[],"Quarter":[],"districts":[],"pincodes":[],"count":[],"amount":[]}

    top_tra_state_list = os.listdir(top_transaction_path)

    for i in top_tra_state_list:
        p_i = top_transaction_path + i + "/"
        state_list = os.listdir(p_i)

        for j in state_list:
            p_j = p_i + j + "/"
            year_list = os.listdir(p_j)

            for k in year_list:
                p_k = p_j + k
                data = open(p_k,'r')
                e = json.load(data)

                if e["data"]["districts"]:
                    for districts in e["data"]["districts"]:
                        district = districts["entityName"]
                        count_ = districts['metric']['count']
                        amt = districts['metric']['amount']
                        topTransaction["State"].append(i)
                        topTransaction["Year"].append(j)
                        topTransaction["Quarter"].append(int(k.strip('.json')))
                        topTransaction["districts"].append(district)
                        topTransaction["count"].append(count_)
                        topTransaction["amount"].append(amt)
                        topTransaction["pincodes"].append(None)

                if e["data"]["pincodes"]:
                    for pincodes in e["data"]["pincodes"]:
                        pincode = pincodes["entityName"]
                        count_ = pincodes['metric']['count']
                        amt = pincodes['metric']['amount']
                        topTransaction["State"].append(i)
                        topTransaction["Year"].append(j)
                        topTransaction["Quarter"].append(int(k.strip('.json')))
                        topTransaction["districts"].append(None)
                        topTransaction["count"].append(count_)
                        topTransaction["amount"].append(amt)
                        topTransaction["pincodes"].append(pincode)

    df_top_transaction  = pd.DataFrame(topTransaction)
    st.write(df_top_transaction)

    '''                                   Top . User                                '''
    top_user_path = "Z:/radhakrishnan/DS_Phonepe/data/top/user/country/india/state/"
    topUser = {"State":[],"Year":[],"Quarter":[],"districts":[],"pincodes":[],"registeredUsers":[]}

    top_user_state_list = os.listdir(top_user_path)

    for i in top_user_state_list:
        p_i = top_user_path + i + "/"
        state_list = os.listdir(p_i)

        for j in state_list:
            p_j = p_i + j + "/"
            year_list = os.listdir(p_j)

            for k in year_list:
                p_k = p_j + k
                data = open(p_k,'r')
                e = json.load(data)

                if e["data"]["districts"]:
                    for districts in e["data"]["districts"]:
                        district = districts["name"]
                        registeredUsers = districts['registeredUsers']
                        topUser["State"].append(i)
                        topUser["Year"].append(j)
                        topUser["Quarter"].append(int(k.strip('.json')))
                        topUser["districts"].append(district)
                        topUser["registeredUsers"].append(registeredUsers)
                        topUser["pincodes"].append(None)

                if e["data"]["pincodes"]:
                    for pincodes in e["data"]["pincodes"]:
                        pincode = pincodes["name"]
                        registeredUsers = pincodes['registeredUsers']
                        topUser["State"].append(i)
                        topUser["Year"].append(j)
                        topUser["Quarter"].append(int(k.strip('.json')))
                        topUser["districts"].append(None)
                        topUser["registeredUsers"].append(registeredUsers)
                        topUser["pincodes"].append(pincode)

    df_top_user  = pd.DataFrame(topUser)
    st.write(df_top_user)

                        


    mydb = {
        'host' : 'localhost',
        'database' : 'guvi',
        'user' :'postgres',
        'password' : 'ags009',
        'port' : '5432'

    }

    # mydb = {

    # 'host' : 'dpg-cmmvudocmk4c73e4qfh0-a.oregon-postgres.render.com',
    # 'database' : 'guvi_yby8',
    # 'user' :'guvi_yby8_user',
    # 'password' : 'MFyUGk2fbpvmiRZ8FaXIBt56uXD9eMWc',
    # 'port' : '5432'
    # }

    connection = psycopg2.connect(**mydb)

    cursor = connection.cursor()

    create_table_query = '''
        CREATE TABLE IF NOT EXISTS agg_tra (
            id SERIAL PRIMARY KEY,
            State VARCHAR(255),
            Year VARCHAR(255),
            Quarter INT,
            Transaction_type VARCHAR(255),
            Transaction_count INT,
            Transaction_amount FLOAT
        );
    '''
    cursor.execute(create_table_query)
    insert_data_query = '''
        INSERT INTO agg_tra (State, Year, Quarter, Transaction_type, Transaction_count, Transaction_amount) VALUES (%s, %s, %s, %s, %s, %s);
    '''
    data_to_insert = [
        tuple(row) for row in df_aggregated_transaction.values
    ]

    cursor.executemany(insert_data_query, data_to_insert)
    connection.commit()

    create_table_agg_user = '''
        CREATE TABLE IF NOT EXISTS agg_user (
            id SERIAL PRIMARY KEY,
            State VARCHAR(255),
            Year INT,
            Quarter INT,
            Brands VARCHAR(255),
            user_count INT,
            user_percentage FLOAT
        );
    '''
    cursor.execute(create_table_agg_user)
    insert_user_agg_query = '''
        INSERT INTO agg_user (State, Year, Quarter,Brands, user_count, user_percentage) VALUES (%s,%s, %s, %s, %s, %s);
    '''
    data_to_insert_tr_us = [
        tuple(row) for row in df_aggregated_user.values
    ]

    cursor.executemany(insert_user_agg_query, data_to_insert_tr_us)

    connection.commit()


    create_table_map_tra = '''
        CREATE TABLE IF NOT EXISTS map_tra (
            id SERIAL PRIMARY KEY,
            State VARCHAR(255),
            Year INT,
            Quarter INT,
            name VARCHAR(255),
            count INT,
            amount FLOAT
        );
    '''
    cursor.execute(create_table_map_tra)
    insert_map_tra_query = '''
        INSERT INTO map_tra (State, Year, Quarter,name, count, amount) VALUES (%s,%s, %s, %s, %s, %s);
    '''
    data_to_insert_map_tra = [
        tuple(row) for row in df_map_transaction.values
    ]

    cursor.executemany(insert_map_tra_query, data_to_insert_map_tra)

    connection.commit()


    create_table_map_usr = '''
        CREATE TABLE IF NOT EXISTS map_usr (
            id SERIAL PRIMARY KEY,
            State VARCHAR(255),
            Year INT,
            Quarter INT,
            district VARCHAR(255),
            count INT,
            registereduser FLOAT
        );
    '''
    cursor.execute(create_table_map_usr)
    insert_map_usr_query = '''
        INSERT INTO map_usr (State, Year, Quarter,district,registereduser ) VALUES (%s, %s, %s, %s, %s);
    '''
    data_to_insert_map_usr = [
        tuple(row) for row in df_map_user.values
    ]

    cursor.executemany(insert_map_usr_query, data_to_insert_map_usr)

    connection.commit()



    create_table_top_tra = '''
        CREATE TABLE IF NOT EXISTS top_tra (
            id SERIAL PRIMARY KEY,
            State VARCHAR(255),
            Year INT,
            Quarter INT,
            district VARCHAR(255),
            pincode VARCHAR(225),
            count INT,
            amount FLOAT
        );
    '''
    cursor.execute(create_table_top_tra)
    insert_top_tra_query = '''
        INSERT INTO top_tra (State, Year, Quarter,district,pincode, count, amount) VALUES (%s,%s,%s, %s, %s, %s, %s);
    '''
    data_to_insert_top_tra = [
        tuple(row) for row in df_top_transaction.values
    ]

    cursor.executemany(insert_top_tra_query, data_to_insert_top_tra)

    connection.commit()


    create_table_top_usr = '''
        CREATE TABLE IF NOT EXISTS top_usr (
            id SERIAL PRIMARY KEY,
            State VARCHAR(255),
            Year INT,
            Quarter INT,
            district VARCHAR(255),
            pincode VARCHAR(225),
            registereduser FLOAT
        );
    '''
    cursor.execute(create_table_top_usr)
    insert_top_usr_query = '''
        INSERT INTO top_usr (State, Year, Quarter,district,pincode,registereduser ) VALUES (%s,%s, %s, %s, %s, %s);
    '''
    data_to_insert_top_usr = [
        tuple(row) for row in df_top_user.values
    ]

    cursor.executemany(insert_top_usr_query, data_to_insert_top_usr)

    connection.commit()


    cursor.close()
    connection.close()

