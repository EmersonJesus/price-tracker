from bs4 import BeautifulSoup
from selenium import webdriver
import time
import smtplib
import email.message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

driver = webdriver.Firefox()

url = "https://www.amazon.com.br/dp/B091G767YB/"

driver.get(url)