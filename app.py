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
        password="123456789",
        database="eventdn",
        
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
    
    Your database consists of two tables: `speakers` and `events`.
    
    The `speakers` table has the following columns:
    - speaker_id (Primary Key)
    - speaker_name
    - event_id (Foreign Key referencing event_id in the `events` table)
    
    The `events` table has the following columns:
    - event_id (Primary Key)
    - event_name \n\n For example,\nExample 1: How many speakers are there for the event "Tech Expo 2023"?
    The SQL command will be something like this SELECT COUNT(*) FROM speakers WHERE  event_name = 'Tech Expo 2023';
    \nExample 2: List all speakers for the event "Global Business Forum".
    The SQL command will be something like this SELECT s.speaker_name FROM speakers s JOIN events e ON s.event_id = e.event_id WHERE e.event_name = 'Global Business Forum';
    
    also the sql code should not have ``` in beginning or end and sql word in output
    """
]


# prompt=[
#     """
#     You are an expert in converting English questions to SQL query!
#     The SQL database has the name Event and has the following columns - NAME, DESCRIPTION, 
#     SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
#     the SQL command will be something like this SELECT COUNT(*) FROM Event ;
#     \nExample 2 - Tell me  the Event Description happening in Conference 2024?, 
#     the SQL command will be something like this SELECT * FROM Event 
#     where Name="Conference 2024"; 
#     also the sql code should not have ``` in beginning or end and sql word in output
#     """
# ]


#Streamlit app
st.set_page_config(page_title="I can Retrieve Any SQL query");
st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input",key="input")
submit = st.button("Ask the question")

#if submit is clicked

# if submit:
#     response = get_gemini_response(question,prompt)
#     print(response)
#     response = read_sql_query(response,"eventdatabase.db")
#     st.subheader("The Response is")
#     for row in response:
#         print(row)
#         st.header(row)

if submit:
    response = get_gemini_response(question, prompt)
    print(response)
    response = execute_sql_query(response)
    st.subheader("The Response is")
    for row in response:
        print(row)
        st.write(row)  # Write each row to the Streamlit app

