from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import sqlite3
import time
#launch url
con = sqlite3.connect('google.db')
options = webdriver.ChromeOptions()
options.add_argument('headless')
#Supress warnings
options.add_argument('log-level=3')
prefs = {"profile.managed_default_content_settings.images":2,
         "profile.default_content_setting_values.notifications":2,
         "profile.managed_default_content_settings.stylesheets":2,
         "profile.managed_default_content_settings.cookies":2,
         "profile.managed_default_content_settings.javascript":1,
         "profile.managed_default_content_settings.plugins":1,
         "profile.managed_default_content_settings.popups":2,
         "profile.managed_default_content_settings.geolocation":2,
         "profile.managed_default_content_settings.media_stream":2,
         "disk-cache-size": 4096
         }
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(75)
driver.implicitly_wait(75)

rows = con.execute("SELECT url FROM urllist WHERE title = '' OR title IS NULL ORDER BY RANDOM()").fetchall()
i = 0
for row in rows:
    i += 1
    print(f"##### ENTRY {i} ##### \n: {row[0]}")
    try:
        driver.get(row[0])
        c = driver.page_source
    except:
        print("Couldn't open page : {}".format(row[0]))
        driver.close()
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(75)
        driver.implicitly_wait(75)
        continue
    soup = BeautifulSoup(c, 'html.parser')
    title = ''
    description = ''
    keywords = ''
    titleArray = soup.findAll("title")
    metaDescriptionArray = soup.findAll("meta", {"name": "description"})
    metaKeywordsArray = soup.findAll("meta", {"name": "keywords"})
    if len(titleArray) >= 1:
        title = titleArray[0].text
    if len(metaDescriptionArray) == 1:
        if ('content' in dict(metaDescriptionArray[0].attrs)):
            description = metaDescriptionArray[0]['content']
    if len(metaKeywordsArray) == 1:
        if ('content' in dict(metaKeywordsArray[0].attrs)):
            keywords = metaKeywordsArray[0]['content']
    title = title.replace("'", ' ')
    title = title.replace('"', " ")
    title = title.strip()
    description = description.replace("'", ' ')
    description = description.replace('"', " ")
    description = description.strip()
    keywords = keywords.replace("'", ' ')
    keywords = keywords.replace('"', " ")
    keywords = keywords.strip()
    con.execute(f"UPDATE urllist SET title = '{title}', keywords= '{keywords}', description= '{description}' WHERE url='{row[0]}';")
    con.commit()    
driver.close()
