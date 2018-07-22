from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from chatterbot.response_selection import get_random_response
import wikipediatest
import extractheadline
from difflib import SequenceMatcher
import datetime
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
app.debug = True
news_bot = ChatBot("News Bot",
                   storage_adapter="chatterbot.storage.SQLStorageAdapter",
                   response_selection_method=get_random_response,)

#english_bot.train("chatterbot.corpus.english")


@app.route("/")
def home():
    return render_template("/index.html")

@app.route("/get")
def get_bot_response():

    user_text = request.args.get('msg')
    print(user_text)
    if(user_text == "" or user_text == "\n"):
        return "Sorry, I don't understand."


    # First check is headline question
    headline_question = ["What is the news headline today?",
                        "News headline today?",
                        "Tell me a current news",
                        "Tell me today news",
                        "Give me another news"]
    ratio = []
    for i in headline_question:
        seq = SequenceMatcher(None, user_text.lower(), i.lower())
        ratio.append(seq.ratio() * 100)

    print("headline_question ratio: " + str(max(ratio)))
    if max(ratio) > 70:
        # Check is today headlines already extracted
        today_date = datetime.datetime.today().strftime('%A %d %B %Y')

        try:
            conn = sqlite3.connect("db.sqlite3")
        except Error as e:
            print(e)

        cur = conn.cursor()
        cur.execute("SELECT COUNT(text) FROM response WHERE text = \'" + today_date + "\'")

        rows = cur.fetchone()

        # for row in rows:
        rr, = rows
        response = news_bot.get_response(today_date)

        print(today_date)
        print(response)
        print("rr: " + str(rr))
        # If no today headlines
        if rr <= 0:
            extractheadline.main()

            # Train
            news_bot.set_trainer(ChatterBotCorpusTrainer)
            news_bot.train("D:\TARUC\Sem 1\BACS2003 Artificial Intelligence\ChatBot part 2\headlines.yml")

            response = news_bot.get_response(today_date)
            print(response)

        return str(response)

    # if not headline question,
    response = news_bot.get_response(user_text)

    print(str(response) + "\tConfidence value: " + str(response.confidence))
    if response.confidence >= 0.80:
        return str(response)
    else:
        wiki_result = wikipediatest.main(user_text)

        if wiki_result[0]:
            news_bot.set_trainer(ListTrainer)
            news_bot.train([user_text, wiki_result[1]])
            print(wiki_result[1])

            return wiki_result[1]
        else:
            return "Sorry, I don't understand."


# @app.route("/test")
# def test1():
#     return "test success"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
