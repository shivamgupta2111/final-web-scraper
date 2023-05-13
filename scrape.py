#%%
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import pandas as pd
#%%
# set up Chrome options to run headless
chrome_options = Options()
#%%
# create Chrome driver
driver = webdriver.Chrome(options=chrome_options)
#%%
# navigate to Google search page
driver.get("https://www.google.com")
#%%
# locate the search box and enter query
search_box = driver.find_element(By.CLASS_NAME, 'gLFyf')
search_box.send_keys("site:youtube.com openinapp.co")
search_box.send_keys(Keys.RETURN)
#%%
def scrape(links):
    # extract the first 10,000 search results
    elements = driver.find_elements(By.CSS_SELECTOR, "div.v7W49e a")
    for result in elements:
        link = result.get_attribute('href')
        if link == None:
            continue
        if "google.com" not in link:
            links.append(link)
        if len(links) >= 10000:
            break
#%%
#%%
links = []
scrape
while True:
    try:
        driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pnnext"]'))))
        scrape(links)
        driver.find_element(By.XPATH, '//*[@id="pnnext"]').click()
        print("Navigating to Next Page")
        # scrape(links)
    except (TimeoutException, WebDriverException) as e:
        print("Last page reached")
        break
#%%
# close the browser
# driver.quit()
#%%
# print the scraped links
for link in links:
    print(link)
#%%
links
newLink = [*set(links)] #remove the duplicate links in list
with open('youtube_urls.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['URL'])
    for link in newLink:
        writer.writerow([link])

# links.pop(0)
# links.pop(0)
# Allchannel = []
# for link in len(links):
#     driver.get(links[link])
#     time.sleep(5)
#     channellink = driver.find_elements(By.CSS_SELECTOR, "#text.style-scope.ytd-channel-name.complex-string a.yt-simple-endpoint.style-scope.yt-formatted-string")
#     # channellink= driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[2]/div[1]/ytd-video-owner-renderer/div[1]/ytd-channel-name/div/div/yt-formatted-string/a"]').click()
#     channel = list(dict.fromkeys(map(lambda a: a.get_attribute("href"),channellink)))
#     print(channel)
#     Allchannel.append(channel)

# with open('youtube_channel_urls.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['channel URL'])
#     for Allchannel in channel:
#         writer.writerow([channel])

url = pd.read_csv(r"C:\Users\shiva\OneDrive\Documents\python\youtube_urls.csv")
# print(url.URL[])
# links= ["https://www.youtube.com/watch?v=UmcrUf4cBWw"]
allchannel = []
URL = url['URL']
for i in range(0,len(URL)):
    driver.get(URL[i])
    # time.sleep(5)
    channellink = driver.find_elements(By.CSS_SELECTOR, "#text.style-scope.ytd-channel-name.complex-string a.yt-simple-endpoint.style-scope.yt-formatted-string")
    # channellink= driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[2]/div[1]/ytd-video-owner-renderer/div[1]/ytd-channel-name/div/div/yt-formatted-string/a"]').click()
    channel = list(dict.fromkeys(map(lambda a: a.get_attribute("href"),channellink)))
    allchannel.extend(channel)
    
print(allchannel)
with open('youtube_channel_urls.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['channel URL'])
    for channel in allchannel:
        writer.writerow([channel])