# NordVPN Support Assistant

A **Retrieval-Augmented Generation (RAG)** chatbot for providing support using NordVPN's Help Center documentation.

## Features

- **Intelligent Document Retrieval**: Powered by ChromaDB vector database.
- **Context-Aware Responses**: Utilizes OpenAI's GPT-3.5 Turbo for intelligent conversation.
- **Troubleshooting Support**: Detects country and device for tailored connectivity solutions.
- **Conversation History Management**: Maintains context for better assistance.
- **Comprehensive Testing Suite**: Ensures high-quality performance.
- **Memory-Efficient Document Processing**: Optimized for resource efficiency.

## Prerequisites

- Python 3.9+
- Poetry (for dependency management)
- OpenAI API Key

## Installation

### Clone the Repository
```bash
git clone https://github.com/your-username/ai_labs-support-assistant.git
cd nordvpn-support-assistant
```

### Install Dependencies
```bash
poetry install
```

### Set Up Environment Variables
1. Create a `.env` file in the project root.
2. Add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Database Initialization

Before running the assistant, initialize the ChromaDB with Help Center articles:
```bash
poetry run python scripts/initialize_db.py
```

## Running the Assistant

To start the assistant, use:
```bash
poetry run python ai_labs/run.py
```

---

With this setup, you’re ready to leverage the NordVPN Support Assistant for enhanced user support. For any questions or issues, feel free to raise an issue in the repository.

