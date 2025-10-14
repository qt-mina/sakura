# 📂 Project Structure

```
sakurachat-bot/
├── .github/                 # GitHub workflows and configurations
│   ├── README.md            # General information about the GitHub setup
│   └── workflows/           # CI/CD workflows
│       ├── README.md        # Information about the workflows
│       └── redeploy.yml     # Workflow for redeployment
├── Sakura/                  # Core bot package <--- You are here
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
