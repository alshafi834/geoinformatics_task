#import necessary packages
import os
import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime

url = 'https://howis.eglv.de/pegel/html/uebersicht_internet.php' # define the URL
response = requests.get(url) # sending the request to the url
soup = BeautifulSoup(response.content, 'html.parser') # scrapping the html content with beautifulsoup

tooltip_divs = soup.select('div.tooltip') # selecting all the div with class 'tooltip'
tooltip_heads = [] # defining an array
id_counter = 1 # defining a counter flag

# looping through the tooltip divs
for div in tooltip_divs:
    tooltip_head = div.select_one('.tooltip-head').text.replace('\n', '') # removing whitespace
    tooltip_head_data = ['s'+str(id_counter), tooltip_head, datetime.now().strftime('%Y-%m-%d %H:%M:%S')] # pushing sid, name and date into the array
    tooltip_values = div.select('td.tooltip-value') # selecting the tooltip values
    # looping over the tooltip values
    for i, value in enumerate(tooltip_values):
        if i == 0:
            tooltip_head_data.append('w') # if it's first index, then push 'w' as a param
            trimmedValue = value.text.replace('\xa0', '') # clearing the value
            if trimmedValue.isdigit():
                tooltip_head_data.append(trimmedValue) # pushing only if it's not empty
                tooltip_heads.append(tooltip_head_data) # pushing into the main array
    id_counter += 1 # increasing the counter
 
id_counter = 1 # Resetting the counter
# Repeating the same procedure to extract discharge values 'q'
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

filename = '/Users/aalshafi/GeoInformatics/finalassignment/periodic_data.csv' # define the file name with the path
file_exists = os.path.isfile(filename) # Check if the file exists

# Write the data to a CSV file
with open(filename, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    if not file_exists:  # Check if the file exists and if not, write the header row
        writer.writerow(['sid', 'place', 'timestamp', 'param', 'value']) # write the csv header
    for item in tooltip_heads:
        writer.writerow(item)
