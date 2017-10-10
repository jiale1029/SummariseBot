
#SummariseBot for Telegram
#CE1003 Assignment 1
#
#Purpose of the bot: The bot collects the chats and stored it on a localhost MySQL database according to the chat_id, and when the user asks for a summary,
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
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

db = DBHelper()
summaryString = ""
current_id="butthole"
error = "Not enough text la dei, so few messages also you lazy to read?" #error code to be displayed
bot = telepot.Bot("431724541:AAGI1UK2P7PlG3Klg4fHKe3tlxO8wUFo7Lk")

def startSummarise(chat_id):
	db.__init__("ChatDB")
	textTuple = db.get_Message(chat_id,messages)  #gets messages from MySQL server
	textString = '. '.join([' '.join(x) for x in textTuple]) #converts the text from tuple to string format
	textString = unicode(textString,errors="ignore") 
	if textString == "":
		bot.sendMessage(chat_id,error) #bot sends error when the database does not contain any messages
	else:
		summaryString = textranker(textString)
		summaryString = format(summaryString)
		print("Summary requested from " + chat_id)
		if summaryString == "[]": #output will be [] if there is not enough data, bot sends error message
			bot.sendMessage(chat_id,error)
		else:
			string = string[1:-1]
			bot.sendMessage(chat_id,"Your requested summary has arrived! \n \n "+ summaryString) #bot sends summarised texts

def handle(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	chat_id = str(chat_id)
	if content_type == "text": #checks whether user entered text
		global messages
		messages = msg["text"]
		if messages[:13] == "@SummarierBot": #checks whether user called bot
			keyboard = InlineKeyboardMarkup(inline_keyboard=[
				[dict(text='Summarise messages', callback_data='summarise')],
				[dict(text='Clear messages', callback_data='clear')],[dict(text="Send feedback", callback_data='feedback')]])
			bot.sendMessage(chat_id,"Hey guys, what can I do for you?",reply_markup=keyboard)
		elif messages[:9] == "/feedback": #checks for feedback command and sends it to our feedback group.
			bot.sendMessage(-263652411, messages[9:] + " received from " + chat_id)
		elif messages[0] != "/": #ignore messages starting with /, saves other messages into database.
			db.__init__("ChatDB")
			db.add_Message(chat_id,messages)
			print("Received "+messages+" from " + chat_id)

def format(string):
	string = string.replace("u'","")
	string = string.replace("u\"","")
	string = string.replace("\\n"," ")
	string = string.replace("!'","!")
	string = string.replace("!\"","!")
	string = string.replace("!,","!")
	string = string.replace("?'","?")
	string = string.replace("?\"","?")
	string = string.replace("?,","?")
	string = string.replace(".',",".")
	string = string.replace(".\",",".")
	string = string.replace("!.","!")
	string = string.replace("?.","?")
	return string

def on_callback_query(msg):
	query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
	chat_id = telepot.origin_identifier(msg)
	chat_id = chat_id[0]
	chat_id = str(chat_id)
	print(query_data + " requested from " + chat_id)
	if query_data == "summarise":
		db.__init__("ChatDB")
		startSummarise(chat_id)
	elif query_data == "clear":
		db.__init__("ChatDB")
		db.remove_Message(chat_id, messages)
		bot.sendMessage(chat_id, "Messages have been cleared.")
	elif query_data == "feedback":
		bot.sendMessage(chat_id,"Type \'/feedback [your feedback here]\' to send us some feedback!")

MessageLoop(bot,{"chat":handle,'callback_query':on_callback_query}).run_as_thread()
print ("I'm awake and currently collecting your chats")
while 1:
	time.sleep(10) #keeps bot awake


