# -*- coding: utf-8 -*-
"""

@author: Sravani
"""
def extract_data_points(job,div):
    for a in div.findAll('a',attrs={'class':'jobtitle turnstileLink'}):
        job['Title']=a['title']
    for a1 in div.findAll('a',attrs={'data-tn-element':'companyName'}):
        job['CompanyName']=a1.text.strip()
    for span in div.findAll('span',attrs={'class':'ratingsContent'}):
        job['Rating']=span.text.strip()
    for span1 in div.findAll('span',attrs={'class':'location accessible-contrast-color-location'}):
        job['Location']=span1.text.strip()
    for div1 in div.findAll('div',attrs={'class':'summary'}):
        summary=div1.text.strip()
        job['Summary']=re.sub('  +',' ',summary.replace("\n",""))
    for span2 in div.findAll('span',attrs={'class':'date'}):
        job['ate']=span2.text.strip()
    return job

def get_data_from_webpage(data_collected,soup):
    job_posts=[]
    for div in soup.findAll('div',attrs={'class':'row'}):
        job=dict()
        job=extract_data_points(job,div)
        job_posts.append(div['data-jk'])
        single_job_post_extension_url="https://www.indeed.com/viewjob?jk="+div['data-jk']
        job["Url"]=single_job_post_extension_url
        driver.get(single_job_post_extension_url)
        job_soup=BeautifulSoup(driver.page_source,"html.parser")
        for inside_div in job_soup.findAll('div',attrs={'class':'jobsearch-jobDescriptionText'}):
            details=inside_div.text.strip()[:100]+"..."
            job["Details"]=re.sub(' +',' ',details.replace("\n"," "))
        data_collected.append(job)
    return data_collected
            
def scrape_data(url_to_scrape,number_of_pages_nos):
    data_collected=[]
    for i in range(0,number_of_pages_nos):
        extension=""
        if i is not 0:
            extension="&start="+str(i*10)
            url=url_to_scrape+extension
            driver.get(url)
            soup=BeautifulSoup(driver.page_source,"html.parser")
            data_collected=get_data_from_webpage(data_collected,soup)
    return data_collected

def start_scraping(keywords,name_of_city,number_of_pages):
    BASE_URL= "https://in.indeed.com/"
    name_of_city='+'.join(name_of_city.split(' '))
    keywords='+'.join(keywords.split(' '))
    url_to_scrape=BASE_URL +"/jobs?q="+keywords+"&l="+name_of_city
    number_of_pages_nos=int(number_of_pages.strip())
    data_collected=scrape_data(url_to_scrape,number_of_pages_nos)
    data=pd.DataFrame(data_collected)
    data.to_csv("jobs.csv")

import streamlit as st
import pandas as pd
import requests
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
st.title('Job postings in Glassdoor')
st.markdown("""
         This app performs web scrap and show you details about job openinngs of your desired position
         * **Data Source:**
""")
st.sidebar.header('User Input Featurers')
Role=st.sidebar.text_input('Enter the Job Role') 
Location=st.sidebar.text_input('Preferred Location in India') 
page_count=st.sidebar.text_input('Enter No of pages') 
start_scraping(Role,Location,page_count)

df=pd.read_csv("jobs.csv")
available_job_roles=sorted(df.Title.unique())
selected_job_roles=st.sidebar.multiselect('Similar Job Roles',available_job_roles,available_job_roles)

#filtering data
df_selected_data=df[df.Title.isin(selected_job_roles)]
df_selected_data
