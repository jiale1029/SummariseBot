#SummariseBot for Telegram
#CE1003 Assignment 1
#
#Purpose of the bot: The bot collects the chats and stored it on a localhost database according to the chat_id, and when the user asks for a summary,
#                    the bot will once again retrieve data from the database and summarise it using textranker.
#
#Author: Team Instant Summarisers
#Date Created: 20/9/2017 

from summarizer import textranker
import telepot
from telepot.loop import MessageLoop
from chatdb import DBHelper 
import MySQLdb
import time

db = DBHelper()

error = "Not enough text la dei, so few messages also you lazy to read?" #error code to be displayed

bot = telepot.Bot("321746669:AAHNwsV42SX_KOmkYaAYW1eCNH8ydWI6fsE")

def startSummarise(chat_id):
	db.__init__("ChatDB")
	textTuple = db.get_Message(chat_id,messages)  #gets messages from MySQL server
	textString = ' ~ '.join([''.join(x) for x in textTuple]) #converts the text from tuple to string format
	textString = unicode(textString,errors="ignore") 
	if textString == "": 
		bot.sendMessage(chat_id,error) #bot sends error when the database does not contain any messages
	else:
		summaryString = textranker(textString)
		print("Summary requested from " + chat_id)
		if summaryString == "[]": #output will be [] if there is not enough data, bot sends error message
			bot.sendMessage(chat_id,error)
		else:
			bot.sendMessage(chat_id,"Your requested summary has arrived! \n \n "+ summaryString[3:-2]) #bot sends summarised texts

def handle(msg):
	content_type , chat_type ,chat_id = telepot.glance(msg)
	if content_type == "text": #checks whether user entered text
		global messages
		messages = msg["text"] 
		chat_id= str(chat_id)
		if messages == "/summarise": #checks whether user entered summarise command
			db.__init__("ChatDB")
			startSummarise(chat_id)
		elif messages == "/clear": #checks whether use entered clear command
			db.__init__("ChatDB")
			db.remove_Message(chat_id, messages)
			bot.sendMessage(chat_id, "Messages have been cleared.")
		elif messages[0] != "/": #ignore messages starting with /, saves other messages into database.
			db.__init__("ChatDB")
			db.add_Message(chat_id,messages)
			print("Received "+messages+" from " + chat_id)

MessageLoop(bot,{"chat":handle}).run_as_thread()
print ("I'm awake and currently collecting your chats")
while 1:
	time.sleep(10) #keeps bot awake
