NordVPN Support Assistant
A Retrieval-Augmented Generation (RAG) chatbot for providing support using NordVPN's Help Center documentation.
Features

Intelligent document retrieval using ChromaDB vector database
Context-aware responses using OpenAI's GPT-3.5 Turbo
Support for connectivity troubleshooting with country and device detection
Conversation history management
Comprehensive test suite for quality assurance
Memory-efficient document processing

Prerequisites

Python 3.9+
Poetry (dependency management)
OpenAI API Key

Installation

Clone the repository:

bashCopygit clone https://github.com/your-username/ai_labs-support-assistant.git
cd nordvpn-support-assistant

Install dependencies:

poetry install

Set up environment variables:

Create a .env file in the project root
Add your OpenAI API key:

OPENAI_API_KEY=your_openai_api_key_here

Database Initialization
Before running the assistant, initialize the ChromaDB with Help Center articles:
bashCopypoetry run python scripts/initialize_db.py

Running the Assistant
poetry run python ai_labs/run.py
