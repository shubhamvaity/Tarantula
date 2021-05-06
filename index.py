from flask import Flask, render_template, request, redirect, session, flash
import Searcher, AjaxUpdater 
import math
app = Flask('Tarantula Server')
app.secret_key = "INSY_WINSY"
@app.route("/")
def main():
	
	return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
	searcher = Searcher.Searcher('google.db')
	if request.method == 'GET':
		term = request.args.get('term')
		term = term.replace("'","")
		term = term.replace('"',"")
		if term == '':
			return("""<h1 style='font-family:Roboto;'>Please enter a search query<h1>""")
		type1 = request.args.get('type')
		if request.args.get('page') != None: page = request.args.get('page')
		else: page = 1 
		if type1 == 'web':
			searchType = request.args.get('searchType')
			if searchType ==  'lucky':
				luckyUrl = searcher.getLuckySiteResult(term.lower())
				return redirect(str(luckyUrl))
			else:
				numResults, searchTime, resultsHtml, pageSize = searcher.getSiteResultsHtml(page, term.lower())
				searchTime = str(searchTime)[:4]
				pagesToShow = 10
				paginationContainer =''
				page = int(page)	
				numPages = math.ceil(int(numResults)/int(pageSize))
				pagesLeft = min(int(pagesToShow), int(numPages))
				currentPage = page - math.floor(int(pagesToShow)/2)

				if currentPage < 1 : currentPage = 1
				if (currentPage + pagesLeft > numPages + 1): currentPage = numPages -pagesLeft +1
				while pagesLeft != 0 and currentPage <= numPages:
					if currentPage == page:
						paginationContainer += f'''<li class="waves-effect active" style='background:green;'>
						<a>{currentPage}</a>
						</li>'''
					else:
						paginationContainer += f'''<li class="waves-effect">
						<a href='/search?term={term}&type={type1}&page={currentPage}'>
						<spans>{currentPage}</span>
						</a>
						</li>'''
					currentPage += 1
					pagesLeft -= 1
				return render_template('search.html', term=term,type1=type1,searchTime=searchTime,numResults=numResults,resultsHtml=resultsHtml,numPages=numPages,pagesLeft=pagesLeft,currentPage=currentPage,paginationContainer=paginationContainer)
		elif type1 == 'images':
			numResults = searcher.getImageNumResults(term.lower())
			searchTime, resultsHtml, pageSize= searcher.getImageResultsHtml(page, term.lower())
			searchTime = str(searchTime)[:4]
			pagesToShow = 10
			paginationContainer =''
			page = int(page)	
			numPages = math.ceil(int(numResults)/int(pageSize))
			pagesLeft = min(int(pagesToShow), int(numPages))
			currentPage = page - math.floor(int(pagesToShow)/2)

			if currentPage < 1 : currentPage = 1
			if (currentPage + pagesLeft > numPages + 1): currentPage = numPages -pagesLeft +1
			while pagesLeft != 0 and currentPage <= numPages:
				if currentPage == page:
					paginationContainer += f'''<li class="waves-effect active" style='background:green;'>
						<a>{currentPage}</a>
						</li>
					'''
				else:
					paginationContainer += f'''<li class="waves-effect">
						<a href='/search?term={term}&type={type1}&page={currentPage}'>
						<spans>{currentPage}</span>
						</a>
						</li>'''
				currentPage += 1
				pagesLeft -= 1
			return render_template('search.html', term=term,type1=type1,searchTime=searchTime,numResults=numResults,resultsHtml=resultsHtml,numPages=numPages,pagesLeft=pagesLeft,currentPage=currentPage,paginationContainer=paginationContainer)
			# return 'COMING SOON!!'
		elif type1 == 'torrents':
			numResults = searcher.getTorrentNumResults(term.lower())
			searchTime, resultsHtml, pageSize= searcher.getTorrentResultsHtml(page, term.lower())
			searchTime = str(searchTime)[:4]
			pagesToShow = 10
			paginationContainer =""
			page = int(page)	
			numPages = math.ceil(int(numResults)/int(pageSize))
			pagesLeft = min(int(pagesToShow), int(numPages))
			currentPage = page - math.floor(int(pagesToShow)/2)

			if currentPage < 1 : currentPage = 1
			if (currentPage + pagesLeft > numPages + 1): currentPage = numPages -pagesLeft +1
			while pagesLeft != 0 and currentPage <= numPages:
				if currentPage == page:
					paginationContainer += f'''
						<li class="waves-effect active" style='background:green;'>
						<a>{currentPage}</a>
						</li>
					'''
				else:
					paginationContainer += f'''
						<li class="waves-effect">
						<a href='/search?term={term}&type={type1}&page={currentPage}'>
						<spans>{currentPage}</span>
						</a>
						</li>
					'''
				currentPage += 1
				pagesLeft -= 1
			return render_template('search.html', term=term,type1=type1,searchTime=searchTime,numResults=numResults,resultsHtml=resultsHtml,numPages=numPages,pagesLeft=pagesLeft,currentPage=currentPage,paginationContainer=paginationContainer)
		else:
			return '404'	

@app.route('/ajax/updateImageCount', methods=['POST'])
def updateImageCount():
	if request.method == 'POST':
		if request.form['imageUrl'] == '':
			print('BLANK URL')
			return ''
		print(f'URL of Image Clicked :: {request.form["imageUrl"]}')
		ajaxUpdater = AjaxUpdater.AjaxUpdater('google.db')
		updateImageStatus = ajaxUpdater.updateImageCount(request.form['imageUrl'])
	return ''

@app.route('/ajax/setBroken', methods=['POST'])
def setBroken():
	if request.method == 'POST':
		if request.form['src'] == '':
			print('BLANK URL')
			return '' #Error
		print(f'Broken URL :: {request.form["src"]}')
		ajaxUpdater = AjaxUpdater.AjaxUpdater('google.db')
		setBrokenStatus = ajaxUpdater.setBroken(request.form['src'])
		return request.form['src']	
	return ''
if __name__ == "__main__":
    app.run(debug=True)