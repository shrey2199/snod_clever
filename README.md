<p align="center">
  <a href="https://heroku.com/deploy?template=https://github.com/shrey2199/snod_clever">
    <img src="https://img.shields.io/badge/Deploy%20To%20Heroku-blueviolet?style=for-the-badge&logo=heroku" width="200" />
  </a>
</p>
<p align="center">
  <a href="https://t.me/shrey_contact_bot">
    <img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" width="200" />
  </a>
</p>

# S.N.O.D Revision Bot

A Bot Made By :-
  1. Shreyansh
  2. Omkar
  3. Nischay
  4. Divyansh

## Deploy on Heroku

Use The Deploy to Heroku Button given at the TOP !!

Enter the Relevant Configurations and Deploy !!

## Run Locally

Installing Requirements.. 

    pip install -r requirements.txt

Then Edit config.py with variables listed below !

And then run the bot by 

    python3 bot.py

## Deploy with Docker

### Two Methods

#### Method 1

Edit config.py with variables listed below !

Build Docker Image.. 

    docker build . -t revisionbot

Run Docker Container.. 

    docker run --name revisionbot revisionbot

#### Method 2

Build Docker Image ..

    docker build . -t revisionbot

Run The Docker Container and Define the Variables in One Command

    docker run --name revisionbot -e BOT_TOKEN="<your_bot_token>" -e DATABASE_URL="<your_postgres_database_url>" -e WEBSITE_URL="<website_url_of_bot>" -d revisionbot

## Variables

- `BOT_TOKEN`
  - Values :- Valid BOT TOKEN Obtained from Botfather.
  - Default Value :- `"XXXXXXXXX:ABCDEFGHIJKLMNOPQRST"`
  - Use :- To connect to Telegram as BOT.

- `WEBSITE_URL`
  - Values :- URL of Server where Bot is deployed.
  - Use :- To Use Web UI of Bot Data.

## Bot Commands

`/start` - Welcome Message !!

`/help` - Get Instructions on How to Use to bot !!

## BotFather SetCommands

    start - To Start The Bot !
    help - To See the Instructions !
    revise - To Begin The Revision !
    id - To Get The ID & Pass For Web UI !
    result - To Get Result in Lost Case !
    changeid - To Change Existing Web UI Credentials !
