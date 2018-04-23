import time
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
from sys import platform
import requests
import pymongo
from bson.json_util import dumps
from dateutil import parser
import pytz
import pandas as pd


def init_browser():
    if platform == "darwin":
        executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    else:
        executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    # create mars_data dict that we can insert into mongo
    mars_data = {}
    # get mars news
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204%3A19&blank_scope=Latest"
    browser.visit(url)
    time.sleep(7)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    article_list = soup.find_all("li", class_='slide')
    news_title = article_list[0].find('div', class_='content_title').text
    news_p = article_list[0].find('div', class_='article_teaser_body').text
    mars_data['news_title'] = news_title
    mars_data['news_p'] = news_p

    # get mars photo
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(7)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image = soup.find("a", class_='button fancybox')
    featured_image = image['data-fancybox-href']
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image
    mars_data['featured_image_url'] = featured_image_url
   
    #get mars weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(7)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    weather_list = soup.find("div", {'id':'timeline'})
    mars_weather = weather_list.find('p', class_='tweet-text').text
    mars_data['mars_weather'] = mars_weather

    #get mars facts
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    time.sleep(7)
    df = tables[0]
    df.columns = ['Profile', 'Stat']
    df.set_index('Profile', inplace=True)
    html_table = df.to_html()
    html_table = html_table.replace('\n', '')
    mars_data['mars_facts'] = html_table

    return mars_data




