from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

#set the executable path and initialize the chrome browser in splinter
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:/Users/thenry/Desktop/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def mars_news(browser):
    browser = init_browser()

    #visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    # Convert the browser html to a soup object and then quit the browser
    html =  browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    # add try/except for error handling
    slide_elem = news_soup.select_one('ul.item_list li.slide')

    # Use the parent element to find the first `a` tag and save it as `news_title`
    news_title = slide_elem.find("div", class_='content_title').get_text()

    #use the parent element to find the paragraph text
    news_paragraph = slide_elem.find('div', class_='article_teaser_body').get_text()    
    return news_title, news_paragraph

def featured_image(browser):

    browser = init_browser()

    #visit url
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    #find and click the full image button. An id can only be used one time throughout the entire page.
    full_image_elem =  browser.find_by_id('full_image')
    full_image_elem.click()

    #find the more info button and click that.
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    #parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    #find the relative image url.
    img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    #use the base url to create an absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    return img_url

def mars_facts():
    #scrape the facts table into a dataframe
    df = pd.read_html('https://space-facts.com/mars/')[0]

    #assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # convert DataFrame back into HTML format      
    return df.to_html()

def mars_hemi(browser):

    #same code below use to gather hemisphere list of dictionaries

    #visit the url for mars hemispheres images.
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    #find and click on 'Cerberus Hemisphere Enhanced' mars hemisphere
    cer_hemi_small = browser.find_by_text('Cerberus Hemisphere Enhanced').click()

    #find and click on the 'open' button using its id.
    cer_hemi_big = browser.find_by_id('wide-image-toggle').click()

    #parse the resulting html with beautifulsoup
    html = browser.html
    cer_soup = BeautifulSoup(html, 'html.parser')

    #find the relative image url with its img tag
    cer_url_rel = cer_soup.select_one('img.wide-image').get("src")

    #use the base url to create an absolute url
    cer_url_big = f'https://astrogeology.usgs.gov{cer_url_rel}'

    # find the title using h2 tag with class=title and get the text only
    cer_title_big = cer_soup.select_one('h2.title').get_text()

    #visit the url     
    browser.visit(url)

    #find and click on 'Schiaparelli Hemisphere Enhanced' mars hemisphere
    sch_hemi_small = browser.find_by_text('Schiaparelli Hemisphere Enhanced').click()
    sch_hemi_big = browser.find_by_id('wide-image-toggle').click()

    html = browser.html
    sch_soup = BeautifulSoup(html, 'html.parser')

    sch_url_rel = sch_soup.select_one('img.wide-image').get("src")
    sch_url_big= f'https://astrogeology.usgs.gov{sch_url_rel}'
    sch_title_big = sch_soup.select_one('h2.title').get_text()

    browser.visit(url)

    #find and click on 'Syrtis Major Hemisphere Enhanced' mars hemisphere
    syr_hemi_small = browser.find_by_text('Syrtis Major Hemisphere Enhanced').click()
    syr_hemi_big = browser.find_by_id('wide-image-toggle').click()

    html = browser.html
    syr_soup = BeautifulSoup(html, 'html.parser')

    syr_url_rel = syr_soup.select_one('img.wide-image').get("src")
    syr_url_big = f'https://astrogeology.usgs.gov{syr_url_rel}'
    syr_title_big = syr_soup.select_one('h2.title').get_text()

    browser.visit(url)

    #find and click on 'Valles Marineris Hemisphere Enhanced' mars hemisphere
    val_hemi_small = browser.find_by_text('Valles Marineris Hemisphere Enhanced').click()
    val_hemi_big = browser.find_by_id('wide-image-toggle').click()
    html = browser.html
    val_soup = BeautifulSoup(html, 'html.parser')

    val_url_rel = val_soup.select_one('img.wide-image').get("src")
    val_url_big = f'https://astrogeology.usgs.gov{val_url_rel}'
    val_title_big = val_soup.select_one('h2.title').get_text()

    return cer_url_big, cer_title_big, sch_url_big, sch_title_big, syr_url_big, syr_title_big, val_url_big, val_title_big

#Initialize the browser.Create a data dictionary.End the WebDriver and return the scraped data.
def scrape_all():

    # initialize headless driver for deployment
    browser = Browser("chrome", executable_path= "chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)

    cer_url_big, cer_title_big, sch_url_big, sch_title_big, syr_url_big, syr_title_big, val_url_big, val_title_big = mars_hemi(browser)

    # run all scraping functions and store results in data dictionary
    data = {
        "news_title": news_title,
        "news_paragraph" : news_paragraph,
        "featured_image" : featured_image(browser),
        "facts": mars_facts(),
        "Cerberus_url": cer_url_big,
        "Cerberus_title": cer_title_big,
        "Schiaparelli_url": sch_url_big,
        "Schiaparelli_title": sch_title_big,
        "Syrtis_url": syr_url_big,
        "Syrtis_title": syr_title_big,
        "Valles_url": val_url_big,
        "Valles_title": val_title_big,
        "last_modified" : dt.datetime.now()
    }
    return data

