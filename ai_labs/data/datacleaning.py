import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

from ai_labs.src.utils.logger import setup_logger

# Setup logger
logger = setup_logger(__name__)


def clean_text(raw_text: str) -> str:
    """Clean and normalize text input."""
    # Check if text is not empty
    if not raw_text:
        return ""

    # 1. Remove HTML tags
    text_no_html = BeautifulSoup(raw_text, "html.parser").get_text()

    # 2. Remove unnecessary characters
    text_no_symbols = text_no_html.replace("\u00a0", " ").replace("\r", " ").replace("\t", " ")

    # 3. Normalize letter case
    text_normalized_case = text_no_symbols.lower()

    # 4. Remove excess punctuation
    text_no_excess_punctuation = re.sub(r"[!?.]{2,}", ".", text_normalized_case)

    # 5. Normalize whitespace
    return " ".join(text_no_excess_punctuation.split())


# Load JSON file
with Path("hc_articles.json").open(encoding="utf-8") as file:
    data = json.load(file)

# Clean content of all articles
cleaned_articles: list[dict[str, str]] = [
    {
        "url": article["url"],  # Keep URL unprocessed
        "title": clean_text(article["title"]),  # Clean title
        "name": clean_text(article["name"]),  # Clean name alternative
        "body": clean_text(article["body"]),  # Clean main text
    }
    for article in data
]

# Save cleaned JSON file
with Path("cleaned_hc_articles.json").open("w", encoding="utf-8") as file:
    json.dump(cleaned_articles, file, ensure_ascii=False, indent=4)

logger.info("Cleaned JSON file saved as 'cleaned_hc_articles.json'.")
