from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import sqlite3
import time
#launch url
con = sqlite3.connect('google.db')
options = webdriver.ChromeOptions()
# options.add_argument('headless')
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
cate = {'MOVIES':'Movies','GAMES':'Games','MUSIC':'Music','APPLICATION':'Apps','ANIME':'Anime','DOCUMENTARIES':'Documentaries','OTHERS':'Other','TELEVISION':'TV'}
for i in range(1,51):
    print(f'##############  PAGE {i} #################')
    url = f"https://1377x.to/cat/Documentaries/{i}/"
    try:
        driver.get(url)
        c = driver.page_source
    except:
        print("Couldn't open page : {}".format(url))
        driver.close()
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(75)
        driver.implicitly_wait(75)
        continue
    page_soup = BeautifulSoup(c, 'html.parser')
    for row in page_soup.find_all('tr')[1:]:
        torrent_url ="https://www.1377x.to"
        torrent_name = row.findChildren('td', {'class': 'coll-1 name'})[0].text
        torrent_name = torrent_name.replace('"', " ")
        torrent_name = torrent_name.replace("'", " ")
        torrent_name = torrent_name.replace(".", " ")
        torrent_name = torrent_name.replace(",", " ")
        torrent_name = torrent_name.replace("-", " ")
        torrent_name = torrent_name.replace("[", " ")
        torrent_name = torrent_name.replace("]", " ")



        torrent_name = torrent_name.strip()
        t_url = row.findChildren('td')[0].findChildren('a')[1].attrs['href']
        torrent_url += t_url
        seeders_count= row.findChildren('td', {'class': 'coll-2 seeds'})[0].text
        leechers_count = row.findChildren('td', {'class': 'coll-3 leeches'})[0].text
        torrent_size = row.findChildren('td', {'class': 'coll-4'})[0].text.split(seeders_count)[0]
        category = ''
        for k in cate:
                    # print(cate[k])
                    if (cate[k] in url):
                        # print('cat found',k)
                        category = k
        row = con.execute(f"SELECT torrentname FROM torrents WHERE torrenturl = '{torrent_url}'").fetchall()
        if(len(row)) == 0:
            print(f"INSERT INTO torrents (torrentname, torrenturl, seederscount, leecherscount, torrentsize) VALUES ('{torrent_name}', '{torrent_url}', {seeders_count}, {leechers_count}, '{torrent_size}')")
            con.execute(f"INSERT INTO torrents (torrentname, torrenturl, seederscount, leecherscount, torrentsize, torrentcat) VALUES ('{torrent_name}', '{torrent_url}', {seeders_count}, {leechers_count}, '{torrent_size}','{category}')")
            con.commit()
        else:
            print('DUPLICATE:: {} | {} | {} | {} | {} | {}\n'.format(torrent_name, torrent_url, seeders_count, leechers_count, torrent_size, category))	
    time.sleep(3)
driver.close()
