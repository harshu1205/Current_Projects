from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import Databases as DB
from UserData import UserData
Database = DB.GetDB()

options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

st.markdown("Main page")

#If not already existing UserData
User = UserData()

def GetUserData():
    return User
def UpdateUserData(DataType, newData):
    User.UpdateData(DataType, newData)

# streamlit run C:\Users\harsh\PycharmProjects\pythonProject\main.py
