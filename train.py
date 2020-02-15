from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging
import sys

logging.basicConfig(level=logging.INFO)

bot = ChatBot(
    'Aldo',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    database_uri='mongodb://127.0.0.1:27017/chatbot'
)

trainer = ChatterBotCorpusTrainer(bot)

inpFile = sys.argv[1]

trainer.train(inpFile)

print("Done.")
