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

``

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
        
``

