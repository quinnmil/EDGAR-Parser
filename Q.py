# EDGAR Fund Parser
# Solution to coding challenge from Quovo
# Author: Quinn Milionis
# 5-13-19


## IMPORTS ##
import urllib.request
import re
import csv
from bs4 import BeautifulSoup

## GLOBALS ##
BASE_URL = "https://www.sec.gov"

# fullURL = "https://www.sec.gov/cgi-bin/browse-edgar?CIK=0001166559&Find=Search&owner=exclude&action=getcompany"


## CORE FUNCTIONS ##

def getXML(cik):
    ''' Takes a cik number and returns a link an 13F filing. 
    '''
    # Open results page
    url = "https://www.sec.gov/cgi-bin/browse-edgar?CIK=" + cik + "&Find=Search&owner=exclude&action=getcompany"
    page = urllib.request.urlopen(url)

    soup = BeautifulSoup(page,'html.parser')

    # select result table
    table = soup.find('table', summary="Results")
    # return xml file to open 

    if table is None: 
        print("No luck with that CIK, sorry!")
        return


    filling = None
    for row in table.find_all_next("tr"): # rows on page
        cell = row.find_all('td')
        if (cell):
                # right now, always pulls the first (most recent) filing. 
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
    page = urllib.request.urlopen(fillingDetail);
    soup = BeautifulSoup(page,'html.parser')
    
    # Gets the name of fund from this page, used to title output file. 
    name = soup.find('span', attrs={'class' : 'companyName'}).text[:15]

    xmlLink = None
    links = soup.find_all('a')
    for link in links: 
        if ("informationtable.xml" in link.text) and (".html" not in link.get('href')):
            xmlLink = BASE_URL +link.get('href');

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
        headers = ["Name of Issuer", "Title of Class",\
            "CUSIP", "Value", "ssh Prnamt", "ssh Prnamt Type",\
            "Investment Discression", "Voting Authority - Sole",\
            "Voting Authroity - Shared"]
        tsv_writer.writerow(headers)
        for t in infoTables:
            # parse data from table
            row = []
            row.append(t.nameOfIssuer.text)
            row.append(t.titleOfClass.text)
            row.append(t.cusip.text)
            row.append(t.value.text)
            row.append(t.shrsOrPrnAmt.sshPrnamt.text)
            row.append(t.shrsOrPrnAmt.sshPrnamtType.text)
            row.append(t.investmentDiscretion.text)
            row.append(t.votingAuthority.Sole.text)
            row.append(t.votingAuthority.Shared.text)
        
            tsv_writer.writerow(row)

        
def main():

    # get cik number from user
    print ("Please enter CIK Number: ")
    cik = input();
    if cik:
        xml, name = getXML(cik)
        if xml:
            parseXML(xml, name)
    # If program was unable to either get input, or return a link to the xml file, return
    return 

# 0001166559 - BILL & MELINDA GATES FOUNDATION TRUST


if __name__ == "__main__":
    main()
