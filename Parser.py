# EDGAR Fund Parser
# Solution to coding challenge from Quovo
# Author: Quinn Milionis
# 5-13-19

## IMPORTS ##
import urllib.request
import csv
from bs4 import BeautifulSoup

## GLOBALS ##
BASE_URL = "https://www.sec.gov"


## CORE FUNCTIONS ##

def getXML(cik):
    ''' Takes a cik number and returns a link an 13F filing and name of fund. 
    '''
    # Open results page
    url = "https://www.sec.gov/cgi-bin/browse-edgar?CIK=" + cik + "&Find=Search&owner=exclude&action=getcompany"
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page,'html.parser')

    # select result table
    table = soup.find('table', summary="Results")

    if table is None: 
        print("No luck with that CIK, sorry!")
        return

    # check each row in table for "13F" filing
    filling = None
    for row in table.find_all_next("tr"): # rows on page
        cell = row.find_all('td')
        if (cell):
                # right now, always pull the first (most recent) 13F filing. 
                if "13F" in cell[0].text:
                    filling = cell[1].find('a')['href']
                break
        continue

    if (filling == None):
        print("sorry, no 13F filings found for this CIK")
        return

    page.close()

    # Filling Detail page lists versions of the 13F filling. 
    fillingDetail = BASE_URL+filling
    page = urllib.request.urlopen(fillingDetail)
    soup = BeautifulSoup(page,'html.parser')
    
    # Gets the name of fund from this page, used to title output file. 
    name = soup.find('span', attrs={'class' : 'companyName'}).text[:15]

    # find linkt to xml file. 
    xmlLink = None
    links = soup.find_all('a')
    for link in links: 
        if ("informationtable.xml" in link.text) and (".html" not in link.get('href')):
            xmlLink = BASE_URL +link.get('href')

    if xmlLink:
        return xmlLink, name
    print ('No xml file found')
    return


def parseXML(xml, name):
    ''' Takes link to 13F xml file and parses into tsv file.
    @args: 
        xml: link to xml file (string)
        name: name of fund (string)
    '''
    
    file = urllib.request.urlopen(xml)

    # Lots of options for parsing XML, but BS supports lxml, 
    # which is faster than the builtin python etree parser. 
    soup = BeautifulSoup(file, 'xml')
    # print(soup.prettify())
    fileName = name +'.tsv'
    with open(fileName, 'w') as out_file:

        tsv_writer = csv.writer(out_file, delimiter='\t')
        
        infoTables = soup.find_all('infoTable')

        # parses and writes headers 
        headers = []
        for h in infoTables[0].find_all():
            headers.append(h.name)
        tsv_writer.writerow(headers)

        # parses and writes row content
        for t in infoTables:
            row = []
            child = t.find_all()
            for t in child:
                row.append(t.text)
            tsv_writer.writerow(row)
            
    print("Success. Fund holding written to ", fileName)
    return 
        
def main():
    ''' Get CIK number for user and writes fund holdings to .tsv file
    '''
    print ("Please enter CIK Number: ")
    cik = input()
    if cik:
        xml, name = getXML(cik)
        if xml:
            parseXML(xml, name)
    # If program was unable to either get input, or return a link to the xml file, return
    return 

# 0001166559 - BILL & MELINDA GATES FOUNDATION TRUST

if __name__ == "__main__":
    main()