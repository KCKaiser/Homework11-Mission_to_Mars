from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import time

###########################################################################

def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    #### NASA Mars News
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    
    time.sleep(5)
    html = browser.html
    soup = bs(html, 'html.parser')

    list_text = soup.body.find("div", class_ = "list_text")

    news_date = list_text.find("div", class_ = "list_date").text
    news_title = list_text.find("div", class_ = "content_title").text
    news_p = list_text.find("div", class_ = "article_teaser_body").text

    #### JPL Mars Space Images - Featured Image
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)

    browser.click_link_by_partial_text('FULL IMAGE')

    time.sleep(5)

    image_html = browser.html

    soup = bs(image_html, 'html.parser')

    partial_img = soup.find("img", class_ = "fancybox-image")["src"]
    featured_image_url = img_url[:24] + partial_img

    #### Mars Weather
    twitter_url = 'https://twitter.com/marswxreport?lang=en'

    response = requests.get(twitter_url)

    soup = bs(response.text, 'html.parser')

    mars_tweets = soup.find_all("p", class_ = "TweetTextSize")

    for tweet in mars_tweets:
        tweettext = tweet.text
        if tweettext.find("Sol") != -1 and tweettext.find("pressure") != -1 and tweettext.find("low") != -1:
            mars_weather = tweettext
            break
        else: 
            continue

    #### Mars Facts
    facts_url = "http://space-facts.com/mars/"

    tables = pd.read_html(facts_url)

    mars_df = tables[0]
    mars_df.columns = ["description", "value"]
    mars_df = mars_df.set_index("description")
 
    facts_html = mars_df.to_html(classes = "table table-striped")

    #### Mars Hemispheres
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(hemi_url)

    hemi_html = browser.html

    soup = bs(hemi_html, 'html.parser')

    hemisphere_image_urls = []

    h3_soup = soup.find_all("h3")

    for h3 in h3_soup:
        click_link = h3.text
        title = click_link[:-9]
        browser.click_link_by_partial_text(click_link)
        
        hemi_html = browser.html
        
        hemi_soup = bs(hemi_html, 'html.parser')
        img_url = browser.url[:29] + hemi_soup.find("img", class_ = "wide-image")["src"]
        
        dictionary = {"title" : title,
                    "img_url" : img_url}
        hemisphere_image_urls.append(dictionary)
        browser.back()
        
    browser.quit()
    post = {
        "news_date" : news_date,
        "news_title" : news_title,
        "news_text" : news_p,
        "featured_image" : featured_image_url,
        "mars_weather" : mars_weather,
        "mars_facts" : facts_html,
        "mars_hemispheres" : hemisphere_image_urls  
    }
    return post

