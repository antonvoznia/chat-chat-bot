# Bonus assignment stage 5

## The assignment

1. Your task is to write the bot code and the controller code. The bot will be the infected computer, and the controller is what you use to control the bots.

2. Both parts should use gist.github.com to communicate.

3. The goal is to run some of your bots as 'infected' computers in the github channel, and you also connect to this channel with your controller to control them.

4. The communication between the bots and the controller should not be easily detected as 'bots' in the channel, therefore all communication should look like normal English markdown or text (text, images and emojis are accepted). You should use some steganography technique to hide your messages as English.

5. The controller should check if the bots are alive periodically

6. The controller should give orders to the bot and the bot should answer the output of the orders
The minimum orders are the following commands:
	- w (list of users currently logged in)
	- ls <PATH> (list content of specified directory)
	- id (if of current user)
	- Copy a file from the bot to the controller. The file name is specified
	- Execute a binary inside the bot given the name of the binary. Example: ‘/usr/bin/ps’

7. Publish the whole code in GitHub and put the link as a flag for this stage.

## Usage

The bot and controller use GitHub Gist for communication.
I created private gist for a testing:
https://gist.github.com/antonvoznia/b49c44a9d3e4bdb097826cccb121cc38

to start not-bot.py 

```
python not-bot.py GITHUB_TOKEN GIST_ID USER PASSWORD
```

to start not-controller.py
```
python not-controller.py GITHUB_TOKEN GIST_ID
```

####GITHUB_TOKEN
To execute the bot you need to use own GitHub token:
https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

####GIST_ID
In my case it is b49c44a9d3e4bdb097826cccb121cc38

####USER and PASSWORD and IP
The username and a password and an ip of a machine where to copy the file via get command (see bellow)

####not-controller.py
contains the next commands
* --help - prints
* ping - to check if is alive bot'
* delete - to clear the gist and delete all messages
* get <path_to_file> - to copy a file in <path_to_file> from a bot to /tmp/ directory
* cmd - execute a bash command where 'cmd' - a bash command