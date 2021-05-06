import sqlite3
import time
class Searcher:
	def __init__(self, dbname):
		self.con = sqlite3.connect(dbname)

	def __del__(self):
		self.con.close()

	def getMatchRows(self, q):
		#Strings to build the query
		fieldList = 'w0.urlid'
		tableList = ''
		clauseList = ''
		wordIds = []

		#Split the words by spaces
		words = q.split(' ')
		tableNumber = 0

		for word in words:
			#Get the word ID
			query = f"SELECT rowid FROM wordlist WHERE word='{word}'"
			#print(query)
			wordRow = self.con.execute(query).fetchone()
			if wordRow != None:
				wordId = wordRow[0]
				wordIds.append(wordId)
				if tableNumber > 0:
					tableList += ','
					clauseList += ' AND '
					clauseList += f"w{tableNumber-1}.urlid = w{tableNumber}.urlid AND "
				fieldList += f",w{tableNumber}.location"
				tableList += f"wordlocation w{tableNumber}"
				clauseList += f"w{tableNumber}.wordid = {wordId}"
				tableNumber += 1

		#Create the query from the separate parts
		if clauseList == '' and tableList == '':
			return None,wordIds
		fullQuery = f"SELECT {fieldList} FROM {tableList} WHERE {clauseList}"
		print(fullQuery)
		cur = self.con.execute(fullQuery)
		rows = [row for row in cur]
		return rows,wordIds


	def getScoredList(self, rows, wordIds):
		totalScores = dict([(row[0],0) for row in rows])
		#--------------WEIGHTS-----------------#
		weights = [
		(2.0,self.frequencyScore(rows)),
		(2.0,self.locationScore(rows)),
		(1.0,self.distanceScore(rows)),
		(1.0,self.inboundLinkScore(rows)),
		(1.0,self.pageRankScore(rows)),
		(1.0,self.linktextscore(rows,wordIds))
		]
		for(weight,scores) in weights:
			for url in totalScores:
				totalScores[url] += weight*scores[url]
		return totalScores
	
	def getUrlName(self, id):
		return self.con.execute(f"SELECT url FROM urllist WHERE rowid={id}").fetchone()[0]

	def getUrlTuple(self, id):
		return self.con.execute(f"SELECT url, title, description, keywords, clicks FROM urllist WHERE rowid={id}").fetchone()

	def normalizeScores(self, scores, smallIsBetter=0):
		vsmall = 0.00001 #Avoid division by 0 errors
		if smallIsBetter:
			minScore = min(scores.values())
			return dict([(u,float(minScore)/max(vsmall,l)) for (u,l) in scores.items()])
		else:
			maxScore = max(scores.values())
			if maxScore == 0: maxScore = vsmall
			return dict([(u, float(c)/maxScore) for (u,c) in scores.items()])

	def frequencyScore(self,rows):
		counts = dict([(row[0],0) for row in rows])
		for row in rows: counts[row[0]] += 1
		return self.normalizeScores(counts)

	def locationScore(self, rows):
		locations = dict([(row[0],1000000) for row in rows])
		for row in rows:
			loc = 0
			# print(row[1:])
			for value in row[1:]:
				loc += int(value) #loc = sum(int(row[1:]))
			# print(loc)
			if loc < locations[row[0]]: locations[row[0]] = loc
		return self.normalizeScores(locations,smallIsBetter=1)
			
	def distanceScore(self, rows):
		#If there's only one word, everyone wins!
		if len(rows[0]) <= 2:
			# print(rows[0])
			return dict([(row[0],1.0) for row in rows])

		#Initialize the dictionary with large values
		minDistance = dict([(row[0],100000) for row in rows])

		for row in rows:
			dist = sum([abs(int(row[i])-int(row[i-1])) for i in range(2,len(row))])
			if dist < minDistance[row[0]]: minDistance[row[0]] = dist
		return self.normalizeScores(minDistance, smallIsBetter = 1)


	def inboundLinkScore(self,rows):
		uniqueUrls = set([row[0] for row in rows])
		inboundCount = dict([(u, self.con.execute(f"SELECT COUNT(*) FROM link WHERE toid={u}").fetchone()[0]) for u in uniqueUrls])
		# print(f"Inbound Count is {inboundCount}")
		return self.normalizeScores(inboundCount)


	def pageRankScore(self,rows):
		pageranks = dict([(row[0],self.con.execute(f"SELECT score FROM pagerank WHERE urlid={row[0]}").fetchone()[0]) for row in rows])
		maxrank = max(pageranks.values())
		normalizedscores = dict([(u,float(l)/maxrank) for (u,l) in pageranks.items()])
		return normalizedscores

	def linktextscore(self,rows,wordids):
		linkscores = dict([(row[0],0) for row in rows])
		vsmall = 0.00001 #Avoid division by 0 errors
		
		for wordid in wordids:
			cur = self.con.execute(f"SELECT link.fromid, link.toid FROM linkwords, link WHERE wordid={wordid} and linkwords.linkid=link.rowid")
			for (fromid,toid) in cur:
				if toid in linkscores:
					pr = self.con.execute(f"SELECT score FROM pagerank WHERE urlid={fromid}").fetchone()[0]
					linkscores[toid] += pr
		maxscore = max(linkscores.values())	
		normalizedscores=dict([(u,float(l)/max(maxscore,vsmall)) for (u,l) in linkscores.items()])
		return normalizedscores

	# def query(self, q):
	# 	start_time = time.time()
	# 	rows,wordIds = self.getMatchRows(q)
	# 	if rows == None or len(rows) == 0:
	# 		end_time = time.time()
	# 		searchtime = end_time - start_time
	# 		# print(f"Time Taken ::{searchtime} seconds")
	# 		# print(f"No results matching query '{q}'")
	# 		return (0,searchtime)
	# 	scores = self.getScoredList(rows, wordIds)
	# 	rankedScores = sorted([(score,url) for (url,score) in scores.items()], reverse=1)

	# 	end_time = time.time()
	# 	searchtime = end_time - start_time
	# 	# print(f"Found {len(rankedScores)} results in {searchtime} seconds")
	# 	return(len(rankedScores),searchtime, rankedScores)
	# 	# for (score,urlid) in rankedScores[:]:
	# 	# 	print(f"{score}\t{getUrlName(urlid)}")

	def getLuckySiteResult(self,q):
		rows,wordIds = self.getMatchRows(q)
		if rows == None or len(rows) == 0:
			return ('')
		scores = self.getScoredList(rows, wordIds)
		rankedScores = sorted([(score,url) for (url,score) in scores.items()], reverse=1)
		return(self.getUrlName(rankedScores[0][1]))

	def getSiteResultsHtml(self, page, q):
		pageSize = 20
		fromLimit = (int(page) - 1) * pageSize
		start_time = time.time()
		rows,wordIds = self.getMatchRows(q)
		if rows == None or len(rows) == 0:
			end_time = time.time()
			searchtime = end_time - start_time
			return (0, searchtime, f"""<div class='siteResults'><p> Your search - <em><b>{q}</b></em> - did not match any documents.  </p>   <p style='margin-top:1em'><b>Suggestions:</b></p> 
<ul style='margin-left:1.3em;margin-bottom:2em'><li>Make sure that all words are spelled correctly.</li><li>Try different keywords.</li><li>Try more general keywords.</li><li>Try fewer keywords.</li></ul></div>""", pageSize)
		scores = self.getScoredList(rows, wordIds)
		rankedScores = sorted([(score,url) for (url,score) in scores.items()], reverse=1)
		end_time = time.time()
		searchtime = end_time - start_time
		resultsHtml = "<div class='siteResults'>"
		for (score,urlid) in rankedScores[fromLimit : pageSize + fromLimit]:
			# print(f"{score}\t{self.getUrlTuple(urlid)}")
			urlTuple = self.getUrlTuple(urlid)
			url = urlTuple[0]
			title = urlTuple[1]
			description = urlTuple[2]
			# keywords = urlTuple[3]
			# clicks = urlTuple[4]	

			title = title[:110]

			description = self.trimDescription(description, 250, url)
			urlTrimmed = self.trimUrl(url, 75)
			if title == '':
				title = urlTrimmed.split('//')[1]

			resultsHtml += f"""<div class='resultContainer'>
								<span class='title'>
				 					<a class='result' href='{url}' data-linkId='{urlid}'>{title}</a>
								</span>
								<span class ='url'><a href='{url}' style='text-decoration:inherit;color: #006621;'>{urlTrimmed}</a></span><br>
							  	<span class ='description'>{description}</span>
						  	  </div>"""

		resultsHtml += '</div>'
		return (len(rankedScores), searchtime, resultsHtml.strip(), pageSize)

	def getImageResultsHtml(self, page, q):
		pageSize = 30
		fromLimit = (int(page) - 1) * pageSize
		# print('FROM LIMIT:',fromLimit)
		start_time = time.time()
		q = f"%{q}%"
		query = f"SELECT rowid, siteurlid, imageurl, alt, title, clicks, broken FROM images WHERE (title LIKE '{q}' OR alt LIKE '{q}') AND broken = 0 ORDER BY clicks DESC LIMIT {fromLimit},{pageSize}"
		# print(query)
		imageResults = self.con.execute(query).fetchall()
		# print(len(imageResults))
		# print(imageResults)
		resultsHtml = "<div class='imageResults'>"
		count = 0
		i = 0
		
		
		while(i < len(imageResults)):
			count += 1
			imageid = imageResults[i][0]
			siteUrl = self.getUrlName(int(imageResults[i][1]))
			imageUrl = imageResults[i][2]
			alt = imageResults[i][3]
			title = imageResults[i][4]
			if title != '':
				displayText = title
			elif alt != '':
				displayText = alt
			else: displayText = imageUrl
			resultsHtml += f"<div class='gridItem image{count}'>"
			resultsHtml += f"<a href='{imageUrl}' data-fancybox data-caption='{displayText}' data-siteurl='{siteUrl}'>"
			resultsHtml += "<script>$(document).ready(function(){"
			resultsHtml += f"loadImage(\"{imageUrl}\",\"image{count}\");"
			resultsHtml += '});</script>'
			resultsHtml += f"""<span class='details'>{displayText}</span>
								 </a>
								 </div>"""
			i += 1
		resultsHtml += "</div>"
		end_time = time.time()
		searchtime = end_time - start_time
		return (searchtime, resultsHtml.strip(), pageSize)

	def getTorrentResultsHtml(self, page, q):
		pageSize = 20
		fromLimit = (int(page) - 1) * pageSize
		# print('FROM LIMIT:',fromLimit)
		start_time = time.time()
		q = f"%{q}%"
		query = f"SELECT * FROM torrents WHERE torrentname LIKE '{q}' OR torrenturl LIKE '{q}' ORDER BY seederscount DESC LIMIT {fromLimit},{pageSize}"
		# print(query)
		torrentResults = self.con.execute(query).fetchall()
		print(len(torrentResults))
		resultsHtml = "<div class='torrentResults'>"
		count = 0
		i = 0
		
		
		while(i < len(torrentResults)):
			count += 1
			torrentName = torrentResults[i][0]
			torrentName = torrentName[:110]
			torrentUrl = torrentResults[i][1]
			torrentUrlTrimmed = self.trimUrl(torrentUrl, 75)
			seedersCount = torrentResults[i][2]
			leechersCount = torrentResults[i][3]
			torrentSize = torrentResults[i][4]
			torrentCat = torrentResults[i][5]
			if 'B' not in torrentSize:
				torrentSize = 'Size Unknown'


			resultsHtml += f"""<div class='resultContainer'>
								<span class='title'>
				 					<a class='result' href='{torrentUrl}'> {torrentName} | [{torrentSize}]</a>
								</span>
								<span class ='url'><a href='{torrentUrl}' style='text-decoration:inherit;color: #006621;'>{torrentUrlTrimmed}</a></span><br>
								<span style='text-decoration:inherit;color: #c54404;font-weight: bold;'>
								<button class="btn" style="background-color: #007405; border-radius: 10px;height: 23px;line-height: 0px;">Seeders: {seedersCount}<i class="material-icons right" style="color: #10e415;
								    transform: rotate(270deg);">forward</i></button>
								
								<button class="btn" style="background-color: #9f1309;border-radius: 10px;height: 23px;line-height: 0px;">Leechers: {leechersCount}<i class="material-icons right" style="color: #ff695e;
								    transform: rotate(90deg);">forward</i></button> 
								<button class="btn" style="background-color:#11083e;border-radius: 10px;height: 23px;line-height: 0px;">{torrentCat}</button> 
								</span>
						  	  </div>"""

			i += 1
		resultsHtml += "</div>"
		end_time = time.time()
		searchtime = end_time - start_time
		return (searchtime, resultsHtml.strip(), pageSize)

	def getImageNumResults(self, q):
		q = f"%{q}%"
		query = f"SELECT COUNT(*) FROM images WHERE title LIKE '{q}' OR alt LIKE '{q}' AND broken = 0"
		# print(query)
		numResults = self.con.execute(query).fetchone()[0]
		# print('Num results:',numResults)
		return numResults

	def getTorrentNumResults(self, q):
		q = f"%{q}%"
		query = f"SELECT COUNT(*) FROM torrents WHERE torrentname LIKE '{q}' OR torrenturl LIKE '{q}'"
		# print(query)
		numResults = self.con.execute(query).fetchone()[0]
		# print('Num results:',numResults)
		return numResults


	def trimDescription(self, string1, characterLimit, url):
		if len(string1) > characterLimit: dots = f" ...<a href='{url}'>Read More..</a>"	
		else: dots = ''
		return (string1[:characterLimit]+dots)

	def trimUrl(self, string1, characterLimit):
		if len(string1) > characterLimit: dots = "..."
		else: dots = ''
		return (string1[:characterLimit]+dots)
