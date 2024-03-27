#Invoice Extractor

from dotenv import load_dotenv

load_dotenv() # it will take all environment varibales from .env
import streamlit as st
import os
import sqlite3
import google.generativeai as genai
import mysql.connector

##configuring api key
##google authenticating the key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"));

##function to load gemini Pro vision model and get response
## Load Gemini pro vision model
model=genai.GenerativeModel('gemini-pro')

def get_gemini_response(question,prompt):
    response = model.generate_content([prompt[0],question])
    return response.text

##Function to retrive the query from the database

# def read_sql_query(sql,db):
#     conn = sqlite3.connect(db)
#     cur = conn.cursor()
#     cur.execute(sql)
#     rows = cur.fetchall()
#     conn.commit()
#     conn.close()
#     for row in rows:
#         print(row)
#     return rows

def execute_sql_query(sql):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="superangles",
        
        
    )
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    connection.commit()
    connection.close()
    return rows


##defining the prompt

prompt = [
    """
    You are an expert in converting English questions to SQL queries!
    
    Your database consists of two tables: `1_live_career_counseling_sessions_speaker`,`1_contactus`,`1_exhibitor_gallery`,`1_event_master`.
    
    The `1_live_career_counseling_sessions_speaker` table has the following columns:
    - lccss_id (Primary Key)
    - lccss_name
    - lccss_email
    - lccss_company_name
    - lccss_time
    - lccss_designation
    - lccss_description
    - lccss_linkedin
    - lccss_twitter
    - lccss_instagram
    - lccss_pic
    - speaker_status
    - lccss_status
    
    The `1_contactus` table has the following columns:
    - cu_id (Primary Key)
    - First_name
    - Last_name
    - Designation
    - Email
    - Mobile
    - Message
    - DateTime

    The `1_exhibitor_gallery` table has the following colums:
    - eg_name
    - eg_caption
    - eg_status

    The `1_event_master` table has the following columns;
    - aem_event_nickname
    - aem_name
    - aem_shortname
    - aem_description
    - aem_organized_by
    - aem_full_address
    - aem_location
    - aem_location_coordinates
    - aem_live_date_time
    - aem_start_date
    - aem_end_date
    - aem_relaxation_date \n\n For example,\nExample 1: Give me the contact details?
    The SQL command will be something like this SELECT * FROM 1_contactus;
    \nExample 2: List all speakers of superangles summit?.
    The SQL command will be something like this SELECT lccss_name,lccss_company_name,lccss_description FROM 1_live_career_counseling_sessions_speaker;
    \nExample 3: List all exhibitor of superangles summit?.
    The SQL command will be something like this SELECT eg_name,eg_caption,eg_status FROM 1_exhibitor_gallery;
    \nExample 3: List all the  events?.
    The SQL command will be something like this SELECT aem_event_nickname,aem_name,aem_description FROM 1_event_master;
    

    also the sql code should not have ``` in beginning or end and sql word in output
    """
]




#Streamlit app
st.set_page_config(page_title="I can Retrieve Any SQL query");
st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input",key="input")
submit = st.button("Ask the question")

#if submit is clicked


if submit:
    response = get_gemini_response(question, prompt)
    print(response)
    response = execute_sql_query(response)
    st.subheader("The Response is")
    for row in response:
        print(row)
        st.write(row)  # Write each row to the Streamlit app

