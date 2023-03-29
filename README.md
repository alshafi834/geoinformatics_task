# Documentation of Geoinformatics final assignment WS2022/23

## General Idea
The general idea of this task is to scrape master data of different location along with the periodic water level(w) and discharge level(q) data and analyse it with QGIS connecting with the database.

## One time scrapping of Master data of Gauges
The one time master data of different gaues are scrapped from the eglv website. The URL example is https://howis.eglv.de/pegel/html/stammdaten_html/MO_StammdatenPegel.php?PIDVal=32. To scrape the master data of different locations PID value was changed with a loop and all the master data was scrapped from the website. Each location consists of different parameters which are described as follows:

Pegelnummer - the level number of the gauge 
Gewässer - the body of water <br />
Flusskilometer - the length scale along the river <br />
Pegelnullpunkt - referrance height of the water level measurement <br />
Einzugsgebiet - the total catchment of the river <br />
Rechtswert - easting in Gauss-Krüger co-ordinate system <br />
Hochwert - northing in Gauss-Krüger co-ordinate system <br />
MHW - Mean high water level measured in cm <br />
MW - Mean water level measured in cm <br />
MNW - Mean low water level measured in cm <br />

All these data has been scrapped from the website looping over the URL and stored into a csv file first. A script was written to scrape these data and storing this data into a postgres table afterwards. The script was written in python and run with jupyter notebook. The jupyter notebook file is also provided in this repository here. To have a quick overview of the script we are attaching it here as well.

```
import requests
from bs4 import BeautifulSoup
import geopandas as gpd
import pandas as pd
import csv

%load_ext sql
%sql postgresql://env_master:M123xyz@localhost/groundwater

base_url = r"https://howis.eglv.de/pegel/html/stammdaten_html/MO_StammdatenPegel.php?PIDVal="


with open('output.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    
# Define the column headers
column_headers = ['urlparamid', 'pegelnummer', 'gewasser', 'flusskilometer', 'pegelnullpunkt', 'einzugsgebiet', 'rechtswert', 'hochwert', 'mhw', 'mw', 'mnw']

# Write the column headers to the CSV file
writer.writerow(column_headers)

for i in range(1, 93):
url = base_url + str(i)

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
td_tags = soup.find_all('td')
td_texts = [td.text.strip() for td in td_tags]
td_texts.insert(0, i)
selected_td_texts = [td_texts[i] for i in [0, 3, 5, 7, 9, 11, 13, 15, 18, 21, 24]]
selected_td_texts = [val if val not in ("", "-") else None for val in selected_td_texts]

var1 = selected_td_texts[0]
var2 = selected_td_texts[1]
var3 = selected_td_texts[2]
var4 = selected_td_texts[3]
var5 = selected_td_texts[4]
var6 = selected_td_texts[5]
var7 = selected_td_texts[6]
var8 = selected_td_texts[7]
var9 = selected_td_texts[8]
var10 = selected_td_texts[9]
var11 = selected_td_texts[10]

if selected_td_texts[1] is not None:
    print(selected_td_texts)
    writer.writerow(selected_td_texts)

from shapely.geometry import Point
import sqlalchemy

df = pd.read_csv("output.csv")
#print(df)


gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.rechtswert, df.hochwert), crs="EPSG:31466")
print(gdf)

engine = sqlalchemy.create_engine("postgresql://env_master:M123xyz@localhost/groundwater")
conn = engine.connect()

gdf.to_postgis('Masterdata', con=conn, if_exists='append', index=False)
```

This script is able to scrape to all the master data of all location and store it to the postgres table. Before storing the data to postgres table it creates a new geom column fron the easting and northing columnt so that postgres can identify the column as a geometry column. As the easting and northing were on Gauss-Krüger coordinate system, we used EPSG 31466 to convert the coordinates.


Before running the script we have to make sure that we set up the database and the masterdata table properly. 
* To set up the database, a sql script has been written which needs to be executed first. The sql script can be found here.
* To set up the Masterdata table, another script needs to be executed which can be found here.

If we run the script after setting up the database and the table, then all the scraped data will be stored properly. To check if the data has been stored properly, we can run the sql magic query in jupyterlab notebook as follows:
```
%load_ext sql
%sql postgresql://env_master:M123xyz@localhost/groundwater
%sql select * from "Masterdata"
```


## Periodic web scraping of time series

In this exercise we have scraped the periodic time series data from the eglv website: https://howis.eglv.de/pegel/html/uebersicht_internet.php. A python script was written which is able to scrape the time series data with water level W(t) and discharge Q(t) value. This script can be run from jupyterlab notebook. The script is attached below:
```
import os
import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime

url = 'https://howis.eglv.de/pegel/html/uebersicht_internet.php'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

tooltip_divs = soup.select('div.tooltip')
tooltip_heads = []
id_counter = 1

for div in tooltip_divs:
    tooltip_head = div.select_one('.tooltip-head').text.replace('\n', '')
    tooltip_head_data = ['s'+str(id_counter), tooltip_head, datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    tooltip_values = div.select('td.tooltip-value')
    for i, value in enumerate(tooltip_values):
        if i == 0:
            tooltip_head_data.append('w')
            trimmedValue = value.text.replace('\xa0', '')
            if trimmedValue.isdigit():
                tooltip_head_data.append(trimmedValue)
                tooltip_heads.append(tooltip_head_data)
    id_counter += 1
 
id_counter = 1
for div in tooltip_divs:
    tooltip_head = div.select_one('.tooltip-head').text.replace('\n', '')
    tooltip_head_data = ['s'+str(id_counter), tooltip_head, datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    tooltip_values = div.select('td.tooltip-value')
    for i, value in enumerate(tooltip_values):
        if i == 1:
            tooltip_head_data.append('q')
            trimmedValue = value.text.replace('\xa0', '')
            if len(trimmedValue) > 2:
                tooltip_head_data.append(trimmedValue)
                tooltip_heads.append(tooltip_head_data)
    id_counter += 1

filename = '/Users/aalshafi/GeoInformatics/finalassignment/periodic_data.csv'
file_exists = os.path.isfile(filename)

# Write the data to a CSV file
with open(filename, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    if not file_exists:  # Check if the file exists and if not, write the header row
        writer.writerow(['sid', 'place', 'timestamp', 'param', 'value'])
    for item in tooltip_heads:
        writer.writerow(item)
```

To make sure that the script is run periodically, we set up a cron job with the help of crontab in macOS. Crontab allows to schedule a job in linux based machine. To set up the cronjob we have to provide the time schedule and the path of the script along with the path of the python3. We also need to put the script into a .py file and save it so that we can execute the script as a cronjob with crontab.

To open the crontab run the command:
```
crontab -e
```
It will open the crontab with VIM editor. Then pressing the key 'i', it editor will be activated to edit the content inside. After writting the command inside of the crontab file press 'esc' to deactivate the edit mode. Then type ':wq' to save and exit the crontab file. The crontab command in my machine was as follows but you might need to change the path in your machine based on the location you put the script. 
```
*/5 * * * * /Users/aalshafi/opt/anaconda3/bin/python3 /Users/aalshafi/GeoInformatics/finalassignment/cronscript.py
```
This command will run the script every five minutes and store the scraped data into a csv file called periodic_data.csv.


Now we need to upload the data into the postgres table from the csv file and delete all rows from csv file. We are following this strategy to avoid any potential data loss in the meantime. To perform this action we wrote another script which will take care of uploading the csv rows into the database and delete all the rows from the csv file. Before running the script we have to set up the postgres table by running the sql query here. After setting up the database table, if we run the below script, it will upload all the data into the database and remove the csv file. 
```
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
```

This script is also run as a cronjob every 7 minutes with the same strategy of crontab. The command we write in the crontab file should be as follows:
```
*/7 * * * * /Users/aalshafi/opt/anaconda3/bin/python3 /Users/aalshafi/GeoInformatics/finalassignment/cronscript2.py
```


## Georeference five gauge location maps
To georeferrance five gauge location we have selected five different maps of five different locations. This five maps were then georeferenced on top of another real map. The procedure of georeferencing has been described below:



## PostgreSQL / PostGIS
At first the database scheme was created. To create the database user and the database we have to execute the sql scripts. Make sure you are on the same path where the sql scripts are located.
* To create the database user run the command: `psql -U postgres -d postgres -h localhost -f 010_create_users_for_groundwater_db.sql`
* To create the database run the command: `psql -U postgres -d postgres -h localhost -f 020_create_database_groundwater_db.sql`

Now we have to create the other three tables which are Masterdata, Waterlevel, and Stations accordingly:
* To create the Masterdata table run the command: `psql -U env_master -d groundwater -h localhost -f 030_create_masterdata_table.sql`
* To create the Waterlevel table run the command: `psql -U env_master -d groundwater -h localhost -f 040_create_waterlevel_table.sql`
* To create the Stations table run the command: `psql -U env_master -d groundwater -h localhost -f 050_create_stations_tables.sql`. All the stations data were inserted manually for this table.

After creating the database tables and storing all the data into the table by running the scripts, now we can create different views to extract one parameter. 
* To get all the "w" value along with stations geom data, we can create a view with the following sql query:
``
create view v_stations_w as
select s.sid, s.geometry, s.name, m.timestamp, m.param, m.value 
from "Stations" s, "Waterlevel" m
where m.sid = s.sid and param='w';
and PARAM = 'W';
``
* To get all the "q" value along with stations geom data, we can create a view with the following sql query:
``
create view v_stations_w as
select s.sid, s.geometry, s.name, m.timestamp, m.param, m.value 
from "Stations" s, "Waterlevel" m
where m.sid = s.sid and param='w';
and PARAM = 'Q';
``
