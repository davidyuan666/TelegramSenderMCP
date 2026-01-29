# PetriCode - Telegram Bot Framework

A Python-based Telegram bot framework for message interaction and external information retrieval.

## Features

- 🤖 Easy-to-use Telegram bot interface
- 📡 External API integration
- 🔄 Asynchronous message handling
- 🌐 Web scraping capabilities
- 📊 Data processing and formatting

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and configure your bot token:
```bash
cp petircode/.env.example petircode/.env
```

4. Edit `.env` and add your Telegram bot token

## Usage

```bash
python -m petircode.main
```

## Configuration

Edit `petircode/.env` file:
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token from @BotFather
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

## Project Structure

```
petircode/
├── __init__.py
├── main.py          # Entry point
├── bot.py           # Bot core logic
├── config.py        # Configuration management
├── handlers/        # Message handlers
├── services/        # External services
└── utils/           # Utility functions
```
