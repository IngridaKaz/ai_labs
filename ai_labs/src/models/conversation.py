from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class ConversationState:
    """
    Maintains the state of a conversation including user information and message history.
    """

    country: str | None = None
    device: str | None = None
    conversation_history: list[dict[str, str]] = field(default_factory=list)
    needs_connectivity_info: bool = False
    start_time: datetime = field(default_factory=datetime.now)

    def add_message(self, role: str, content: str) -> None:
        """
        Add a message to the conversation history.

        Args:
            role: The role of the message sender ('user' or 'assistant')
            content: The content of the message
        """
        self.conversation_history.append({"role": role, "content": content, "timestamp": datetime.now(UTC).isoformat()})

    def get_recent_history(self, num_messages: int = 3) -> list[dict[str, str]]:
        """
        Get the most recent messages from the conversation history.

        Args:
            num_messages: Number of recent messages to retrieve

        Returns:
            List of recent messages
        """
        return self.conversation_history[-num_messages:]

    def reset(self) -> None:
        """Reset the conversation state while preserving user information."""
        self.needs_connectivity_info = False
        self.conversation_history = []
        self.start_time = datetime.now(UTC)

    def get_user_info_summary(self) -> str:
        """
        Get a formatted summary of user information.

        Returns:
            A string containing relevant user information
        """
        info = []
        if self.country:
            info.append(f"Country: {self.country}")
        if self.device:
            info.append(f"Device: {self.device}")
        return "\n".join(info) if info else "No user information available"
