class ConnectivityChecker:
    """
    Utility class for checking connectivity-related queries and managing troubleshooting flows.
    """

    def __init__(self) -> None:
        self.connectivity_keywords: set[str] = {
            "connect",
            "connection",
            "connecting",
            "disconnect",
            "disconnecting",
            "internet",
            "network",
            "wifi",
            "speed",
            "slow",
            "can't connect",
            "unable to connect",
            "connection failed",
            "no internet",
            "timeout",
            "drops",
            "dropping",
            "unstable",
            "keeps disconnecting",
        }

    def is_connectivity_issue(self, text: str) -> bool:
        """
        Check if the query is related to connectivity issues.

        Args:
            text: The user's query text

        Returns:
            True if the query is about connectivity issues, False otherwise
        """
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.connectivity_keywords)

    def get_required_info_prompt(self, country: str | None = None, device: str | None = None) -> str:
        """
        Generate the appropriate prompt for requesting missing connectivity information.

        Args:
            country: The user's country if already provided
            device: The user's device if already provided

        Returns:
            A prompt requesting the missing information
        """
        if not country:
            return "Before I help you troubleshoot, could you please tell me which country you're connecting from?"
        if not device:
            return "And what device are you using? (e.g., Windows, Mac, Android, iOS)"
        return None
