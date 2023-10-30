## Time Bot

A Discord bot to check each other's time

## How to setup

rename the `.env.example` file to `.env` and enter your `Bot token`, `prefix` (default=!) And `Mongodb uri`.

### Create Virtual environment (OPTIONAL)

Linux

```bash
python3 -m venv .venv
source .venv/bin/activate

```
Windows

```ps
python -m venv .venv
.venv/Scripts/activate

```

### install dependencies

```bash
pip install -r requirements.txt

```

OR

```bash
poetry install

```

### Start the bot

Linux

```bash
python3 -m bot.main

```
Windows

```ps
python -m bot.main

```
