import sys
from pathlib import Path

from openai import OpenAI

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from ai_labs.src.config import OPENAI_API_KEY, OPENAI_MODEL
from ai_labs.src.database.chroma_client import ChromaDBClient
from ai_labs.src.models.conversation import ConversationState
from ai_labs.src.utils.connectivity_checker import ConnectivityChecker
from ai_labs.src.utils.logger import setup_logger

logger = setup_logger(__name__)


class ChatAssistant:
    """
    Main chat assistant class that handles user interactions and generates responses.
    """

    def __init__(self) -> None:
        self.db_client = ChromaDBClient()
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
        self.connectivity_checker = ConnectivityChecker()

    def generate_prompt(self, question: str, context: str, conv_state: ConversationState) -> str:
        """Generate the complete prompt for the language model."""
        user_info = conv_state.get_user_info_summary()
        recent_history = conv_state.get_recent_history()

        return f"""You are a helpful NordVPN support assistant. Use the following information to provide accurate and helpful responses.

        User Information:
        {user_info}

        Recent Conversation:
        {' '.join([f"{msg['role']}: {msg['content']}" for msg in recent_history])}

        Relevant Documentation:
        {context}

        Current Question: {question}

        Provide a clear, concise response focusing on solving the user's problem. If you need more information, ask for it specifically. If you do not know the answer say so."""

    def generate_response(self, question: str, results: dict, conv_state: ConversationState) -> str:
        """Generate a response using the retrieved context and conversation history."""
        contexts = []
        for doc, metadata in zip(results["documents"][0], results["metadatas"][0], strict=False):
            contexts.append(f"Source: {metadata['title']}\n{doc}")

        context = "\n\n---\n\n".join(contexts)
        prompt = self.generate_prompt(question, context, conv_state)

        response = self.openai_client.chat.completions.create(
            model=OPENAI_MODEL, messages=[{"role": "system", "content": prompt}, {"role": "user", "content": question}]
        )

        return response.choices[0].message.content

    def process_message(self, user_input: str, conv_state: ConversationState) -> str:
        """Process user message and generate appropriate response."""
        conv_state.add_message("user", user_input)

        # Handle connectivity-related queries
        if self.connectivity_checker.is_connectivity_issue(user_input):
            prompt = self.connectivity_checker.get_required_info_prompt(conv_state.country, conv_state.device)
            if prompt:
                conv_state.needs_connectivity_info = True
                return prompt

        # Update user information if needed
        if conv_state.needs_connectivity_info:
            if not conv_state.country:
                conv_state.country = user_input
                prompt = self.connectivity_checker.get_required_info_prompt(conv_state.country, conv_state.device)
                if prompt:
                    return prompt
            elif not conv_state.device:
                conv_state.device = user_input
                conv_state.needs_connectivity_info = False

        # Query relevant documents and generate response
        results = self.db_client.query(user_input)
        response = self.generate_response(user_input, results, conv_state)

        conv_state.add_message("assistant", response)
        return response


def main() -> None:
    """Main function to run the chat interface."""
    assistant = ChatAssistant()
    conv_state = ConversationState()

    logger.info("NordVPN Support Assistant started")

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ["quit", "exit", "bye"]:
                logger.info("Chat session ended")
                break

            response = assistant.process_message(user_input, conv_state)
            logger.info(f"Assistant response: {response}")

        except KeyboardInterrupt:
            logger.info("Chat session interrupted")
            break
        except Exception:
            logger.exception("Error occurred")
            conv_state.reset()


if __name__ == "__main__":
    main()
