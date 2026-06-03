#  Discord Clicker Bot

![Python](https://img.shields.io/badge/Python-3.13-%233776AB) ![discord.py](https://img.shields.io/badge/discord.py-5865F2) ![SQLite](https://img.shields.io/badge/database-SQLite-003B57)

A clicker game for discord servers. Players click a button, compete on a leaderboard, and maybe get blessed. The game data is saved to a local SQLite database.

---

## Requirements

```
discord.py
python-dotenv
```

---

## Setup

**Clone the repository:**

```
git clone https://github.com/LucasdeOliveira03/Discord-Clicker.git
```

**Install dependencies:**

```
pip install -r requirements.txt
```

**Create a `.env` file** with the bot token:

```
TOKEN=Discord_bot_token
```

**Run the bot:**

```
python bot.py
```

> The database will be created automatically on the first run.

---

## Commands

| Command    | Description                                          |
|------------|------------------------------------------------------|
| `!clicker` | Spawns the click button in the channel. 				      |
| `!board`   | Displays the leaderboard.                            |
