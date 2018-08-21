from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import requests


def instantiate_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1420,1080')
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(r'C:\Users\thiag\Desktop\SQL-DU\day4\chromedriver', 
        chrome_options=chrome_options)
    return driver
driver = webdriver.Chrome()


def scraped():
    final_data = {}
    final_data["mars_news"] = marsNews()
    final_data["mars_image"] = marsImage()
    final_data["mars_weather"] = marsWeather()
    final_data["mars_facts"] = marsFacts()
    final_data["mars_hemisphere"] = marsHemisphere()

    return final_data

def marsNews():
    driver = webdriver.Chrome()
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    driver.get(news_url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find("div", class_ = "content_title").text
    news_content = soup.find("div", class_ = "article_teaser_body").text
    news = [news_title, news_content]
    driver.quit()
    return news


def marsImage():
    driver = webdriver.Chrome()
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    driver.get(image_url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    images = soup.find("a", class_ = "button fancybox")
    featured_image_url = image_url + images.get('data-fancybox-href')
    driver.quit()
    return featured_image_url 

def marsWeather():
    twitter_url = url = "https://twitter.com/marswxreport?lang=en"
    html = driver.page_source
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"lxml")
    tweets = soup.findAll('li',{"class":'js-stream-item'})
    tweet_records = []
    for tweet in tweets:
        if tweet.find('p',{"class":'tweet-text'}):
            tweet_text = tweet.find('p',{"class":'tweet-text'}).text.encode('utf8').strip()
        tweet_records.append(tweet_text)
    mars_weather_status = tweet_records[1]
    return mars_weather_status

def marsFacts():
    data = requests.get("https://space-facts.com/mars/")
    soup = BeautifulSoup(data.content, 'lxml')
    mars_table = soup.find_all('table')[0]
    mars_data = pd.read_html(str(mars_table))[0]
    mars_data.columns = ["Description", "Value"]
    mars_data = mars_data.set_index("Description")
    mars_facts = mars_data.to_html(index = True, header =True)
    return mars_facts

def marsHemisphere():
    driver = webdriver.Chrome()
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    driver.get(hemisphere_url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    mars_hemisphere_list = []
    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_url = "https://astrogeology.usgs.gov/" + end_link
        mars_hemisphere_list.append({"title": title, "img_url": image_url})

    def get_high_res_url(some_url):
        response = requests.get(some_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all("a")
        tifs = [j for j in links if ".tif" in j.attrs.get('href')]
        return tifs[0].get('href')

    updated_photos = []

    for data in mars_hemisphere_list:
        link_to_check = data.get('img_url')
        title = data.get('title')
        final_image_url = get_high_res_url(link_to_check)
        updated_photos.append({
            'Title': title,
            'Url': final_image_url
        })
    driver.quit()
    return updated_photos    