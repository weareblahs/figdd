import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import urllib.request
import configparser
import sys
import time

# Read config
config = configparser.ConfigParser()
config.read('figdd.ini')
igch = config['IntelGraphics']['Channel']
igver = config['IntelGraphics']['Version']
igchl = config['IntelGraphics']['DownloadChangelogs']
igdl = config['IntelGraphics']['Downloader']

# Detect "Channel" property in config file then set driver name and scrape URL according to the property
if igch == "arc":
    URL = "https://www.intel.com/content/www/us/en/download/726609/intel-arc-graphics-windows-dch-driver.html"
    drivername = "Intel® Arc™ Graphics Windows DCH Driver"
elif igch == "arcbeta":
    URL = "https://www.intel.com/content/www/us/en/download/729157/intel-arc-graphics-windows-dch-driver-beta.html"
    drivername = "Intel® Arc™ Graphics Windows DCH Driver - BETA"
elif igch == "graphics":
    URL = "https://www.intel.com/content/www/us/en/download/19344/intel-graphics-windows-dch-drivers.html"
    drivername = "Intel® Graphics – Windows DCH Drivers"
elif igch == "graphicsbeta":
    URL = "https://www.intel.com/content/www/us/en/download/19387/intel-graphics-beta-windows-dch-drivers.html"
    drivername = "Intel® Graphics - BETA Windows DCH Drivers"

# Run first-time config if Channel property is 0
if igch == "0":
    print(
        '''You haven't set your preferred driver channel yet. Please select one of your preferred driver to download below:
        [1] Intel Arc A730M / A370M / A350M
        [2] Intel Arc A370M / A350M (beta)
        [3] Intel HD Graphics / Intel UHD Graphics / Intel Iris
        [4] Intel HD Graphics / Intel UHD Graphics / Intel Iris (beta)''')
    configsel = input("Please choose your selection and press ENTER: ")
    if configsel == "1":
        config.set("IntelGraphics","Channel","arc")
        with open('figdd.ini', 'w') as configfile:
            config.write(configfile)
        print('Configuration complete! Please run this script again.')
        exit()
    elif configsel == "2":
        config.set("IntelGraphics","Channel","arcbeta")
        with open('figdd.ini', 'w') as configfile:
            config.write(configfile)
        print('Configuration complete! Please run this script again.')
        exit()
    elif configsel == "3":
        config.set("IntelGraphics","Channel","graphics")
        with open('figdd.ini', 'w') as configfile:
            config.write(configfile)
        print('Configuration complete! Please run this script again.')
        exit()
    elif configsel == "4":
        config.set("IntelGraphics","Channel","graphicsbeta")
        with open('figdd.ini', 'w') as configfile:
            config.write(configfile)
        print('Configuration complete! Please run this script again.')
        exit()

# Start searching Intel website code for download URL
response = requests.get(URL)
soup = BeautifulSoup(response.content)
if igver == "exe":
    predownloadurl = soup.find("button", {"data-modal-id": "1"})
    downloadurl = str(predownloadurl["data-href"])
elif igver == "zip":
    predownloadurl = soup.find("button", {"data-modal-id": "2"})
    downloadurl = (str(predownloadurl["data-href"]))
os.system('cls')

# Get changelogs URL if DownloadChangelogs is set to 1
if igchl == "1":
    prechangelogsurl = soup.find("a", {"class": "dc-page-documentation-list__item--fixed"})
    changelogsurl = (str(prechangelogsurl["href"]))

# Filename replacement to get version number
filename = str(os.path.basename(urlparse(downloadurl).path))
fr1 = filename.replace('igfx_win_','')
version = fr1.replace('.exe','')

# Get filesize for confirmation
fileproperties = urllib.request.urlopen(downloadurl)
filesize = int(fileproperties.length)
filesize_post_calculation = str(filesize / 1024 / 1024)
final_filesize = str(filesize_post_calculation[0:6] + 'MB')

# Confirmation
print('Please confirm the download details before you proceed downloading.')
print('Driver name: ' + drivername)
print('Driver Version: ' + version)
print('Filesize: ' + final_filesize)
downloadconfirmation = input('Start download? [Y/N]: ')

# Start download process
if downloadconfirmation == "Y" or downloadconfirmation == "y":
    print("Starting download...")
    if igchl == "1":
        print("Downloading changelogs...")
        if igdl == "aria2c":
            os.system("aria2c -x 16 -s 16 " + changelogsurl)
        else:
            print('No downloader selected in config! Exiting...')
            exit()
        print("Changelog download complete!")
    print("Downloading " + drivername + " version " + version + "...")
    if igdl == "aria2c":
        os.system("aria2c -x 16 -s 16 " + downloadurl)
        print("Download complete!")
        print("You can find your driver files at the same directory where FIGDD is on. Double-click on the driver to start installing. Exiting in 5 seconds...")
        time.sleep(5000)

else:
    print("Abort download.")
    exit()