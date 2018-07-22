from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response
import extractheadline
from chatterbot.conversation import Statement
import datetime
import sqlite3
from sqlite3 import Error
# Uncomment the following lines to enable verbose logging
# import logging
# logging.basicConfig(level=logging.INFO)

# Create a new instance of a ChatBot

bot = ChatBot('News Bot', response_selection_method=get_random_response)

#conv = open('testfile.txt', 'r').readlines()

#bot.set_trainer(ListTrainer)

#bot.train(['hi', '<a href="google.co,">lalala</a>'])

bot.set_trainer(ChatterBotCorpusTrainer)
##

extractheadline.main()
bot.train(
     "chatterbot.corpus.english",
     # "chatterbot.corpus.english.humor",
     # "chatterbot.corpus.english.emotion",
     # "chatterbot.corpus.english.food",
     # "chatterbot.corpus.english.conversations",
     # "D:\TARUC\Sem 1\BACS2003 Artificial Intelligence\ChatBot part 2\profile.yml",
     # "D:\TARUC\Sem 1\BACS2003 Artificial Intelligence\ChatBot part 2\politics.yml",
    "D:\TARUC\Sem 1\BACS2003 Artificial Intelligence\ChatBot part 2\headlines.yml"
 )
today_date = datetime.datetime.today().strftime('%A %d %B %Y')
print(today_date)
try:
    conn = sqlite3.connect("db.sqlite3")
except Error as e:
    print(e)

cur = conn.cursor()
cur.execute("SELECT COUNT(text) FROM statement WHERE text = \'" + today_date + "\'")

rows = cur.fetchone()

#for row in rows:
print(rows)

rr, = rows
print(rr)

# while True:
#     request = input('You: ')
#
#     if("bye" in request.lower() or "goodbye" in request.lower()):
#         break
#
#     response = bot.get_response(request)
#     # statement = Statement(request)
#     # confidence_level = bot.logic.process(statement)
#     # print(confidence_level)
#
#     # statement = bot.input.process_input(request)
#     # confidence, response = bot.logic.process(statement)
#     print(response.confidence)
#
#     print('Bot: ', response)
