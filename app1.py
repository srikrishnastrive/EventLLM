#Invoice Extractor

from dotenv import load_dotenv

load_dotenv() # it will take all environment varibales from .env
import streamlit as st
import os
import sqlite3
import google.generativeai as genai


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

def read_sql_query(sql,db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

##defining the prompt

prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name Event and has the following columns - NAME, DESCRIPTION, 
    SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM Event ;
    \nExample 2 - Tell me  the Event Description happening in Conference 2024?, 
    the SQL command will be something like this SELECT * FROM Event 
    where Name="Conference 2024"; 
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
    response = get_gemini_response(question,prompt)
    print(response)
    response = read_sql_query(response,"eventdatabase.db")
    st.subheader("The Response is")
    for row in response:
        print(row)
        st.header(row)


