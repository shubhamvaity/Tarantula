import Searcher
searcher=Searcher.Searcher('google.db')
search_query = input('Enter search query: ')
searcher.query(search_query.lower())

