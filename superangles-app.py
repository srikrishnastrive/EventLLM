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
    
    Your database consists of two tables: `1_live_career_counseling_sessions_speaker`,`1_live_career_counseling_sessions`,`1_contactus`,`1_sessions_speaker_mapping`,`1_exhibitor_gallery`,`1_event_master`.
    
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

    The `1_live_career_counseling_sessions` table has the follwing colums:
    - lccs_id
    - aem_id
    - lccs_type
    - lccs_name
    - lccs_sub_title
    - lccs_speaker_name
    - lccs_moderator_pic
    - lccs_moderator_name
    - lccs_moderator_designation
    - lccs_moderator_desc
    - lccs_host_pic
    - lccs_host_designation: varchar(255) DEFAULT NULL
    - lccs_host_desc: varchar(255) DEFAULT NULL
    - lccs_start_datewtime_for_showlive: datetime DEFAULT NULL
    - lccs_start_datewtime: datetime DEFAULT NULL
    - lccs_end_datewtime: datetime DEFAULT NULL
    - lccs_zoom_id: varchar(255) DEFAULT NULL
    - lccs_zoom_pwd: varchar(120) DEFAULT NULL
    - lcss_room_id: varchar(255) DEFAULT NULL
    - lccs_live_status: enum('live','yet_to_start','finished') NOT NULL DEFAULT 'yet_to_start'
    - lccs_past_session_video_url: varchar(255) DEFAULT NULL
    - lccs_orderby: int(11) DEFAULT NULL
    - lccs_status: enum('active','inactive') DEFAULT 'active'
    - lccss_meeting_id: longtext NOT NULL
    - lccss_meeting_room_name: longtext NOT NULL
    - lccss_meeting_url: longtext NOT NULL

    

    The `1_sessions_speaker_mapping` table has the following colums:
    -  ssm_id
    -  lccs_id
    -  lccss_id
    -  ssm_status
  
    
    
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
    \nExample 3: List all the speakers of Opening Ceremony?.
    The SQL command will be something like this SELECT s.lccss_name FROM 1_live_career_counseling_sessions ses JOIN 1_sessions_speaker_mapping map ON ses.lccs_id = map.lccs_id JOIN 1_live_career_counseling_sessions_speaker s ON map.lccss_id = s.lccss_id WHERE ses.lccs_name = 'Opening Ceremony';
    /nExample 4: List all the sessions of Ashneer Grover.
    The SQL command will be something like this: SELECT ses.lccs_name FROM 1_live_career_counseling_sessions ses JOIN 1_sessions_speaker_mapping map ON ses.lccs_id = map.lccs_id JOIN 1_live_career_counseling_sessions_speaker s ON map.lccss_id = s.lccss_id WHERE s.lccss_name = 'Ashneer Grover';
    \nExample 5: List all exhibitor of superangles summit?.
    The SQL command will be something like this SELECT eg_name,eg_caption,eg_status FROM 1_exhibitor_gallery;
    \nExample 6: List all the  events?.
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

