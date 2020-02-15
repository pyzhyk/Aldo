#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import json
import random
import string
import logging
import subprocess
from time import sleep
import wikipedia
import configparser
from langdetect import detect

import telegram
from telegram.error import NetworkError, Unauthorized

import speech_recognition as sr
from watson_developer_cloud import VisualRecognitionV3

from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response
from chatterbot.trainers import ListTrainer
from chatterbot.comparisons import JaccardSimilarity, LevenshteinDistance

update_id = None

config = configparser.ConfigParser()
config.read('config.ini')

chatbot = ChatBot(
    'Aldo',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": LevenshteinDistance,
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.1
        }
    ],
    preprocessors = [
        'chatterbot.preprocessors.clean_whitespace'
    ],
    filters=[
        'chatterbot.filters.RepetitiveResponseFilter'
    ],
    database_uri='mongodb://127.0.0.1:27017/chatbot',
    response_selection_method=get_random_response
)

trainer = ListTrainer(chatbot)
trainer.train([
    "What's your name?", "My name is Aldo.",
    "What is your name?", "My name is Aldo.",
    "What's your name?", "Aldo.",
    "What is your name?", "Aldo.",
    ])

    # Your IMB Watson API Key
visual_recognition = VisualRecognitionV3(
    '2018-03-19',
    iam_apikey=config['api']['watson'])

def internet_search(query):
    f = open("wiki-queries.txt", "a")
    try:
        #query_lang = detect(query)
        wikipedia.set_lang('en')
        page = wikipedia.page(query)
        summary = wikipedia.summary(query, sentences=2)
        f.write("- - " + query + "\n")
        f.write("  - " + summary + "\n")
        return summary + "...\n\n" + "Read more at: " + page.url
        f.close()
    except:
        for newquery in wikipedia.search(query):
            try:
                #newquery_lang = detect(newquery)
                wikipedia.set_lang('en')
                page = wikipedia.page(newquery)
                summary = wikipedia.summary(newquery, sentences=2)
                f.write("- - " + newquery + "\n")
                f.write("  - " + summary + "\n")
                return summary + "...\n\n" + "Read more at: " + page.url
                f.close()
            except:
                return "I don't know about it"

def fix_capitalization(usrStr):
    numLetters = 0
    newstr = []
    for s in usrStr.split('. '):
        tmp = re.sub('^(\s*\w+)', lambda x:x.group(1).title(), s)
        newstr.append(tmp)
        if s.lstrip()[0] != tmp.lstrip()[0]:
            numLetters += 1
    return '. '.join(newstr).replace(' i ', ' I ')

def main():
    global update_id
    # Telegram Bot Authorization Token
    bot = telegram.Bot(config['api']['telegram'])
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            loop(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            update_id += 1

def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def loop(bot):
    global update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        if update.message:
            print(type(update.message.text))
            if update.message.photo:
                try:
                    filename = "images/" + update.message.from_user.first_name + "_" + randomString() + ".jpg"
                    photo_file = update.message.photo[-1].get_file()
                    photo_file.download(filename)
                    print(filename)
                    with open(filename, 'rb') as images_file:
                        classes = visual_recognition.classify(
                        images_file,
                        threshold='0.6',
                	    classifier_ids='default').get_result()
                        images = classes["images"][0]
                        classifiers = images["classifiers"][0]
                        ii = 0
                        message = ""
                        len_cl = 0
                        for i in classifiers["classes"]:
                            len_cl = len_cl + 1
                        print(len_cl)
                        while ii < len_cl:
                            print(ii)
                            classes = classifiers["classes"][ii]
                            img_class = classes["class"]
                            score = classes["score"]
                            message = message + img_class + " - " + "{0:.0%}".format(score) + "\n"
                            ii = ii + 1
                        update.message.reply_text(message)
                        os.remove(filename)
                except:
                    pass
            elif update.message.text:
                if update.message.text == '/start':
                    update.message.reply_text('Hello, ' + update.message.from_user.first_name + ". I am state-of-the-art artificial intelligence bot. How are you doing?")
                elif update.message.text == '/help':
                    update.message.reply_text('Look what I can do, ' + update.message.from_user.first_name + ":\n• Intelligent text chat\n• Voice recognition\n• Wikipedia search: just type 'search for smth'\n• Image recognition. Send me an image and I'll try to detect objects on it.\n\nSource code can be found at: github.com/pyzhyk/aldo")
                else:
                    if "search for" in str.lower(update.message.text):
                            query = str(update.message.text).split('search for ', 2)[0]
                            intrnt_srch = internet_search(str.lower(query))
                            if not intrnt_srch:
                                update.message.reply_text("Sorry, I cannot find '" + query + "' in Wikipedia.")
                            else:
                                update.message.reply_text(intrnt_srch)
                    else:
                        user_input = update.message.text
                        print(update.message.from_user.first_name + ": " + user_input)
                        chatbot_response = fix_capitalization(str(chatbot.get_response(user_input)))
                        update.message.reply_text(chatbot_response)
                        print("Bot: " + str(chatbot_response))
            elif update.message.voice:
                r = sr.Recognizer()
                filename = "voices/" + update.message.from_user.first_name + "_" + randomString()
                voice_ogg = filename + ".ogg"
                voice_wav = filename + ".wav"
                voice_file = update.message.voice.get_file()
                voice_file.download(voice_ogg)
                print(voice_ogg)

                ffmpegCommand = "ffmpeg -i " + voice_ogg + "  " + voice_wav
                process = subprocess.Popen(ffmpegCommand.split(), stdout=subprocess.PIPE)
                output, error = process.communicate()

                print(voice_wav)
                with sr.WavFile(voice_wav) as source:
                        audio = r.listen(source)
                        print(type(audio))
                try:
                        recognized = r.recognize_google(audio)
                        print(recognized)
                        chatbot_response = fix_capitalization(str(chatbot.get_response(recognized)))
                        update.message.reply_text(chatbot_response)
                        os.remove(voice_wav)
                        os.remove(voice_ogg)
                except:
                        update.message.reply_text("I cannot recognize your speech.")
            else:
                update_id = update.update_id + 1

if __name__ == '__main__':
    main()
