# This program is written to crawl the job position webs (TradeMe Jobs)
# And extract position information and give statistics for jobs available on certain day
# Statistics also include: total of the jobs available, words occurrence by frequency
# Last Edited: 2015-11-12 17:00:00 GMT+12

import requests
from bs4 import BeautifulSoup

def job_spider(max_pages):
    page = 1
    numlist = list()
    words = ''
    countsum = dict()
    
# first url to search for the IT jobs and second url to search for engineering jobs
    while page <= max_pages:
        #url = "http://www.trademe.co.nz/browse/categoryattributesearchresults.aspx?cid=5000&search=1&nofilters=1&originalsidebar=1&rptpath=5000-&key=1296886198&page="+str(page)+"&sort_order=jobs_default"
        url = "http://www.trademe.co.nz/browse/categoryattributesearchresults.aspx?cid=5000&search=1&nofilters=1&originalsidebar=1&key=1297305918&page="+str(page)+"&sort_order=jobs_default&rptpath=5000-5056-"
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text,"html.parser")
        list_soup = soup.findAll('li', {'class':'JobCardDetailsColumn'})
        print(len(list_soup))
        countpp = 0
        
        for info in list_soup:
            title = info.find('div',{'class':'jobCardListingTitle'})
            position = title.text.strip()
            words = words + ' ' + position
            match = position.split()
            filters = ["Senior","Manager","Lead","Director","Solution","Intermediate","Experienced"] 
            if not list(set(filters) & set(match)):          
                print(position) 
                href = title.find('a').get('href')
                print("http://www.trademe.co.nz"+href)
                countpp += 1
        print("Page number:",page,", Jobs Available:",countpp)
        numlist.append(countpp)
        page += 1

# Counts the occurrence frequency for different words 
    words = words.split()
    for word in words:
        countsum[word] = countsum.get(word,0)+1
    countsum = sorted([(v,k) for k,v in countsum.items()],reverse=True)
    for k,v in countsum:
        print(k,v)
    print("Total Jobs Available:",sum(numlist))
   

job_spider(20)
