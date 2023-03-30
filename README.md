# Documentation of Geoinformatics final assignment WS2022/23

## Group members
This assignment is done by the following contributors:
* Abu Hena AL Shafi(Matriculation no: 28103): @alshafi834
* Safayet Bin Azam(Matriculation no: 28406): @prangonsafayet

## General Idea

The general idea of this task is to scrape master data of different location along with the periodic water level(w) and discharge level(q) data and analyse it with QGIS connecting with the database.

----------------------------------------------------------------------------------------------------------------------

## Exercise-1: One time scrapping of Master data of Gauges
The one time master data of different gauges are scraped from the eglv website. The URL example is https://howis.eglv.de/pegel/html/stammdaten_html/MO_StammdatenPegel.php?PIDVal=32. To scrape the master data of different locations PID value was changed with a loop and all the master data was scrapped from the website. Each location consists of different parameters which are described as follows:

**Pegelnummer** - the level number of the gauge 
**Gewässer** - the body of water <br />
**Flusskilometer** - the length scale along the river <br />
**Pegelnullpunkt** - referrance height of the water level measurement <br />
**Einzugsgebiet** - the total catchment of the river <br />
**Rechtswert** - easting in Gauss-Krüger co-ordinate system <br />
**Hochwert** - northing in Gauss-Krüger co-ordinate system <br />
**MHW** - Mean high water level measured in cm <br />
**MW** - Mean water level measured in cm <br />
**MNW** - Mean low water level measured in cm <br />

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

----------------------------------------------------------------------------------------------------------------------


## Exercise-2: Periodic web scraping of time series

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
----------------------------------------------------------------------------------------------------------------------

## Exercise-3: Georeference five gauge location maps
To georeferrance five gauge location we have selected five different maps of five different locations. This five maps were then georeferenced on top of another real map. The procedure of georeferencing has been described below:

* At first the location map was from the provided URL and from the Stammdaten, the map was selected and it was cropped accordingly to fit <br /> <img width="276" alt="image" src="https://user-images.githubusercontent.com/34316105/228907307-ae45bf8b-3787-4800-94ca-afa8ddc8f9f3.gif">

* Then on QGIS the Georeferencer option was selected frin the Layers tab on the top <br /> <img width="400" alt="image" src="https://user-images.githubusercontent.com/34316105/228908539-f22afc13-8f98-437f-854c-b75ffc30466f.png">

* From the Georeferencer window, the map was opened through the "Open Raster" option <br/> <img width="400" alt="image" src="https://user-images.githubusercontent.com/34316105/228909822-a22174e1-722b-4801-9d5e-1d1ee0c29983.png">

* In the QGIS main window the command was typed in with the longitude latitude values found in google maps. The command was 
`go lang_val lat_val`. It directed to the actual position of the desired destination on the map. <br/> <img width="400" alt="image" src="https://user-images.githubusercontent.com/34316105/228910626-c7c07241-a0dd-4dfb-b92b-ed3bdd556cae.png">

* Then on the Georeferencer window, a suitable GCP point was chosen in the raster image through the "Add Point" Option. <br/> <img width="400" alt="image" src="https://user-images.githubusercontent.com/34316105/228911252-fbc56cee-b7f5-41c3-88e0-91fc392c8e75.png"><br/><br/>This popped up a window where "From Map Canvas" was selected from the bottom left. <br/> <img width="400" alt="image" src="https://user-images.githubusercontent.com/34316105/228911641-712f4346-1f69-4fe4-8033-13c9421c85aa.png"><br/> <br/><br/>Then this point from the raster image was searched in the actual map and selected. After that "Ok" button was selected to add the GCP point entry for the raster image and the map.<br/> <br/>This process was done 20-25 times to recieve more accuracy for Georeferencing.

* After adding all the points, the "Start Geo Referencing" button was used from the Georeferencer window. <br/> <img width="400" alt="image" src="https://user-images.githubusercontent.com/34316105/228912374-84b4d376-dfe3-4342-b3d1-f9d7ce280729.png">

Inside "Transformation settings, the type of Transformation was "Thin Plain Spline" and the Target CRS was "EPSG:25832 - ETRS89 / UTM zone 32N".

* This created a layer on top of the actual map inside the QGIS main window with the rastered map on top of the Openmap and the points have been used to georeference these two maps.

<img width="600" alt="image" src="https://user-images.githubusercontent.com/34316105/228913109-52ad1265-71b4-4d07-8fa3-2510051b58f1.png">



----------------------------------------------------------------------------------------------------------------------

## Exercise-4: PostgreSQL / PostGIS
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
----------------------------------------------------------------------------------------------------------------------

## Exercise-5: QGIS
In this exercise we connected the postgres database with QGIS with the help of PostGIS. After connecting with the database, our goal is to load the data in Open Street Map and then show all the timeseries data with animation by the help of temporal controller. Here is the step by step guide to the procedure:
* At first we have to install the PostGIS extension so that QGIS can be connected with the database properly
* Then we can connect with the database with the postgis layer. In order to do that we have to go to add layer and then add postgis layer. It will open a window. We can define a new database connection clicking on the 'new' button. Then we have to provide a name, host, database name, user name and password. Also make sure then we check the 'Also list tables with no geometry' option. Now if we click on the 'ok' button and if all the credentials are okay, it will create a connection with the database. The postgis connection window should look like this: <br /> <img width="149" alt="image" src="https://user-images.githubusercontent.com/34316616/228754554-d095ab13-31d4-42a9-a8f8-8c2f96b88841.png">
* Now all the database tables and views will be loaded in QGIS. We can see those on the left menu under PostgreSQL menu: <br /> <img width="102" alt="image" src="https://user-images.githubusercontent.com/34316616/228756405-23f17223-6e29-4b0d-b292-94e311f132d8.png">
* As our geometry column was generated with Gauss-Krüger coordinate system, so we have to make sure that we change the EPSG to 31466 before creating the layer: <br /> <img width="100" alt="image" src="https://user-images.githubusercontent.com/34316616/228757009-9946c5e9-70c6-4c41-8701-4d66a702c4b8.png">
* Then if we add the Stations table to QGIS, it will appear on our project: <br /> <img width="178" alt="image" src="https://user-images.githubusercontent.com/34316616/228757685-fe32c142-4513-48e2-9fd5-08b1e0f0e80c.png">
* To show the labels for each station, we can go to properties and then labels. Then we can choose single label and choose name as a value. Then we can set the text formatting according to preferance and apply it. It should create the label for each of the stations: <br /> <img width="231" alt="image" src="https://user-images.githubusercontent.com/34316616/228758875-61b541bb-ce31-40c3-a058-7e271e355672.png"> <br /> <img width="276" alt="image" src="https://user-images.githubusercontent.com/34316616/228759114-b3dd90c1-e272-47d4-a9ed-ffd2212ad941.png">
* Now we can add open street map so that the stations are better visible on top of a map. We can add open street map by going to web from the top menu and then select openlayers plugin -> openStreetMap -> OpenStreetMap: <br /> <img width="276" alt="image" src="https://user-images.githubusercontent.com/34316616/228759916-4a62c5ef-5323-498d-9127-7fdd4feae7aa.png">
* Now we can also add the Waterlevel table as a new layer: <br /> <img width="192" alt="image" src="https://user-images.githubusercontent.com/34316616/228760647-5b21d2e1-b21a-414d-8ee3-ff353bcbaf77.png">
* Now we have to join the tables. In order to do that open the processing toolbox and search with join. Under 'Vector general' option you should find the 'join attributes by field value' option. Now we have to choose the table for input layer 1 and input layer 2 and define the table field to join. Join type should be 'create separate feature for each matching feature(one to many)'. Check the 'Discard records which could not be joined' and 'Open output file after after running algorithm' options. Now if we press 'run', it should create a new joined layer. <br /> <img width="262" alt="image" src="https://user-images.githubusercontent.com/34316616/228762316-2968099f-6338-41b2-a5e4-8a2b00543f08.png">
* Now we can uncheck the Stations layer and only use the joined layer for the next steps. At first we can set the label following the same procedure: <br /> <img width="262" alt="image" src="https://user-images.githubusercontent.com/34316616/228763423-52ee7ca7-d8cc-41ef-823f-f9452630d709.png">
* Now we have both water level (w) and discharge (q) value in our joined layer. We need to filter out only the water level (w) value so that we can show the water level in our temporal controller. To keep only the 'W' value as a param, we can filter the layer with the expression `"param" = 'w'`. The filter window should look like this: <br /> <img width="128" alt="image" src="https://user-images.githubusercontent.com/34316616/228767154-7229b3d4-d37a-46b5-a6b1-7ced5250502f.png">
* Now we can set the temporal only with the 'W' values. In order to do that we have to check the 'Dynamic temporal controller' and then select 'Single field with Date/Time' and 'Include start, include end' as conficuration and limits accordingly. The field should be 'timestamp'. Now if we apply it, the temporal should be set: <br /> <img width="125" alt="image" src="https://user-images.githubusercontent.com/34316616/228768352-6d799e47-1f6d-4008-93ae-7192583057e4.png">
* No we can set the symbology. Open the properties of the joined layer and go to 'symbology' tab. Increase the size first to make it more visible. Then we can choose 'Graduated' option. The value option should be 'value'. We can change the color and increase the classes. Mode should be equal interval. We can then classify and press 'apply'. <br /> <img width="125" alt="image" src="https://user-images.githubusercontent.com/34316616/228769718-41aecbcc-caa9-458c-98a5-8ce99759a685.png">
* We can now open the temporal controller from the view option. Go to 'panel' and select 'temporal controller'. Now press on the play button. We can now set the animation range, step and duration. Now if we play the temporal controller, it will show the water level with animation. Since the water level is not changing much, the animation doesn't look impressive enough for this case. <br /> <img width="167" alt="image" src="https://user-images.githubusercontent.com/34316616/228773997-95cb1740-f35a-4e73-98db-fc9fd7c62806.png">







