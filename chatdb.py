import MySQLdb
import os

class DBHelper:
	def __init__(self, dbname = "ChatDB"):
		self.conn = MySQLdb.connect("localhost", "root", "p@ssword", "ChatDB")
		self.cursor = self.conn.cursor()
		self.conn.set_character_set('utf8')
		self.cursor.execute('SET NAMES utf8;')
		self.cursor.execute('SET CHARACTER SET utf8;')
		self.cursor.execute('SET character_set_connection=utf8;')

	def add_Message(self, chat_id, messages):
		try:
			add = "INSERT INTO content(chat_id, messages) VALUES ('"'%s'"','"'%s'"')" %(chat_id,messages)
			self.cursor.execute(add) 
			self.conn.commit()
		except MySQLdb.Error as er:
			print("Got error when adding message")

	def remove_Message(self, chat_id, messages):
		try:
			delete = """DELETE FROM content WHERE chat_id = %s""" %chat_id
			self.cursor.execute(delete)
			self.conn.commit()
		except MySQLdb.Error as er:
			print("Got error when clearing message")

	def update_Message(self, chat_id, messages):
		update = "SELECT chat_id, GROUP_CONCAT(messages SEPARATOR ';') FROM content GROUP BY chat_id"
		self.cursor.execute(update) 
		self.conn.commit()
	
