import Crawler
import pickle
import Searcher
# pagelist = ["https://w3schools.com/"]

crawler=Crawler.crawler('google.db')

#Recrawling from newpages file.
# with open('newpages','rb') as file:
# 	newpagesSet = pickle.load(file)
# file.close()

#Calculating Page Rank
# crawler.calculatePageRank()

#Create SCHEMA
crawler.createindextables()
# crawler.crawl(pagelist, depth=3)
# crawler.crawl(list(newpagesSet), depth=3)


