# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 00:10:49 2017

@author: krish
"""
import urllib.request as ur
from bs4 import BeautifulSoup
import pandas as pd
import sys
import datetime

# Function to scrape the data from the given url
# Require three arguments 
# 1. base url - base url of the site to scrape
# 2. start url -  url of the starting page to scrape
# 3. no_of_pages -  number of pages to scrape 

import pymysql
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='webscrape')
cursor=conn.cursor()
conn.set_charset('utf8')
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')
def main(baseurl,starturl,no_of_pages):
    page=ur.urlopen(starturl)
    soup = BeautifulSoup(page,"lxml")
    reviews = soup.findAll('div',{'class':'reviewSelector'})
    review_collection=pd.DataFrame()
    r=1
    for i in range(no_of_pages):
        for review in reviews:
            subject= review.find('span',{'class':'noQuotes'}).text
            usrname= review.find('div',{'class':'username mo'}).text
            review_content=  review.find('p',{'class':'partial_entry'}).text  
            review_time = review.find('span',{'class':'ratingDate relativeDate'}).text
            usrlocation= review.find('div',{'class':'location'})
            if(usrlocation == None):
                usrlocation=""
            else:
                usrlocation= review.find('div',{'class':'location'}).text
            now = datetime.datetime.now()
            review_id=str(now.year)+"_"+str(now.month)+"_"+str(now.day)+"_"+str(now.hour)+"_"+str(now.minute)+"_"+str(now.second)+"_"+str(now.microsecond)+"_"+str(r)
            r=r+1
            cursor.execute('''INSERT into scraped_data (subject_content, user_name,review,review_time,user_location,scrape_ID)
                  values (%s, %s, %s, %s, %s, %s)''',(subject, usrname,review_content,review_time,usrlocation,review_id))
            temp = pd.DataFrame({'subject':[subject], 'name':[usrname],'review':[review_content],'time':[review_time],'location':[usrlocation],'ID':[review_id]})
            review_collection=pd.concat([review_collection,temp])
            nextpage=soup.findAll('a',{'class':'nav next rndBtn ui_button primary taLnk'})
            url=baseurl+nextpage[0]['href']
            page=ur.urlopen(url)
            soup = BeautifulSoup(page,"lxml")
            reviews = soup.findAll('div',{'class':'reviewSelector'})
            conn.commit()
        print(i)
    return(review_collection)

if __name__ == "__main__":
    #baseurl=r'https://www.tripadvisor.com.sg'
    #starturl=r'https://www.tripadvisor.com.sg/Hotel_Review-g293974-d1604061-Reviews-White_House_Hotel_Istanbul-Istanbul.html#REVIEWS'
    #no_of_pages=20
    baseurl=sys.argv[1]
    starturl=sys.argv[2]
    no_of_pages=int(sys.argv[3])
    review_collection=main(baseurl,starturl,no_of_pages)
    conn.close()
    review_collection.to_csv("review_collection.csv",index=False)
    print("Completed")