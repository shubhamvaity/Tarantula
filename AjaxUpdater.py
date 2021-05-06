import sqlite3
import time
class AjaxUpdater:
	def __init__(self, dbname):
		self.con = sqlite3.connect(dbname)

	def __del__(self):
		self.con.close()

	def updateImageCount(self, imageUrl):
		if str(self.con.execute(f"UPDATE images SET clicks = clicks + 1 WHERE imageUrl='{imageUrl}'").rowcount) == '1':
			self.con.commit()
			return '1'
		else:
			return '0'

	def setBroken(self, src):
		if str(self.con.execute(f"UPDATE images SET broken=1 WHERE imageUrl='{src}'").rowcount) == '1':
			self.con.commit()
			return '1'
		else:
			return '0'