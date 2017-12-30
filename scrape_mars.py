import time
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver

def scrape():
    def init_browser():
    executable_path = {"executable_path": 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)
    #-------------------------MARS NEWS-----------------------------
    # initialize browser
    browser = init_browser()
    
    #create blank dictionary for returns
    mars_news = {}
    
    # set the url and visit
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)
    
    html = browser.html
    soup = BeautifulSoup(html, "lxml")
    
    mars_news["news_title"] = soup.find("div", class_="content_title").next_element.get_text()
    mars_news["news_p"] = soup.find("div", class_="article_teaser_body").get_text()

    #-------------------------Featured Image-----------------------------
    browser = init_browser()
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    
    browser.visit(url)
    time.sleep(1)
    
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    image = soup.find('a', class_='button fancybox')
    featured_image_url = "https://www.jpl.nasa.gov" + image["data-fancybox-href"]

    #-------------------------MARS WEATHER-----------------------------
    browser = init_browser()
    url = "https://twitter.com/marswxreport?lang=en"
    
    browser.visit(url)
    time.sleep(1)
    
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    
    weather = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    
    for i in weather:
        j = i.text.split()
        if j[0] != "Sol":
            continue
        else:
            mars_weather = i.text
            break

    #-------------------------MARS FACTS-----------------------------
    url = "https://space-facts.com/mars/"
    
    mars_table = pd.read_html(url)

    #-------------------------MARS HEMISPHERES-----------------------------
    browser = init_browser()
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    base_url = "https://astrogeology.usgs.gov"

    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    url_list = []
    title_list =[]
    jpg_url_list =[]
    hemisphere_image_urls = []

    results = soup.find('div', class_="collapsible results")
    links = results.find_all('a', class_="item product-item")
    titles= results.find_all('h3')

    for link in links:
        url_list.append(base_url+link["href"])
        
    for title in titles:
        title_list.append(title.text)
        
    for item in url_list:
        browser.visit(item)
        time.sleep(1)
        
        html = browser.html
        soup = BeautifulSoup(html, 'lxml')
        
        downloads = soup.find('div', class_="downloads")
        jpg = downloads.find_all('a')
        jpg_url = jpg[0]["href"]
        jpg_url_list.append(jpg_url)
        

    for i in range(0,len(title_list)):
        hemisphere_image_urls.append({"title": title_list[i], "img_url": jpg_url_list[i]})

    #------------------CREATE SINGLE DICTIONARY WITH ALL DATA---------------
    scraped_data = {}

    scraped_data["news"] = mars_news
    scraped_data["feat_img"] = featured_image_url
    scraped_data["weather"] = mars_weather
    scraped_data["facts"] = mars_table
    scraped_data["hemispheres"] = hemisphere_image_urls

    return scraped_data