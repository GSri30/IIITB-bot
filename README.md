# IIITB-bot

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/GSri30/IIITB-bot/blob/main/LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-green)]("#")
[![Issues](https://img.shields.io/github/issues-raw/GSri30/IIITB-bot)](https://github.com/GSri30/IIITB-bot/issues)
[![Closed Issues](https://img.shields.io/github/issues-closed-raw/GSri30/IIITB-bot)](https://github.com/GSri30/IIITB-bot/issues)
[![PR's Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)]("#") 
[![Pull Requests](https://img.shields.io/github/issues-pr/GSri30/IIITB-bot)]("#")
[![Contributors](https://img.shields.io/github/contributors/GSri30/IIITB-bot)]("#")

A discord bot which can be used to avoid spam in university discord servers. Apart from basic verification, other features will be added eventually! Feel free to suggest (if any).
It has been deployed in IIITB servers and will soon be installed in IIITB discord server.

# 🛠️ Installation

Method 1:
1. Install pipenv
2. pipenv install
3. pipenv shell

Method 2:
Install using requirements.txt

Method 3:
1. docker-compose build
2. docker-compose up -d

# 🖮 Setup

- Create a discord application bot in discord developer portal.
- Invite the bot into your private discord server. (Make one if required)
- Create required roles and channels in your server. (Can use [my server template](https://discord.new/6rfHQhPEuqfz)) 
- Feel free to edit settings.py in accordance to your requirements.
- Fill the required environment variables
```
DISCORD_TOKEN=" "
# email-id
SENDER_ID=" "
SENDER_PASSWORD=" "
MYSQL_HOST=" "
MYSQL_DATABASE=" "
MYSQL_ROOT_USER=" "
MYSQL_ROOT_PASSWORD=" "

# channels
RULES=" "
WELCOME=" "
SAC=" "
REGISTRATION=" "
ADMIN_LOG=" "
DEVELOPERS=" "
CP=" "

# roles
ADMIN=" "
NEWBIE=" "

# guild
GUILD=" "

# Clist API
CLIST_USERNAME=" "
CLIST_KEY=" "

```
- RUN python3 Main.py




## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/GSri30/IIITB-bot/issues). 

## ☑️ Show your support

Give a ⭐️ if this project helped you!

## 📝 License

This project is [MIT](https://github.com/GSri30/IIITB-bot/blob/main/LICENSE) licensed.