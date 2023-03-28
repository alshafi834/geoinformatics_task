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

# for div in tooltip_divs:
#     tooltip_head = div.select_one('.tooltip-head').text.replace('\n', '')
#     tooltip_head_data = ['s'+str(id_counter), tooltip_head, datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
#     tooltip_values = div.select('td.tooltip-value')
#     for value in tooltip_values:
#         tooltip_head_data.append(value.text.replace('\xa0', ''))
#     tooltip_heads.append(tooltip_head_data)
#     id_counter += 1

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
