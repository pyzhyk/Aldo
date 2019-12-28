from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging

logging.basicConfig(level=logging.INFO)

bot = ChatBot(
    'Peter',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    database_uri='mongodb://127.0.0.1:27017/chatbot'
)

trainer = ChatterBotCorpusTrainer(bot)

trainer.train(
	"chatterbot.corpus.english",
    "./train/chat.yml",
    "./train/jokes.yml",
)

print("Done.")