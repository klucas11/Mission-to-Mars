# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests


def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Scrape the NASA Mars News Site to collect the latest News Title and Paragraph Text
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    # HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve all elements that contain article information
    article = soup.find('li', class_='slide')
    news_title = article.find('div', class_="content_title").text
    news_paragraph = article.find('div', class_="article_teaser_body").text
    link = article.a['href']
    news_article_link = 'https://mars.nasa.gov/' + link

    # Find the image url for the current Featured Mars Image
    # URL of page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Navigate to page with image info
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info = browser.find_link_by_partial_text("more info")
    more_info.click()

    # Scrape image info
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image = soup.find('figure', class_='lede')
    link = image.a['href']
    featured_image_url = 'https://www.jpl.nasa.gov' + link

    # Scrape the latest Mars weather tweet.
    # URL of page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    # Scrape weather report tweet
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.find('p', class_='tweet-text').text

    # Use Pandas to scrape the table containing facts about the planet.
    # URL of page to be scraped
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    # Scrape planet profile table
    table = pd.read_html(url)

    # Using pandas to convert to DataFrame
    mars_facts_df = pd.DataFrame(table[1])
    mars_facts_df.columns = ['Description', 'Value']

    # convert dataframe to html
    mars_facts_html = mars_facts_df.to_html()

    # Find the title and image url for each hemisphere
    # URL of page to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Create list to hold info
    hemisphere_images = []

    # Scrape for info
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find("div", class_="collapsible results")
    hemispheres = results.find_all("div", class_="item")
    # print(hemispheres)

    # Loop through each hemisphere
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        src = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + src
        browser.visit(image_link)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_images.append({"title": title, "img_url": image_url})

    # Dicitonary storing scraped data
    mars_scrape_dictionary = {}
    mars_scrape_dictionary = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "news_article_link": news_article_link,
        "featured_image": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts_html": mars_facts_html,
        "hemisphere_images": hemisphere_images}

    browser.quit()
    return(mars_scrape_dictionary)
