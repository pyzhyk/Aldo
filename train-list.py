from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import logging
import sys

logging.basicConfig(level=logging.INFO)

bot = ChatBot(
    'Aldo',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    database_uri='mongodb://127.0.0.1:27017/chatbot'
)

trainer = ListTrainer(bot)

inpFile = sys.argv[1]

print('Using '+inpFile)

fileHandler = open(inpFile, "r")
lines = list()
while True:
	line = fileHandler.readline()
	#print(line)
	if not line :
		break;
	lines.append(line)

trainer.train(lines)
fileHandler.close()

print('Done.')
