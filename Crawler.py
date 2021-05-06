import datetime, string, sqlite3, re, pickle
from urllib.request import urlopen, urljoin
from bs4 import BeautifulSoup 
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
#List of words to ignore
ignorewords=set()
f = open("stop_words.txt","r")
for i in f:
    ignorewords.add(i.split('\n')[0])

class crawler:
    # Initialize the crawler with the name of database
    
    def __init__(self,dbname):
        self.con = sqlite3.connect(dbname)
    
    def __del__(self):
        self.con.close()
    
    def dbcommit(self):
        self.con.commit()
    
    def getEntryId(self,table,field,value,createnew = True):
        # Auxilliary function for getting an entry id and adding it if it's not present
        # Index an individual page
        cur = self.con.execute(f"SELECT rowid FROM {table} WHERE {field}='{value}'")
        res = cur.fetchone()
        if(res == None):
            cur = self.con.execute(f"INSERT INTO {table} ({field}) VALUES ('{value}')")
            return cur.lastrowid
        else:
            return res[0]   

    def addToIndex(self,url,soup):
        indexingString = '{} :: Indexing {}'.format(str(datetime.datetime.now()), url)
        print(indexingString)
        if(self.isIndexed(url)):
            return
        # Get the individual words
        text = self.getTextOnly(soup)
        #print('TEXT : ',text)
        words = self.separateWords(text) 
        #print('WORDS: ',words) 
        #Get the URL ID
        urlid = self.getEntryId('urllist','url',url)
        title = ''
        description = ''
        keywords = ''
        titleArray = soup.findAll("title")
        metaDescriptionArray = soup.findAll("meta", {"name": "description"})
        metaKeywordsArray = soup.findAll("meta", {"name": "keywords"})
        try:
            if len(titleArray) == 1:
                title = titleArray[0].text
            if len(metaDescriptionArray) == 1:
                if ('content' in dict(metaDescriptionArray[0].attrs)):
                    description = metaDescriptionArray[0]['content']
            if len(metaKeywordsArray) == 1:
                if ('content' in dict(metaKeywordsArray[0].attrs)):
                    keywords = metaKeywordsArray[0]['content']
        except:
            return
        title = title.replace("'", ' ')
        title = title.replace('"', " ")
        title = title.strip()
        description = description.replace("'", ' ')
        description = description.replace('"', " ")
        description = description.strip()
        keywords = keywords.replace("'", ' ')
        keywords = keywords.replace('"', " ")
        keywords = keywords.strip()
        updateURLMetadataQuery = "UPDATE urllist SET title = '{}', description = '{}', keywords = '{}' WHERE rowid = '{}'".format(title, description, keywords, urlid)
        # print(updateURLMetadataQuery)
        cur = self.con.execute(updateURLMetadataQuery)

        # Link each word to this url
        for i in range(len(words)):
            word = words[i]
            #Cleaning Words 
            if(word in ignorewords or len(word)>32 or word.isdigit()):
                continue
            wordid = self.getEntryId('wordlist','word',word)
            self.con.execute(f"INSERT INTO wordlocation(urlid, wordid, location) VALUES ({urlid}, {wordid}, {i})")     
            # Extract the text from an HTML page (no tags)

    def getTextOnly(self,soup):
        # Extract the text from an HTML page (no tags)
        v = soup.string
        if(v == None):
            c = soup.contents
            if(len(c) != 0):
                resultText = ''   
                for t in c:
                    subText = self.getTextOnly(t)
                    if(subText != None):
                        resultText = resultText + subText + '\n'
                #print('RT : ',resultText)
                return(resultText)
        else:
            #print('STRIP : ',v.strip())
            #Removes White Spaces from Both sides   
            return(v.strip())    

                
        
    def separateWords(self,text):
        # print("TEXT : ",text)
        # splitter=re.compile('\\W*')
        # return [s.lower() for s in splitter.split(text) if s!='']
        if(text == None):
            return None
        res = re.sub('['+string.punctuation+']', '',text.lower()).split()
        return(res)
      
    def isIndexed(self,url):
        # Return true if this url is already indexed
        u = self.con.execute(f"SELECT rowid FROM urllist WHERE url='{url}'").fetchone()
        if(u != None):
            # Check if it has actually been crawled
            v=self.con.execute(f"SELECT * FROM wordlocation WHERE urlid={u[0]}").fetchone()
            if(v != None): 
                return True
        return False
     
    def addLinkRef(self,urlFrom,urlTo,linkText):
        # Add a link between two pages
        words = self.separateWords(linkText)
        if(words == None):
            return
        for i in words:
            if(i.isdigit() or not i.isalnum()):
                words.remove(i)  
        # HERE print("WORDS : ",words)
        
        fromid = self.getEntryId('urllist','url',urlFrom)
        toid = self.getEntryId('urllist','url',urlTo)
        if(fromid == toid):
            return
        cur = self.con.execute(f"INSERT INTO link(fromid,toid) VALUES ({fromid},{toid})") 
        linkid = cur.lastrowid
        for word in words:
            if word in ignorewords:
                continue
            wordid = self.getEntryId('wordlist','word',word) 
            self.con.execute(f"INSERT INTO linkwords(linkid,wordid) VALUES ({linkid},{wordid})")  
     
    def crawl(self,pages,depth=1):
        # Starting with a list of pages, do a breadth
        # first search to the given depth, indexing pages
        # as we go
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
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
        for i in range(depth):
            newpages = set()
            for page in pages:
                try:
                    # c = urllib.request.urlopen(page)
                    #c = requests.get(page)
                    driver.get(page)
                    c = driver.page_source
                except:
                    print("Couldn't open page : {}".format(page))
                    driver.close()
                    driver = webdriver.Chrome(options=options)
                    driver.set_page_load_timeout(75)
                    driver.implicitly_wait(75)
                    continue
                #soup = BeautifulSoup(c.read()) 
                #soup = BeautifulSoup(c.content,'html.parser')
                soup = BeautifulSoup(c,'html.parser')
                
                for script in soup(["script", "style"]):
                    script.decompose()  
                self.addToIndex(page,soup)
                links = soup('a')
                for link in links:
                    if ('href' in dict(link.attrs)):
                        url = urljoin(page,link['href'])

                        if url.find("'")!=-1 or url[0:11] == 'javascript' or url[0:3] == 'tel' or url[0:6] == 'mailto' or url[0:9] == 'whatsapp': 
                            #Dont Index(Skipping) redundant URLS
                            continue

                        url = url.split('#')[0] # remove location portion 
                        # url=url.split('?')[0]
                        url = url.split('%')[0]


                        if url[0:4] == 'http' and not self.isIndexed(url):
                            newpages.add(url)
                            pages_file = open('pages','wb')
                            newpages_file = open('newpages','wb')
                            pickle.dump(newpages, newpages_file)
                            pickle.dump(pages, pages_file)
                            newpages_file.close()
                            pages_file.close()
                        linkText=self.getTextOnly(link)
                        self.addLinkRef(page,url,linkText)
                images = soup('img')
                for image in images:
                    alt = ''
                    src = ''
                    title = ''
                    if ('src' in dict(image.attrs)):
                        imageUrl=urljoin(page,image['src'])
                        imageUrl=imageUrl.split('?')[0]
                        imageUrl=imageUrl.strip()
                        if imageUrl[0:5] == 'data:':
                            continue
                        imageRowQuery = f"SELECT rowid FROM images WHERE imageurl='{imageUrl}'"
                        # print(imageRowQuery)
                        cur = self.con.execute(imageRowQuery)
                        res = cur.fetchone()
                        if res != None:
                            continue
                        if imageUrl.find("'")!=-1: 
                            continue
                        if ('alt' in dict(image.attrs)):
                            alt=image['alt']
                            alt = alt.replace("'", ' ')
                            alt = alt.replace('"', " ")
                            alt = alt.strip()
                        if ('title' in dict(image.attrs)):
                            title=image['title']
                            title = title.replace("'", ' ')
                            title = title.replace('"', " ")
                            title = title.strip()
                        # print(f'Image- {imageUrl}')
                        urlid = self.getEntryId('urllist','url',page) 
                        insertImageQuery = f"INSERT INTO images(siteurlid, imageurl, alt, title) VALUES ('{urlid}','{imageUrl}','{alt}','{title}')"
                        # print(insertImageQuery)
                        self.con.execute(insertImageQuery)
                self.dbcommit()
            pages=newpages
        driver.close()

    def calculatePageRank(self,iterations=100):
        # clear out the current PageRank tables
        self.con.execute('DROP TABLE IF EXISTS pagerank')
        self.con.execute('CREATE TABLE pagerank(urlid PRIMARY KEY,score)')
        
        # initialize every url with a PageRank of 1
        self.con.execute('INSERT INTO pagerank SELECT rowid, 1.0 FROM urllist')
        self.dbcommit()
        
        for i in range(iterations):
            print ("Iteration %d" % (i))
            for (urlid,) in self.con.execute('SELECT rowid FROM urllist'):
                pr=0.15
                # Loop through all the pages that link to this one
                for (linker,) in self.con.execute(f'SELECT DISTINCT fromid FROM link WHERE toid={urlid}'):
                    # Get the PageRank of the linker
                    linkingpr = self.con.execute(f'SELECT score FROM pagerank where urlid={linker}').fetchone()[0]
                    # Get the total number of links from the linker
                    linkingcount = self.con.execute(f'SELECT COUNT(*) FROM link WHERE fromid = {linker}').fetchone()[0]
                    pr += 0.85*(linkingpr/linkingcount)
                self.con.execute(f'UPDATE pagerank SET score = {pr} WHERE urlid = {urlid}')
        self.dbcommit()

     # Create the database tables
    def createindextables(self):
        self.con.execute('CREATE TABLE IF NOT EXISTS urllist(url, title VARCHAR, description VARCHAR, keywords VARCHAR, clicks INTEGER)')
        self.con.execute('CREATE TABLE IF NOT EXISTS images(siteurlid, imageurl, alt VARCHAR, title VARCHAR, clicks INTEGER, broken INTEGER)')
        self.con.execute('CREATE TABLE IF NOT EXISTS torrents(torrentname, torrenturl, seederscount INTEGER, leecherscount INTEGER, torrentsize)')
        self.con.execute('CREATE TABLE IF NOT EXISTS wordlist(word)')
        self.con.execute('CREATE TABLE IF NOT EXISTS wordlocation(urlid,wordid,location)')
        self.con.execute('CREATE TABLE IF NOT EXISTS link(fromid integer,toid integer)')
        self.con.execute('CREATE TABLE IF NOT EXISTS linkwords(wordid,linkid)')
        self.con.execute('CREATE INDEX IF NOT EXISTS wordidx on wordlist(word)')
        self.con.execute('CREATE INDEX IF NOT EXISTS urlidx on urllist(url)')
        self.con.execute('CREATE INDEX IF NOT EXISTS wordurlidx on wordlocation(wordid)')
        self.con.execute('CREATE INDEX IF NOT EXISTS urltoidx on link(toid)')
        self.con.execute('CREATE INDEX IF NOT EXISTS urlfromidx on link(fromid)')
        self.dbcommit()