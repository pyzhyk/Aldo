# [Aldo](https://github.com/pyzhyk/Aldo/)

[![License](https://img.shields.io/badge/license-GPL-yellow.svg)][license]

[license]: https://www.gnu.org/licenses/gpl.html


#### State-of-the-art artificial intelligence bot

[![Screenshot-1](https://raw.githubusercontent.com/pyzhyk/Aldo/master/screenshot.jpg)](https://raw.githubusercontent.com/pyzhyk/Aldo/master/screenshot.jpg)

## Prerequisites

- MongoDB – [docs.mongodb.com/manual/installation](https://docs.mongodb.com/manual/installation/)
- IBM Watson account – [ibm.com/watson](https://www.ibm.com/watson)
- Telegram Bot – [core.telegram.org/bots](https://core.telegram.org/bots#6-botfather)

## Getting started

- Install python3.6 and ffmpeg
```bash
apt install python3.6 python3-pip ffmpeg
```
- Install python libraries
```bash
pip3 install --upgrade nltk SpeechRecognition langdetect "watson-developer-cloud>=2.4.1" wikipedia chatterbot chatterbot_corpus python-telegram-bot
```
- Clone the repository
```bash
git clone https://github.com/pyzhyk/aldo
```
- Put your IBM Watson API Key and Telegram Bot Token in `config.ini`
```
[api]
watson = WATSON_API_KEY
telegram = TELEGRAM_BOT_TOKEN
```

## Training your bot:
- English corpus + chat and jokes yaml training
```bash
python3.6 train.py chatterbot.corpus.english
python3.6 train.py train/chat.yml
python3.6 train.py train/jokes.yml
```
- Txt list file training
```bash
python3.6 train-list.py train/movies1.txt
```

## Running your bot:
```bash
python3.6 bot.py
```

## Donate
![](https://pyzhyk.org/img/14s7eocgkPRXxbwMrjykmpkZixWDu5rGiY-256.png)

BTC [14s7eocgkPRXxbwMrjykmpkZixWDu5rGiY](bitcoin:14s7eocgkPRXxbwMrjykmpkZixWDu5rGiY)
