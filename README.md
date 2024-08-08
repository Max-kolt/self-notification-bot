# self-notification-bot

### Services:
 - [bot-handler](./bot-handler) - bot for processing telegram messages and dialog with the user
 - [notification](./bot-notification) - service for sending scheduled notifications

### Get started:

First of all, define your bot's 
TELEGRAM_TOKEN , API_ID and API_HASH 
of your telegram account in the [.env](.env) file

Docker: 
 - define your bot's TELEGRAM_TOKEN , API_ID and API_HASH 
   of your telegram account in the [.env](.env) file
 - run command `docker-compose up -d`

Manually:
 - *need python 3.11 and pip*  
 - start PostgreSQL server and create your database
 - define database info in [.env](.env) file
 - create virtual environment with command `python3.11 -m venv venv`
 - activate virtual environment with command:
   - `source venv/bin/activate` (Linux) 
   - `venv/bin/activate` (Windows)
 - Install project requirements with command: `pip install -r requirements.txt`
 - Run [bot-handler](./bot-handler) and [notification service](./bot-notification) individually with command `python main.py`
