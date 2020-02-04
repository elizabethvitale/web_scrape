import requests
from getpass import getpass
from bs4 import BeautifulSoup
import os.path
from os import path
import csv
import time

count = []
sysdescr = []
name = input("USERNAME:")
password = getpass("PASSWORD:")

if not (path.exists("encoded_data.html")):
    r = requests.get('https://edgehealth.cox.com/index.php?body=verreport.php', auth=(name, password),verify=False)
    print(r.status_code)
    if(r.status_code == 401):
        exit(1)
    f = open("encoded_data.html", "wb")
    f.write(r.content)
    f.close()

with open('datasheet.csv', 'w', newline='') as csv_file:
    pass

z = open("encoded_data.html", "r")
soup = BeautifulSoup(z, 'html5lib')
tablesData = soup.select('table.stickyHeader tr')
for data in tablesData:
    time.sleep(1)
    d = data.find_all('font')
    try:
        count.append(d[0].text)
        ip_addr = '' 
        link = d[1].find('a')
        url  = link['href']
        url2 = 'https://edgehealth.cox.com/index.php' + url
        print(url2) 
        r2 = requests.get(url2, auth=(name,password),verify=False, stream=True, timeout=None)
        print(r2.status_code)
        
        for line in r2.iter_lines():
            
            if("<td nowrap align=left id=report><font color=><a href='?body=ping.php&ip_address=".encode() in line):
                line = line.decode()
                ending = line.find("</a")
                beginning = line.find("'>")
                result = line[beginning+2:ending]
                print(result)
                ip_addr = result
                break
                
        sysdescr.append(d[2].text)
        print(ip_addr)
        with open('datasheet.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([d[0].text, d[2].text, ip_addr])
    except Exception as e:
        print('failed')
        print(e)
            
    



