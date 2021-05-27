import streamlit as st
import pandas as pd

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
