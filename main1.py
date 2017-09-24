from summarizer import textranker
import telepot
from telepot.loop import MessageLoop
import time
import os
from chatdb import DBHelper 
import MySQLdb

db = DBHelper()

bot = telepot.Bot("386469540:AAH9X1I7y76sDZ2TQsFhJ_4Z9J7hpU6-oww")

def startSummarise(chat_id):
	db.conn = MySQLdb.connect("localhost", "prof", "p@ssword", "ChatDB")
	db.cursor = db.conn.cursor()
	summaryString = textranker("ChatDB")
	if summaryString == "[]": #output will be [] if there is not enough data
		bot.sendMessage(chat_id,"Not enough messages for me to summarise la dei, so few messages also lazy to read ah?")
	else:
		bot.sendMessage(chat_id,summaryString)

def handle(msg):
	content_type , chat_type ,chat_id = telepot.glance(msg)
	if content_type == "text":
		messages = msg["text"]
		if messages == "/summarise":
			db.conn = MySQLdb.connect("localhost", "root", "p@ssword", "ChatDB")
			db.cursor = db.conn.cursor()
			startSummarise(chat_id)
		elif messages == "/clear":
			db.conn = MySQLdb.connect("localhost", "root", "p@ssword", "ChatDB")
			db.cursor = db.conn.cursor()
			db.remove_Message(chat_id, messages)
		elif messages[0] != "/": #ignore messages starting with /
			db.conn = MySQLdb.connect("localhost", "root", "p@ssword", "ChatDB")
			db.cursor = db.conn.cursor()
			db.add_Message(chat_id,messages)
			db.update_Message(chat_id, messages)

MessageLoop(bot,{"chat":handle}).run_as_thread()
print ("I'm awake and currently collecting your chats")
while 1:
	time.sleep(10)