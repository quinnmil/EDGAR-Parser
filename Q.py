import urllib.request
import re
import csv
from bs4 import BeautifulSoup



BASE_URL = "https://www.sec.gov"
# cik = input()
cik = "1678226"
fullURL = "https://www.sec.gov/cgi-bin/browse-edgar?CIK=0001166559&Find=Search&owner=exclude&action=getcompany"
url = "https://www.sec.gov/cgi-bin/browse-edgar?CIK=" + cik + "&Find=Search&owner=exclude&action=getcompany"



results =[]

def getInput():
    # get cik number from user
    print ("Please enter CIK Number: ")
    cik = input();
    return cik


def getXML(cik):

    # Open results page
    url = "https://www.sec.gov/cgi-bin/browse-edgar?CIK=" + cik + "&Find=Search&owner=exclude&action=getcompany"
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page,'html.parser')

    # select result table
    table = soup.find('table', summary="Results")
    # return xml file to open 

    filling = None
    for row in table.find_all_next("tr"): # rows on page
        cell = row.find_all('td')
        if (cell):
            # print (cell[0].text)
            # print(type(cell[0]))
            # print (cell[0], "-----", cell[1])
            # TODO: deal with situation where this isn't found
            if "13F" in cell[0].text:
                # print(cell[0])
                filling = cell[1].find('a')['href']
                # right now, just pulls the first (most recent) filing
                # could append to results list. 
                break
        continue

    if (filling == None):
        print("sorry, no 13F filings found for this CIK")
        return

    page.close()
    # print("filling = ",filling)
    fillingDetail = BASE_URL+filling

    page = urllib.request.urlopen(fillingDetail);

    soup = BeautifulSoup(page,'html.parser')
    # print(soup.prettify())
    xmlLink = None
    links = soup.find_all('a')
    for link in links: 
        # print(link.get('href'))
        if ("informationtable.xml" in link.text) and (".html" not in link.get('href')):
            # print ('this is the one', link)
            xmlLink = BASE_URL +link.get('href');

    if xmlLink:
        return xmlLink
    print ('No xml file found')
    return

def parseXML(xml):
    
    file = urllib.request.urlopen(xml)

    soup = BeautifulSoup(file, 'xml')
    # print(soup.prettify())

    with open('outputFile.tsv', 'w') as out_file:

        tsv_writer = csv.writer(out_file, delimiter='\t')
        infoTables = soup.find_all('infoTable')
        # print(infoTables)
        for t in infoTables:
            name = t.nameOfIssuer.text
            titleOfClass = t.titleOfClass.text
            cisip = t.cusip.text
            row = [name, titleOfClass, cisip]
            tsv_writer.writerow(row);

    





def main():
    cik = getInput()
    if cik:
        xml = getXML(cik)
        if xml:
            parseXML(xml)
    
    return 

# Google capital CIK=1678226
# gates foundation 0001166559


if __name__ == "__main__":
    main()
