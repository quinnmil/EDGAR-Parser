import urllib.request
import re
from bs4 import BeautifulSoup

# Google capital CIK=1678226


BASE_URL = "https://www.sec.gov"
# cik = input()
cik = "1678226"
fullURL = "https://www.sec.gov/cgi-bin/browse-edgar?CIK=0001166559&Find=Search&owner=exclude&action=getcompany"
url = "https://www.sec.gov/cgi-bin/browse-edgar?CIK=" + cik + "&Find=Search&owner=exclude&action=getcompany"


results =[]
page = urllib.request.urlopen(url)

soup = BeautifulSoup(page,'html.parser')

# selects table
table = soup.find('table', summary="Results")

def getInput():
    # get cik number from user
    print ("Please enter CIK Number: ")
    cik = input();

def getXML(cik):
    # return xml file to open 
    return 0
# print(table)

filling = None
for row in table.findAll("tr" ,attrs={'class': 'blueRow'}): # rows on page
    cell = row.find_all('td')
    # print (cell[0], "-----", cell[1])
    # TODO: deal with situation where this isn't found
    if "13F" in cell[0]:
        filling = cell[1].find('a')['href']
        # right now, just pulls the first (most recent) filing
        # could append to results list. 
        break;

if (filling == None):
    print("sorry, no 13F filings found")
    # exit function

page.close()

fillingDetail = BASE_URL+filling

page = urllib.request.urlopen(fillingDetail);

soup = BeautifulSoup(page,'html.parser')
# print(soup.prettify())

xmlLink = soup.find('a', href=re.compile(".xml"))

print(xmlLink)





    # link = cell.find('a', id="documentsbutton")
    # print(cell)
    # first_column = row.find_all('td')[0]
    # print (first_column)
    # children = row.findChildren('td') 
    # for c in children:
    #     if "13F-HR" in c:
    #         print (c)
