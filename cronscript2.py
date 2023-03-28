
import pandas as pd
import psycopg2
import sqlalchemy
import os

engine = sqlalchemy.create_engine("postgresql://env_master:M123xyz@localhost/groundwater")
conn = engine.connect()
#conn = psycopg2.connect(host="localhost", database="groundwater", user="env_master", password="M123xyz")

df = pd.read_csv('periodic_data.csv')

df.to_sql('Waterlevel', con=conn, if_exists='append', index=False)

# delete all rows except the header from the CSV file
os.remove('periodic_data.csv')