from summarizer import textranker
import telepot
from telepot.loop import MessageLoop
import time
import os
from chatdb import DBHelper 
import MySQLdb

db = DBHelper()

bot = telepot.Bot("321746669:AAHNwsV42SX_KOmkYaAYW1eCNH8ydWI6fsE")

def startSummarise(chat_id):
	db.conn = MySQLdb.connect("localhost", "root", "p@ssword", "ChatDB")
	db.cursor = db.conn.cursor()
	textTuple = db.get_Message(chat_id,messages)
	textString =str(textTuple)
	summaryString = textranker(textString)
	if summaryString == "[]": #output will be [] if there is not enough data
		bot.sendMessage(chat_id,"Not enough text la dei, so few messages also you lazy to read?")
	else:
		bot.sendMessage(chat_id,summaryString)

def handle(msg):
	content_type , chat_type ,chat_id = telepot.glance(msg)
	if content_type == "text":
		global messages
		messages = msg["text"]
		chat_id= str(chat_id)
		if messages == "/summarise@SummarierBot":
			db.__init__("ChatDB")
			startSummarise(chat_id)
		elif messages == "/clear@SummarierBot":
			db.__init__("ChatDB")
			db.remove_Message(chat_id, messages)
			bot.sendMessage(chat_id, "Messages have been cleared.")
		elif messages[0] != "/": #ignore messages starting with /
			db.__init__("ChatDB")
			db.add_Message(chat_id,messages)
			print("Received "+messages+" from " + chat_id)

MessageLoop(bot,{"chat":handle}).run_as_thread()
print ("I'm awake and currently collecting your chats")
while 1:
	time.sleep(10)
