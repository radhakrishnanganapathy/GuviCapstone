import psycopg2
import pandas as pd

parms = {
     "dbname" : "rkrish_db",
     "user" : "radhakrishnan",
     "password" :"weJyKwjSj60UNzr4MXIEZ79FV7sf2ZHY",
     "host" : "dpg-coiuro5jm4es739v1hvg-a.oregon-postgres.render.com",
     "port" : 5432

}

con = psycopg2.connect(**parms)
cursor = con.cursor()

if con:
     print("successfully connected")
else:
     print("error")

channel = '''select * from channel'''
cursor.execute(channel)
ch = cursor.fetchall()
col1 = [col[0] for col in cursor.description]
ch_df = pd.DataFrame(ch,columns=col1)
ch_df.to_json('channel.json', index=False)

videos = '''select * from videos'''
cursor.execute(videos)
vd = cursor.fetchall()
col = [col[0] for col in cursor.description]
vd_df = pd.DataFrame(vd,columns=col)
vd_df.to_json('videos.json', index=False)

comments = '''select * from comments'''
cursor.execute(comments)
com = cursor.fetchall()
col1 = [col[0] for col in cursor.description]
co_df = pd.DataFrame(com,columns=col1)
co_df.to_json('comments.json', index=False)

playlist = '''select * from playlist'''
cursor.execute(playlist)
pl = cursor.fetchall()
col1 = [col[0] for col in cursor.description]
pl_df = pd.DataFrame(pl,columns=col1)
pl_df.to_json('playlist.json', index=False)

cursor.close()
con.close()

print("success")