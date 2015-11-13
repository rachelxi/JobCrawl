# This program is written to crawl the job position webs (TradeMe Jobs)
# And extract position information and give statistics for jobs available on certain day
# Statistics also include: total of the jobs available, words occurrence by frequency
# 1st Edited: 2015-11-12 17:00:00 GMT+12
# 2nd Edited: 2015-11-13 19:37:00 GMT+12

import requests
from bs4 import BeautifulSoup
from datetime import *

# Two files one to write the positions and link information; one to put statistics
file_name1 = 'Job_List.txt'
file_name2 = 'Words_Stats.txt'
file_content1 = 'Time and Date Produced:' + str(datetime.now()) + '\n'
file_content2 = 'Time and Date Produced:' + str(datetime.now()) + '\n'

def job_spider(max_pages):
# Extract information from every page, give statistics of mostly occurred words in title
# and append recommended job list
    global file_content1,file_content2
    
    page = 1
    numlist = list()
    words = ''
    countsum = dict()
    recommend = dict()
    
# first url to search for the IT jobs and second url to search for engineering jobs
# Trade Me Jobs change key on url everyday please remember to refresh every day
    while page <= max_pages:
        url = """http://www.trademe.co.nz/browse/categoryattributesearchresults.aspx?
        cid=5000&search=1&nofilters=1&originalsidebar=1&rptpath=5000-&key=1299137359&page="""+str(page)+"&sort_order=jobs_default"
        #url = """http://www.trademe.co.nz/browse/categoryattributesearchresults.aspx?
        #cid=5000&search=1&nofilters=1&originalsidebar=1&key=1299146246&page="""+str(page)+"&sort_order=jobs_default&rptpath=5000-5056-"
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text,"html.parser")
        list_soup = soup.findAll('li', {'class':'JobCardDetailsColumn'})
        countpp = 0
        
# Delete special characters in job title for further processing; filters to delete 
# unwanted jobs; whitelist to include more jobs mostly likely to fit in; calculate
# the number of positions for each page
        for info in list_soup:
            title = info.find('div',{'class':'jobCardListingTitle'})
            position0 = title.text.strip().replace("/"," ").replace("-","")
            position1 = position0.replace("(","").replace(")","").replace(",","")
            position = position1.replace("|","").replace("&","").replace("!","")
            words += ' ' + position
            match = position.split()
            filters = ["Senior","Manager","Lead","Director","Solution","Intermediate","Experienced"]
            whitelist = ["Graduate","GRADUATE","Junior"] 
            if not list(set(filters) & set(match)):          
                href = "http://www.trademe.co.nz"+title.find('a').get('href')
                countpp += 1
                file_content1 += "\n%d.\t%s\n%s" % (countpp,position,href)
                if list(set(whitelist) & set(match)):
                    recommend[position]=href
        print("Page number:%d, Jobs Available:%d" % (page,countpp))
        file_content1 += "\nPage number:%d, Jobs Available:%d\n" % (page,countpp)
        numlist.append(countpp)
        page += 1

# Counts the occurrence frequency for different words in job title
    words = words.split()
    for word in words:
        countsum[word] = countsum.get(word,0)+1
    countsum = sorted([(v,k) for k,v in countsum.items()],reverse=True)
    for k,v in countsum:
        file_content2 += "\n%d\t%s" % (k,v)
# Calculate the total available jobs
    print("Total Jobs Available:",sum(numlist))
    file_content1 += "\nTotal Jobs Available:%d" % sum(numlist)
# Append the recommended job list
    file_content1 += "\n\nRecommended Jobs List:"
    for k,v in recommend.items():
        file_content1 += "\n\t%s\n%s" % (k,v)
   
pages = input("Enter pages to fetch:")
job_spider(int(pages))
# Write to files
f1 = open(file_name1,'w')
f1.write(file_content1)
f1.close()
f2 = open(file_name2,'w')
f2.write(file_content2)
f2.close()
