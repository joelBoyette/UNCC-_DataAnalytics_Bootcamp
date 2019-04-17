
# coding: utf-8

# ## Step 1
# 
# ### NASA Mars News
# 
# * Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
# 
# ```python
# # Example:
# news_title = "NASA's Next Mars Mission to Investigate Interior of Red Planet"
# 
# news_p = "Preparation of NASA's next spacecraft to Mars, InSight, has ramped up this summer, on course for launch next May from Vandenberg Air Force Base in central California -- the first interplanetary launch in history from America's West Coast."
# ```

# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time


# Initialize browser
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def mars_scrape_function():
    
    # Initialize browser
    browser = init_browser()

    mars_news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"


    # Retrieve page with the requests module
    response = requests.get(mars_news_url)

    # Create BeautifulSoup object; parse with 'lxml.parser'
    soup = BeautifulSoup(response.text, 'lxml')

    # results are returned as an iterable list
    nasa_headline_results = soup.find('div', class_="content_title").text


    nasa_par_results = soup.find('div',class_ = "rollover_description_inner").text

            

    # JPL Mars Space Images - Featured Image
    # Visit the url for JPL Featured Space Image here.
    # 
    # Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    # 
    # Make sure to find the image url to the full size .jpg image.
    # 
    # Make sure to save a complete url string for this image.
    # 
    # # Example:
    # featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'



    mars_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(mars_image_url)
    time.sleep(5)
    browser.click_link_by_partial_text('FULL IMAGE')
    
    time.sleep(5)
    browser.click_link_by_partial_text('more info')
    
    navigated_mars_image_url = browser.url
    
    
    # Retrieve page with the requests module
    mars_response = requests.get(navigated_mars_image_url)
    soup = BeautifulSoup(mars_response.text, 'lxml')

    results = soup.find("figure", class_ = "lede")

    featured_image_url = f'https://www.jpl.nasa.gov/{results.a["href"]}'


    # ### Mars Weather
    # 
    # * Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called `mars_weather`.
    # 
    # ```python
    # # Example:
    # mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'
    # ```

    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'

    # Retrieve page with the requests module
    response = requests.get(mars_weather_url)


    # Create BeautifulSoup object; parse with 'lxml.parser'
    soup = BeautifulSoup(response.text, 'html')


    mars_weather = soup.find("li" , {"id":"stream-item-tweet-1053439926098976774"}).find('p',class_ = "tweet-text").text

    # ### Mars Facts
    # 
    # * Visit the Mars Facts webpage [here](http://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # 
    # * Use Pandas to convert the data to a HTML table string.

    mars_facts_url = 'http://space-facts.com/mars/'

    mars_facts = pd.read_html(mars_facts_url)

    mars_facts_df = mars_facts[0]

    mars_facts_df.columns = ['Item','Metric']

    mars_facts_html_table = mars_facts_df.to_html()
    mars_facts_html_table.replace('\n', '')
    


    # ### Mars Hemispheres
    # 
    # * Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.
    # 
    # * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # 
    # * Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.
    # 
    # * Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
    # 
    # ```python
    # # Example:
    # hemisphere_image_urls = [
    #     {"title": "Valles Marineris Hemisphere", "img_url": "..."},
    #     {"title": "Cerberus Hemisphere", "img_url": "..."},
    #     {"title": "Schiaparelli Hemisphere", "img_url": "..."},
    #     {"title": "Syrtis Major Hemisphere", "img_url": "..."},
    # ]


    mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(mars_hemisphere_url)
    time.sleep(5)
    mars_hemisphere_response = requests.get(mars_hemisphere_url)
    soup = BeautifulSoup(mars_hemisphere_response.text, 'lxml')

    results = soup.find_all("a", class_ = "itemLink product-item")

    hemisphere_image_urls = []
    image_dict = {}

    astro_index = 'https://astrogeology.usgs.gov'

    for result in results:
        
        image_browse = result["href"]
        browser.visit(astro_index+image_browse)
        
        mars_link_response = requests.get(browser.url)
        soup = BeautifulSoup(mars_link_response.text, 'lxml')
        
        image_dict = {"title": soup.find('h2', class_ = 'title').text, 
                     "image_url" : astro_index + soup.find('img', class_ = "wide-image")['src']}
  
        hemisphere_image_urls.append(image_dict)

    
    mars_scrape_dict = {"mars_news_headline": nasa_headline_results,
                        "mars_news_par": nasa_par_results,
                        "mars_feature_images" : featured_image_url,
                        "mars_weather": mars_weather,
                        "mars_facts": mars_facts_html_table,
                        "mars_hemisphere_images": hemisphere_image_urls
                        }

    return mars_scrape_dict


