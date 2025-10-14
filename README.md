# 🌸 Sakura - A Telegram Bot  
[![Telegram Bot](https://img.shields.io/badge/Chat%20Now-@SluttySakuraBot-fd79a8?logo=telegram&style=for-the-badge)](https://t.me/SluttySakuraBot)  
[![GitHub Created At](https://img.shields.io/github/created-at/qt-sakura/sakurachat-bot?style=for-the-badge&logo=github&label=Created&color=orange)](https://github.com/qt-sakura/sakurachat-bot)

**Sakura Bot** is your soft, helpful, and caring conversational partner, embodying Sakura Haruno's supportive and gentle persona.
From heartfelt check-ins to playful sticker replies — Sakura's got you covered.

---

## 💡 Overview

Whether you're looking to:
- Experience a one-on-one chat with Sakura Haruno  
- Get thoughtful and caring replies
- Enjoy spontaneous sticker reactions in private or group chats  
- Or immerse yourself in a supportive, gentle, and helpful "Sakura" persona...

**Sakura Bot** brings emotional depth, playful fun, and a caring energy right into your Telegram chat window.

> **"Every line feels like her lips are almost touching yours—yet holding the kiss."** 🌙💖

---

## ✨ Features

- **Contextual AI-Powered Conversations** — Powered by **Google Gemini** and **ElevenLabs**, Sakura provides thoughtful, context-aware responses tailored to the conversation.
- **Image, Poll, and Voice Message Analysis** — Send an image, poll, or voice message, and Sakura will analyze and comment on it.
- **Contextual Emoji Reactions** — The bot automatically reacts to messages with animated emojis that match the context of the conversation.
- **Sticker-Reply Support** — Reply to Sakura's messages with a sticker, and she'll send one back.
- **Telegram Stars Integration** — Support the bot using Telegram Stars with the `/meow` command.
- **Supporter Leaderboard** — View the top supporters with the `/fams` command.
- **Group / Private Chats** — Sakura responds in private DMs or when "Sakura" is mentioned or replied to in a group.
- **Enhanced Performance** — A robust backend with a **PostgreSQL** database and a **Valkey** cache ensures a fast and persistent user experience.

---

## 🛠️ Commands

| Command      | Description                                   |
|--------------|-----------------------------------------------|
| `/start`     | Wake up Sakura and get a welcome message 🌸    |
| `/help`      | Show usage instructions and a short guide 💁   |
| `/ping`      | Check the bot's response time 🏓               |
| `/meow`       | Support the bot with Telegram Stars ⭐        |
| `/fams`    | View the list of top supporters 🏆             |

---

## ⚙️ Tech Stack

- **Language:** Python 3.8+
- **Core Libraries:** `Kurigram`, `aiohttp`
- **AI APIs:** Google Gemini, ElevenLabs
- **Database:** PostgreSQL (via `asyncpg`)
- **Caching:** Valkey (a high-performance Redis fork)
- **Performance:** `uvloop` (for asyncio event loop), `orjson` (for fast JSON processing)
- **Hosting:** Any server or VPS that supports Python.

---

## 📂 Project Structure

```
sakurachat-bot/
├── .github/                 # GitHub workflows and configurations
│   ├── README.md            # General information about the GitHub setup
│   └── workflows/           # CI/CD workflows
│       ├── README.md        # Information about the workflows
│       └── redeploy.yml     # Workflow for redeployment
├── Sakura/                  # Core bot package
│   ├── __main__.py          # Main entry point
│   ├── __init__.py          # Package initialization
│   ├── state.py             # Bot state management
│   │
│   ├── Core/                # Core functionality and utilities
│   │   ├── __init__.py
│   │   ├── config.py        # Configuration and environment variables
│   │   ├── logging.py       # Custom colored logging setup
│   │   ├── utils.py         # General utility functions
│   │   ├── helpers.py       # Bot-specific helper functions
│   │   ├── errors.py        # Error handling and custom exceptions
│   │   ├── server.py        # Dummy HTTP server for deployment
│   │   └── authentication.py # Owner/user authentication
│   │
│   ├── Database/            # Data management and persistence
│   │   ├── __init__.py
│   │   ├── database.py      # PostgreSQL database operations
│   │   ├── valkey.py        # Valkey/Redis cache operations
│   │   ├── sessions.py      # User session management
│   │   ├── cache.py         # Caching layer and utilities
│   │   ├── constants.py     # Data constants and storage utilities
│   │   ├── conversation.py  # Conversation history management
│   │   └── keys.py          # Redis key management
│   │
│   ├── Chat/                # AI integrations and responses
│   │   ├── __init__.py
│   │   ├── response.py      # Main AI response coordination
│   │   ├── chat.py          # Unified AI chat client
│   │   ├── prompts.py       # Character prompts and AI instructions
│   │   ├── images.py        # Image analysis and processing
│   │   ├── polls.py         # Poll analysis functionality
│   │   └── voice.py         # Voice message processing
│   │
│   ├── Modules/             # User interface and interactions
│   │   ├── __init__.py
│   │   ├── handlers.py      # Message and update handlers
│   │   ├── commands.py      # Command implementations
│   │   ├── callbacks.py     # Callback query handlers
│   │   ├── keyboards.py     # Inline keyboard creation
│   │   ├── messages.py      # Message templates and constants
│   │   ├── reactions.py     # Emoji reactions and contextual responses
│   │   ├── stickers.py      # Sticker handling and responses
│   │   ├── effects.py       # Pyrogram effects and animations
│   │   ├── typing.py        # Chat action indicators
│   │   ├── updates.py       # Update processing and routing
│   │   ├── image.py         # Image handling
│   │   ├── poll.py          # Poll handling
│   │   └── payments.py      # Telegram Stars payment handling
│   │
│   └── Services/            # Bot services and specialized functions
│       ├── __init__.py
│       ├── broadcast.py     # Broadcasting to users/groups
│       ├── tracking.py      # User and chat tracking
│       ├── limiter.py       # Rate limiting and spam protection
│       ├── cleanup.py       # Memory and data cleanup tasks
│       └── stats.py         # Bot statistics and monitoring
│
├── requirements.txt         # Dependencies
├── Dockerfile               # Docker container configuration
├── Procfile                 # Process file for deployment
├── example.env              # Example environment variables
└── README.md                # Project documentation
```

---

## 🌸 Sakura Bot

A cute and charming Telegram bot that brings soft chats, sweet flirts, and a cozy vibe to your day.

---

## 🚀 Getting Started

1.  **Visit [@SluttySakuraBot](https://t.me/SluttySakuraBot) on Telegram.**
2.  **Press `/start`** to wake her up.
3.  **Chat freely** or use commands like `/help` to explore.
4.  **Enjoy** the conversation!

---

## 👤 Creator

Crafted with love by **Asadul Islam (Asad)**  
Telegram: [@asad_ofc](https://t.me/asad_ofc)

---

### 💌 Connect with Me

<p align="center">
  <a href="https://t.me/asad_ofc"><img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" /></a>
  <a href="mailto:mr.asadul.islam00@gmail.com"><img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" /></a>
  <a href="https://youtube.com/@asad_ofc"><img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" /></a>
  <a href="https://instagram.com/aasad_ofc"><img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white" /></a>
  <a href="https://tiktok.com/@asad_ofc"><img src="https://img.shields.io/badge/TikTok-000000?style=for-the-badge&logo=tiktok&logoColor=white" /></a>
  <a href="https://x.com/asad_ofc"><img src="https://img.shields.io/badge/X-000000?style=for-the-badge&logo=twitter&logoColor=white" /></a>
  <a href="https://facebook.com/aasad.ofc"><img src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white" /></a>
  <a href="https://www.threads.net/@aasad_ofc"><img src="https://img.shields.io/badge/Threads-000000?style=for-the-badge&logo=threads&logoColor=white" /></a>
  <a href="https://discord.com/users/1067999831416635473"><img src="https://img.shields.io/badge/Discord-asad__ofc-5865F2?style=for-the-badge&logo=discord&logoColor=white" /></a>
</p>

---

## 📄 License

This bot is built for wholesome fun and free use.  
**Attribution is appreciated — spread love, not shade.**

---

> **Sakura Bot** — *Soft talks. Sweet vibes.*  
[Start now → @SluttySakuraBot](https://t.me/SluttySakuraBot)
