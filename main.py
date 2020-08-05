import requests
from bs4 import BeautifulSoup
import smtplib
import schedule
import time
import sys

def check_price(URL, threshold_price):
    headers= {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"}
    try:
        page= requests.get(URL,headers=headers)
    except:
        print("URL could not be accessed. Please check validity of URL")
        sys.exit()

    soup= BeautifulSoup(page.content,features="html.parser") # BeautifulSoup(page.content,"html.parser") doesn't work at times. Reason not found.
    title= soup.find(id="productTitle").get_text().strip()
    price = soup.find(id ='priceblock_dealprice').get_text()[1:].strip().replace(',','')    
    if price is None:
        price= soup.find(id="priceblock_saleprice").get_text()[1:].strip().replace(',','')
    if price is None:
        price= soup.find(id="priceblock_ourprice").get_text()[1:].strip().replace(',','')    
    if title is not None and price is not None:       
        Fprice= float(price)
        if (Fprice<threshold_price):
            alert_me(URL,title,price)

def alert_me(URL,title,price):
    server= smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo();
    server.starttls()
    server.ehlo()
    server.login('YOUR_EMAIL_name','GOOGLE_APP_PASSWORD') #will need to authorize Google to allow non-secure apps and obtain Google App Password for this script to run on YOUR_EMAIL
    subject= 'Price fell down for '+ title
    body= 'Buy it now here: '+URL
    msg= f"Subject:{subject}\n\n{body}"
    server.sendmail("YOUR_EMAIL","TO_EMAIL",msg)
    print('Email alert sent')
    server.quit()



URL= input("Enter URL of the Amazon product page to be monitored: ")
threshold_price= float(input("Enter product price below which email alert is to be sent: "))
def job():
    check_price(URL,threshold_price)
job()
schedule.every(1).hour.do(job)
while (True):
    schedule.run_pending()
    time.sleep(2)
    
    
    
