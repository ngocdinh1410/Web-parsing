# -*- coding: utf-8 -*-
"""
Spyder Editor
#BaoNgoc_Dinh_Parser
This is a temporary script file.
"""

x = 5
import requests 
import time     
import re       
from bs4 import BeautifulSoup 

# create an empty list
data  = [] 
# access the webpage as Chrome
my_headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
#run loops so it will parse thru multiple web pages.
movie="parasite_2019"
pageNum = 5

for k in range(1,pageNum+1):
    # Give the url of the page
    page = 'https://rottentomatoes.com/m/'+movie+'/reviews?type=&sort=&page='+str(k)+'' 
    # Initialize src to be False
    src  = False

    # Now get the page

    # try to scrape 5 times
    for i in range(1,6): 
        try:
            # get url content
            response = requests.get(page, headers = my_headers)
            # get the html content
            src = response.content
            # if we successuflly got the file, break the loop
            break 
        # if requests.get() threw an exception, i.e., the attempt to get the response failed
        except:
            print ('failed attempt #',i)
            # wait 2 secs before trying again
            time.sleep(2)
    # if we could not get the page 
    if not src:
       # couldnt get the page, print that we could not and continue to the next attempt
       print('Could not get page: ', page)
       # move on to the next page
       continue 
    else:
       # got the page, let the user know
       print('Successfully got page: ', page)
    soup = BeautifulSoup(src.decode('ascii', 'ignore'), 'lxml')
    #find the contents inside all the 'row review_table_row tag
    content = soup.findAll('div',{'class':re.compile('row review_table_row')})
    for stuff in content:
        # initialize to not found
        reviewer_name = 'NA'
        review_icon  = 'NA'
        review_source = 'NA'
        review_content = 'NA'
        review_date = 'NA'
        #find the content inside the appropriate tag, append them into data:
        a=stuff.find('a')
        if a:
            reviewer_name=a.text.strip()
        icon=stuff.find('div',{'class':'icon'})
        if icon:
            review_icon=icon.get('class')[-1]
        em=stuff.find('em')
        if em:
            review_source=em.text.strip()
        container=stuff.find('div',{'class':'the_review'})
        if container:
            review_content=container.text.strip()
        dates=stuff.find("div",{"class":"review-date"})
        if dates:
            review_date=dates.text.strip()
        data.append([reviewer_name, review_icon, review_source,review_content,review_date])

for article in data:
    print(article)
#create text file:
with open('baongoc_dinh_parasite_2019.txt', mode='w', encoding='utf-8') as f:
    for statement in data:
        f.write(statement[0] + '\t' + statement[1] + '\t' + statement[2] + statement[3]+'\t'+statement[4]+ '\n')
with open('baongoc_dinh_parasite_2019.txt', mode='r', encoding = 'utf-8') as f:
    data = f.read()
    
# break into lines, then break each line into article_type, aritcle_url, article_text
# throw away last element because it is simply an empty line
data = data.split('\n')[0:-1]

for i in range(0,len(data)):
    data[i] = data[i].split('\t')